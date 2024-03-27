# Copyright (c) 2024-2026 Dawid Kurek <hello@dawikur.dev>
"""Repalette an image based on the mode and contrast."""

from collections.abc import Mapping
from typing import Optional, Protocol, TypeVar, Union

from PIL import Image
from tqdm import tqdm

from chiroptera.colors import Colors
from chiroptera.palette import Contrast, Mode, Palette
from chiroptera.scheme import Scheme

# Type aliases for clarity
RGBTuple = tuple[int, int, int]
ColorScheme = dict[str, RGBTuple]  # Map color name to RGB tuple
PixelPalette = dict[RGBTuple, RGBTuple]
PaletteKey = TypeVar("PaletteKey")


def palette_tokens(
    palette: Palette, scheme: Scheme, mode: Mode, contrast: Contrast
) -> dict[str, str]:
    """Return all palette and scheme tokens accepted by template files."""
    return {
        **palette.add_rgb().flatten(),
        **scheme.add_rgb().flatten(),
        "name": "chiroptera",
        "mode": mode.value,
        "contrast": contrast.value,
    }


class PixelAccess(Protocol):
    """The RGB pixel access operations used from Pillow."""

    def __getitem__(self, xy: tuple[int, int]) -> Union[float, tuple[int, ...]]: ...

    def __setitem__(
        self, xy: tuple[int, int], color: Union[float, tuple[int, ...]]
    ) -> None: ...


def __rgb_pixel(pixel: Union[float, tuple[int, ...]]) -> RGBTuple:
    """Return an RGB triple from a Pillow pixel value."""
    if not isinstance(pixel, tuple) or len(pixel) < 3:
        raise ValueError("expected an RGB pixel")
    return (pixel[0], pixel[1], pixel[2])


def __calculate_avg(palette: Mapping[PaletteKey, RGBTuple]) -> float:
    """Calculate average color from the palette.

    Args:
        palette: Dictionary mapping pixel values to RGB tuples

    Returns:
        Average RGB value across all colors in palette
    """
    palette_sum = 0
    for _, color in palette.items():
        palette_sum += color[0] + color[1] + color[2]

    return palette_sum / (len(palette) * 3)


def __get_scheme(mode: Mode, contrast: Contrast, colors: Colors) -> ColorScheme:
    """Get a color scheme based on the mode and contrast.

    Args:
        mode: Dark or light mode
        contrast: Hard, normal, or soft contrast
        colors: Colors object for generating the palette

    Returns:
        Dictionary mapping color names to RGB tuples
    """
    scheme_tmpl = Palette(mode, contrast, colors).add_rgb()

    scheme: ColorScheme = {}

    for name, color in scheme_tmpl.items():
        scheme[name] = (
            int(str(color["r"]), 16),
            int(str(color["g"]), 16),
            int(str(color["b"]), 16),
        )

    return scheme


def __get_schemes(
    pixels: PixelAccess,
    size: tuple[int, int],
    mode_out: Mode,
    contrast: Contrast,
    colors: Colors,
) -> tuple[PixelPalette, tuple[ColorScheme, ColorScheme]]:
    """Get the input and output color schemes based on the mode and contrast.

    Args:
        pixels: PIL PixelAccess object for reading image pixels
        size: Image dimensions (width, height)
        mode_out: Target output mode (dark or light)
        contrast: Contrast level
        colors: Colors object for generating palettes

    Returns:
        Tuple of (pixel_palette, (input_scheme, output_scheme))
    """
    scheme_dark = __get_scheme(Mode.DARK, contrast, colors)
    scheme_light = __get_scheme(Mode.LIGHT, contrast, colors)

    palette: PixelPalette = {}
    for y in tqdm(range(size[1]), desc="read"):
        for x in range(size[0]):
            pixel = __rgb_pixel(pixels[x, y])
            palette[pixel] = pixel

    scheme_dark_avg = __calculate_avg(scheme_dark)
    scheme_light_avg = __calculate_avg(scheme_light)
    palette_avg = __calculate_avg(palette)

    mode_in = (
        Mode.DARK
        if (
            pow(palette_avg - scheme_dark_avg, 2)
            < pow(palette_avg - scheme_light_avg, 2)
        )
        else Mode.LIGHT
    )

    return (
        palette,
        (
            scheme_dark if (mode_in == Mode.DARK) else scheme_light,
            scheme_dark if (mode_out == Mode.DARK) else scheme_light,
        ),
    )


def __find_closest(
    scheme_in: ColorScheme, scheme_out: ColorScheme, color: tuple[int, ...]
) -> tuple[Optional[RGBTuple], Optional[RGBTuple]]:
    """Find the closest color in the scheme using Euclidean distance.

    Args:
        scheme_in: Input color scheme to search
        scheme_out: Output color scheme to map to
        color: RGB tuple to find closest match for

    Returns:
        Tuple of (closest_input_color, corresponding_output_color) or (None, None)
    """
    color0, color1, color2 = color[:3]

    distance = 255 * 255 * 3 + 1
    out_name = None

    for name, (wings0, wings1, wings2) in scheme_in.items():
        errors = [color0 - wings0, color1 - wings1, color2 - wings2]
        error = sum(err * err for err in errors)

        if error < distance:
            distance = error
            out_name = name

    if out_name is None:
        return None, None
    return scheme_in[out_name], scheme_out[out_name]


