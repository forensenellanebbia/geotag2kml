# geotag2kml v0.1

I needed a tool on Microsoft Windows to parse thousands of geotagged pictures and view them on Google Earth.

My script was written to:

- parse recursively geotagged pictures
- create a KML file to view geotagged pictures on Google Earth
- group and sort GPS data by date
- show visually for each date where the first geotagged picture was taken. Each first GPS point is indicated by the icon of a small man
- connect the GPS points of each date with a colored line
- get the preview of a picture when clicking on a placemark
- list make and model information of each digital camera used to take and geotag the analyzed photos

== Prerequisites ==
  - python v2.7
  - exiftool (rename the executable into "exiftool.exe" and put it in the same folder of the script)
  - Google Earth

== Usage ==

Run the script and type the absolute path of the directory to be parsed.

