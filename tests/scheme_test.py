# Copyright (c) 2024-2026 Dawid Kurek <hello@dawikur.dev>
"""Tests for scheme module."""

import pytest

from chiroptera.ansi import Ansi
from chiroptera.palette import Contrast, Mode, Palette
from chiroptera.scheme import Scheme


@pytest.fixture
def dark_normal_palette() -> Palette:
    """Create a dark normal palette for testing."""
    return Palette(Mode.DARK, Contrast.NORMAL)


@pytest.fixture
def dark_normal_scheme(dark_normal_palette: Palette) -> Scheme:
    """Create a dark normal scheme for testing."""
    return Scheme(dark_normal_palette)


def test_scheme_initialization(dark_normal_palette: Palette) -> None:
    """Test that scheme initializes with correct structure."""
    scheme = Scheme(dark_normal_palette)

    # Check top-level keys
    assert "fg" in scheme
    assert "bg" in scheme
    assert "ui" in scheme

    # Check that categories are dictionaries
    assert isinstance(scheme["fg"], dict)
    assert isinstance(scheme["bg"], dict)
    assert isinstance(scheme["ui"], dict)


def test_scheme_str_format(dark_normal_palette: Palette) -> None:
    """Test that scheme properly formats to str."""
    scheme = Scheme(dark_normal_palette)

    assert str(scheme).startswith("Scheme{")


def test_scheme_repr_format(dark_normal_palette: Palette) -> None:
    """Test that scheme properly formats to repr."""
    scheme = Scheme(dark_normal_palette)

    assert repr(scheme).startswith("Scheme{")


def test_scheme_fg_structure(dark_normal_scheme: Scheme) -> None:
    """Test foreground color structure."""
    fg = dark_normal_scheme["fg"]

    # Check semantic color names
    assert "normal" in fg
    assert "note" in fg
    assert "mark" in fg
    assert "ignore" in fg

    # Check chromatic colors
    for color in ["red", "green", "blue", "yellow", "magenta", "cyan"]:
        assert color in fg
        assert isinstance(fg[color], Ansi)


def test_scheme_bg_structure(dark_normal_scheme: Scheme) -> None:
    """Test background color structure."""
    bg = dark_normal_scheme["bg"]

    # Check semantic color names
    assert "normal" in bg
    assert "highlight" in bg
    assert "mark" in bg

    # Check chromatic colors
    for color in ["red", "green", "blue", "yellow", "magenta", "cyan"]:
        assert color in bg
        assert isinstance(bg[color], Ansi)


def test_scheme_ui_structure(dark_normal_scheme: Scheme) -> None:
    """Test UI color structure."""
    ui = dark_normal_scheme["ui"]

    # Check semantic color names
    assert "normal" in ui
    assert "highlight" in ui

    # Check chromatic colors
    for color in ["red", "green", "blue", "yellow", "magenta", "cyan"]:
        assert color in ui
        assert isinstance(ui[color], Ansi)


def test_scheme_color_mapping(dark_normal_palette: Palette) -> None:
    """Test that scheme correctly maps palette colors."""
    scheme = Scheme(dark_normal_palette)

    # Foreground mappings
    assert scheme["fg"]["normal"] == dark_normal_palette["fg"]
    assert scheme["fg"]["note"] == dark_normal_palette["fg.dim"]
    assert scheme["fg"]["mark"] == dark_normal_palette["fg.bright"]
    assert scheme["fg"]["ignore"] == dark_normal_palette["bg.bright"]
    assert scheme["fg"]["red"] == dark_normal_palette["red.bright"]

    # Background mappings
    assert scheme["bg"]["normal"] == dark_normal_palette["bg"]
    assert scheme["bg"]["highlight"] == dark_normal_palette["bg.dim"]
    assert scheme["bg"]["mark"] == dark_normal_palette["bg.bright"]
    assert scheme["bg"]["red"] == dark_normal_palette["red.dim"]

    # UI mappings
    assert scheme["ui"]["normal"] == dark_normal_palette["bg.bright"]
    assert scheme["ui"]["highlight"] == dark_normal_palette["bg.dim"]
    assert scheme["ui"]["red"] == dark_normal_palette["red"]


def test_scheme_nested_access(dark_normal_scheme: Scheme) -> None:
    """Test nested dictionary access pattern."""
    # Access pattern: scheme['fg']['normal']['hex']
    fg_normal_hex = dark_normal_scheme["fg"]["normal"]["hex"]
    assert isinstance(fg_normal_hex, str)
    assert fg_normal_hex.startswith("#")

    # Access pattern: scheme['ui']['red']['256']
    ui_red_256 = dark_normal_scheme["ui"]["red"]["256"]
    assert isinstance(ui_red_256, str)
    assert 0 <= int(ui_red_256) <= 255


def test_scheme_dict_interface(dark_normal_scheme: Scheme) -> None:
    """Test dict-like interface."""
    # __contains__
    assert "fg" in dark_normal_scheme
    assert "invalid" not in dark_normal_scheme

    # __iter__
    keys = list(dark_normal_scheme)
    assert "fg" in keys
    assert "bg" in keys
    assert "ui" in keys

    # items()
    items = list(dark_normal_scheme.items())
    assert len(items) == 3  # fg, bg, ui


