# Copyright (c) 2024-2026 Dawid Kurek <hello@dawikur.dev>
"""Generates a palette based on mode and contrast."""

from copy import deepcopy
from enum import Enum
from typing import Optional

from chiroptera.ansi import Ansi
from chiroptera.colors import Colors


class Mode(Enum):
    """Mode of the palette."""

    DARK = "dark"
    LIGHT = "light"


class Contrast(Enum):
    """Contrast of the palette."""

    HARD = "hard"
    NORMAL = "normal"
    SOFT = "soft"


class Palette(dict[str, Ansi]):
    """Generates a palette based on mode and contrast.

    This class wraps a dictionary of color names to Ansi objects,
    providing dict-like access while maintaining type safety.
    """

    def __init__(self, mode: Mode, contrast: Contrast, colors: Optional[Colors] = None):
        super().__init__()
        if colors is None:
            colors = Colors()

        # Colors range from min (dark) to max (light) in LAB lightness space
        # For DARK mode: bg is dark (near min), fg is mid-range
        # For LIGHT mode: bg is light (near max), fg is darker for better contrast
        # Foreground is fixed per mode; contrast variants affect only backgrounds.
        if mode == Mode.DARK:
            fg = round((colors.min + colors.max) / 2) + 2.5
            bg = colors.min + 1  # Near darkest, but not absolute min
            step = 1  # Positive step moves toward lighter colors
        else:
            fg = (
                round((colors.min + colors.max) / 2) - 3.5
            )  # Darker for closely matched contrast and WCAG AA
            bg = colors.max - 1  # Near lightest, but not absolute max
            step = -1  # Negative step moves toward darker colors

        # Adjust background based on contrast preference
        # HARD: push bg further from fg for maximum contrast
        # SOFT: pull bg closer to fg for reduced contrast
        if contrast == Contrast.HARD:
            bg -= step  # Move bg away from fg (darker for DARK, lighter for LIGHT)
        elif contrast == Contrast.SOFT:
            bg += step  # Move bg toward fg (lighter for DARK, darker for LIGHT)

        # Create background variants with subtle lightness differences
        bg_dim = bg - step  # Dimmer than normal bg
        bg_bright = bg + 2 * step  # Brighter than normal bg (highlight)

        # Create foreground variants with more pronounced differences
        # Uses 2*step for dim and bright, WCAG AA foregrounds.
        fg_dim = fg - 2 * step
        fg_bright = fg + 2 * step

        tint = colors["tint"]

        self["bg.dim"] = Ansi(0, tint(bg_dim))
        self["bg"] = Ansi(0, tint(bg))
        self["bg.bright"] = Ansi(0, tint(bg_bright))

        self["fg.dim"] = Ansi(8, tint(fg_dim))
        self["fg"] = Ansi(7, tint(fg))
        self["fg.bright"] = Ansi(15, tint(fg_bright))

        for i in range(colors.min, colors.max + 1):
            self[f"tint{i}"] = Ansi(None, tint(i))

        for i, name in enumerate(["red", "green", "yellow", "blue", "magenta", "cyan"]):
            self[name + ".dim"] = Ansi(i + 1, colors[name](bg))
            self[name] = Ansi(i + 1, colors[name](fg))
            self[name + ".bright"] = Ansi(i + 9, colors[name](fg_bright))

    def __str__(self) -> str:
        inner = ", ".join(f"{key}: {value}" for key, value in self.items())
        return f"Palette{{{inner}}}"

    def __repr__(self) -> str:
        return str(self)

    def add_rgb(self) -> "Palette":
        """Adds r, g and b values to palette based on hex."""

        palette = deepcopy(self)

        for name, ansi in palette.items():
            palette[name] = ansi.add_rgb()

        return palette

    def flatten(self) -> dict[str, str]:
        """Flattens palette to a single level dictionary."""

        flat: dict[str, str] = {}

        for name, ansi in self.items():
            for key, value in ansi.items():
                flat[f"{name}.{key}"] = str(value)

        return flat
