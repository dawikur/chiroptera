# AI Agent Guide for chiroptera

This file provides context for AI agents (Claude Code, Cursor, Copilot, etc.) when working with the chiroptera colorscheme generator.

## Project Overview

**chiroptera** 🦇 is a Vim colorscheme generator that creates perceptually uniform color palettes using LAB color space. It generates 6 colorscheme variants (dark/light × hard/normal/soft) with symmetric contrast ratios and WCAG AA compliant syntax highlighting colors.

### Name Origin

The name is inspired by **bat wings**:
- **Two wings** = dark and light modes (duality of day/night)
- **Membrane tension** between wing bones (patagium) = hard/normal/soft contrast levels
- **Perfect wing symmetry** = symmetric contrast ratios between dark and light modes
- **Nocturnal nature** = fits the terminal/coding aesthetic
- **Echolocation precision** = perceptual accuracy of LAB color space

## Quick Commands

### Build and Generate

```bash
# Generate all colorscheme files
python scripts/generate_chiroptera

# View palette (dark normal)
python bin/chiroptera --dark

# View palette (light hard)
python bin/chiroptera --light --hard
```

### Testing

```bash
# Run all tests (76 tests)
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/contrast_test.py

# Run with coverage
pytest --cov=chiroptera --cov-report=term-missing
```

### Linting

```bash
# Type checking (strict mode)
mypy chiroptera/

# Code formatting
black chiroptera/ tests/

# Import sorting
isort chiroptera/ tests/

# Linting
pylint chiroptera/

# Pre-commit hooks (runs all checks)
pre-commit run --all-files
```

### Installation

```bash
# Install in development mode
pip install -e .

# Install dependencies
pip install -r requirements.txt
```

## Architecture

The color generation flow:

1. **Base Colors** (`colors.py`): Define base hex colors (gruvbox-inspired)
2. **LAB Conversion** (`colors.py`): Convert to LAB color space for interpolation
3. **Palette Generation** (`palette.py`): Generate 18-step gradient with Mode and Contrast
4. **Scheme Organization** (`scheme.py`): Organize palette into semantic categories (fg/bg/ui)
5. **ANSI Mapping** (`ansi.py`): Convert to ANSI codes (2, 8, 16, 256-color, hex)
6. **Template Processing** (`utils.py`): Apply colors to Vim template files
7. **File Generation** (`scripts/generate`): Output final colorscheme files

### Key Components

- **Colors class** (`colors.py`):
  - Manages LAB color space conversions
  - Provides callable color generators: `colors["red"](10)` generates red at lightness level 10
  - Supports iteration: `for color in colors` yields chromatic color names
  - String representation: `str(colors["red"])` returns base hex color

- **ColorFunction wrapper** (`colors.py`):
  - Dual interface: callable for generation, string for base hex
  - Enables pattern: `str(colors[name]).replace("#", "")`

- **Palette class** (`palette.py`):
  - Generates complete color sets based on Mode (DARK/LIGHT) and Contrast (HARD/NORMAL/SOFT)
  - Creates foreground/background variants with symmetric contrast ratios
  - Flat structure: `fg`, `bg`, `red.bright`, `green.dim`, etc.
  - Methods: `add_rgb()` adds RGB components, `flatten()` creates flat dict
  - Dict-like access with full interface

- **Scheme class** (`scheme.py`):
  - Higher-level semantic organization of Palette colors
  - Hierarchical structure: `fg`, `bg`, `ui` categories
  - Each category contains: `normal`, `note`, `mark`, `ignore` + chromatic colors
  - Access pattern: `scheme['fg']['normal']['hex']`
  - Methods: `add_rgb()` adds RGB components, `flatten()` creates flat dict
  - Dict-like access with full interface

- **Ansi class** (`ansi.py`):
  - Dataclass with private fields (`_ansi_2`, `_ansi_16`, `_hex`, etc.)
  - Dict-like interface for all access: `ansi["256"]`, `ansi["hex"]`
  - Converts between color formats (2/8/16/256-color, hex, RGB)
  - Implements xterm-256 color space quantization
  - Full dict-like interface: `__getitem__`, `__setitem__`, `__contains__`, `__iter__`, `items()`

- **Template system**:
  - Files ending in `_tmpl` contain placeholders like `{bg.hex}` or `{fg.normal.hex}`
  - Simple string replacement (not format_map due to Vim fold markers)
  - 612 tokens available (369 from Palette + 243 from Scheme)

### Directory Structure

- `chiroptera/`: Python module with color generation logic (6 modules)
  - `__init__.py`: Package exports
  - `ansi.py`: ANSI color code handling and conversion
  - `colors.py`: Base colors, LAB color space conversions
  - `palette.py`: Palette generation with Mode/Contrast enums
  - `scheme.py`: Semantic color organization
  - `utils.py`: Template formatting and image repaletting
- `tests/`: Comprehensive test suite (76 tests, 75% coverage)
  - `ansi_test.py`: ANSI conversion and dataclass interface
  - `colors_test.py`: Colors class, iteration, string representation
  - `contrast_test.py`: WCAG contrast ratios and symmetry
  - `coverage_boost_test.py`: Edge case coverage tests
  - `integration_test.py`: End-to-end integration tests
  - `palette_test.py`: Palette generation and variants
  - `scheme_test.py`: Scheme organization tests
