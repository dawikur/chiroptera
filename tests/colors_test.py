# Copyright (c) 2024-2026 Dawid Kurek <hello@dawikur.dev>
"""Tests for Colors class"""

from typing import Callable, cast

import numpy as np
import skimage
from numpy.typing import NDArray

from chiroptera.colors import BaseColors, Colors

RGB2LAB = cast(
    Callable[[NDArray[np.float64]], NDArray[np.float64]], skimage.color.rgb2lab
)


def test_colors_initialization() -> None:
    """Test that Colors class initializes correctly."""
    colors = Colors()
    assert colors.min == 1
    assert colors.max == 17


def test_colors_with_custom_base() -> None:
    """Test Colors with custom BaseColors."""
    base = BaseColors()
    colors = Colors(base)
    assert callable(colors["tint"])
    assert callable(colors["red"])
    assert callable(colors["green"])
    assert callable(colors["blue"])
    assert callable(colors["yellow"])
    assert callable(colors["cyan"])
    assert callable(colors["magenta"])


def test_tint_generates_valid_hex() -> None:
    """Test that tint generates valid hex colors."""
    colors = Colors()

    for i in range(colors.min, colors.max + 1):
        hex_color = colors["tint"](i)
        assert hex_color.startswith("#")
        assert len(hex_color) == 7
        # Verify it's valid hex
        _ = int(hex_color[1:], 16)


def test_chromatic_colors_generate_valid_hex() -> None:
    """Test that chromatic colors generate valid hex colors."""
    colors = Colors()

    for color_name in ["red", "green", "yellow", "blue", "magenta", "cyan"]:
        for i in range(colors.min, colors.max + 1):
            hex_color = colors[color_name](i)
            assert hex_color.startswith("#")
            assert len(hex_color) == 7
            # Verify it's valid hex
            _ = int(hex_color[1:], 16)


def test_chromatic_colors_preserve_tint_lightness() -> None:
    """Chromatic colors retain the requested LAB lightness after gamut mapping."""
    colors = Colors()

    for index in range(colors.min, colors.max + 1):
        tint_hex = colors["tint"](index)
        tint_rgb = np.array(
            [int(tint_hex[offset : offset + 2], 16) / 255.0 for offset in (1, 3, 5)]
        )
        tint_lightness = cast(float, RGB2LAB(tint_rgb)[0])

        for color_name in ["red", "green", "yellow", "blue", "magenta", "cyan"]:
            hex_color = colors[color_name](index)
            rgb = np.array(
                [
                    int(hex_color[offset : offset + 2], 16) / 255.0
                    for offset in (1, 3, 5)
                ]
            )
            lightness = cast(float, RGB2LAB(rgb)[0])
            assert abs(lightness - tint_lightness) < 0.5


def test_tint_gradient_monotonic() -> None:
    """Test that tint creates a monotonic gradient from dark to light."""
    colors = Colors()

    # Extract lightness values (first two hex digits approximate lightness)
    lightness_values: list[int] = []
    for i in range(colors.min, colors.max + 1):
        hex_color = colors["tint"](i)
        # Convert first byte as rough lightness proxy
        r_value = int(hex_color[1:3], 16)
        lightness_values.append(r_value)

    # Check that values generally increase (allowing small variations due to LAB conversion)
    for i in range(len(lightness_values) - 1):
        assert (
            lightness_values[i] <= lightness_values[i + 1] + 5
        )  # Allow small tolerance


def test_colors_boundary_values() -> None:
    """Test colors at boundary indices."""
    colors = Colors()

    # Should work at min and max
    _ = colors["tint"](colors.min)
    _ = colors["tint"](colors.max)
    _ = colors["red"](colors.min)
    _ = colors["red"](colors.max)


def test_colors_iteration() -> None:
    """Test that Colors can be iterated over chromatic colors."""
    colors = Colors()

    color_list = list(colors)

    # Should iterate over the 6 chromatic colors + tint
    assert len(color_list) == 7
    assert color_list == ["tint", "red", "yellow", "green", "cyan", "blue", "magenta"]


def test_colors_callable_compatibility() -> None:
    """Test that colors[name] is still callable for generating colors."""
    colors = Colors()

    # Should still be callable for generating colors at indices
    for color in ["red", "yellow", "green", "cyan", "blue", "magenta"]:
        color_fn = colors[color]

        # Should be callable
        assert callable(color_fn)

        # Should generate valid hex at different indices
        hex_at_min = color_fn(colors.min)
        hex_at_max = color_fn(colors.max)

        assert hex_at_min.startswith("#")
        assert hex_at_max.startswith("#")
        assert len(hex_at_min) == 7
        assert len(hex_at_max) == 7
