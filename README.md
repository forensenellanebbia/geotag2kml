# geotag2kml

Blog post: http://forensenellanebbia.blogspot.it/2015/08/geotag2kml-python-script-to-create-kml.html

I needed a tool on Microsoft Windows to parse thousands of geotagged pictures and show them on Google Earth.

My script was written to:

- parse recursively geotagged pictures
- create a KML file to show geotagged pictures on Google Earth
- group and sort GPS data by date
- show visually for each date where the first geotagged picture was taken. Each first GPS point is indicated by the icon of a small man
- connect the GPS points of each date with a colored line
- get the preview of a picture when clicking on a placemark
- list make and model information of each digital camera used to take and geotag the analyzed photos

== Prerequisites ==
  - Python v2.7+
  - Exiftool v9+ (rename the executable into "exiftool.exe" and put it in the same folder of the script)
  - Google Earth v7+

== Usage ==

Run the script and type the absolute path of the directory to be parsed.
The script will create a file named "GoogleEarth.kml" and will save it into the given path.

