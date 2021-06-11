#!/bin/python3

import sys
import csv
from datetime import datetime, time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import gmplot
import math


def degMin2deg(x):
    x = float(x)
    return (int(x/100)) + ((x%100)/60)


def radians(degrees):
    return degrees*math.pi/180


def latlon2m(lat1, long1, lat2, long2):
    r = 6371000 # this is the radius of the earth   
    dLat = radians(lat2) - radians(lat1) # change in latitude in radians
    dLong = radians(long2) - radians(long1) # change in longitude in radians
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(radians(lat1))*math.cos(radians(lat2))*math.sin(dLong/2)*math.sin(dLong/2)
    d = 2*r*math.asin(math.sqrt(a)) # distance in meters
    return d


def plotPath(coordiantes, origin=None): # coordinates stored as timestamp | Lat | Long
    x = []
    y = []
    refX = []
    refY = []

    for coordinate in coordiantes:
        y.append(coordinate[1])
        x.append(coordinate[2])
    
    fig, ax = plt.subplots(figsize=(18 ,15))
    ax.plot(x, y, color='blue')
    if origin:
        if not dynamic:
            for coordinate in origin:
                refY.append(coordinate[1])
                refX.append(coordinate[2])
            ax.scatter(refX, refY, color='red')

    plot_title = title + " Latitude & Longitude Position"
    ax.set(xlabel = 'Longitude (Degrees)', ylabel = 'Latitude (Degrees)', title = plot_title)
    fig.savefig(("../Images/" + datetitle + " Lat long position.png"), bbox_inches='tight')
    plt.tight_layout()
    plt.show()


def plotDistance(coordiantes, reference=None): # coordinates stored as timestamp | Lat | Long
    poleCircumference = 40007.863 # circumference of earth along polar plane in kms
    equaCircumference = 40075.017 # circimference of earth along equatorial plane in kms
    lats = [] # distance from origin lat measurement in m
    longs = [] # distance from origin long measurement in m
    refLats = []
    refLongs = []

    if reference: # if the refernce file has been provided use that for reference
        origin = [reference[0][1], reference[0][2]]
        if dynamic:
            for coords in reference:
                dLat = (coords[1] - origin[0]) * ((poleCircumference/2)/180) * 1000
                dlong = (coords[2] - origin[1]) * ((equaCircumference/4)/90) * 1000
                refLats.append(dLat)
                refLongs.append(dlong)       
    else:
        origin = (coordinates[0][1], coordiantes[0][2])

    for coordinate in coordiantes:
        dLat = (coordinate[1] - origin[0]) * ((poleCircumference/2)/180) * 1000
        dlong = (coordinate[2] - origin[1]) * ((equaCircumference/4)/90) * 1000
        lats.append(dLat)
        longs.append(dlong)
    
    fig, ax = plt.subplots(figsize=(18 ,15))
    ax.plot(longs, lats, color='blue', label="Calculated")
    if dynamic:
        ax.plot(refLongs, refLats, color='red', alpha=0.4, label="Desired")
    else:
        ax.scatter(0, 0, color='red', label="Desired")
    plot_title = title + " Position from origin"
    ax.set(xlabel = "Distance (meters)", ylabel = "Distance (meters)", title = plot_title)
    ax.legend(title="GPS Position", loc='upper right', shadow=True)
    fig.savefig(("../Images/" + datetitle + " Position from origin.png"), bbox_inches='tight')
    plt.tight_layout()
    plt.show()


def plotError(coordinates, reference):
    error = []
    time = range(len(coordinates))
    origin = [reference[0][1], reference[0][2]]
    if dynamic:
        return
    
    for coord in coordinates:
        error.append(latlon2m(origin[0], origin[1], coord[1], coord[2]))
    fig, ax = plt.subplots(figsize=(18 ,15))
    ax.plot(time, error)
    plot_title = title + " Error over time"
    ax.set(xlabel = "time (ms)", ylabel = "Error (meters)", title = plot_title)
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    fig.savefig(("../Images/" + datetitle + " error over time.png"), bbox_inches='tight')
    plt.tight_layout()
    plt.show()

