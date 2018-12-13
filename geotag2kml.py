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

You can view the GNU General Public License at <http://www.gnu.org/licenses/>
*******************************************************************************

geotag2kml - WARNING: This program is provided "as-is"

Author    : Gabriele Zambelli (Twitter: @gazambelli)
Blog post : http://forensenellanebbia.blogspot.it/2015/08/geotag2kml-python-script-to-create-kml.html

This script will create a Google Earth KML file from geotagged photos and videos

Prerequisites:
 - Python v2.7
 - ExifTool (https://www.sno.phy.queensu.ca/~phil/exiftool/)
   (Recommended version: 10.62+. If you're using Windows, please rename the executable of ExifTool to "exiftool.exe")

Version history
[v0.5] 2018-12-13
[v0.4] 2018-12-08
[v0.3] 2018-04-07
[v0.2] 2016-04-03
[v0.1] 2015-08

Script tested on:
 - Windows 10 (1803)      | ExifTool 11.12 | Python 2.7.13
 - Ubuntu 16.04           | ExifTool 10.10 | Python 2.7.12
 - macOS Sierra (10.12.6) | ExifTool 10.76 | Python 2.7.10
 - Google Earth Pro 7.3.2

References:
 EXIFTOOL
 - ExifTool GPS Tags                 : https://sno.phy.queensu.ca/~phil/exiftool/TagNames/GPS.html
 - ExifTool Application Documentation: https://sno.phy.queensu.ca/~phil/exiftool/exiftool_pod.html
 GOOGLE EARTH
 - Generating a Google Earth KML file: http://u88.n24.queensu.ca/exiftool/forum/index.php/topic,1688.msg7373.html#msg7373
 - KML Reference                     : https://developers.google.com/kml/documentation/kmlreference#kmlextensions
 - Altitude Modes                    : https://developers.google.com/kml/documentation/altitudemode
"""

from collections import Counter
from datetime import datetime
import binascii
import csv
import os
import platform
import random
import subprocess
import sys

version = "0.5"

# color legend
red       = "ff0000ff"
yellow    = "ff00ffff"
violet    = "ffaa00ff"
green     = "ff00ff00"
pink      = "fff8a5f8"
brownish  = "ff0055ff"
white     = "ffffffff"
darkblue  = "ffff0000"
mustard   = "ff00aaaa"
lightblue = "ffffaa55"

line_colors = [red, yellow, violet, green, pink, brownish, white, darkblue, mustard, lightblue]

def welcome():
    try:
        subprocess.check_output(["exiftool", "-ver"]) #check if exiftool exists
    except:
        print "\n\n ERROR: exiftool was not found\n\n\n"
        sys.exit()
    if len(sys.argv) == 1:
        print "\n geotag2kml (v%s)" % version
        exift_ver = os.popen("exiftool -ver").read()
        if float(exift_ver) < 10.62:
            print "\n !! It's recommended to use a more recent version of ExifTool !!\n"
        print "\n This script will create a Google Earth KML file from geotagged photos and videos"
        print "\n How to use:\n\n ==> python " + os.path.basename(sys.argv[0]) + " AbsolutePathToAnalyze"
        print "\n [The script will search recursively                 ]"
        print " [The output files will be saved under the given path]\n\n"
        sys.exit()
    elif len(sys.argv) == 2:
        if os.path.exists(sys.argv[1]) == True:
            os.chdir(sys.argv[1])
        else:
            print "\n ERROR: the path %s doesn't exist" % sys.argv[1]
            sys.exit()

def os_check(exift_cmd):
	if my_os != "Windows":
		exift_cmd = exift_cmd.replace('"',"'")
	return exift_cmd

def sea_level(refvalue):
	if refvalue.find('Above') != -1:
		return(refvalue[:refvalue.find('Above')-1] + " A")
	else:
		return(refvalue[:refvalue.find('Below')-1] + " B")

def kml_creation(kml_type):
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
					<href>http://maps.google.com/mapfiles/kml/paddle/pink-blank.png</href>
				</Icon>
				<hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
			</IconStyle>
			<LabelStyle>
				<scale>1.1</scale>
			</LabelStyle>
			<ListStyle>
				<ItemIcon>
					<href>http://maps.google.com/mapfiles/kml/paddle/pink-blank-lv.png</href>
				</ItemIcon>
			</ListStyle>
		</Style>
		<Style id="sh_arrow">
			<IconStyle>
				<scale>1.4</scale>
				<Icon>
					<href>http://maps.google.com/mapfiles/kml/shapes/arrow.png</href>
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
					<href>http://maps.google.com/mapfiles/kml/shapes/man.png</href>
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
					<href>http://maps.google.com/mapfiles/kml/paddle/pink-blank.png</href>
				</Icon>
				<hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
			</IconStyle>
			<LabelStyle>
				<scale>0</scale>
			</LabelStyle>
			<ListStyle>
				<ItemIcon>
					<href>http://maps.google.com/mapfiles/kml/paddle/pink-blank-lv.png</href>
				</ItemIcon>
			</ListStyle>
		</Style>
		<Style id="sn_man">
			<IconStyle>
				<scale>1.2</scale>
				<Icon>
					<href>http://maps.google.com/mapfiles/kml/shapes/man.png</href>
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
					<href>http://maps.google.com/mapfiles/kml/shapes/arrow.png</href>
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

	# COLUMN LAYOUT REMINDER
	# column[0] = DateTimeOriginal/(or CreationDate if DateTimeOriginal is missing)
	# column[1] = Filename
	# column[2] = Directory (relative path)
	# column[3] = GPSLongitude
	# column[4] = GPSLatitude
	# column[5] = GPSAltitude
	# column[6] = Make
	# column[7] = Model
	# 
	# GPSAltitudeRef
	# 0 = Above Sea Level
	# 1 = Below Sea Level
	# http://www.sno.phy.queensu.ca/~phil/exiftool/faq.html

	# write placemarks
	counter_wp_date = 0
	counter_row = 0
	for yyyy in uniq_yyyy:
		w.write("\t<Folder>\n")
		w.write("\t\t\t<name>%s</name>\n" % yyyy) #Waypoints grouped by year (yyyy)
		for yyyy_mm in uniq_yyyy_mm:
			if yyyy_mm[:4] == yyyy:
				w.write("\t\t\t<Folder>\n")
				w.write("\t\t\t\t<name>%s</name>\n" % yyyy_mm) #Waypoints grouped by year-month (yyyy_mm)
				for date in uniq_dates:
					if date[:7] == yyyy_mm:
						w.write("\t\t\t\t<Folder>\n")
						w.write("\t\t\t\t\t<name>%s</name>\n" % date) #Waypoints grouped by date
						counter_wp_date    += 1   #counter_wp_date increases every time date in uniq_dates changes
						counter_1stwp_date  = 0
						w.write("\t\t\t\t\t<open>%d</open>\n" % counter_wp_date)
						for row in open(file_exif):
							counter_row += 1
							column  = row.split("\t")
							c_dto   = column[0]
							c_fn    = column[1]
							c_dir   = column[2]
							c_long  = column[3]
							c_lat   = column[4]
							c_alt   = column[5]
							c_make  = column[6]
							c_model = column[7]
							if date in row:
								counter_1stwp_date += 1
								
								thumbs_styleid = c_fn[:c_fn.find(".")].lower() + "_" + str(counter_row)
								thumbs_style   = '''					<Style id="sh_%s">
						<IconStyle>
							<scale>1.3</scale>
							<Icon>
								<href>%s/%s</href>
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
								<href>%s/%s</href>
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
								''' % (thumbs_styleid,c_dir.lower(),c_fn.lower(),thumbs_styleid,c_dir.lower(),c_fn.lower(),thumbs_styleid,thumbs_styleid,thumbs_styleid)
								
								if kml_type == "thumbs":
									w.write(thumbs_style)
								
								w.write("\t\t\t\t\t<Placemark>\n")
								w.write("\t\t\t\t\t\t<name>%s | %s %s | (%s) | %s</name>\n" % (c_dto, c_make, c_model.rstrip('\n'), sea_level(c_alt),c_fn))
								w.write("\t\t\t\t\t\t<description><![CDATA[<table><tr><td>")
								if c_fn.lower().endswith(".mov"):
									w.write("<embed type='application/x-mplayer2' src='%s/%s' name='MediaPlayer' height='250' ShowControls='1' ShowStatusBar='1' ShowDisplay='1' autostart='0'></embed></td></tr></table>]]></description>\n" % (c_dir.lower(),c_fn.lower()))
								else:
									w.write("<img src='%s/%s' height='250'></td></tr></table>]]></description>\n" % (c_dir.lower(),c_fn.lower()))
								if counter_1stwp_date == 1:    # this is the 1st waypoint of a new path. Set the icon "msn_man".
									w.write("\t\t\t\t\t\t<styleUrl>#msn_man</styleUrl>\n\t\t\t\t\t\t<Point><coordinates>%s,%s</coordinates></Point>" % (c_long,c_lat))
								else:
									if kml_type == "thumbs":
										w.write("\t\t\t\t\t\t\t<styleUrl>#msn_%s</styleUrl>\n\t\t\t\t\t\t\t<Point><coordinates>%s,%s</coordinates></Point>" % (thumbs_styleid,c_long,c_lat))
									else:
										w.write("\t\t\t\t\t\t<styleUrl>#msn_pink-blank</styleUrl>\n\t\t\t\t\t\t<Point><coordinates>%s,%s</coordinates></Point>" % (c_long,c_lat))
								if counter_wp_date <= 10:
									line_color = line_colors[counter_wp_date-1]   #for each path line choose a color among the predefined colors
								else:
									line_color = "ff" + binascii.b2a_hex(os.urandom(3)) #for each path line choose a random color different from the predefined colors
								w.write("\n\t\t\t\t\t</Placemark>\n")
						w.write('''					<Placemark>
						<name>Path %s: toggle to show/hide</name>
						<description>Path %s</description>
						<Style>
							<LineStyle>
								<color>%s</color>
								<width>4.0</width>
							</LineStyle>
						</Style>
						<MultiGeometry> 
							<LineString>
							<tessellate>%d</tessellate>
							<coordinates>''' % (date,date,line_color,counter_wp_date))
						for row in open(file_exif):
							column = row.split("\t")
							c_dto   = column[0]
							c_fn    = column[1]
							c_dir   = column[2]
							c_long  = column[3]
							c_lat   = column[4]
							c_alt   = column[5]
							c_make  = column[6]
							c_model = column[7]
							if date in row:
								w.write(str(c_long) + "," + str(c_lat).rstrip('\n') + ",0\t") # ",0" means no altitude defined
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


welcome() 

start_time = datetime.now()
ptime      = start_time.strftime('%Y%m%d_%H%M%S')

my_os            = platform.system()
file_temp        = ptime + '_temp.csv'
file_exif        = ptime + '_exif.csv'
file_GoogleEarth = ptime + '_'

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
# Exiftool will seek recursively for files with specific extensions and metadata fields


#********************** SEARCH GEOTAGGED PICTURES **********************

exift_base   = "exiftool -q -r *"
exift_ext    = "-ext jpg -ext jpeg -ext tif -ext tiff"
exift_fields = "-filename -directory -gpslongitude# -gpslatitude# -gpsaltitude -make -model"

#CASE 1 - FIND pictures with DateTimeOriginal
exift_cmd = '%s %s -if "defined $exif:gpslongitude" -if "defined $exif:DateTimeOriginal" -T -datetimeoriginal %s >> %s' % (exift_base, exift_ext, exift_fields, file_temp)
exift_cmd = os_check(exift_cmd)
os.system(exift_cmd)

#CASE 2 - FIND pictures without DateTimeOriginal that have both CreateDate+ModifyDate. Get CreateDate.
exift_cmd = '%s %s -if "defined $gpslongitude" -if "not defined $DateTimeOriginal" -if "defined $Make" -if "defined $Model" -if "defined $CreateDate" -if "defined $ModifyDate" -T -CreateDate %s >> %s' % (exift_base, exift_ext, exift_fields, file_temp)
exift_cmd = os_check(exift_cmd)
os.system(exift_cmd)

#CASE 3 - FIND pictures without DateTimeOriginal/CreateDate but with ModifyDate
exift_cmd = '%s %s -if "defined $gpslongitude" -if "not defined $DateTimeOriginal" -if "defined $Make" -if "defined $Model" -if "not defined $CreateDate" -if "defined $ModifyDate" -T -ModifyDate %s >> %s' % (exift_base, exift_ext, exift_fields, file_temp)
exift_cmd = os_check(exift_cmd)
os.system(exift_cmd)

#********************** SEARCH GEOTAGGED VIDEOS (tested against iPhone videos) **********************
exift_ext = '-ext mov'
exift_cmd = '%s %s -if "defined $gpslongitude" -if "defined $CreationDate" -T -CreationDate %s >> %s' % (exift_base, exift_ext, exift_fields, file_temp)
exift_cmd = os_check(exift_cmd)
os.system(exift_cmd)

#********************** SEARCH GEOTAGGED HEIC **********************
exift_ext = '-ext heic'
exift_cmd = '%s %s -if "defined $gpslongitude" -Filename' % (exift_base, exift_ext)
exift_cmd = os_check(exift_cmd)
counter_heic = os.popen(exift_cmd).read()
counter_heic = (counter_heic.count("File Name"))
#***********************************************************


#Count line: the number of lines in the file is the number of geotagged files found
with open(file_temp, 'r') as r:
    numlines = len(r.readlines())

r.close()

#Create a new CSV file sorted by DateTimeOriginal
if numlines > 0:
	with open(file_temp, 'r') as r:
		with open(file_exif, 'w') as w:
			w.write("DateTimeOriginal\tFilename\tDirectory\tGpsLongitude\tGpsLatitude\tGpsAltitude\tMake\tModel\n") #header row
			for row in sorted(r):
				w.write(row)

	r.close()
	w.close()

	#find unique dates. This information will be used to name folders        
	csv_rows = csv.DictReader(open(file_exif), delimiter='\t')

	uniq_dates  = []
	uniq_models = []

	for csv_row in csv_rows:
		csv_DTO = csv_row["DateTimeOriginal"] #DTO = DateTimeOriginal
		csv_DTO = csv_DTO[:10] # Grab YYYY:MM:DD (first 10 characters)
		csv_MM  = csv_row["Make"] + " " + csv_row["Model"] #MM = Make Model
		uniq_dates.append(csv_DTO)
		uniq_models.append(csv_MM)
		
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
print "\ngeotag2kml (v%s)" % version
print "\nScript started : " + str(start_time)
print "Script finished: " + str(end_time)
print('Duration       : {}'.format(end_time - start_time))
print "-------------------------------------------\n"

#print summary
print "Geotagged file(s) found: %d" % numlines

if numlines > 0:
	print "Unique date(s) found   : %d\n" % len(uniq_dates)
	print "Geotagged file(s) found per device type:"
	for makemodel, freq in uniq_models_counter.most_common(): #most_common() returns a list ordered from the most common element to the least
		print "  *   %s (%d)" % (makemodel,freq)
	print "\nOutput files:"
	print "  ==> %s" % file_exif
	print "  ==> %s" % file_GoogleEarth + "icons.kml"
	print "  ==> %s" % file_GoogleEarth + "thumbs.kml"
	
if counter_heic > 0:
	print "-------------------------------------------"
	print "WARNING: Detected %d HEIC file(s) containing GPS data" % counter_heic
	print "This file type is not supported yet."
	print "Convert the HEIC file(s) to JPEG and re-run the script.\n"