# geotag2kml

### Description
Blog post: http://forensenellanebbia.blogspot.it/2015/08/geotag2kml-python-script-to-create-kml.html

The is a cross-platform script that uses [Exiftool](https://www.sno.phy.queensu.ca/~phil/exiftool/) to find geotagged files and parse their metadata. It then creates two different Google Earth .KML files to display the photos/videos found.

The .KML file will be structured this way:

- GPS points are grouped and sorted by YYYY | YYYY:MM | YYYY:MM:DD;
- the first GPS point of each date is indicated with an icon different from the other points of the same date;
- the GPS points occurred on the same date are connected with a colored line;
- placemark names contain: "Timestamp | Make Model | Altitude | Filename";
- when clicking on a placemark icon, the picture preview appears.

![KML](https://pbs.twimg.com/media/DuULuZeX4AUDOVJ.jpg)
![KML](https://pbs.twimg.com/media/CMdDUfDWcAQfmvD.png)

---
### Prerequisites
  - Python v2.7
  - Exiftool *(recommended version: 10.62 or above. If you're using Windows, please rename the executable of ExifTool to "exiftool.exe")*
---
### How to use

Run the script and type the absolute path of the directory to parse. Examples:

- **Microsoft Windows**: python geotag2kml.py C:\MyPhotos
- **Ubuntu**: python geotag2kml.py /home/username/Desktop/Photos

The output files will be saved under the given path.
