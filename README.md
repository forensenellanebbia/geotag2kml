# geotag2kml

### Description
Blog post: http://forensenellanebbia.blogspot.it/2015/08/geotag2kml-python-script-to-create-kml.html

The is a cross-platform script that uses ExifTool to find geotagged files and parse their metadata. It then creates two different Google Earth .KML files to display the photos/videos found.

The .KML file will be structured this way:

- GPS points are grouped and sorted by YYYY | YYYY:MM | YYYY:MM:DD;
- the first GPS point of each date is indicated with an icon different from the other points of the same date;
- the GPS points occurred on the same date are connected with a colored line;
- placemark names contain: "Timestamp | Make Model | Filename";
- when clicking on a placemark icon, the picture preview appears.

![KML](https://pbs.twimg.com/media/DuULuZeX4AUDOVJ.jpg)

![KML](https://pbs.twimg.com/media/CMdDUfDWcAQfmvD.png)

---
### Prerequisites
  - Python v2.7
    - [geopy](https://pypi.org/project/geopy/)
	- [Pillow](https://python-pillow.org/)
    - [randomcolor](https://pypi.org/project/randomcolor/)
  - [Exiftool](https://www.sno.phy.queensu.ca/~phil/exiftool/) *(recommended version: 10.80 or above. If you're using Windows, please rename the executable to "exiftool.exe")*
  - [ImageMagick](https://imagemagick.org/) *(Win/Mac)* or [libheif-examples](https://launchpad.net/~strukturag/+archive/ubuntu/libheif) *(Ubuntu)*

### How to install each component
**#Python dependencies**<br>
- geopy: pip install geopy
- Pillow: pip install Pillow
- randomcolor: pip install randomcolor

**#Windows**<br>
- ExifTool: https://www.sno.phy.queensu.ca/~phil/exiftool/ (Windows Executable - rename to *exiftool.exe*)
- ImageMagick: https://imagemagick.org/script/download.php#windows (Win64 dynamic at 16 bits-per-pixel component)

**#Ubuntu**<br>
- ExifTool: https://www.sno.phy.queensu.ca/~phil/exiftool/ (Compile from source code: perl Makefile.PL && make && sudo make install)
- libheif-examples: sudo add-apt-repository ppa:strukturag/libheif && sudo apt-get update && sudo apt-get install libheif-examples

**#Mac OS**<br>
- ExifTool: https://www.sno.phy.queensu.ca/~phil/exiftool/ (MacOS Package)
- ImageMagick: brew install --with-libheif imagemagick
---
### How to use

Run the script and type the absolute path of the directory to parse. Examples:

- **Microsoft Windows**: python geotag2kml.py C:\MyPhotos
- **Ubuntu**: python geotag2kml.py /home/username/Desktop/Photos

The output files will be saved under the given path.
