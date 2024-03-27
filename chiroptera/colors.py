# Copyright (c) 2024-2026 Dawid Kurek <hello@dawikur.dev>
"""Base colors and meta information."""

from copy import deepcopy
from typing import Callable, Optional, cast

import numpy as np
import numpy.typing as npt
import skimage


class BaseColors(dict[str, str]):
    """Base color definitions for the chiroptera colorscheme.

    Provides foundational hex colors for tint (background/foreground)
    and six chromatic colors. These colors are then interpolated in
    LAB color space to create perceptually uniform gradients.

    Color sources:
        - dark/light: Inspired by gruvbox and solarized themes
        - Chromatic colors: Optimized for WCAG AA contrast ratios
    """

    def __init__(self) -> None:
        super().__init__()
        # Background and foreground tint base colors
        # Inspired by gruvbox: https://github.com/morhetz/gruvbox
        self["dark"] = "#242425"
        self["light"] = "#f8f5e8"

        # Chromatic colors optimized for WCAG AA contrast
        # Base colors adapted from gruvbox for better contrast
        self["red"] = "#ad1817"
        self["yellow"] = "#b86700"
        self["green"] = "#98971a"
        self["cyan"] = "#388971"
        self["blue"] = "#458588"
        self["magenta"] = "#b16286"


class Colors(dict[str, Callable[[float], str]]):
    """LAB color space interpolator for generating color gradients.

    Converts base hex colors to LAB color space and provides callable
    functions to generate colors at different lightness levels. This
    enables perceptually uniform color transitions between dark and
    light modes.

    The Colors class maps color names to generator functions:
        colors["red"](10) -> generates red color at lightness level 10

    Attributes:
        min: Minimum lightness index (1) - darkest usable color
        max: Maximum lightness index (17) - lightest usable color
    """

    min: int
    max: int

    def __init__(self, base: Optional[BaseColors] = None) -> None:
        super().__init__()

        def __hex2lab(entry: str) -> npt.NDArray[np.float64]:
            """Convert hex color to LAB color space.

            Args:
                entry: Hex color string (e.g., "#ff0000")

            Returns:
                LAB color array [L, a, b] where:
                    L: Lightness (0-100)
                    a: Green-red axis
                    b: Blue-yellow axis
            """
            entry = entry.strip("#")
            rgb = [int(entry[i : i + 2], 16) / 255.0 for i in (0, 2, 4)]
            return cast(
                npt.NDArray[np.float64],
                skimage.color.rgb2lab(rgb),  # pyright: ignore[reportUnknownMemberType]
            )

        def __rgb_from_lab(lab: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
            """Convert LAB to sRGB without clipping out-of-gamut channels."""
            xyz = cast(
                npt.NDArray[np.float64],
                skimage.color.lab2xyz(lab),  # pyright: ignore[reportUnknownMemberType]
            )
            conversion_matrix: npt.NDArray[np.float64] = np.array(
                [
                    [3.24048134, -0.96925495, 0.05564664],
                    [-1.53715152, 1.87599000, -0.20404134],
                    [-0.49853633, 0.04155593, 1.05731107],
                ],
                dtype=np.float64,
            )
            rgb_linear = cast(
                npt.NDArray[np.float64],
                np.dot(  # pyright: ignore[reportUnknownMemberType]
                    xyz,
                    conversion_matrix,
                ),
            )
            positive: npt.NDArray[np.bool_] = rgb_linear > 0.0031308
            rgb: npt.NDArray[np.float64] = np.empty_like(rgb_linear)
            rgb[positive] = 1.055 * np.power(rgb_linear[positive], 1 / 2.4) - 0.055
            rgb[~positive] = 12.92 * rgb_linear[~positive]
            return rgb

        def __lab2hex(lab: npt.NDArray[np.float64]) -> str:
            """Convert LAB color to hex string.

            Args:
                lab: LAB color array [L, a, b]

            Returns:
                Hex color string (e.g., "#ff0000")
            """
            rgb = __rgb_from_lab(lab)

            # Some high-chroma LAB colours cannot be represented by sRGB at
            # the requested lightness.  Clipping their RGB channels changes
            # their lightness substantially.  Instead, preserve L and hue
            # while reducing chroma to the most saturated in-gamut value.
            if np.any(rgb < 0.0) or np.any(  # pyright: ignore[reportUnknownMemberType]
                rgb > 1.0
            ):
                low, high = 0.0, 1.0
                chroma: npt.NDArray[np.float64] = np.array(
                    lab[1:], dtype=np.float64, copy=True
                )
                for _ in range(24):
                    scale = (low + high) / 2.0
                    candidate: npt.NDArray[np.float64] = np.array(
                        lab, dtype=np.float64, copy=True
                    )
                    candidate[1:] = chroma * scale
                    candidate_rgb = __rgb_from_lab(candidate)
                    if np.all(  # pyright: ignore[reportUnknownMemberType]
                        candidate_rgb >= 0.0
                    ) and np.all(  # pyright: ignore[reportUnknownMemberType]
                        candidate_rgb <= 1.0
                    ):
                        low = scale
                        rgb = candidate_rgb
                    else:
                        high = scale

            rgb_values = [
                int(rgb[i] * 255.0) for i in (0, 1, 2)  # pyright: ignore[reportAny]
            ]
            return f"#{rgb_values[0]:02x}{rgb_values[1]:02x}{rgb_values[2]:02x}"

        base = base or BaseColors()

        dark_lab = __hex2lab(base["dark"])
        light_lab = __hex2lab(base["light"])

        chromatic_labs = {
            name: __hex2lab(base[name])
            for name in ("red", "yellow", "green", "cyan", "blue", "magenta")
        }

        # 18 steps provides fine-grained control for contrast adjustments
        # Steps 0-17 span from dark_lab to light_lab in LAB space
        steps = 18

        def __tint(idx: float) -> npt.NDArray[np.float64]:
            """Generate tint color at given lightness index.

            Interpolates between dark and light base colors in LAB space.

            Args:
                idx: Lightness index (0 = darkest, steps = lightest)

            Returns:
                LAB color array for the tint at this lightness
            """
            assert 0 <= idx
            assert idx <= steps
            return dark_lab + idx * (light_lab - dark_lab) / steps

        def __col(lab: npt.NDArray[np.float64], idx: float) -> npt.NDArray[np.float64]:
            """Generate chromatic color at given lightness index.

            Preserves the chroma (a, b components) of the base color while
            adjusting lightness to match the tint at the same index.

            Args:
                lab: Base chromatic color in LAB space
                idx: Lightness index to match

            Returns:
                LAB color with adjusted lightness
            """
            lab = deepcopy(lab)
            lab[0] = __tint(idx)[0]  # Replace L component, keep a/b
            return lab

        def __color_generator(lab: npt.NDArray[np.float64]) -> Callable[[float], str]:
            """Return a hex color generator for a chromatic LAB value."""
            return lambda idx: __lab2hex(__col(lab, idx))

        # Store color generators as callable functions via closures
        # This enables the pattern: colors["red"](10)
        self["tint"] = lambda idx: __lab2hex(__tint(idx))
        self.update(
            {name: __color_generator(lab) for name, lab in chromatic_labs.items()}
        )

        self.min = 1
        self.max = steps - 1
