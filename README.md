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
  - [Exiftool](https://exiftool.org/) 
  - [ImageMagick](https://imagemagick.org/) *(Win/Mac)* or [libheif](https://launchpad.net/~strukturag/+archive/ubuntu/libheif) *(Ubuntu)*

### How to install each component
**#Python3 dependencies**<br>
- pip3 install geopy Pillow randomcolor

**#Windows 10 x64**<br>
- ExifTool: https://exiftool.org/ (rename the executable to *exiftool.exe*)
- ImageMagick: https://imagemagick.org/script/download.php#windows (Win64 dynamic at 16 bits-per-pixel component)

**#Ubuntu (last tested with Ubuntu 22.04.1 LTS)**<br>
```bash
#ExifTool
sudo apt install libimage-exiftool-perl -y

#libheif
sudo apt-get install libheif-examples

#Google Earth
wget -O ~/google-earth.deb https://dl.google.com/dl/earth/client/current/google-earth-pro-stable_current_amd64.deb && sudo dpkg -i ~/google-earth.deb
```

**#Mac OS (tested with macOS Big Sur 11.0.1)**<br>
- If you're having any issue while installing Pillow, try:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && brew install libjpeg && pip3 install Pillow --user
```
- ExifTool: https://exiftool.org/ (MacOS Package)
- ImageMagick
```bash
brew install imagemagick
```
---
### How to use the script

Run the script and type the absolute path of the directory to parse. Examples:

- **Microsoft Windows**: python3 geotag2kml.py C:\MyPhotos
- **Ubuntu**: python3 geotag2kml.py /home/username/Desktop/Photos

The output files will be saved under the given path.
