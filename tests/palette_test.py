# Copyright (c) 2024-2026 Dawid Kurek <hello@dawikur.dev>
"""Tests for Palette class"""

from chiroptera.palette import Contrast, Mode, Palette


def test_palette_dark_normal() -> None:
    """Test dark mode with normal contrast."""
    palette = Palette(Mode.DARK, Contrast.NORMAL)

    assert "bg" in palette
    assert "fg" in palette
    assert "red" in palette
    assert "green" in palette
    assert "blue" in palette


def test_palette_light_normal() -> None:
    """Test light mode with normal contrast."""
    palette = Palette(Mode.LIGHT, Contrast.NORMAL)

    assert "bg" in palette
    assert "fg" in palette
    assert "red" in palette


def test_palette_all_contrasts() -> None:
    """Test that all contrast levels work."""
    for contrast in [Contrast.HARD, Contrast.NORMAL, Contrast.SOFT]:
        palette = Palette(Mode.DARK, contrast)
        assert "bg" in palette
        assert "fg" in palette


def test_palette_contains_ansi_codes() -> None:
    """Test that palette entries have ANSI codes."""
    palette = Palette(Mode.DARK, Contrast.NORMAL)

    # bg should have ANSI code 0
    assert palette["bg"]["16"] == 0
    # fg should have ANSI code 7
    assert palette["fg"]["16"] == 7


def test_palette_str_format() -> None:
    """Test palette properly formats to str."""
    palette = Palette(Mode.DARK, Contrast.NORMAL)

    assert str(palette).startswith("Palette{")


def test_palette_repr_format() -> None:
    """Test palette properly formats to repr."""
    palette = Palette(Mode.DARK, Contrast.NORMAL)

    assert repr(palette).startswith("Palette{")


def test_palette_contains_hex_colors() -> None:
    """Test that palette entries have hex colors."""
    palette = Palette(Mode.DARK, Contrast.NORMAL)

    for name in ["bg", "fg", "red", "green", "blue"]:
        assert "hex" in palette[name]
        hex_color = palette[name]["hex"]
        assert str(hex_color).startswith("#")
        assert len(str(hex_color)) == 7


def test_palette_add_rgb() -> None:
    """Test add_rgb adds RGB components."""
    palette = Palette(Mode.DARK, Contrast.NORMAL).add_rgb()

    for name in ["bg", "fg", "red"]:
        assert "r" in palette[name]
        assert "g" in palette[name]
        assert "b" in palette[name]
        assert "rgb" in palette[name]

        # Verify RGB values are in valid range
        assert 0 <= int(str(palette[name]["r"]), 16) <= 255
        assert 0 <= int(str(palette[name]["g"]), 16) <= 255
        assert 0 <= int(str(palette[name]["b"]), 16) <= 255


def test_palette_flatten() -> None:
    """Test flatten creates single-level dict."""
    palette = Palette(Mode.DARK, Contrast.NORMAL).add_rgb()
    flat = palette.flatten()

    # Should have flattened keys like "bg.hex", "bg.r", etc.
    assert "bg.hex" in flat
    assert "bg.r" in flat
    assert "fg.hex" in flat
    assert "red.hex" in flat
    assert "bg.bright.hex" in flat

    # All values should be strings
    for value in flat.values():
        assert isinstance(value, str)


def test_palette_dark_vs_light_different() -> None:
    """Test that dark and light modes produce different colors."""
    dark_palette = Palette(Mode.DARK, Contrast.NORMAL)
    light_palette = Palette(Mode.LIGHT, Contrast.NORMAL)

    # Background colors should be different
    assert dark_palette["bg"]["hex"] != light_palette["bg"]["hex"]
    assert dark_palette["fg"]["hex"] != light_palette["fg"]["hex"]


def test_palette_contrast_variants_different() -> None:
    """Test that different contrast levels produce different colors."""
    hard = Palette(Mode.DARK, Contrast.HARD)
    normal = Palette(Mode.DARK, Contrast.NORMAL)
    soft = Palette(Mode.DARK, Contrast.SOFT)

    # Background colors should differ between contrasts
    assert hard["bg"]["hex"] != normal["bg"]["hex"]
    assert normal["bg"]["hex"] != soft["bg"]["hex"]


def test_palette_has_dim_and_bright_variants() -> None:
    """Test that palette includes dim and bright color variants."""
    palette = Palette(Mode.DARK, Contrast.NORMAL)

    for color in ["red", "green", "blue", "yellow", "cyan", "magenta"]:
        assert color in palette
        assert f"{color}.dim" in palette
        assert f"{color}.bright" in palette


def test_palette_has_bg_variants() -> None:
    """Test that palette includes bg variants."""
    palette = Palette(Mode.DARK, Contrast.NORMAL)

    assert "bg.dim" in palette
    assert "bg" in palette
    assert "bg.bright" in palette


def test_palette_has_fg_variants() -> None:
    """Test that palette includes fg variants."""
    palette = Palette(Mode.DARK, Contrast.NORMAL)

    assert "fg.dim" in palette
    assert "fg" in palette
    assert "fg.bright" in palette
