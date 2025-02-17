# Changelog

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
