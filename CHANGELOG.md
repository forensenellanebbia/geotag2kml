# Changelog
All notable changes to this project will be documented in this file.

## [v0.5] - 2018-12-13
### Added
- Creation of two different .KML files: 
    1. .KML file with standard placemark **icons**
    2. .KML file with **thumbnails** of geotagged images used as placemark icons. It can take some time to load this file.
- Detection of geotagged .HEIC images

### Changed
- GPS points are grouped by: YYYY | YYYY:MM | YYYY:MM:DD. Useful when dealing with a large amount of files.
- Output files renamed to: *ScriptExecTimestamp*_exif.csv, *ScriptExecTimestamp*_icons.kml and *ScriptExecTimestamp*_thumbs.kml
---
## [v0.4] - 2018-12-08
### Changed
- The script is now cross-platform
- Changed field separator from * to |
### Fixed
- Random color assignment for path lines
---
## [v0.3] - 2018-04-07
### Added
- Support for iPhone geotagged videos (.MOV)
---
## [v0.2] - 2016-04-03
### Fixed
- General bug fixes 
---
## [v0.1] - 2015-08
- First public release
