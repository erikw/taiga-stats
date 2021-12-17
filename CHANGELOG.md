# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2021-12-17
- More roboust version check.

## [1.2.2] - 2021-12-01
- Fix travis build badge

## [1.2.1] - 2021-12-01
- Bug fix: should not crash if $XDG_CONFIG_HOME is not set in the envionment.
- Bug fix: The submodule importlib.metadata was added in 3.8. Added the backport importlib-metadata package to python <3.8.
- Set up Travis builds: https://app.travis-ci.com/github/erikw/taiga-stats

## [1.2.0] - 2021-11-04
- Upgrade dependencies, most notably python-taiga to `1.0.0`

## [1.1.0] - 2021-11-04
- Add `--version|-v` flags.

## [1.0.4] - 2021-11-04
- Add installation instructions with `pipx`.

## [1.0.3] - 2021-11-04
- Trim wheel size by removing img/ and sample_data/.

## [1.0.2] - 2021-11-03
- Update README.md with setup instructions (--url, --auth-token).

## [1.0.1] - 2021-11-02
- Add README.md badges for easier overview of current status and support.

## [1.0.0] - 2021-11-02
- Published on pypy.org
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
