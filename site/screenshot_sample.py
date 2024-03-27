"""Small preview model used for theme screenshots."""

from dataclasses import dataclass
from enum import Enum


class Mode(str, Enum):
    """Theme modes available for the preview."""

    DARK = "dark"
    LIGHT = "light"


@dataclass(frozen=True)
class Preview:
    """Compact token set used to render a theme preview."""

    mode: Mode
    contrast: str
    accent: str
    tokens: dict[str, str]


def build_preview(mode: Mode, contrast: str = "normal") -> Preview:
    """Create a compact set of tokens for a rendered preview."""
    if contrast not in {"hard", "normal", "soft"}:
        raise ValueError(f"Unknown contrast: {contrast!r}")

    background = "#373736" if mode is Mode.DARK else "#dbd7c3"
    foreground = "#a3a092" if mode is Mode.DARK else "#5d5b56"

    tokens = {
        "background": background,
        "foreground": foreground,
        "accent": "#83a598",
        "muted": "#928f84",
    }

    # Bright accents stay readable on the selected background.
    return Preview(
        mode=mode,
        contrast=contrast,
        accent=tokens["accent"],
        tokens=tokens,
    )


preview = build_preview(Mode.DARK)
print(f"{preview.mode.value} · {preview.contrast}: {preview.accent}")
