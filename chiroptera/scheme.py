# Copyright (c) 2024-2026 Dawid Kurek <hello@dawikur.dev>
"""Higher-level scheme abstraction that organizes palette colors semantically."""

from copy import deepcopy

from chiroptera.ansi import Ansi
from chiroptera.palette import Palette


class Scheme(dict[str, dict[str, Ansi]]):
    """Higher-level scheme that organizes palette colors semantically.

    Provides a hierarchical structure with three categories:
        - fg: Foreground colors (normal, note, mark, ignore, + chromatic)
        - bg: Background colors (normal, highlight, mark, + chromatic)
        - ui: UI colors (normal, highlight, + chromatic)

    Access pattern: scheme['fg']['normal']['hex']
    """

    def __init__(self, palette: Palette):
        """Initialize scheme from a palette.

        Args:
            palette: The palette to organize into a scheme
        """
        super().__init__()

        # Foreground colors: high contrast for text readability
        self["fg"] = {
            "normal": palette["fg"],  # Main foreground
            "note": palette["fg.dim"],  # Dimmed text (line numbers, etc.)
            "mark": palette["fg.bright"],  # Bright text (marks, highlights)
            "ignore": palette["bg.bright"],  # Very dim (non-text, whitespace)
            # Chromatic foreground colors (all bright for syntax highlighting)
            "red": palette["red.bright"],
            "green": palette["green.bright"],
            "blue": palette["blue.bright"],
            "yellow": palette["yellow.bright"],
            "magenta": palette["magenta.bright"],
            "cyan": palette["cyan.bright"],
        }

        # Background colors: low contrast for subtle backgrounds
        self["bg"] = {
            "normal": palette["bg"],  # Main background
            "highlight": palette["bg.dim"],  # Dimmed background (current line)
            "mark": palette["bg.bright"],  # Bright background (selections)
            # Chromatic background colors (all dim for subtle backgrounds)
            "red": palette["red.dim"],
            "green": palette["green.dim"],
            "blue": palette["blue.dim"],
            "yellow": palette["yellow.dim"],
            "magenta": palette["magenta.dim"],
            "cyan": palette["cyan.dim"],
        }

        # UI colors: medium contrast for interface elements
        self["ui"] = {
            "normal": palette["bg.bright"],  # UI elements (menus, borders)
            "highlight": palette["bg.dim"],  # Highlighted UI (selected menu item)
            # Chromatic UI colors (normal contrast)
            "red": palette["red"],
            "green": palette["green"],
            "blue": palette["blue"],
            "yellow": palette["yellow"],
            "magenta": palette["magenta"],
            "cyan": palette["cyan"],
        }

    def __str__(self) -> str:
        inner = ", ".join(f"{key}: {value}" for key, value in self.items())
        return f"Scheme{{{inner}}}"

    def __repr__(self) -> str:
        return str(self)

    def add_rgb(self) -> "Scheme":
        """Adds r, g and b values to all colors in the scheme.

        Returns:
            A new Scheme with RGB components added to all Ansi objects
        """
        scheme = deepcopy(self)

        for colors in scheme.values():
            for name, ansi in colors.items():
                colors[name] = ansi.add_rgb()

        return scheme

    def flatten(self) -> dict[str, str]:
        """Flattens scheme to a single level dictionary.

        Returns:
            A flat dictionary with keys like "fg.normal.hex", "bg.red.256", etc.
        """
        flat: dict[str, str] = {}

        for category, colors in self.items():
            for name, ansi in colors.items():
                for key, value in ansi.items():
                    flat[f"{category}.{name}.{key}"] = str(value)

        return flat
