#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
*********************************** LICENSE ***********************************
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You can view the GNU General Public License at <https://www.gnu.org/licenses/>
*******************************************************************************

geotag2kml - WARNING: This program is provided "as-is"

Author    : Gabriele Zambelli (Twitter: @gazambelli)
Blog post : https://forensenellanebbia.blogspot.com/2015/08/geotag2kml-python-script-to-create-kml.html

This script will create a Google Earth KML file from geotagged photos and videos

Prerequisites (see the Readme file for more information):
 - Python v3.8+
    * geopy       : https://pypi.org/project/geopy/
    * Pillow      : https://python-pillow.org/
    * randomcolor : https://pypi.org/project/randomcolor/
 - ExifTool       : https://exiftool.org/
   (If you're using Windows, please rename the executable of ExifTool to "exiftool.exe")
 - ImageMagick    : https://imagemagick.org/

Version history
[v0.7] 2020-12-24 Updated to Python3, fixed broken URLs
[v0.6] 2018-12-19
[v0.5] 2018-12-13
[v0.4] 2018-12-08
[v0.3] 2018-04-07
[v0.2] 2016-04-03
[v0.1] 2015-08

Script tested on:
 - Windows 10 (20H2)      | ExifTool 12.12 | Python 3.8.3
 - Ubuntu 20.04           | ExifTool 11.88 | Python 3.8.5
 - macOS Big Sur (11.0.1) | ExifTool 12.12 | Python 3.8.2
 - Google Earth Pro 7.3.3.7786

References:
 EXIFTOOL
  - ExifTool GPS Tags                 : https://exiftool.org/TagNames/GPS.html
  - ExifTool Application Documentation: https://exiftool.org/exiftool_pod.html
 GOOGLE EARTH
  - Generating a Google Earth KML file: https://exiftool.org/forum/index.php/topic,1688.msg7373.html#msg7373
  - KML Reference                     : https://developers.google.com/kml/documentation/kmlreference#kmlextensions
  - Altitude Modes                    : https://developers.google.com/kml/documentation/altitudemode
  - Icons                             : https://sites.google.com/site/gmapsdevelopment/
  - Force to open the external browser: https://support.google.com/earth/forum/AAAA_9IoRZwq5X_DGQMpyo/
 GEOPY
  - Calculating Distance              : https://geopy.readthedocs.io/en/stable/#module-geopy.distance
 RANDOMCOLOR
  - Usage                             : https://github.com/kevinwuhoo/randomcolor-py
  - Examples                          : https://github.com/davidmerfield/randomColor
"""

from collections import Counter
from datetime import datetime
from geopy.distance import geodesic
from PIL import Image, ExifTags
import csv
import os
import platform
import randomcolor
import subprocess
import sys

version            = "0.7"
line_colors_random = []


#***************** FUNCTIONS *****************
def welcome():
	exceptions = 0
	try:
		subprocess.check_output(["exiftool", "-ver"]) #check if exiftool is installed
	except:
		exceptions += 1
		print ("\n ERROR: exiftool was not found")
	if platform.system() == "Linux":
		try:
			subprocess.check_output(["which", "heif-convert"]) #check if libheif-examples is installed
		except:
			exceptions += 1
			print ("\n ERROR: The package libheif-examples was not found")
	else:
		try:
			subprocess.check_output(["magick", "-help"]) #check if ImageMagick is installed
		except:
			exceptions += 1
			print ("\n ERROR: ImageMagick was not found")
	if exceptions > 0:
		print ("\n")
		sys.exit()
	if len(sys.argv) == 1:
		print ("\n geotag2kml (v%s)" % version)
		exift_ver = os.popen("exiftool -ver").read()
		if float(exift_ver) < 10.80:
			print ("\n !! It's recommended to use a more recent version of ExifTool !!\n")
		print ("\n This script will create a Google Earth KML file from geotagged photos and videos")
		print ("\n How to use:\n\n ==> python3 " + os.path.basename(sys.argv[0]) + " AbsolutePathToAnalyze")
		print ("\n [The script will search recursively                 ]")
		print (" [The output files will be saved under the given path]\n\n")
		sys.exit()
	elif len(sys.argv) == 2:
		if os.path.exists(sys.argv[1]) == True:
			os.chdir(sys.argv[1])
		else:
			print ("\n ERROR: the path %s doesn't exist") % sys.argv[1]
			sys.exit()

def os_check(exift_run):
	if my_os != "Windows":
		exift_run = exift_run.replace('"',"'")
	return exift_run

def kml_creation(kml_type):
	# color legend - from left to right: ABGR color space
	red         = "ff0000ff" 
	yellow      = "ff00ffff"
	violet      = "ffaa00ff"
	green       = "ff00ff00"
	pink        = "fff8a5f8"
	brownish    = "ff0055ff"
	white       = "ffffffff"
	darkblue    = "ffff0000"
	mustard     = "ff00aaaa"
	lightblue   = "ffffaa55" #From left to right: (A)lpha=ff,(B)lue=ff,(G)reen=aa,(R)ed=55
	line_colors = [red, yellow, violet, green, pink, brownish, white, darkblue, mustard, lightblue]

	#KML HEADER
	kml_start = """<?xml version="1.0" encoding="UTF-8"?>
	<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
	<Document>
		<name>Summary: %d waypoint(s), %d date(s), %d device(s)</name>
		<open>1</open>
		<Style id="sh_pink-blank">
			<IconStyle>
				<scale>1.3</scale>
				<Icon>
					<href>https://maps.google.com/mapfiles/kml/paddle/pink-blank.png</href>
				</Icon>
				<hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
			</IconStyle>
			<LabelStyle>
				<scale>1.1</scale>
			</LabelStyle>
			<ListStyle>
				<ItemIcon>
					<href>https://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
				</ItemIcon>
			</ListStyle>
		</Style>
		<Style id="sh_arrow">
			<IconStyle>
				<scale>1.4</scale>
				<Icon>
					<href>https://maps.google.com/mapfiles/kml/shapes/arrow.png</href>
				</Icon>
				<hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
			</IconStyle>
			<LabelStyle>
				<scale>1.1</scale>
			</LabelStyle>
			<ListStyle>
			</ListStyle>
		</Style>
		<StyleMap id="msn_pink-blank">
			<Pair>
				<key>normal</key>
				<styleUrl>#sn_pink-blank</styleUrl>
			</Pair>
			<Pair>
				<key>highlight</key>
				<styleUrl>#sh_pink-blank</styleUrl>
			</Pair>
		</StyleMap>
		<Style id="sh_man">
			<IconStyle>
				<scale>1.4</scale>
				<Icon>
					<href>https://maps.google.com/mapfiles/kml/shapes/man.png</href>
				</Icon>
			</IconStyle>
			<LabelStyle>
				<scale>1.1</scale>
			</LabelStyle>
		</Style>
		<Style id="sn_pink-blank">
			<IconStyle>
				<scale>1.1</scale>
				<Icon>
					<href>https://maps.google.com/mapfiles/kml/paddle/pink-blank.png</href>
				</Icon>
				<hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
			</IconStyle>
			<LabelStyle>
				<scale>0</scale>
			</LabelStyle>
			<ListStyle>
				<ItemIcon>
					<href>https://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
				</ItemIcon>
			</ListStyle>
		</Style>
		<Style id="sn_man">
			<IconStyle>
				<scale>1.2</scale>
				<Icon>
					<href>https://maps.google.com/mapfiles/kml/shapes/man.png</href>
				</Icon>
			</IconStyle>
			<LabelStyle>
				<scale>0</scale>
			</LabelStyle>
		</Style>
		<StyleMap id="msn_man">
			<Pair>
				<key>normal</key>
				<styleUrl>#sn_man</styleUrl>
			</Pair>
			<Pair>
				<key>highlight</key>
				<styleUrl>#sh_man</styleUrl>
			</Pair>
		</StyleMap>
		<StyleMap id="msn_arrow">
			<Pair>
				<key>normal</key>
				<styleUrl>#sn_arrow</styleUrl>
			</Pair>
			<Pair>
				<key>highlight</key>
				<styleUrl>#sh_arrow</styleUrl>
			</Pair>
		</StyleMap>
		<Style id="sn_arrow">
			<IconStyle>
				<scale>1.2</scale>
				<Icon>
					<href>https://maps.google.com/mapfiles/kml/shapes/arrow.png</href>
				</Icon>
				<hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
			</IconStyle>
			<LabelStyle>
				<scale>0</scale>
			</LabelStyle>
			<ListStyle>
			</ListStyle>
		</Style>
	""" % (numlines,len(uniq_dates),len(uniq_models))

	# KML FILE CREATION
	w = open(file_GoogleEarth + kml_type + ".kml",'w')
	w.write(kml_start)

	# GPSAltitudeRef
	# 0 = Above Sea Level
	# 1 = Below Sea Level
	# https://exiftool.org/faq.html#Q6

	#PLACEMARK PREPARATION
	counter_wp_date = 0
	for yyyy in uniq_yyyy:
		w.write("\t<Folder>\n")
		w.write("\t\t\t<name>%s</name>\n" % yyyy) #Waypoints grouped by year (yyyy)
		for yyyy_mm in uniq_yyyy_mm:
			if yyyy_mm[:4] == yyyy:
				w.write("\t\t\t<Folder>\n")
				w.write("\t\t\t\t<name>%s</name>\n" % yyyy_mm) #Waypoints grouped by year-month (yyyy:mm)
				for date in uniq_dates:
					if date[:7] == yyyy_mm:
						w.write("\t\t\t\t<Folder>\n")
						w.write("\t\t\t\t\t<name>%s</name>\n" % date) #Waypoints grouped by year-month-day (yyyy:mm:dd)
						counter_wp_date    += 1   #counter_wp_date increases every time date in uniq_dates changes
						counter_1stwp_date  = 0
						counter_row         = 0
						coordinates_longlat = ""
						coordinates_latlong = []
						bing_path           = ""
						w.write("\t\t\t\t\t<open>%d</open>\n" % counter_wp_date)
						
						for row in open(file_exif):
							counter_row += 1
							
							#fields in the csv file
							column   = row.split("\t")
							c_ts     = column[0]
							c_fn     = column[1]
							c_dir    = column[2]
							c_lat    = column[3]
							c_long   = column[4]
							c_alt    = column[5]
							c_make   = column[6]
							c_model  = column[7]
							c_orient = column[8]
							c_imgw   = column[9]
							c_imgh   = column[10]
							
							if date in row:
								counter_1stwp_date += 1
								
								if kml_type == "thumbs":
									#THUMBNAIL CREATION: create a thumbnail image for each geotagged file
									#https://en.proft.me/2016/01/3/how-thumbnail-python-and-pillow/
									#https://stackoverflow.com/questions/13872331/rotating-an-image-with-orientation-specified-in-exif-using-python-without-pil-in
									thumbs_styleid = c_fn[:c_fn.find(".")].lower() + "_" + str(counter_row) #styleid name for thumbnails
									SIZE = (100, 150)
									try:
										if c_fn.lower().endswith(".heic"):
											image_path = prefix_heic + "/" + c_fn[:c_fn.find(".")].lower() + "_heic_" + str(counter_row) + ".jpg" #SrcImgIfHEIC
										else:
											image_path = c_dir + "/" + c_fn #SrcImgIfNotHEIC
										im = Image.open(image_path)
										#EXIF TAG ORIENTATION VALUES: 1=0°,8=90°,3=180°,6=270°
										#https://www.daveperrett.com/articles/2012/07/28/exif-orientation-handling-is-a-ghetto/
										try:
											for orientation in ExifTags.TAGS.keys():
												if ExifTags.TAGS[orientation]=='Orientation':
													break
											exif = dict(im._getexif().items())
											if exif[orientation] == 8:
												im = im.rotate(90, expand=True)
											if exif[orientation] == 3:
												im = im.rotate(180, expand=True)
											if exif[orientation] == 6:
												im = im.rotate(270, expand=True)
										except:
											pass
										im.thumbnail(SIZE)
										thumb_path = "%s/%s.jpg" % (prefix_thumbs,thumbs_styleid)
										im.save(thumb_path, 'JPEG', quality=80)
									except:
										thumb_path = "https://maps.google.com/mapfiles/kml/paddle/pink-blank.png"
									
									#STYLE FOR THUMBNAILS USED AS PLACEMARK ICONS
									thumbs_style   = '''					<Style id="sh_%s">
							<IconStyle>
								<scale>1.3</scale>
								<Icon>
									<href>%s</href>
								</Icon>
							</IconStyle>
							<LabelStyle>
								<scale>1.1</scale>
							</LabelStyle>
							<BalloonStyle>
							</BalloonStyle>
							<ListStyle>
							</ListStyle>
						</Style>
						<Style id="sn_%s">
							<IconStyle>
								<scale>1.1</scale>
								<Icon>
									<href>%s</href>
								</Icon>
							</IconStyle>
							<LabelStyle>
								<scale>0</scale>
							</LabelStyle>
							<BalloonStyle>
							</BalloonStyle>
							<ListStyle>
							</ListStyle>
						</Style>
						<StyleMap id="msn_%s">
							<Pair>
								<key>normal</key>
								<styleUrl>#sn_%s</styleUrl>
							</Pair>
							<Pair>
								<key>highlight</key>
								<styleUrl>#sh_%s</styleUrl>
							</Pair>
						</StyleMap>
									''' % (thumbs_styleid,thumb_path,thumbs_styleid,thumb_path,thumbs_styleid,thumbs_styleid,thumbs_styleid)
									w.write(thumbs_style)
								
								w.write("\t\t\t\t\t<Placemark>\n")
								w.write("\t\t\t\t\t\t<name>%s | %s %s | %s</name>\n" % (c_ts, c_make, c_model, c_fn))
								
								#PLACEMARK POPUP
								pm_d_ThumbSize = 240 #preview image size
								if c_fn.lower().endswith(".heic"):
									#if .heic then point to the .jpg converted file
									img_src = prefix_heic + "/" + c_fn[:c_fn.find(".")].lower() + "_heic_" + str(counter_row) + ".jpg"
								else:
									img_src = "%s/%s" % (c_dir,c_fn)
								
								#description for images with no rotation
								pm_d_std = "\t\t\t\t\t\t<description><![CDATA[<table><tr><td><b>Timestamp</b><td> %s<tr><td><b>Google Maps</b><td> <a href='https://www.google.com/maps/place/%s,%s'>%s,%s</a><tr><td><b>Altitude </b><td> %s<tr><td><b>Device</b><br><br><td> %s %s<br><br><tr><td><b>Path</b><td> %s<tr><td><b>Filename</b><td> %s</table><table><tr><td>" % (c_ts, c_lat, c_long, c_lat, c_long, c_alt, c_make, c_model, c_dir, c_fn)
								
								#description for images with 90CW rotation
								pm_d_90cw = "\t\t\t\t\t\t<description><![CDATA[<table><td><table><tr><td><b>Timestamp</b><td>%s<tr><td><b>Google Maps</b><td> <a href='https://www.google.com/maps/place/%s,%s'>%s,%s</a> <tr><td><b>Altitude</b><td>%s<tr><td><b>Device</b><br><br><td>%s %s<br><br><tr><td><b>Path</b><td> %s<tr><td><b>Filename</b><td>%s</table><td><table><tr><td><img src='%s' style='-webkit-transform:rotate(90deg);position: relative;top:30;width:%d;'></td></tr></table></table>]]></description>\n" % (c_ts,c_lat,c_long,c_lat,c_long,c_alt,c_make,c_model,c_dir,c_fn,img_src,pm_d_ThumbSize)
								
								#description for images without 90CW rotation but with height greater than width
								pm_d_90 = "\t\t\t\t\t\t<description><![CDATA[<table><td><table><tr><td><b>Timestamp</b><td>%s<tr><td><b>Google Maps</b><td> <a href='https://www.google.com/maps/place/%s,%s'>%s,%s</a> <tr><td><b>Altitude</b><td>%s<tr><td><b>Device</b><br><br><td>%s %s<br><br><tr><td><b>Path</b><td> %s<tr><td><b>Filename</b><td>%s</table><td><table><tr><td><img src='%s' height='%d'></td></tr></table></table>]]></description>\n" % (c_ts,c_lat,c_long,c_lat,c_long,c_alt,c_make,c_model,c_dir,c_fn,img_src,pm_d_ThumbSize)

								#.mov files need application/x-mplayer2
								if c_fn.lower().endswith(".mov"):
									w.write(pm_d_std)
									w.write("<embed type='application/x-mplayer2' src='%s' name='MediaPlayer' height='%d' ShowControls='1' ShowStatusBar='1' ShowDisplay='1' autostart='0'></embed></td></tr></table>]]></description>\n" % (img_src,pm_d_ThumbSize))
								else:
									if "90 CW" in c_orient:
										w.write(pm_d_90cw)
									else:
										if c_imgh > c_imgw:
											w.write(pm_d_90)
										else:
											w.write(pm_d_std)
											w.write("<img src='%s' height='%d'></td></tr></table>]]></description>\n" % (img_src,pm_d_ThumbSize))
								if counter_1stwp_date == 1:    # this is the 1st waypoint of a new path. Set the icon "msn_man".
									w.write("\t\t\t\t\t\t<styleUrl>#msn_man</styleUrl>\n\t\t\t\t\t\t<Point><coordinates>%s,%s</coordinates></Point>" % (c_long,c_lat))
								else:
									if kml_type == "thumbs":
										w.write("\t\t\t\t\t\t\t<styleUrl>#msn_%s</styleUrl>\n\t\t\t\t\t\t\t<Point><coordinates>%s,%s</coordinates></Point>" % (thumbs_styleid,c_long,c_lat))
									else:
										w.write("\t\t\t\t\t\t<styleUrl>#msn_pink-blank</styleUrl>\n\t\t\t\t\t\t<Point><coordinates>%s,%s</coordinates></Point>" % (c_long,c_lat))
								w.write("\n\t\t\t\t\t</Placemark>\n")
								
								#MEASURE DISTANCE BETWEEN POINTS
								#Google Earth requires: longitude,latitude,altitude
								coordinates_longlat = coordinates_longlat + str(c_long) + "," + str(c_lat) + ",0\t" # ",0" means no altitude defined
								
								#geopy requires: latitude,longitude
								coordinates_latlong.append("(" + str(c_lat) + "," + str(c_long) + ")")
								
								#Bing (lat,long)
								#https://docs.microsoft.com/en-us/bingmaps/articles/create-a-custom-map-url
								bing_path = bing_path + "pos." + str(c_lat) + "_" + str(c_long) + "~"
								
								point_i   = 0
								distance1 = 0
								distance2 = 0
								for point in coordinates_latlong:
									point = point.replace("(","").replace(")","")
									point = tuple(point.split(","))
									point_i += 1
									if point_i < len(coordinates_latlong):
										point1 = point
										point2 = (coordinates_latlong[point_i]).replace("(","").replace(")","")
										point2 = tuple(point2.split(","))
										distance1 = distance1 + geodesic(point1,point2).meters #change from "meters" to "feet" if needed
										distance2 = distance2 + geodesic(point1,point2).km     #change from "km" to "miles" if needed
								distance1 = round(distance1,2)
								distance2 = round(distance2,2)
								if distance2 < 1:
									distance = str(distance1) + " m"  #change to "ft" if needed
								else:
									distance = str(distance2) + " km" #change to "mi" if needed
						
						#create path lines for dates containing more than one point
						if counter_1stwp_date > 1:
							try:
								line_color = line_colors.pop(0)
							except:
								if kml_type == "icons":
									rand_color = randomcolor.RandomColor()
									rand_color = rand_color.generate(luminosity="bright") #output example (RGB): "#6b1ac9" (without quotes)
									rgb_R = rand_color[0][1:3]
									rgb_G = rand_color[0][3:5]
									rgb_B = rand_color[0][5:]
									rgb_A = "ff" #Alpha channel (255 = full opaque)
									#https://en.wikipedia.org/wiki/RGBA_color_space
									line_color = rgb_A + rgb_B + rgb_G + rgb_R
									line_colors_random.append(line_color)
								else:
									line_color = line_colors_random.pop(0)
									
							#write path line
							#Bing url - &mode=W means mode of transportation = Walking
							w.write('''					<Placemark>
							<name>Path %s</name>
							<description><b>Distance traveled:</b><br>%s</br><![CDATA[<table><tr><td><br><b>Path:</b> view on <a href="javascript:window.open('about:blank');" onclick="window.open('https://bing.com/maps/default.aspx?rtp=%s&mode=W');">Bing</a><br><i>(Tested up to 80 waypoints)</i></table>]]></description>
							<Style>
								<LineStyle>
									<color>%s</color>
									<width>4.0</width>
								</LineStyle>
							</Style>
							<MultiGeometry> 
								<LineString>
								<tessellate>%d</tessellate>
								<coordinates>''' % (date,distance,bing_path,line_color,counter_wp_date))
							w.write(coordinates_longlat)
							w.write('''</coordinates>
								</LineString>
							</MultiGeometry> 
						</Placemark>''')
						w.write("\n\t\t\t\t</Folder>\n") #close yyyy:mm:dd
				w.write("\t\t\t</Folder>\n") #close yyyy:mm
		w.write("\t\t</Folder>\n") #close yyyy

	#KML FOOTER
	kml_end = "</Document>\n</kml>"
	w.write(kml_end)
	w.close()


#***************** BEGIN *****************
welcome() 

start_time = datetime.now()
ptime      = start_time.strftime('%Y%m%d_%H%M%S')

my_os            = platform.system() #Possible output: Windows: Windows, Linux: Linux, Mac: Darwin
file_temp        = ptime + '_temp.csv'
file_exif        = ptime + '_exif.csv'
file_GoogleEarth = ptime + '_'

prefix_thumbs = ptime + "_thumbs"
prefix_heic   = ptime + "_heic"

with open(file_temp, 'w') as w:
	w.write("DateTimeOriginal\tCreateDate\tCreationDate\tModifyDate\tFilename\tDirectory\tGpsLatitude\tGpsLongitude\tGpsAltitude\tMake\tModel\tOrientation\tImageWidth\tImageHeight\n") #header row
w.close()

# EXIFTOOL: explanation of the options used by the script
# (DateTimeOriginal is in LOCAL TIME)
#
# -q          (-quiet)             Quiet processing
# -ext EXT    (-extension)         Process files with specified extension
# -if EXPR                         Conditionally process files
# defined                          if condition is True
# ref tags:
#          exif:gpslongitude
#          exif:DateTimeOriginal
# -r                               Recursive search
# -gpslongitude# -gpslatitude#    Print coordinates in Decimal Degrees (by default, without #, output is Degrees Minutes Seconds)
#
# Metadata fields that will appear in the CSV output file:
# -datetimeoriginal %s
# -T          (-table)             Output in tabular format
#


#********************** SEARCH GEOTAGGED FILES (tag names are not case sensitive) **********************
exift_search = "exiftool -q -r *"
exift_if     = '-if "defined $gpslongitude"'
exift_tags   = "-datetimeoriginal -CreateDate -CreationDate -ModifyDate -filename -directory -gpslatitude# -gpslongitude# -gpsaltitude -make -model -orientation -imagewidth -imageheight"

exift_run = '%s %s -T %s >> %s' % (exift_search, exift_if, exift_tags, file_temp)
exift_run = os_check(exift_run)
os.system(exift_run)

#The number of lines in the file is the number of geotagged files found
with open(file_temp, 'r') as r:
    numlines = len(r.readlines())-1 #don't count the header row

r.close()

#Check timestamps
temp = []
if numlines > 0:
	os.mkdir(prefix_thumbs)
	csv_rows = csv.DictReader(open(file_temp), delimiter='\t')
	for csv_row in csv_rows:
		csv_tags = csv_row["Filename"] + "\t" + csv_row["Directory"] + "\t" + csv_row["GpsLatitude"] + "\t" + csv_row["GpsLongitude"] + "\t" + csv_row["GpsAltitude"] + "\t" + csv_row["Make"] + "\t" + csv_row["Model"] + "\t" + csv_row["Orientation"] + "\t" + csv_row["ImageWidth"] + "\t" + csv_row["ImageHeight"] + "\n"
		if csv_row["Filename"].lower().endswith(".mov"):
			csv_row = csv_row["CreationDate"] + csv_tags
		else: #for all the other files (NOT .mov)
			if len(csv_row["DateTimeOriginal"]) == 1: #if DateTimeOriginal is missing
				if len(csv_row["CreateDate"]) > 1: #check if CreateDate exists
					csv_row = csv_row["CreateDate"] + "\t" + csv_tags
				if len(csv_row["CreateDate"]) == 1: #if CreateDate is missing
					csv_row = csv_row["ModifyDate"] + "\t" + csv_tags
			if len(csv_row["DateTimeOriginal"]) > 1: #if DateTimeOriginal exists
				csv_row = csv_row["DateTimeOriginal"] + "\t" + csv_tags
		temp.append(csv_row)

	#Create a new CSV with rows sorted by Timestamp
	with open(file_exif, 'w') as w:
		w.write("Timestamp\tFilename\tDirectory\tGpsLatitude#\tGpsLongitude#\tGpsAltitude\tMake\tModel\tOrientation\tImageWidth\tImageHeight\n") #header row
		for row in sorted(temp):
			w.write(row)

	w.close()

	#convert heic to jpg
	counter_row = 0
	for row in open(file_exif):
		counter_row += 1
		column   = row.split("\t")
		c_ts     = column[0]
		c_fn     = column[1]
		c_dir    = column[2]
		c_lat    = column[3]
		c_long   = column[4]
		c_alt    = column[5]
		c_make   = column[6]
		c_model  = column[7]
		c_orient = column[8]
		c_imgw   = column[9]
		c_imgh   = column[10]
		if c_fn.lower().endswith(".heic"):
			try:
				os.mkdir(prefix_heic)
			except:
				pass
			#https://forensenellanebbia.blogspot.com/2018/09/converting-from-heic-to-jpg.html
			dstfile = c_fn[:c_fn.find(".")].lower() + "_heic_" + str(counter_row) + ".jpg"
			if my_os == "Linux":
				heif_linux = "heif-convert %s/%s %s/%s > /dev/null" % (c_dir,c_fn,prefix_heic,dstfile)
				os.system(heif_linux)
			else:
				heif_winosx = "magick %s/%s %s/%s" % (c_dir,c_fn,prefix_heic,dstfile)
				os.system(heif_winosx)
			#remove metadata from the destination .jpg file
			exift_clean = "exiftool -q -overwrite_original -all= -TagsFromFile %s/%s %s/%s" % (c_dir,c_fn,prefix_heic,dstfile)
			os.system(exift_clean)
			#import metadata from the source .heic file
			exift_add   = "exiftool -q -overwrite_original -TagsFromFile %s/%s -FileModifyDate -FileCreateDate %s/%s" % (c_dir,c_fn,prefix_heic,dstfile)
			os.system(exift_add)

	#find unique dates. This information will be used to name folders        
	csv_rows = csv.DictReader(open(file_exif), delimiter='\t')

	uniq_dates  = []
	uniq_models = []

	for csv_row in csv_rows:
		csv_TS = csv_row["Timestamp"] #Timestamp, in order of choice: DateTimeOriginal > CreateDate/CreationDate > ModifyDate
		csv_TS = csv_TS[:10] # Grab YYYY:MM:DD (first 10 characters)
		csv_MM = csv_row["Make"] + " " + csv_row["Model"] #MM = Make Model
		uniq_dates.append(csv_TS)
		uniq_models.append(csv_MM)
	
	uniq_dates_counter  = Counter(uniq_dates)
	uniq_dates          = sorted(set(uniq_dates))  #remove duplicates (set) and sort (sorted)
	uniq_models_counter = Counter(uniq_models)     #duplicate values are used to count the number of files per device model
	uniq_models         = sorted(set(uniq_models)) #remove duplicates (set) and sort (sorted)
	
	uniq_yyyy = []
	for uniq_date in uniq_dates:
		yyyy = uniq_date[:4] #grab YYYY
		uniq_yyyy.append(yyyy)
	uniq_yyyy = sorted(set(uniq_yyyy))

	uniq_yyyy_mm = []
	for uniq_date in uniq_dates:
		yyyy_mm = uniq_date[:7] #grab YYYY:MM
		uniq_yyyy_mm.append(yyyy_mm)
	uniq_yyyy_mm = sorted(set(uniq_yyyy_mm))

	kml_creation("icons")  #create .KML with standard icons
	kml_creation("thumbs") #create .KML with thumbnails

os.remove(file_temp) #remove temporary CSV file

#script duration time
end_time = datetime.now()
print ("\ngeotag2kml (v%s)" % version)
print ("\nScript started : " + str(start_time))
print ("Script finished: " + str(end_time))
print ('Duration       : {}'.format(end_time - start_time))
print ("-------------------------------------------\n")

#print summary
print ("Geotagged file(s) found: %d" % numlines)

if numlines > 0:
	print ("Unique date(s) found   : %d" % len(uniq_dates))
	counter_path = 0
	for uniq_date_counter, freq in uniq_dates_counter.most_common():
		if freq > 1:
			counter_path +=1
	print ("Path(s) created        : %d\n" % counter_path)
	print ("Geotagged file(s) found per device type:")
	for makemodel, freq in uniq_models_counter.most_common(): #most_common() returns a list ordered from the most common element to the least
		print ("  *   %s (%d)" % (makemodel,freq))
	print ("\nOutput files:")
	print ("  ==> %s" % file_exif)
	print ("  ==> %s" % file_GoogleEarth + "icons.kml")
	print ("  ==> %s" % file_GoogleEarth + "thumbs.kml")
