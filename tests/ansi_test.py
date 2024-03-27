# Copyright (c) 2024-2026 Dawid Kurek <hello@dawikur.dev>
"""Tests for Ansi class"""

from chiroptera.ansi import Ansi


def test_ansi_with_ansi16_code() -> None:
    """Test Ansi with ANSI16 code."""
    ansi = Ansi(1, "#cc241d")

    assert ansi["2"] == 1
    assert ansi["8"] == 1
    assert ansi["16"] == 1
    assert "256" in ansi
    assert ansi["hex"] == "#cc241d"


def test_ansi_without_ansi16_code() -> None:
    """Test Ansi without ANSI16 code (tint colors)."""
    ansi = Ansi(None, "#242425")

    assert ansi["2"] == 0
    assert ansi["8"] == 0
    assert ansi["16"] == 0
    assert "256" in ansi
    assert ansi["hex"] == "#242425"


def test_ansi_str_format() -> None:
    """Test Ansi properly formats to str."""
    ansi = Ansi(None, "#242425")

    assert str(ansi) == "Ansi{#242425}"


def test_ansi_repr_format() -> None:
    """Test Ansi properly formats to str."""
    ansi = Ansi(2, "#242425")

    assert repr(ansi) == "Ansi{2: 1, 8: 2, 16: 2, 256: 234, hex: #242425}"


def test_ansi_preserves_hex() -> None:
    """Test that hex color is preserved."""
    hex_color = "#458588"
    ansi = Ansi(4, hex_color)

    assert ansi["hex"] == hex_color


def test_ansi_xterm256_conversion() -> None:
    """Test that xterm256 conversion produces valid values."""
    ansi = Ansi(1, "#cc241d")

    # xterm256 should be in valid range
    assert 0 <= int(ansi["256"]) <= 255
    assert isinstance(ansi["256"], str)


def test_ansi_black() -> None:
    """Test pure black color."""
    ansi = Ansi(0, "#000000")

    assert ansi["2"] == 0
    assert ansi["8"] == 0
    assert ansi["16"] == 0
    assert ansi["hex"] == "#000000"


def test_ansi_white() -> None:
    """Test pure white color."""
    ansi = Ansi(15, "#ffffff")

    assert ansi["2"] == 1
    assert ansi["8"] == 7
    assert ansi["16"] == 15
    assert ansi["hex"] == "#ffffff"


def test_ansi_bright_colors() -> None:
    """Test bright colors (ANSI 9-15)."""
    ansi = Ansi(9, "#ff0000")

    assert ansi["2"] == 1
    assert ansi["8"] == 1
    assert ansi["16"] == 9
