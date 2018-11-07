from lxml import etree
from pykml.factory import KML_ElementMaker as KML
import math

trk_file = "./tracks.txt"

track = open(trk_file, "r")
last_sid = ""
trk_time = ""
coord = ""
ltime = ""
fistLine = True
doc = KML.kml(KML.Document())


def add_line(trk_time, coord):
    global doc
    trk_line = KML.Placemark(
        KML.name(trk_time),
        KML.LineString(
            KML.extrude(True),
            KML.altitudeMode('clampToGround'),
            KML.coordinates(
                coord
            )
        )
    )
    doc.Document.append(trk_line)


def deg_conv(num):
    mnt, deg = math.modf(float(num))
    mnt = mnt*100/60
    return str(deg+mnt)


for line in track:
    line = line[:-1]
    pnt = line.split(" ")
    sid = pnt[0]
    time = pnt[1]
    lat = deg_conv(pnt[2])
    lon = deg_conv(pnt[3])
    if fistLine:
        last_sid = sid
        trk_time = time
        fistLine = False
    if last_sid == sid:
        coord += lon+","+lat+",0 "
        ltime = time
    else:
        trk_time += " - " + ltime
        add_line(trk_time, coord)
        last_sid = sid
        trk_time = time
        coord = ""
if coord != "":
    trk_time += " - " + ltime
    add_line(trk_time, coord)


xml = etree.tostring(doc, pretty_print=True)
print(xml.decode())

outfile = open(__file__.rstrip('.py')+'.kml', 'w')
outfile.write(xml.decode())
