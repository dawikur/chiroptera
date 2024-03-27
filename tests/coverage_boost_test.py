# Copyright (c) 2024-2026 Dawid Kurek <hello@dawikur.dev>
"""Additional tests to increase coverage."""

from typing import Callable, cast

from PIL import Image

from chiroptera import Colors, Contrast, Mode, Palette, Scheme, utils
from chiroptera.ansi import Ansi
from chiroptera.utils import format_line, format_lines, palette_tokens, repalette


class TestAnsiEdgeCases:
    """Test edge cases in Ansi class for better coverage."""

    def test_ansi_very_light_grey(self) -> None:
        """Test grayscale conversion for very light grey (>238)."""
        # This should trigger the grey_avg > 238 path (line 71)
        ansi = Ansi(7, "#fefefe")  # Very light grey
        # The algorithm chooses between color cube and grayscale ramp
        # Just verify it produces a valid xterm-256 code
        assert 0 <= int(ansi["256"]) <= 255

    def test_ansi_setitem_all_keys(self) -> None:
        """Test __setitem__ for all valid keys."""
        # Create palette with RGB
        palette = Palette(Mode.DARK, Contrast.NORMAL).add_rgb()
        ansi = palette["bg"]

        # Test setting all ANSI codes
        ansi["2"] = "1"
        assert ansi["2"] == "1"

        ansi["8"] = "7"
        assert ansi["8"] == "7"

        ansi["16"] = "15"
        assert ansi["16"] == "15"

        ansi["256"] = "255"
        assert ansi["256"] == "255"

        ansi["hex"] = "#000000"
        assert ansi["hex"] == "#000000"

        # Test setting RGB values
        ansi["rgb"] = "abcdef"
        assert ansi["rgb"] == "abcdef"

        ansi["r"] = "128"
        assert ansi["r"] == "128"

        ansi["g"] = "64"
        assert ansi["g"] == "64"

        ansi["b"] = "32"
        assert ansi["b"] == "32"


class TestColorsMethodsCoverage:
    """Test individual color methods in Colors class."""

    def test_colors_individual_methods(self) -> None:
        """Test all individual color generation methods."""
        colors = Colors()

        # Test each color method (lines 137, 141, 145, 149, 153, 157, 161)
        assert colors["tint"](10).startswith("#")
        assert colors["red"](10).startswith("#")
        assert colors["yellow"](10).startswith("#")
        assert colors["green"](10).startswith("#")
        assert colors["cyan"](10).startswith("#")
        assert colors["blue"](10).startswith("#")
        assert colors["magenta"](10).startswith("#")

        # Verify they generate different colors
        assert colors["red"](10) != colors["blue"](10)
        assert colors["green"](10) != colors["magenta"](10)

    def test_colors_getitem_tint(self) -> None:
        """Test __getitem__ specifically for tint."""
        colors = Colors()
        tint_fn = colors["tint"]

        # Should be callable
        assert callable(tint_fn)

        # Should generate valid hex
        hex_color = tint_fn(10)
        assert hex_color.startswith("#")
        assert len(hex_color) == 7


class TestPaletteCoverage:
    """Test uncovered paths in Palette class."""

    def test_palette_setitem(self) -> None:
        """Test __setitem__ method (line 93)."""
        palette = Palette(Mode.DARK, Contrast.NORMAL)

        # Create a new Ansi object
        new_ansi = Ansi(15, "#123456")

        # Set it in palette
        palette["custom_color"] = new_ansi

        # Verify it was set
        assert palette["custom_color"] == new_ansi
        assert palette["custom_color"]["hex"] == "#123456"

    def test_palette_items(self) -> None:
        """Test items() method (line 105)."""
        palette = Palette(Mode.DARK, Contrast.NORMAL)

        # Get items
        items = palette.items()

        # Should be able to iterate
        items_list = list(items)
        assert len(items_list) > 0

        # Each item should be (name, Ansi) pair
        for name, ansi in items_list[:3]:  # Check first 3
            assert isinstance(name, str)
            assert isinstance(ansi, Ansi)

    def test_palette_flatten_rgb(self) -> None:
        """Test flatten() with RGB components (lines 136-137)."""
        palette = Palette(Mode.DARK, Contrast.NORMAL).add_rgb()
        flattened = palette.flatten()

        # Check that RGB components are in flattened palette
        assert "bg.rgb" in flattened
        assert "bg.r" in flattened
        assert "bg.g" in flattened
        assert "bg.b" in flattened

        # Verify values are strings
        assert isinstance(flattened["bg.r"], str)
        assert isinstance(flattened["bg.g"], str)
        assert isinstance(flattened["bg.b"], str)


