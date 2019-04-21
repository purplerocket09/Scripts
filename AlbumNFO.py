#Creates Kodi Compatable NFO file for Music Albums.
import os
import sys
from tinytag import TinyTag
import datetime
import math

print('This Script is for Albums only NOT including Compolations')
print('If path is network location please use UNC path \\\servername\\\path')
path = input("Enter Location of Album: ")

directories = []
tracknames = []
trackpositions = []
trackdurations = []
filetypes = ('.mp3','.m4a','.flac','.ogg','.m4b')
template = 'album.nfo'
type = 'album'
compilation = 'false'

for name in os.listdir(path):
    if name.endswith(filetypes): 
        filename = os.path.join(path, name)
        tag = TinyTag.get(filename)
        title = tag.title
        track = tag.track
        duration = tag.duration
        tracknames.append(title)
        trackpositions.append(track)
        duration =  math.ceil(duration)
        duration = str(datetime.timedelta(seconds=duration))		
        trackdurations.append(duration)

album = tag.album
artist = tag.artist
genre = tag.genre
year = tag.year


createfile = os.path.join(path, 'album.nfo')
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
    file.write("    <musicBrainzAlbumID></musicBrainzAlbumID>\r")
    file.write("    <artistdesc>%s</artistdesc>\r" %artist)
    file.write("    <genre>%s</genre>\r" %genre)
    file.write("    <compilation>%s</compilation>\r" %compilation)
    file.write("    <review></review>\r")
    file.write("    <type>%s</type>\r" %type)
    file.write("    <label></label>\r")
    file.write("    <year>%s</year>\r" %year)	
    file.write("    <albumArtistCredits>\r")	
    file.write("        <artist>%s</artist>\r" %artist)	
    file.write("        <musicBrainzArtistID></musicBrainzArtistID>\r")	
    file.write("    </albumArtistCredits>\r")
    file.close()   
with open(createfile, 'a+') as file:
    for i in range(len(tracknames)):	
        file.write("    <track>\r")	
        file.write("        <musicBrainzTrackID></musicBrainzTrackID>\r")	
        file.write("        <title>%s</title>\r" %tracknames[i])	
        file.write("        <position>%s</position>\r" %trackpositions[i])	
        file.write("        <duration>%s</duration>\r" %trackdurations[i])
        file.write("    </track>\r")
    file.close()
with open(createfile, 'a+') as file:	
    file.write("    <releasetype>%s</releasetype>\r" %type)	
    file.write("</album> \r")	
    file.close()






