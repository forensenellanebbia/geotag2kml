# Changelog
All notable changes to this project will be documented in this file.

## [v0.6] - 2018-12-19
### Added
- Thumbnail creation (stored in a separate folder) for each geotagged file in order to speed up the opening of the "_thumbs" .KML file (Requires: **Pillow**) and avoid crashing Google Earth Pro
- File format conversion from .HEIC to .JPG (Requires: *Win/Mac* **ImageMagick**, *Ubuntu* **libheif-examples**). The script doesn't replace the original files
- Metadata in the placemark pop-ups
- Calculation of the distance traveled for each path (Requires: **geopy**)
- Ability to view GPS points on *Google Maps* website by clicking on the provided URL in the placemark pop-ups
- Ability to view paths on *Bing* by clicking on the provided URL in the paths pop-ups
- Counter for path lines created (paths containing at least two GPS points)
### Changed
- Removed *altitude* from placemark names to make names shorter. The altitude is shown in the placemark pop-ups
- Path lines are assigned a brighter color (Requires: **randomcolor**)
### Fixed
- Pictures with 90-degree rotation (*Orientation* tag: Rotate 90 CW) are now displayed in the correct orientation in the placemark pop-ups
---
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