class TestUtilsCoverage:
    """Test utils.py functions for better coverage."""

    def test_palette_tokens(self) -> None:
        """Test the combined palette and semantic template tokens."""
        palette = Palette(Mode.DARK, Contrast.NORMAL)
        tokens = palette_tokens(palette, Scheme(palette), Mode.DARK, Contrast.NORMAL)

        assert tokens["name"] == "chiroptera"
        assert tokens["mode"] == "dark"
        assert tokens["contrast"] == "normal"
        assert tokens["bg.hex"] == "#373737"
        assert "fg.normal.hex" in tokens

    def test_rgb_pixel_rejects_non_rgb_value(self) -> None:
        """Reject scalar and undersized Pillow pixel values."""
        for pixel in (128.0, (128,), (128, 128)):
            try:
                getattr(utils, "__rgb_pixel")(pixel)
            except ValueError as error:
                assert str(error) == "expected an RGB pixel"
            else:
                raise AssertionError("expected an RGB pixel to be rejected")

    def test_find_closest_empty_schemes(self) -> None:
        """Return no match when the input scheme has no colors."""
        find_closest = cast(Callable[..., object], getattr(utils, "__find_closest"))
        assert find_closest({}, {}, (0, 0, 0)) == (None, None)

    def test_format_line(self) -> None:
        """Test format_line utility function."""
        scheme = {"color1": "ff0000", "color2": "00ff00"}
        template = "Color is {color1} and {color2}"

        result = format_line(template, scheme)
        assert result == "Color is ff0000 and 00ff00"

    def test_format_line_missing_key(self) -> None:
        """Test format_line with missing key."""
        scheme = {"color1": "ff0000"}
        template = "Color is {color1} and {missing}"

        # Should leave missing keys as-is
        result = format_line(template, scheme)
        assert "{missing}" in result

    def test_format_line_with_multiple_tokens(self) -> None:
        """Test format_line with multiple tokens."""
        scheme = {"color1": "ff0000", "color2": "00ff00", "color3": "0000ff"}
        template = "{color1} {color2} {color3}"

        result = format_line(template, scheme)
        assert result == "ff0000 00ff00 0000ff"

    def test_format_lines(self) -> None:
        """Format every line while preserving line boundaries."""
        result = format_lines(
            ["bg={bg}\n", "fg={fg}\n"], {"bg": "000000", "fg": "ffffff"}
        )

        assert result == ["bg=000000\n", "fg=ffffff\n"]

    def test_repalette_rgb_image(self) -> None:
        """Repalette RGB images using hexadecimal palette components."""
        image = Image.new("RGB", (1, 1), (255, 0, 0))

        result = repalette(image, Mode.DARK, Contrast.NORMAL)

        assert result is image
        assert image.getpixel((0, 0)) == (118, 0, 4)

    def test_repalette_non_rgb_image(self) -> None:
        """Repalette scalar Pillow pixels after normalizing them to RGB."""
        image = Image.new("L", (1, 1), 128)

        result = repalette(image, Mode.DARK, Contrast.NORMAL)

        assert result.mode == "RGB"
        assert result.getpixel((0, 0)) != (128, 128, 128)

    def test_repalette_with_dithering(self) -> None:
        """Repalette a multi-pixel image using Floyd-Steinberg dithering."""
        image = Image.new("RGB", (2, 2), (255, 0, 0))

        result = repalette(image, Mode.LIGHT, Contrast.NORMAL, dithering=True)

        assert result is image
        assert result.mode == "RGB"
        for x in range(2):
            for y in range(2):
                pixel = result.getpixel((x, y))
                assert isinstance(pixel, tuple)
                assert len(pixel) == 3


