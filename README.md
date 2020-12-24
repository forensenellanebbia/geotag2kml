# geotag2kml

### Description
Blog post: https://forensenellanebbia.blogspot.com/2015/08/geotag2kml-python-script-to-create-kml.html

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
  - Python v3.8+
    - [geopy](https://pypi.org/project/geopy/)
	- [Pillow](https://python-pillow.org/)
    - [randomcolor](https://pypi.org/project/randomcolor/)
  - [Exiftool](https://exiftool.org/) *(If you're using Windows, please rename the executable to "exiftool.exe")*
  - [ImageMagick](https://imagemagick.org/) *(Win/Mac)* or [libheif-examples](https://launchpad.net/~strukturag/+archive/ubuntu/libheif) *(Ubuntu)*

### How to install each component
**#Python3 dependencies**<br>
- pip3 install geopy Pillow randomcolor

**#Windows 10 x64**<br>
- ExifTool: https://exiftool.org/ (Windows Executable - rename to *exiftool.exe*)
- ImageMagick: https://imagemagick.org/script/download.php#windows (Win64 dynamic at 16 bits-per-pixel component)

**#Ubuntu (tested with Ubuntu 20.04) **<br>
- ExifTool: sudo apt install libimage-exiftool-perl
- libheif-examples: sudo add-apt-repository ppa:strukturag/libde265 && sudo add-apt-repository ppa:strukturag/libheif && sudo apt-get update && sudo apt-get install libheif-examples
- Google Earth: wget -O ~/google-earth.deb https://dl.google.com/dl/earth/client/current/google-earth-pro-stable_current_amd64.deb && sudo dpkg -i ~/google-earth.deb

**#Mac OS (tested with macOS Big Sur 11.0.1) **<br>
- If you're having any issue while installing Pillow, try: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && brew install libjpeg && pip3 install Pillow --user
- ExifTool: https://exiftool.org/ (MacOS Package)
- ImageMagick: brew install imagemagick
---
### How to use

Run the script and type the absolute path of the directory to parse. Examples:

- **Microsoft Windows**: python3 geotag2kml.py C:\MyPhotos
- **Ubuntu**: python3 geotag2kml.py /home/username/Desktop/Photos

The output files will be saved under the given path.
