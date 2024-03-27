# Release checklist

Reusable checklist for preparing and publishing a stable release.

## Plan the release

- [ ] Confirm the scope of the release and review all issues and pull requests
  targeted for the release.
- [ ] Triage unresolved bugs and document any intentional deferrals.
- [ ] Review feedback from the previous release.
- [ ] Decide whether this release changes palette tokens, generated output,
  highlight groups, CLI behavior, or public Python APIs.
- [ ] Decide whether the Python package will be published to PyPI.

## Verify the candidate

- [ ] Update the version in `pyproject.toml`.
- [ ] Update `CHANGELOG.md` with user-visible changes, fixes, and migration
  notes.
- [ ] Update README, Vim help, and examples when behavior or installation
  changes.
- [ ] Run `make test` and confirm all tests pass with 100% coverage.
- [ ] Run `make lint`.
- [ ] Run `pre-commit run --all-files`.
- [ ] Run `make build` and verify all generated colorschemes and assets.
- [ ] Smoke-test every colorscheme in Vim and Neovim when available.
- [ ] Check contrast guarantees and inspect visual changes in both modes.
- [ ] Run `make package`.
- [ ] Run `twine check dist/*`.
- [ ] Test the installed wheel and CLI in a clean environment.
- [ ] Run `make site` and inspect the generated site locally.
- [ ] Confirm `git diff --check` passes.
- [ ] Review the complete diff and confirm generated files are up to date.

## Compatibility review

- [ ] Verify supported Python versions and dependency changes.
- [ ] Verify Vim and Neovim compatibility.
- [ ] Check bundled plugin integrations affected by highlight-group changes.
- [ ] Confirm template tokens remain compatible, or document breaking changes.
- [ ] Check terminal behavior with true color and fallback colors.
- [ ] Review security advisories and dependency updates.

## Publish the release

- [ ] Merge the verified release candidate into `main`.
- [ ] Push the release commit and confirm GitHub Actions is green.
- [ ] Create an annotated tag matching the release version from the verified
  commit.
- [ ] Push the tag to GitHub.
- [ ] Create the GitHub release using the matching changelog section.
- [ ] Mark the release as the latest stable release.
- [ ] Attach distribution artifacts when appropriate.
- [ ] Publish to PyPI if that decision was made.

## Update the website and integrations

- [ ] Publish the site generated from the release commit.
- [ ] Check the canonical URL and Open Graph preview.
- [ ] Verify installation instructions use the new stable release.
- [ ] Check plugin-manager installation from the tagged repository.
- [ ] Update any external package, plugin, or documentation references.

## Announce and follow up

- [ ] Publish release notes with the most important user-visible changes.
- [ ] Announce the release in the relevant Vim/Neovim communities.
- [ ] Link to the changelog, installation instructions, and issue tracker.
- [ ] Monitor issues, CI failures, and compatibility reports after release.
- [ ] Update the next release section in `CHANGELOG.md` when appropriate.
- [ ] Record any follow-up work in `TODO.md`.
