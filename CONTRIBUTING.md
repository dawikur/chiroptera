# Contributing to chiroptera

Thanks for considering a contribution. chiroptera is a color system generator
with a Vim and Neovim renderer, so changes to its generator, templates, and
generated output should remain consistent across all six mode and contrast
variants.

## Reporting bugs and proposing changes

Open a GitHub issue for bugs, missing highlight groups, plugin integrations,
or feature ideas. For visual problems, include:

- Vim or Neovim version, terminal, and whether true color is enabled;
- the selected chiroptera variant;
- the relevant plugin and its version, when applicable;
- a minimal reproduction and a screenshot when it helps.

Please use ordinary GitHub issues for accessibility, contrast, and visual
problems. See [SECURITY.md](SECURITY.md) only for security-sensitive reports.

## Development setup

```bash
pip install -r requirements.txt
make test
make lint
make build
```

Use `make site` to build the publishable documentation site in `build/site/`.

## Making a change

- Keep pull requests focused and explain the user-visible effect.
- Add or update tests for changes to Python generation logic.
- Run `make test`, `make lint`, and `make build` before opening a pull request.
- Changes to palette or contrast logic must preserve the documented contrast
  guarantees; update the contrast tests and README tables when values change.
- Changes to `colors/chiroptera_tmpl.vim` require regenerated colorschemes.
- Plugin support belongs in `colors/chiroptera/plugins/` and should gracefully
  link to existing groups when practical.
- Update the README or changelog when a change affects users or release notes.

## Style

Python code is formatted with Black and isort, checked with mypy and pylint,
and tested with pytest. Run `pre-commit run --all-files` before submitting when
possible.

By contributing, you agree that your work may be distributed under this
repository's [MIT License](LICENSE).
