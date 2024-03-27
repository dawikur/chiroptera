# Copyright (c) 2024-2026 Dawid Kurek <hello@dawikur.dev>
"""Tests for WCAG contrast ratios."""

from pathlib import Path
from typing import Union

import pytest

from chiroptera import Contrast, Mode, Palette


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert hex color to RGB tuple.

    Args:
        hex_color: Hex color string (e.g., "#ff0000")

    Returns:
        RGB tuple with values 0-255
    """
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    """Calculate relative luminance using WCAG formula.

    Implements the WCAG 2.1 relative luminance calculation with gamma correction.

    Args:
        rgb: RGB tuple with values 0-255

    Returns:
        Relative luminance value (0.0-1.0)
    """
    r, g, b = (x / 255.0 for x in rgb)
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(hex1: Union[str, int], hex2: Union[str, int]) -> float:
    """Calculate WCAG contrast ratio between two colors.

    Args:
        hex1: First color (hex string or integer)
        hex2: Second color (hex string or integer)

    Returns:
        WCAG contrast ratio (1.0-21.0)
    """
    lum1 = relative_luminance(hex_to_rgb(str(hex1)))
    lum2 = relative_luminance(hex_to_rgb(str(hex2)))
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)


class TestContrastRatios:
    """Test WCAG contrast ratios for accessibility."""

    def test_foreground_roles_are_stable_across_contrast_variants(self) -> None:
        """Keep foreground roles fixed while contrast variants change backgrounds."""
        color_names = ["red", "green", "yellow", "blue", "magenta", "cyan"]
        foreground_names = (
            ["fg.dim", "fg", "fg.bright"]
            + color_names
            + [f"{color}.bright" for color in color_names]
        )

        for mode in [Mode.DARK, Mode.LIGHT]:
            palettes = [Palette(mode, contrast).add_rgb() for contrast in Contrast]

            for name in foreground_names:
                values = {palette[name]["hex"] for palette in palettes}
                assert (
                    len(values) == 1
                ), f"{mode.value} {name} should not vary with contrast: {values}"

    @pytest.mark.parametrize(
        "contrast,expected_ratio",
        [
            (Contrast.HARD, 5.39),
            (Contrast.NORMAL, 4.66),
            (Contrast.SOFT, 3.98),
        ],
    )
    def test_dark_mode_contrast(
        self, contrast: Contrast, expected_ratio: float
    ) -> None:
        """Test dark mode has expected contrast ratios."""
        palette = Palette(Mode.DARK, contrast).add_rgb()
        bg_hex = palette["bg"]["hex"]
        fg_hex = palette["fg"]["hex"]
        ratio = contrast_ratio(bg_hex, fg_hex)

        # Allow 0.05 tolerance for floating point differences
        assert abs(ratio - expected_ratio) < 0.05, (
            f"Dark {contrast.value}: expected {expected_ratio}:1, "
            f"got {ratio:.2f}:1 (bg={bg_hex}, fg={fg_hex})"
        )

    @pytest.mark.parametrize(
        "contrast,expected_ratio",
        [
            (Contrast.HARD, 5.39),
            (Contrast.NORMAL, 4.77),
            (Contrast.SOFT, 4.23),
        ],
    )
    def test_light_mode_contrast(
        self, contrast: Contrast, expected_ratio: float
    ) -> None:
        """Test light mode has expected contrast ratios."""
        palette = Palette(Mode.LIGHT, contrast).add_rgb()
        bg_hex = palette["bg"]["hex"]
        fg_hex = palette["fg"]["hex"]
        ratio = contrast_ratio(bg_hex, fg_hex)

        # Allow 0.05 tolerance for floating point differences
        assert abs(ratio - expected_ratio) < 0.05, (
            f"Light {contrast.value}: expected {expected_ratio}:1, "
            f"got {ratio:.2f}:1 (bg={bg_hex}, fg={fg_hex})"
        )

    @pytest.mark.parametrize(
        "contrast", [Contrast.HARD, Contrast.NORMAL, Contrast.SOFT]
    )
    def test_symmetric_contrast(self, contrast: Contrast) -> None:
        """Test that dark and light modes have symmetric contrast ratios."""
        dark_palette = Palette(Mode.DARK, contrast).add_rgb()
        light_palette = Palette(Mode.LIGHT, contrast).add_rgb()

        dark_ratio = contrast_ratio(
            dark_palette["bg"]["hex"], dark_palette["fg"]["hex"]
        )
        light_ratio = contrast_ratio(
            light_palette["bg"]["hex"], light_palette["fg"]["hex"]
        )

        difference = abs(dark_ratio - light_ratio)

        # Fixed foregrounds keep colour roles stable across contrast variants.
        # Dark and light modes remain perceptually close.
        assert difference < 0.25, (
            f"{contrast.value}: dark={dark_ratio:.2f}:1, "
            f"light={light_ratio:.2f}:1, difference={difference:.2f}"
        )

    def test_hard_contrast_meets_wcag_aa(self) -> None:
        """Test that hard contrast variant meets WCAG AA standard."""
        # WCAG AA requires 4.5:1 for normal text
        for mode in [Mode.DARK, Mode.LIGHT]:
            palette = Palette(mode, Contrast.HARD).add_rgb()
            ratio = contrast_ratio(palette["bg"]["hex"], palette["fg"]["hex"])

            assert ratio >= 4.5, (
                f"{mode.value} hard contrast should meet WCAG AA (>= 4.5:1), "
                f"got {ratio:.2f}:1"
            )

    def test_hard_and_normal_text_meet_wcag_aa(self) -> None:
        """Test normal text and syntax colours meet AA outside soft mode."""
        color_names = ["red", "green", "yellow", "blue", "magenta", "cyan"]

        for mode in [Mode.DARK, Mode.LIGHT]:
            for contrast in [Contrast.HARD, Contrast.NORMAL]:
                palette = Palette(mode, contrast).add_rgb()
                bg_hex = palette["bg"]["hex"]

                for name in ["fg"] + color_names:
                    ratio = contrast_ratio(bg_hex, palette[name]["hex"])
                    assert ratio >= 4.5, (
                        f"{mode.value} {contrast.value} {name} should meet WCAG AA "
                        f"(>= 4.5:1), got {ratio:.2f}:1"
                    )

    def test_bright_colors_meet_wcag_aa(self) -> None:
        """Test that bright color variants meet WCAG AA standard."""
        for mode in [Mode.DARK, Mode.LIGHT]:
            for contrast in Contrast:
                palette = Palette(mode, contrast).add_rgb()
                bg_hex = palette["bg"]["hex"]

                for color in ["red", "green", "yellow", "blue", "magenta", "cyan"]:
                    bright_hex = palette[f"{color}.bright"]["hex"]
                    ratio = contrast_ratio(bg_hex, bright_hex)

                    # All bright colors meet WCAG AA (4.5:1) for important syntax elements
                    assert ratio >= 4.5, (
                        f"{mode.value} {contrast.value} {color}_bright should meet "
                        f"WCAG AA (4.5:1), got {ratio:.2f}:1"
                    )

    def test_soft_mode_requires_bright_text_for_wcag_aa(self) -> None:
        """Keep soft text intentionally below AA while bright roles remain accessible."""
        color_names = ["red", "green", "yellow", "blue", "magenta", "cyan"]

        for mode in [Mode.DARK, Mode.LIGHT]:
            palette = Palette(mode, Contrast.SOFT).add_rgb()
            bg_hex = palette["bg"]["hex"]

            for name in ["fg"] + color_names:
                assert contrast_ratio(bg_hex, palette[name]["hex"]) < 4.5

            for name in ["fg.bright"] + [f"{color}.bright" for color in color_names]:
                assert contrast_ratio(bg_hex, palette[name]["hex"]) >= 4.5

    def test_readme_bright_contrast_table_matches_palette(self) -> None:
        """Keep the documented bright-color ratios synchronized with the palette."""
        readme = Path(__file__).parents[1] / "README.md"
        documented_table = readme.read_text(encoding="utf-8")

        for color in ["red", "green", "yellow", "blue", "magenta", "cyan"]:
            ratios: list[str] = []
            for mode in [Mode.DARK, Mode.LIGHT]:
                palette = Palette(mode, Contrast.NORMAL).add_rgb()
                ratio = contrast_ratio(
                    palette["bg"]["hex"], palette[f"{color}.bright"]["hex"]
                )
                ratios.append(f"**{ratio:.2f}:1** ✅")

            expected_row = f"| {color}.bright | {ratios[0]} | {ratios[1]} |"
            assert expected_row in documented_table

    def test_dim_colors_low_contrast(self) -> None:
        """Test that dim color variants have intentionally low contrast for backgrounds."""
        for mode in [Mode.DARK, Mode.LIGHT]:
            palette = Palette(mode, Contrast.NORMAL).add_rgb()
            bg_dim_hex = palette["bg.dim"]["hex"]

            for color in ["red", "green", "yellow", "blue", "magenta", "cyan"]:
                dim_hex = palette[f"{color}.dim"]["hex"]
                ratio = contrast_ratio(bg_dim_hex, dim_hex)

                # Should have low contrast (< 2.0) for subtle background highlights
                assert ratio < 2.0, (
                    f"{mode.value} {color}_dim should have low contrast "
                    f"for background use, got {ratio:.2f}:1"
                )