def plotMap(coordiantes, reference=None):
    lats = []
    longs = []
    apikey = # removed for publishing

    for coordinate in coordiantes:
        lats.append(coordinate[1])
        longs.append(coordinate[2])
    
    avgLats = (min(lats) + max(lats)) / 2
    avgLongs = (min(longs) + max(longs)) / 2

    print("Reference point for map: Lat: {}, Long: {}".format(avgLats, avgLongs))

    filename = title + "googleMap"

    gmap = gmplot.GoogleMapPlotter(avgLats, avgLongs, 18, apikey=apikey)
    gmap.plot(lats, longs, edge_width=4, color='blue')
    if reference:
        if dynamic:
            refLats = []
            refLongs = []
            for coords in reference:
                refLats.append(coords[1])
                refLongs.append(coords[2])
            gmap.plot(refLats, refLongs, color='red')
        else:
            refLats = [reference[0][1]]
            refLongs = [reference[0][2]]
            gmap.scatter(refLats, refLongs, symbol='+', marker=False, color='red', size=2)
    gmap.draw('../Images/{}.html'.format(filename))


def plotCNo(satellites):
    fig, ax = plt.subplots(figsize=(18 ,15))
    timestamps = list(satellites.keys())
    x = range(len(timestamps))
    SatIDs = satellites.values()
    tmp = []

    for sats in SatIDs:
        for sat in sats:
            if int(sat) not in tmp:
                tmp.append(int(sat))
    tmp.sort()

    ax.set_prop_cycle(plt.cycler("color", plt.cm.hsv(np.linspace(0,1,len(tmp)))))
    for count, sv in enumerate(tmp):
        y = []
        for sats in SatIDs:
            for sat in sats:
                if str(sv) in sats:
                    if sat == str(sv):
                        try:
                            y.append(float(sats[sat][0]))
                        except ValueError:
                            y.append(0)
                        break
                else:
                    y.append(0)
                    break
        ax.plot(x, y, label=sv)
    plot_title = title + " Carrier noise ratio of Satellites in view"
    ax.set(xlabel = 'Time (s)', ylabel = 'C/No (dB/Hz)', title = plot_title)
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    ax.legend(title="Satellite ID", loc='lower right', shadow=True, ncol=2)
    fig.savefig(("../Images/" + datetitle + " Carrier noise ratio.png"), bbox_inches='tight')
    plt.tight_layout()
    plt.show()

if len(sys.argv) > 2:
    sourceFile = sys.argv[2] # this is the file that was used to generate the binary file for the SDR
infile = sys.argv[1] # this is the file from the GPS receiver
timetofix = 0
dataValid = False
firstFix = False
svSNR = {}
satellites = {} # Make this a dict in a dict. {Timestamp: {SVid: SNR[]}}
currentTime = 0
startTime = datetime.now()
coordinates = [] # coordiantes stored as timestamp | Lat | Long
referenceCoords = [] # coordinates that act as reference
dynamic = False # is the file being graphed a static or dynamic spoof scenario
title = ""

if '.txt' in infile:
    datetitle = infile[:-4]
elif '.nmea' in infile:
    datetitle = infile[:-5]
else:
    raise NameError("Input file is not in correct format")

chunkedtitle = datetitle.split("_")

if 'dynamic' in infile:
    dynamic = True
    indexer = chunkedtitle.index("dynamic")
else:
    indexer = chunkedtitle.index("static")

title = chunkedtitle[indexer] + " " + chunkedtitle[indexer + 1]

