# Copyright (c) 2024-2026 Dawid Kurek <hello@dawikur.dev>
"""Integration tests"""

import subprocess
import sys
from pathlib import Path

from chiroptera import Contrast, Mode, Palette
from chiroptera.utils import format_line


def test_format_line_function() -> None:
    """Test the format_line utility function."""
    test_string = "Background: {bg.hex}, Foreground: {fg.hex}"
    palette = Palette(Mode.DARK, Contrast.NORMAL).add_rgb()
    tokens = palette.flatten()

    result = format_line(test_string, tokens)

    # Should have replaced placeholders
    assert "{bg.hex}" not in result
    assert "{fg.hex}" not in result
    assert "#" in result  # Should contain hex colors


def test_palette_consistency() -> None:
    """Test that palette generation is consistent."""
    palette1 = Palette(Mode.DARK, Contrast.NORMAL)
    palette2 = Palette(Mode.DARK, Contrast.NORMAL)

    # Same parameters should produce same colors
    assert palette1["bg"]["hex"] == palette2["bg"]["hex"]
    assert palette1["fg"]["hex"] == palette2["fg"]["hex"]
    assert palette1["red"]["hex"] == palette2["red"]["hex"]


def test_cli_renders_template(tmp_path: Path) -> None:
    """The CLI can render a user-owned template with palette tokens."""
    template = tmp_path / "theme.conf.tmpl"
    output = tmp_path / "theme.conf"
    _ = template.write_text("background={bg.hex}\naccent={fg.red.hex}\n")

    result = subprocess.run(
        [
            sys.executable,
            "bin/chiroptera",
            "--dark",
            "--template",
            str(template),
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert output.read_text() == "background=#373737\naccent=#fea391\n"
    assert result.stdout == ""


def test_cli_renders_template_to_stdout(tmp_path: Path) -> None:
    """The CLI writes a rendered template to stdout without --output."""
    template = tmp_path / "theme.conf.tmpl"
    _ = template.write_text("background={bg.hex}\naccent={fg.red.hex}\n")

    result = subprocess.run(
        [sys.executable, "bin/chiroptera", "--dark", "--template", str(template)],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout == "background=#373737\naccent=#fea391\n"


def test_cli_prints_scheme_names_with_dot_notation() -> None:
    """The CLI prints semantic scheme names in the same dotted form as templates."""
    result = subprocess.run(
        [sys.executable, "bin/chiroptera", "--light", "--soft", "-n", "^bg\\."],
        check=True,
        capture_output=True,
        text=True,
    )

    names = {line.partition(" = ")[0] for line in result.stdout.splitlines()}

    assert "bg.magenta" in names
    assert all("_" not in name for name in names)
