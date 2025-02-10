# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
## [1.7.0] - 2025-02-11
### Changed
- Upgrade to Python 3.11-3.12 to fix build errors related to https://github.com/urllib3/urllib3/issues/2168. As a a part of this, upgrade of major versions in matplotlib, pylint etc.

## [1.6.0] - 2022-04-05
### Changed
- Rename master branch to main

## [1.5.0] - 2022-04-01
### Changed
- Update dependencies
- Switch from flake8 to pylint, to solve depdendency issue with mkdocs.

## [1.4.0] - 2022-01-31
### Changed
- Improve release commands with poetry version bump feature.

## [1.3.0] - 2021-12-17
### Changed
- More roboust version check.

## [1.2.2] - 2021-12-01
### Fixed
- Travis build badge

## [1.2.1] - 2021-12-01
## Added
- Set up Travis builds: https://app.travis-ci.com/github/erikw/taiga-stats
### Fixed
- Bug fix: should not crash if $XDG_CONFIG_HOME is not set in the envionment.
- Bug fix: The submodule importlib.metadata was added in 3.8. Added the backport importlib-metadata package to python <3.8.

## [1.2.0] - 2021-11-04
### Changed
- Upgrade dependencies, most notably python-taiga to `1.0.0`

## [1.1.0] - 2021-11-04
## Added
- `--version|-v` flags.

## [1.0.4] - 2021-11-04
## Added
- Installation instructions with `pipx`.

## [1.0.3] - 2021-11-04
## Changed
- Trim wheel size by removing img/ and sample_data/.

## [1.0.2] - 2021-11-03
## Changed
- Update README.md with setup instructions (--url, --auth-token).

## [1.0.1] - 2021-11-02
## Added
- README.md badges for easier overview of current status and support.

## [1.0.0] - 2021-11-02
- Published on pypy.org

## Fixed
- Prevent python 3.10.0 as it does not currently work with numpy for this version.

## [0.1.1] - 2021-11-02
- Make README.md images work on pypi.org

## [0.1.0] - 2021-11-02
- No feature changes from previous version.
- Project being properly built with poetry. Restructuring of the source modules.
- Once this is working, there will soon be an 1.0.0 release, also published to pypi.org

## [0.0.4] - 2018-02-02
- New command: list_us_statuses
- Add setup.txt for requirements.
- Small bug fixes.

## [0.0.3] - 2015-12-06
- Major README update on project and features.
- Improve help texts and configuration files.

## [0.0.2] - 2015-12-02
- Minor README updates.

## [0.0.1] - 2015-12-02
- Initial import from other old VCS.
