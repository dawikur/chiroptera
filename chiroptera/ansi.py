# Copyright (c) 2024-2026 Dawid Kurek <hello@dawikur.dev>
"""Converts ansi16 and hex color to dict with ansi2, ansi8, ansi16, ansi256 and hex values."""

from copy import deepcopy
from math import pow as math_pow
from typing import Optional, Union


class Ansi(dict[str, Union[str, int]]):
    """Converts ansi16 and hex color to ANSI color codes.

    All attributes are private. Use dict-like access (ansi["256"], ansi["hex"])
    instead of direct attribute access.
    """

    def __init__(self, ansi16: Optional[int], hex_color: str):
        super().__init__()
        # Convert hex color to closest xterm-256 color code
        # xterm-256 palette structure:
        #   0-15:    Standard ANSI colors
        #   16-231:  6x6x6 RGB color cube (216 colors)
        #   232-255: Grayscale ramp (24 shades)
        # Reference:
        #   https://github.com/tmux/tmux/blob/dae2868d1227b95fd076fb4a5efa6256c7245943/colour.c#L57

        # Parse hex color to RGB components (0-255)
        rgb = [
            int(hex_color[1:3], 16),
            int(hex_color[3:5], 16),
            int(hex_color[5:7], 16),
        ]

        # Xterm color cube uses only 6 levels per RGB channel
        # q2c maps quantization index (0-5) to actual RGB value
        q2c = [0x00, 0x5F, 0x87, 0xAF, 0xD7, 0xFF]

        # Quantize each RGB component to nearest of 6 levels (0-5)
        # Thresholds: <48→0, <114→1, otherwise scale linearly
        rgb_q = [
            int(0 if unit < 48 else 1 if unit < 114 else ((unit - 35) / 40))
            for unit in rgb
        ]

        # Calculate xterm-256 color cube index
        # Formula: 16 + 36*r + 6*g + b (where r,g,b are 0-5)
        xterm256 = 16 + (36 * rgb_q[0]) + (6 * rgb_q[1]) + rgb_q[2]

        # Get the quantized RGB values
        rgb_c = [q2c[unit] for unit in rgb_q]

        # If color doesn't exactly match color cube, check if grayscale ramp is closer
        if rgb != rgb_c:
            # Apply gamma correction (2.2) for perceptually accurate brightness
            rgb_l: list[float] = [math_pow(unit / 255.0, 2.2) for unit in rgb]
            linear_grey_avg: float = sum(rgb_l) / 3

            # Convert back from linear to sRGB
            grey_avg: float = 255.0 * math_pow(linear_grey_avg, 1 / 2)

            # Map to grayscale ramp index (0-23)
            if grey_avg > 238:
                grey_idx = 23
            else:
                grey_idx = int((grey_avg - 3) / 10)

            # Calculate actual grey value from index
            grey = 8 + (10 * grey_idx)

            # Compare Euclidean distance: grayscale vs color cube
            # Use grayscale if it's closer to original color
            if (sum(pow(grey - unit, 2) for unit in rgb)) < (
                sum(pow(pair[0] - pair[1], 2) for pair in zip(rgb_c, rgb))
            ):
                xterm256 = 232 + grey_idx  # Grayscale ramp starts at 232

        # Set ANSI codes
        if ansi16 is None:
            self["2"] = 0
            self["8"] = 0
            self["16"] = 0
        else:
            self["2"] = int((ansi16 % 8) != 0)
            self["8"] = int(ansi16 % 8)
            self["16"] = int(ansi16)

        self["256"] = str(int(xterm256))
        self["hex"] = hex_color

    def __str__(self) -> str:
        return f"Ansi{{{self['hex']}}}"

    def __repr__(self) -> str:
        inner = ", ".join(f"{key}: {value}" for key, value in self.items())
        return f"Ansi{{{inner}}}"

    def add_rgb(self) -> "Ansi":
        """Add RGB components (r, g, b, rgb) in-place."""
        ansi = deepcopy(self)

        rgb = str(self["hex"])[1:]  # Remove '#' prefix
        ansi["rgb"] = rgb
        ansi["r"] = rgb[0:2]
        ansi["g"] = rgb[2:4]
        ansi["b"] = rgb[4:6]

        return ansi