- `bin/`: CLI tool (`chiroptera`) for viewing palettes
- `scripts/`: Build script (`generate`) for generating colorscheme files
- `colors/`: Generated Vim colorscheme files (gitignored, except templates)
- `assets/`: SVG/PNG previews (programmatically recolored)
- `.github/workflows/`: GitHub Actions CI/CD configuration

## Code Style

- **Formatting**: black, isort (black profile)
- **Type checking**: mypy strict mode (`strict = true`, `ignore_missing_imports = true`)
- **Linting**: pylint
- **Pre-commit hooks**: Configured to run all checks automatically

## Testing

The project has comprehensive unit tests covering:

- **Color generation**: LAB color space conversions, gradient monotonicity
- **Palette generation**: All mode/contrast combinations, color variants
- **ANSI conversion**: Code mapping, xterm-256 quantization
- **Contrast ratios**: WCAG compliance, symmetric dark/light modes
- **Template formatting**: Placeholder replacement, special cases
- **Iteration and string conversion**: Colors class dual interface

Tests are automatically run in CI on Python 3.9 through 3.14.

### Contrast Tests

The `contrast_test.py` suite verifies:
- Dark and light modes maintain documented contrast ratios
- Closely matched contrast between modes (difference < 0.25)
- Hard contrast variant exceeds WCAG AA (≥ 4.5:1)
- **All** bright color variants meet WCAG AA (≥ 4.5:1) for syntax highlighting
- Dim color variants have low contrast for subtle backgrounds (< 2.0:1)

## CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`) runs on push and PR:
1. Installs dependencies from `requirements.txt`
2. Runs pre-commit hooks (black, mypy, isort, pylint)
3. Runs pytest test suite (76 tests)
4. Generates colorscheme files to verify templates work
5. Uploads generated colorschemes as artifacts

## Key Design Decisions

### LAB Color Space
Colors use LAB space for perceptually uniform interpolation. This ensures:
- Tint progression is visually linear
- Color relationships remain consistent across modes
- Symmetric contrast ratios between dark and light modes

### Contrast Philosophy
- **Normal text**: ~4.6:1 (meets WCAG AA 4.5:1) for balanced daily use
- **Hard text**: ~5.3:1 (exceeds WCAG AA) for higher contrast
- **Soft text**: ~4.0:1 (intentionally below WCAG AA); use bright text roles when AA is required
- **Syntax highlighting**: ≥4.5:1 (all bright colors meet WCAG AA)
- **Background highlights**: ~1.2:1 (intentionally low for subtlety)
- **Symmetric design**: Dark and light modes have closely matched contrast (difference < 0.25)

### Three-Tier Variant System
- **dim**: Low contrast, used as backgrounds
- **normal**: Medium contrast, used for UI
- **bright**: High contrast (WCAG AA), used for foreground syntax

### Color Adjustments
- **Base red**: Changed from `#cc241d` (gruvbox) to `#ad1817` (optimized)
  - Darker, more saturated base produces brighter results at high LAB lightness
  - Achieves 5.95:1 (dark normal) and 6.52:1 (light normal) contrast for red.bright

- **Light mode foreground**: Changed from `middle - 1` to `middle - 3.5`
  - Achieves symmetric contrast ratios with dark mode
  - Difference between modes < 0.25 for all contrast variants

### Backward Compatibility
The refactoring to dataclasses maintains backward compatibility:
- Dict-like access: `palette["bg"]["hex"]`, `colors["red"](10)`
- Iteration support: `for name in palette`, `for color in colors`
- String conversion: `str(colors["red"])` returns base hex

## Documentation

Keep `site/` as the self-contained website module, including generator
inputs; `make site` writes the publishable subset to `build/site/`.

## Important Notes

- **Never** create commits unless explicitly requested by the user
- **Always** read files before modifying them
- **Prefer** editing existing files over creating new ones
- **Use** specialized tools over bash commands when possible
- **Run** tests after modifying color generation logic to verify contrast ratios
- **Check** mypy after type hint changes to ensure strict mode compliance

## Common Tasks

### Adding a New Color
1. Add to `BaseColors` in `colors.py`
2. Add LAB conversion in `Colors.__init__`
3. Add method in `Colors` class
4. Update `__getitem__` to return ColorFunction
5. Add to iteration list if chromatic color
6. Add tests in `test_colors.py`
7. Run tests and verify contrast ratios

### Modifying Contrast
1. Update offset calculations in `palette.py`
2. Update expected values in `test_contrast.py`
3. Run contrast tests to verify WCAG compliance
4. Update README.md contrast tables
5. Regenerate colorscheme files

### Updating Templates
1. Modify `*_tmpl.vim` files in `colors/`
2. Use placeholder format: `{color.variant.format}`
3. Avoid using `{{` or `}}` (conflicts with Vim fold markers)
4. Run `python scripts/generate` to regenerate
5. Verify generated files manually

## Statistics

- **6** Python modules in `chiroptera/`
- **7** test modules in `tests/`
- **671** lines of source code (excluding comments and blank lines)
- **1,070** lines of test code (excluding comments and blank lines)
- **75%** test coverage (100% on ansi.py, colors.py, palette.py, scheme.py)
- **76** tests (all passing)
- **100%** mypy strict type checking compliance
- **100%** Python 3.9+ compatible
- **0** linting errors

## External References

- [gruvbox](https://github.com/morhetz/gruvbox) - Color inspiration
- [solarized](https://ethanschoonover.com/solarized/) - Light/dark switching, LAB color space
- [base16](https://github.com/chriskempson/base16) - Palette concept
- [WCAG contrast ratios](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) - Accessibility guidelines
