import os
import math
import sys
import mutagen
from mutagen.flac import FLAC
import datetime


print('This Script is for Albums only NOT including Compolations')
print('It is also only for Albums in flac format')
print('If path is network location please use UNC path \\\servername\\\path')
path = input("Enter Location of Album: ")

tracknames = []
trackpositions = []
trackdurations = []
mbztrackid = []
compilation = 'false'
template = 'album.nfo'


for name in os.listdir(path):
    if name.lower().endswith(".flac"):
        filename    = os.path.join(path, name)
        audio       = FLAC(filename)
        title       = audio.get("title")[0]
        tracknumber = audio.get("tracknumber")[0]
        mbztrackids = audio.get("musicbrainz_trackid")[0]
        duration    = audio.info.length
        duration    =  math.ceil(duration)
        duration    = str(datetime.timedelta(seconds=duration))		
        tracknames.append(title)
        mbztrackid.append(mbztrackids)
        trackpositions.append(tracknumber)		
        trackdurations.append(duration)

comment      = audio.get("comment")[0]
album        = audio.get("album")[0]
artist       = audio.get("artist")[0]
genre        = audio.get("genre")[0]
year         = audio.get("originalyear")[0]
label        = audio.get("label")[0]
mbzartistid  = audio.get("musicbrainz_artistid")[0]
mbzalbumid   = audio.get("musicbrainz_albumid")[0]
releasetype1 = audio.get("release type")[0]
releasetype  = audio.get("releasetype")[0]
originaldate = audio.get("originaldate")[0]

createfile = os.path.join(path, template)
exists = os.path.isfile(createfile)
if exists:
    print("Album.nfo file exists")
    sys.exit()
else:
    import shutil
    shutil.copy(template, path)

with open(createfile, 'a+') as file:
    file.seek(0, 2)
    file.write("<album> \r")    
    file.write("    <title>%s</title>\r" % album)
    file.write("    <musicBrainzAlbumID>%s</musicBrainzAlbumID>\r" %mbzalbumid)
    file.write("    <artistdesc>%s</artistdesc>\r" %artist)
    file.write("    <genre>%s</genre>\r" %genre)
    file.write("    <compilation>%s</compilation>\r" %compilation)
    file.write("    <review>%s</review>\r" %comment)
    file.write("    <type>%s</type>\r" %releasetype)
    file.write("    <label>%s</label>\r" %label)
    file.write("    <year>%s</year>\r" %year)	
    file.write("    <albumArtistCredits>\r")	
    file.write("        <artist>%s</artist>\r" %artist)	
    file.write("        <musicBrainzArtistID>%s</musicBrainzArtistID>\r" %mbzartistid)	
    file.write("    </albumArtistCredits>\r")
    file.close()   
with open(createfile, 'a+') as file:
    for i in range(len(tracknames)):	
        file.write("    <track>\r")	
        file.write("        <musicBrainzTrackID>%s</musicBrainzTrackID>\r" %mbztrackid[i])	
        file.write("        <title>%s</title>\r" %tracknames[i])	
        file.write("        <position>%s</position>\r" %trackpositions[i])	
        file.write("        <duration>%s</duration>\r" %trackdurations[i])
        file.write("    </track>\r")
    file.close()
with open(createfile, 'a+') as file:	
    file.write("    <releasetype>%s</releasetype>\r" %releasetype)	
    file.write("</album> \r")	
    file.close()