try:
    with open(infile, "r") as nmeaFile:
        for count, line in enumerate(nmeaFile):
            tmp = line.split('*')
            string = tmp[0].split(',')
            msgType = string[0][3:]
            currentTime = datetime.now()
            timestamp2 = (currentTime - startTime).microseconds/1000000
            #
            # Parsing RMC sentences
            #
            if msgType == "RMC":
                if not dataValid:
                    if not firstFix:
                        timetofix += 1
                if string[2] == 'A':
                    dataValid = True
                    if not firstFix:
                        firstFix = True
                else:
                    dataValid = False
            #
            # Parsing GSV sentences
            #
            elif msgType == "GSV":
                NumofMessages = int(string[1])
                sequenceNumber = int(string[2])
                satellitesView = int(string[3])
                satellitesToCalc = satellitesView-(NumofMessages-1)*4 # this will dictate the number the index numbers of final sentence of group
                if sequenceNumber == 1:
                    timestamp = (currentTime - startTime).microseconds/1000000
                try:
                    if sequenceNumber < NumofMessages:                        
                        if string[4] not in svSNR:
                            svSNR[string[4]] = [string[7]]
                        else:
                            svSNR[string[4]].append(string[7])

                        if string[8] not in svSNR:
                            svSNR[string[8]] = [string[11]]
                        else:
                            svSNR[string[8]].append(string[11])
                    
                        if string[12] not in svSNR:
                            svSNR[string[12]] = [string[15]]
                        else:
                            svSNR[string[12]].append(string[15])
                    
                        if string[16] not in svSNR:
                            svSNR[string[16]] = [string[19]]
                        else:
                            svSNR[string[16]].append(string[19])
                    else:
                        if satellitesToCalc >= 1:
                            if string[4] not in svSNR:
                                svSNR[string[4]] = [string[7]]
                            else:
                                svSNR[string[4]].append(string[7])
                        if satellitesToCalc >= 2:
                            if string[8] not in svSNR:
                                svSNR[string[8]] = [string[11]]
                            else:
                                svSNR[string[8]].append(string[11])
                        if satellitesToCalc >=3:
                            if string[12] not in svSNR:
                                svSNR[string[12]] = [string[15]]
                            else:
                                svSNR[string[12]].append(string[15])
                        if satellitesToCalc == 4:
                            if string[16] not in svSNR:
                                svSNR[string[16]] = [string[19]]
                            else:
                                svSNR[string[16]].append(string[19])
                        if satellitesToCalc > 4:
                            raise OverflowError

                except IndexError:
                    pass
                except OverflowError:
                    print("Computational error occured. Access to a value higher than available attempted")
                if sequenceNumber == NumofMessages:
                    if svSNR:
                        satellites[timestamp] = svSNR
                    svSNR = {}

            #
            # Parsing GGA sentences
            #
            elif msgType == "GGA":
                if dataValid:
                    try:
                        latitude = degMin2deg(string[2])
                        longitude = degMin2deg(string[4])
                        if string[3] == 'S':
                            latitude = latitude * -1
                        if string[5] == 'W':
                            longitude = longitude * -1
                        coordinates.append([timestamp2, latitude, longitude])
                    except ValueError:
                        print("No valid coordinates")
                        continue

except IOError:
    print("could not open file. try again")
    sys.exit()

try:    
    with open(sourceFile, "r") as refFile:
        for count, line in enumerate(refFile):
            tmp = line.split('*')
            string = tmp[0].split(',')
            msgType = string[0][3:]
            currentTime = datetime.now()

            if msgType == "GGA":
                try:
                    latitude = degMin2deg(string[2])
                    longitude = degMin2deg(string[4])
                    if string[3] == 'S':
                        latitude = latitude * -1
                    if string[5] == 'W':
                        longitude = longitude * -1
                    referenceCoords.append([(currentTime - startTime).microseconds/1000, latitude, longitude])
                except ValueError:
                    print("No valid coordinates")
                    continue
except IOError:
    print("Reference File not provided")
    pass
    
print("Time to first fix was {} seconds".format(timetofix))
text_params = {'axes.labelsize': 24, 'axes.titlesize' : 30, 'xtick.labelsize': 20, 'ytick.labelsize': 20, 'legend.title_fontsize' : 20, 'legend.fontsize' : 16}
plt.rcParams.update(text_params) 
plotCNo(satellites)
plotPath(coordinates, referenceCoords)
plotDistance(coordinates, referenceCoords)
plotMap(coordinates, referenceCoords)
plotError(coordinates, referenceCoords)