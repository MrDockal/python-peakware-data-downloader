#!/usr/bin/env python

# UTF-8 encoding

# Python script getting, parsing and saving (in csv format) data from https://www.peakware.com.
#
# Author: Alexandre Louisnard alouisnard@gmail.com
# 2017

import sys, codecs
import urllib.request
import re

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
codecs.register_error("strict", codecs.ignore_errors)

listUrl = "https://www.peakware.com/peaks.php?choice=SoE"
outputFile = "peakware.csv"

print("GETTING: {}".format(listUrl))

listPage = urllib.request.urlopen(listUrl).read().decode('utf-8', 'ignore')

# (link, name, altitude)
matchLinks = re.findall(r"""\<li\>\<a\ href\=\"(peaks\.php\?pk\=[0-9]+)\"\>(.*)\<\/a\>\ \(.*\)\<br\/\>[0-9]+\ ft\/([0-9]+)\ m\<\/li\>""", listPage)

print("Found {} summits\n".format(len(matchLinks)))
sys.stdout.flush()

f = codecs.open(outputFile,"w",encoding='utf8')
f.write("name;elevation;latitude;longitude;continent;country;range\n")
f.close()

rec = 0;
err = 0;

for link in matchLinks:
	if link[0]:
		print("GETTING: {}\tAT: {}".format(link[1], link[0]))
		sys.stdout.flush()
		summitPage = urllib.request.urlopen("https://www.peakware.com/" + link[0]).read().decode('utf-8', 'ignore')
		matchName = re.findall(r"""\<h1\>(.+)\<\/h1\>""", summitPage)
		matchElevation = re.findall(r"""Elevation \(meters\):\<\/th\>[\S\s]\<td\>([0-9\,]+)\<\/td\>""", summitPage)
		matchElevation[0] = matchElevation[0].replace(",","")
		matchContinent = re.findall(r"""Continent:\<\/th\>[\S\s]\<td\>(.+)\<\/td\>""", summitPage)
		matchCountry = re.findall(r"""Country:\<\/th\>[\S\s]\<td\>(.+)\<\/td\>""", summitPage)
		matchRange = re.findall(r"""Range/Region:\<\/th\>[\S\s]\<td\>\<a href\=\"areas.php\?a\=[0-9]+\"\>(.+)\<\/a\>\<\/td\>""", summitPage)
		matchLatitude = re.findall(r"""Latitude:\<\/th\>[\S\s]\<td\>(\-?[0-9\.]+)\<\/td\>""", summitPage)
		matchLongitude = re.findall(r"""Longitude:\<\/th\>[\S\s]\<td\>(\-?[0-9\.]+)\<\/td\>""", summitPage)
		if matchName and matchElevation and matchLatitude and matchLongitude:
			result = matchName + matchElevation + matchLatitude + matchLongitude + (matchContinent or ['']) + (matchCountry or ['']) + (matchRange or [''])
			resultString = ';'.join(result)
			rec += 1
			print(str(rec) + "\t" + resultString + "\n")
			f = codecs.open(outputFile,"a",encoding='utf8')
			f.write(resultString + "\n")
			f.close()
		else:
			print("MISSING name, elevation, latitude or longitude")
			err += 1
	else:
		err +=1
	sys.stdout.flush()

print("\n\nRecords: {}\nErrors: {}\n".format(rec, err))

