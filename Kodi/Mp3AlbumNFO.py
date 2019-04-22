import os
import math
import sys
import datetime
import mutagen
from mutagen.mp3 import MP3
from mutagen.mp3 import EasyMP3 as EMP3
from tinytag import TinyTag


print('This Script is for Albums only NOT including Compolations')
print('It is also only for Albums in mp3 format')
print('If path is network location please use UNC path \\\servername\\\path')
path = input("Enter Location of Album: ")


tracknames = []
trackpositions = []
trackdurations = []
mbztrackid = []
compilation = 'false'
template = 'album.nfo'


for name in os.listdir(path):
    if name.lower().endswith(".mp3"):
        filename    = os.path.join(path, name)
        audio       = MP3(filename)
        audio2      = EMP3(filename)
        tag         = TinyTag.get(filename)		
        title       = audio2["title"][0]
        tracknumber = tag.track
        mbztrackids = audio2["musicbrainz_trackid"][0]
        duration    = tag.duration
        duration    = math.ceil(duration)
        duration    = str(datetime.timedelta(seconds=duration))		
        tracknames.append(title)
        mbztrackid.append(mbztrackids)
        trackpositions.append(tracknumber)		
        trackdurations.append(duration)

comment      = audio.get("COMM::eng")
album        = audio2["album"][0]
artist       = audio2["albumartist"][0]
genre        = audio2["genre"][0]
year         = audio2["date"][0]
label        = audio.get("TPUB")
mood         = audio.get("TMOO")
mbzartistid  = audio2["musicbrainz_artistid"][0]
mbzalbumid   = audio2["musicbrainz_albumid"][0]
releasetype  = audio2["musicbrainz_albumtype"][0]

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
    file.write("    <mood>%s</mood>\r" %mood)
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