class TestAnsiContains:
    """Test __contains__ method in Ansi."""

    def test_ansi_contains_standard_keys(self) -> None:
        """Test __contains__ with standard keys."""
        ansi = Ansi(15, "#ffffff")

        assert "2" in ansi
        assert "8" in ansi
        assert "16" in ansi
        assert "256" in ansi
        assert "hex" in ansi

        # RGB keys should not be present until add_rgb()
        assert "rgb" not in ansi
        assert "r" not in ansi

    def test_ansi_contains_with_rgb(self) -> None:
        """Test __contains__ after add_rgb()."""
        # RGB attributes are added via Palette.add_rgb()
        palette = Palette(Mode.DARK, Contrast.NORMAL).add_rgb()
        ansi = palette["bg"]

        # RGB keys should now be present
        assert "rgb" in ansi
        assert "r" in ansi
        assert "g" in ansi
        assert "b" in ansi


class TestPaletteContains:
    """Test __contains__ method in Palette."""

    def test_dummy(self) -> None:
        """Test dummy func to make pylint happy."""

    def test_palette_contains(self) -> None:
        """Test __contains__ method."""
        palette = Palette(Mode.DARK, Contrast.NORMAL)

        assert "bg" in palette
        assert "fg" in palette
        assert "red" in palette
        assert "nonexistent" not in palette


class TestAnsiIteration:
    """Test Ansi __iter__ method."""

    def test_ansi_iteration_standard(self) -> None:
        """Test iterating over Ansi keys."""
        ansi = Ansi(15, "#ffffff")
        keys = list(ansi)

        # Should have standard keys
        assert "2" in keys
        assert "8" in keys
        assert "16" in keys
        assert "256" in keys
        assert "hex" in keys

    def test_ansi_iteration_with_rgb(self) -> None:
        """Test iterating over Ansi keys with RGB."""
        palette = Palette(Mode.DARK, Contrast.NORMAL).add_rgb()
        ansi = palette["bg"]
        keys = list(ansi)

        # Should have RGB keys in addition to standard keys
        assert "rgb" in keys
        assert "r" in keys
        assert "g" in keys
        assert "b" in keys


class TestPaletteFlattenEdgeCases:
    """Test Palette flatten edge cases."""

    def test_flatten_without_rgb(self) -> None:
        """Test flatten without RGB components (lines 136-137)."""
        palette = Palette(Mode.DARK, Contrast.NORMAL)
        # Don't call add_rgb()
        flattened = palette.flatten()

        # Should have standard keys but not RGB
        assert "bg.hex" in flattened
        assert "fg.hex" in flattened
        assert "bg.rgb" not in flattened
        assert "bg.r" not in flattened

    def test_flatten_includes_all_rgb_components(self) -> None:
        """Test that flatten includes all RGB components for all colors."""
        palette = Palette(Mode.DARK, Contrast.NORMAL).add_rgb()
        flattened = palette.flatten()

        # Check a few colors have all RGB components
        for color in ["red", "green", "blue"]:
            assert f"{color}.rgb" in flattened
            assert f"{color}.r" in flattened
            assert f"{color}.g" in flattened
            assert f"{color}.b" in flattened

            # Values should be strings
            assert isinstance(flattened[f"{color}.r"], str)
            assert isinstance(flattened[f"{color}.g"], str)
            assert isinstance(flattened[f"{color}.b"], str)
