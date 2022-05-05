# Changelog

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [1.1.1] - 2022-05-05

### Added

- Support for Python 3.6 through 3.10. (#90)

### Fixed

- `StandalonePipeline` no longer has a dependency on `redis`. SA and HA
pipeline class references must now use the fully-qualified class name. (#89)

## [1.1.0] - 2022-05-01

### Added

- `ConsoleMetricsExporter` for locally debugging pipelines without an APM service. (#46)
- Built-in Elastic APM metrics exporter. (#47)
- `Sequence` class for logical groupings of steps. (#53)

### Changed

- Bumped `redis` dependency to 4.2.2. (#50)
- Bumped `elastic-apm` to 6.9.1. (#56)

### Removed

- Dependencies for `MetricsExporter` and `PipelineLock` modules are no longer included in the base package and must
now be installed separately through `watergrid[...]` metapackages. (#54)
- Documentation from Readme. Docs now located at
[https://armmaster17.github.io/watergrid-python/](https://armmaster17.github.io/watergrid-python/). (#65)

### Fixed

- Resolved issue with objects inside a `DataContext` not being copied when the
  output mode of a step is set to `SPLIT`. (#6)
- Pipeline now stops running if there are no more contexts to process in a new step. (#78)

## [1.0.1] - 2022-04-01
### Fixed

- Broken release pipeline to PyPI.

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


[Unreleased]: https://github.com/ARMmaster17/watergrid-python/compare/1.1.1...HEAD
[1.1.1]: https://github.com/ARMmaster17/watergrid-python/compare/1.1.0...1.1.1
[1.1.0]: https://github.com/ARMmaster17/watergrid-python/compare/1.0.1...1.1.0
[1.0.1]: https://github.com/ARMmaster17/watergrid-python/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/ARMmaster17/watergrid-python/releases/tag/1.0.0
