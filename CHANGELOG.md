# Changelog

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [1.0.0] - 2022-04-01
### Added
- Core library functionality.
- High availability pipeline using the `HAPipeline` class.
- `RedisLock` for high availability mode using Redis.
- Package distribution on PyPI.
- Shared step contexts.
- Context manipulation through the `OutputMode` enum.
- Base class for building a metric exporter to an external APM solution.

### Fixed
- Staggered node startup no longer causes mid-interval pipeline runs on other nodes in HA mode.


[Unreleased]: https://github.com/ARMmaster17/watergrid-python/compare/1.0.0...HEAD
[1.0.0]: https://github.com/ARMmaster17/watergrid-python/releases/tag/1.0.0