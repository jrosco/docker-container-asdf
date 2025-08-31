# Changelog

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.8] - 2025-08-31
### Changed
- 📌 Update golang to version `1.25.0` [#45](https://github.com/jrosco/docker-container-asdf/pull/45)

## [0.1.7] - 2025-07-20
### Changed
- 📌 Update golang to version `1.24.5` [#41](https://github.com/jrosco/docker-container-asdf/pull/41)

## [0.1.6] - 2025-06-10
### Changed
- 📌 Update golang to version `1.24.4` [#39](https://github.com/jrosco/docker-container-asdf/pull/39)
- 
## [0.1.5] - 2025-05-20
### Changed
- 📌 Update golang to version `1.24.3` [#24](https://github.com/jrosco/docker-container-asdf/pull/24)
  
## [0.1.4] - 2025-02-19
### Changed
- 📌 Update asdf to version `0.16.2` [#26](https://github.com/jrosco/docker-container-asdf/pull/26)

## [0.1.3] - 2025-02-19
### Added
- 🍻 Allow users to add a .tool-versions file for installs [#17](https://github.com/jrosco/docker-container-asdf/pull/17)

## [0.1.2] - 2025-02-18
### Changed
- :wrench: Use major, minor and patch version env values for `golang`
- :green_heart: Updated some ci/cd workflow build stuff

## [0.1.1] - 2025-02-17
### Changed
- :pushpin: Update `asdf` to version `0.16.1`

## [0.1.0] - 2025-02-17
### Added
- ⚙️ Improved GitHub Actions workflows:
  - ➕ Added and fine-tuned CI workflows.
  - :sparkles: Introduced a GitHub Action for merging.
- :memo: Added documentation:
  - 📚 Added a changelog.
### Changed
- :wrench: Updated Docker base images to support `asdf v0.16.0`, now using Go instead of Bash scripts.
- :wrench: Updated all Dockerfiles and `docker-compose` configurations to support `asdf > v0.16.0`.
- :memo: Updated documentation:
  - 🛠️ Refined README with updated support version badges and additional details.
- 🛠️ Updated example toolsets for better compatibility.
- :pushpin: Pinned versions to prevent breaking changes with newer releases.
### Removed
- :coffin: Disabled RedHat support due to UBI8 images not supporting Go `v1.23.6`.

## [0.0.0] - 2023-12-16
### Added
- :sparkles: Initial release of the project.

---

### Format:
- **Added** for new features.
- **Changed** for updates to existing functionality.
- **Deprecated** for soon-to-be removed features.
- **Removed** for now-removed features.
- **Fixed** for bug fixes.
- **Security** for vulnerabilities addressed.

[Unreleased]: https://github.com/jrosco/docker-container-asdf/compare/main...HEAD
[0.0.0]: https://github.com/jrosco/docker-container-asdf/compare/0.0.0...HEAD
[0.1.0]: https://github.com/jrosco/docker-container-asdf/compare/0.0.0...0.1.0
[0.1.1]: https://github.com/jrosco/docker-container-asdf/compare/0.1.0...0.1.1
[0.1.2]: https://github.com/jrosco/docker-container-asdf/compare/0.1.1...0.1.2
[0.1.3]: https://github.com/jrosco/docker-container-asdf/compare/0.1.2...0.1.3
[0.1.4]: https://github.com/jrosco/docker-container-asdf/compare/0.1.3...0.1.4
[0.1.5]: https://github.com/jrosco/docker-container-asdf/compare/0.1.4...0.1.5
[0.1.6]: https://github.com/jrosco/docker-container-asdf/compare/0.1.5...0.1.6
[0.1.7]: https://github.com/jrosco/docker-container-asdf/compare/0.1.6...0.1.7
[0.1.8]: https://github.com/jrosco/docker-container-asdf/compare/0.1.7...0.1.8