def __diffuse(
    pixels: PixelAccess,
    x: int,
    y: int,
    quant_error: RGBTuple,
    distribution: float,
) -> None:
    """Diffuse the quantization error to the pixel (Floyd-Steinberg dithering).

    Args:
        pixels: PIL PixelAccess object
        x: Pixel x coordinate
        y: Pixel y coordinate
        quant_error: RGB error tuple from quantization
        distribution: Fraction of error to distribute to this pixel
    """
    pixel = __rgb_pixel(pixels[x, y])

    pixels[x, y] = (
        pixel[0] + int(quant_error[0] * distribution),
        pixel[1] + int(quant_error[1] * distribution),
        pixel[2] + int(quant_error[2] * distribution),
    )


def __apply_palette(
    pixels: PixelAccess,
    image: Image.Image,
    palette: PixelPalette,
    scheme_inout: tuple[ColorScheme, ColorScheme],
) -> None:
    """Apply the closest target color for each unique source color."""
    for color in tqdm(palette, desc="update"):
        _, target = __find_closest(*scheme_inout, color)
        assert target is not None
        palette[color] = target

    for y in tqdm(range(image.height), desc="apply"):
        for x in range(image.width):
            pixels[x, y] = palette[__rgb_pixel(pixels[x, y])]


def __apply_dithering(
    pixels: PixelAccess,
    image: Image.Image,
    scheme_inout: tuple[ColorScheme, ColorScheme],
) -> None:
    """Apply palette conversion using Floyd-Steinberg dithering."""
    for y in tqdm(range(image.height), desc="apply"):
        for x in range(image.width):
            old_pixel = __rgb_pixel(pixels[x, y])
            closest_pixel, new_pixel = __find_closest(*scheme_inout, old_pixel)
            assert closest_pixel is not None and new_pixel is not None
            pixels[x, y] = new_pixel

            quant_error = (
                old_pixel[0] - closest_pixel[0],
                old_pixel[1] - closest_pixel[1],
                old_pixel[2] - closest_pixel[2],
            )

            if (x + 1) < image.width:
                __diffuse(pixels, x + 1, y, quant_error, 7 / 16)

            if (y + 1) < image.height:
                if 0 <= (x - 1):
                    __diffuse(pixels, x - 1, y + 1, quant_error, 3 / 16)

                __diffuse(pixels, x, y + 1, quant_error, 5 / 16)

                if (x + 1) < image.width:
                    __diffuse(pixels, x + 1, y + 1, quant_error, 1 / 16)


def repalette(
    image: Image.Image,
    mode_out: Mode,
    contrast: Contrast,
    colors: Optional[Colors] = None,
    dithering: bool = False,
) -> Image.Image:
    """Repalette an image based on the mode and contrast.

    Args:
        image: PIL Image object to repalette
        mode_out: Target color mode (dark or light)
        contrast: Contrast level (hard, normal, or soft)
        colors: Optional Colors object, creates default if not provided
        dithering: Whether to apply Floyd-Steinberg dithering

    Returns:
        The modified PIL Image object. Non-RGB images are converted to RGB,
        so callers should use the returned image.
    """

    # Pillow returns scalar values for modes such as ``L`` and ``P``.  The
    # palette matching and dithering below operate on RGB triples, so
    # normalize every input image before accessing its pixels.
    if image.mode != "RGB":
        image = image.convert("RGB")

    if colors is None:
        colors = Colors()

    pixels = image.load()
    assert pixels is not None

    palette, scheme_inout = __get_schemes(
        pixels, (image.width, image.height), mode_out, contrast, colors
    )

    if dithering:
        __apply_dithering(pixels, image, scheme_inout)
    else:
        __apply_palette(pixels, image, palette, scheme_inout)

    return image


def format_line(line: str, tokens: dict[str, str]) -> str:
    """Format a line by replacing {token} placeholders with values.

    Note: Uses simple string replacement instead of str.format() because
    template files (e.g., vim files) may contain literal braces for other
    purposes (fold markers like {{{, dict literals, etc.) that would
    conflict with format string syntax.

    Args:
        line: Template string with {placeholder} tokens
        tokens: Dictionary mapping placeholder names to replacement values

    Returns:
        Formatted string with placeholders replaced

    Example:
        >>> format_line("Color: {fg.hex}", {"fg.hex": "#ffffff"})
        "Color: #ffffff"
    """
    for token, value in tokens.items():
        line = line.replace(f"{{{token}}}", value)
    return line


def format_lines(lines: list[str], tokens: dict[str, str]) -> list[str]:
    """Format multiple lines by replacing {token} placeholders.

    Args:
        lines: List of template strings
        tokens: Dictionary mapping placeholder names to replacement values

    Returns:
        List of formatted strings
    """
    return [format_line(line, tokens) for line in lines]
