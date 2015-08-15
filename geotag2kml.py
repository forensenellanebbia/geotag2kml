'''
geotag2kml

Public Release: 08/2015
Author        : Gabriele Zambelli
Blog          : http://forensenellanebbia.blogspot.it
Twitter       : @gazambelli

Python script to extract exif GPS data from photos and generate a Google Earth KML file.

Prerequisites:
  - python v2.7
  - exiftool (rename the executable into "exiftool.exe")
  - Google Earth
  
Use at your own risk

DateTimeOriginal is in LOCAL TIME

Placemark naming layout:
DateTimeOriginal ** Make Model ** Altitude (A=Above Sea Level, B=Below Sea Level), Filename

Useful information at:
http://u88.n24.queensu.ca/exiftool/forum/index.php/topic,1688.msg7373.html#msg7373
'''

from collections import Counter
import csv
import os
import random
import subprocess
import sys
import time

version = "0.1"

# color legend

c_red="ff0000ff"
c_yellow="ff00ffff"
c_violet="ffaa00ff"
c_green="ff00ff00" 
c_pink="fff8a5f8"
c_brownish="ff0055ff"
c_white="ffffffff"
c_darkblue="ffff0000"
c_mustard="ff00aaaa"
c_lightblue="ffffaa55"

colors=[c_red,c_yellow,c_violet,c_green,c_pink,c_brownish,c_white,c_darkblue,c_mustard,c_lightblue]

def welcome():
    os.system('cls')
    print "\n\n geotag2kml v%s\n\n" % version
    print " Enter the absolute path to the parent folder to parse\n (no quotes required - i.e. C:\TEMP\PICTURES)\n (the same path will be used to write the Google Earth KML file)\n\n"
    dir_pic = raw_input(r" ===> ")
    if os.path.exists(dir_pic) == True:
        try:
            subprocess.check_output('exiftool')
        except Exception, err:
            print "\n\n ERROR: missing executable exiftool.exe\n\n\n"
            sys.exit()
        else:
            os.chdir(dir_pic)
    else:
        print "\n ERROR: the path %s doesn't exist" % dir_pic
        time.sleep(2)
        welcome()
 
welcome() 
 
if os.path.exists('temp_exif.csv'):
    os.remove('temp_exif.csv')

if os.path.exists('exif.csv'):
    os.remove('exif.csv')

#run exiftool tool recursively seeking for specific extensions and skipping files without the fields gpslongitude and datetimeoriginal
#csv output tab delimited
    
os.system('exiftool * -ext jpg -ext jpeg -ext tif -ext tiff -if "defined $exif:gpslongitude" -if "defined $exif:DateTimeOriginal" -r -datetimeoriginal -filename -directory -gpslongitude# -gpslatitude# -gpsaltitude -make -model -T >> temp_exif.csv')

#the list gets sorted by DateTimeOriginal
with open('temp_exif.csv', 'r') as r:
    with open('exif.csv', 'w') as w:
        w.write("datetimeoriginal\tfilename\tdirectory\tgpslongitude\tgpslatitude\tgpsaltitude\tmake\tmodel\n")
        for line in sorted(r):
            w.write(line)

r.close()
os.remove('temp_exif.csv')
w.close()

with open('exif.csv', 'r') as r:
    numlines=len(r.readlines())-1

r.close()

#find unique dates. This information will be used to name folders        
reader = csv.DictReader(open("exif.csv"), delimiter='\t')

uniq_dates=[]
uniq_models=[]

for line in reader:
    a = line["datetimeoriginal"]
    a = a[:10]
    uniq_dates.append(a,)
    b = line["make"] + " " + line["model"]
    uniq_models.append(b)
    
uniq_dates  = sorted(set(uniq_dates))

uniq_models_counter = Counter(uniq_models)

uniq_models = sorted(set(uniq_models))

#kml_start contains the first block of data of the KML file

kml_start = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
    <name>Summary: %d waypoints, %d dates, %d devices</name>
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

#KML file creation

if os.path.exists('GoogleEarth.kml'):
    os.remove('GoogleEarth.kml')
    w = open('GoogleEarth.kml','w')
else:
    w = open('GoogleEarth.kml','w')

w.write(kml_start)

'''
COLUMN LAYOUT REMINDER
column[0] = DateTimeOriginal
column[1] = Filename
column[2] = Directory
column[3] = GPSLongitude
column[4] = GPSLatitude
column[5] = GPSAltitude
column[6] = Make
column[7] = Model

GPSAltitudeRef
0 = Above Sea Level
1 = Below Sea Level
http://www.sno.phy.queensu.ca/~phil/exiftool/faq.html
'''

# placemarks

def sea_level(refvalue):
    if refvalue.find('Above') != -1:
        return(refvalue[:refvalue.find('Above')-1] + " A")
    else:
        return(refvalue[:refvalue.find('Below')-1] + " B")

counter_wp_date = 0
for date in uniq_dates:
    w.write("<Folder>\n")
    w.write("\t<name>%s</name>\n" % date)
    counter_wp_date += 1   #counter_wp_date increases every time date in uniq_dates changes
    counter_1stwp_date =0
    w.write("\t<open>%d</open>\n" % counter_wp_date)
    for line in open("exif.csv"):
        column = line.split("\t")
        if date in line:
            counter_1stwp_date += 1
            w.write("        <Placemark>\n")
            w.write("\t\t\t<name>%s *** %s %s *** (%s) *** %s</name>\n" % (column[0], column[6], column[7].rstrip('\n'), sea_level(column[5]),column[1]))
            w.write("\t\t\t<description>\n\t\t\t<![CDATA[<table><tr><td>\n")
            w.write("\t\t\t<img src='%s/%s' width='384' height='288'>\n\t\t\t</td></tr></table>]]>\n\t\t\t</description>\n" % (column[2].lower(),column[1].lower()))
            if counter_1stwp_date == 1:    # value 1 means that it's the first waypoint of a new path (shown with the icon of a man)
                w.write("\t\t\t<styleUrl>#msn_man</styleUrl>\n\t\t\t<Point><coordinates>%s,%s</coordinates></Point>" % (column[3],column[4]))
            else:
                w.write("\t\t\t<styleUrl>#msn_pink-blank</styleUrl>\n\t\t\t<Point><coordinates>%s,%s</coordinates></Point>" % (column[3],column[4]))
            if counter_wp_date <=10:
                color=colors[counter_wp_date-1]
            else:
                color=random.choice(colors)
            w.write("\n        </Placemark>\n")
    w.write('''        <Placemark>
            <name>Path %s on-off</name>
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
                <coordinates>''' % (date,date,color,counter_wp_date))  #choose a random color for each path line
    for line in open("exif.csv"):
        column = line.split("\t")
        if date in line:
            w.write(str(column[3]) + "," + str(column[4]).rstrip('\n') + ",0\t")
    w.write('''
               </coordinates>
              </LineString>
            </MultiGeometry> 
        </Placemark>''')
    w.write("\n</Folder>\n")

#kml_end is the last part of the KML file

kml_end = """</Document>
</kml>
"""

w.write(kml_end)
w.close()

#print successful message

if len(uniq_models)==1:
    print "\n\n Geotagged photos (%d in total) were taken with:\n" % numlines
else:
    print "\n\n Geotagged photos (%d in total) were taken with %d different devices:\n" % (numlines, len(uniq_models))
for makemodel, freq in uniq_models_counter.most_common():
    print " -  %s (%d)" % (makemodel,freq)

print "\n\n Google Earth KML file was successfully created!!\n"

