# geotag2kml

Blog post: http://forensenellanebbia.blogspot.it/2015/08/geotag2kml-python-script-to-create-kml.html

The script uses [Exiftool](https://www.sno.phy.queensu.ca/~phil/exiftool/) to find geotagged files and parse their metadata. It then creates a Google Earth KML file to display the photos/videos found.

The KML file will be structured this way:

- GPS data is grouped and sorted by date;
- the first GPS point of each date is indicated with an icon different from the other points of the same date;
- the GPS points occurred on the same date are connected with a colored line;
- placemark names contain: "Timestamp | Make Model | Altitude | Filename";
- picture previews appear when clicking on a placemark.

![KML](https://pbs.twimg.com/media/CMdDUfDWcAQfmvD.png){:width="800px" height="411px"}

== Prerequisites ==
  - Python v2.7
  - Exiftool v9+ (if you're using Windows, please rename the executable of ExifTool to "exiftool.exe")

== Usage ==

Run the script and type the absolute path of the directory to parse.
This is a cross-platform script.