def test_scheme_add_rgb(dark_normal_scheme: Scheme) -> None:
    """Test add_rgb adds RGB components to all colors."""
    scheme_with_rgb = dark_normal_scheme.add_rgb()

    # Check fg colors have RGB
    fg_normal = scheme_with_rgb["fg"]["normal"]
    assert "rgb" in fg_normal
    assert "r" in fg_normal
    assert "g" in fg_normal
    assert "b" in fg_normal

    # Check bg colors have RGB
    bg_red = scheme_with_rgb["bg"]["red"]
    assert "rgb" in bg_red
    assert "r" in bg_red
    assert "g" in bg_red
    assert "b" in bg_red

    # Check ui colors have RGB
    ui_blue = scheme_with_rgb["ui"]["blue"]
    assert "rgb" in ui_blue
    assert "r" in ui_blue
    assert "g" in ui_blue
    assert "b" in ui_blue


def test_scheme_add_rgb_values(dark_normal_scheme: Scheme) -> None:
    """Test that RGB values are correctly computed."""
    scheme_with_rgb = dark_normal_scheme.add_rgb()

    # Test that rgb string matches r, g, b values
    fg_normal = scheme_with_rgb["fg"]["normal"]
    hex_color = str(fg_normal["hex"])
    expected_rgb = hex_color[1:]  # Remove '#'

    assert fg_normal["rgb"] == expected_rgb
    assert fg_normal["r"] == expected_rgb[0:2]
    assert fg_normal["g"] == expected_rgb[2:4]
    assert fg_normal["b"] == expected_rgb[4:6]


def test_scheme_add_rgb_immutability(dark_normal_scheme: Scheme) -> None:
    """Test that add_rgb returns a new scheme without modifying original."""
    scheme_with_rgb = dark_normal_scheme.add_rgb()

    # Original should not have RGB
    assert "rgb" not in dark_normal_scheme["fg"]["normal"]

    # New scheme should have RGB
    assert "rgb" in scheme_with_rgb["fg"]["normal"]


def test_scheme_flatten(dark_normal_scheme: Scheme) -> None:
    """Test flatten creates single-level dictionary."""
    flat = dark_normal_scheme.flatten()

    # Check that it's a flat dict with string keys and values
    assert isinstance(flat, dict)
    assert all(isinstance(k, str) for k in flat.keys())
    assert all(isinstance(v, str) for v in flat.values())

    # Check fg keys
    assert "fg.normal.hex" in flat
    assert "fg.normal.256" in flat
    assert "fg.red.hex" in flat
    assert "fg.note.hex" in flat

    # Check bg keys
    assert "bg.normal.hex" in flat
    assert "bg.red.hex" in flat
    assert "bg.highlight.hex" in flat

    # Check ui keys
    assert "ui.normal.hex" in flat
    assert "ui.red.hex" in flat


def test_scheme_flatten_with_rgb(dark_normal_scheme: Scheme) -> None:
    """Test flatten includes RGB components when present."""
    scheme_with_rgb = dark_normal_scheme.add_rgb()
    flat = scheme_with_rgb.flatten()

    # Check RGB keys are present
    assert "fg.normal.rgb" in flat
    assert "fg.normal.r" in flat
    assert "fg.normal.g" in flat
    assert "fg.normal.b" in flat

    assert "bg.red.rgb" in flat
    assert "ui.blue.r" in flat


def test_scheme_flatten_values(dark_normal_scheme: Scheme) -> None:
    """Test that flattened values match original nested access."""
    flat = dark_normal_scheme.flatten()

    # Test a few values
    assert flat["fg.normal.hex"] == dark_normal_scheme["fg"]["normal"]["hex"]
    assert flat["bg.red.256"] == str(dark_normal_scheme["bg"]["red"]["256"])
    assert flat["ui.blue.hex"] == dark_normal_scheme["ui"]["blue"]["hex"]


def test_scheme_all_modes_and_contrasts() -> None:
    """Test scheme works with all mode and contrast combinations."""
    for mode in [Mode.DARK, Mode.LIGHT]:
        for contrast in [Contrast.HARD, Contrast.NORMAL, Contrast.SOFT]:
            palette = Palette(mode, contrast)
            scheme = Scheme(palette)

            # Basic structure checks
            assert "fg" in scheme
            assert "bg" in scheme
            assert "ui" in scheme

            # All colors should be Ansi objects
            assert isinstance(scheme["fg"]["normal"], Ansi)
            assert isinstance(scheme["bg"]["red"], Ansi)
            assert isinstance(scheme["ui"]["blue"], Ansi)


def test_scheme_setitem(dark_normal_scheme: Scheme) -> None:
    """Test that __setitem__ allows modifying scheme."""
    new_ansi = Ansi(15, "#ffffff")
    dark_normal_scheme["fg"]["custom"] = new_ansi

    assert "custom" in dark_normal_scheme["fg"]
    assert dark_normal_scheme["fg"]["custom"] == new_ansi


def test_scheme_iteration_contents(dark_normal_scheme: Scheme) -> None:
    """Test iteration yields correct category names."""
    categories = set(dark_normal_scheme)
    assert categories == {"fg", "bg", "ui"}
