#Creates Kodi Compatable NFO file for Music Albums.
import os
import sys
import datetime
import math
import time
import re
import mutagen
from tinytag import TinyTag
from mutagen.mp3 import MP3
from mutagen.mp3 import EasyMP3 as EMP3
from mutagen.flac import FLAC

print('This Script is for Albums only NOT including Compolations')
print('If path is network location please use UNC path \\\servername\\\path')
path = input("Enter Location of Albums: ")

directories = []
tracknames = []
trackpositions = []
trackdurations = []
mbztrackid = []

filetypes = ('.mp3','.m4a','.flac','.ogg')
template = 'album.nfo'
compilation = 'false'
image = 'none'

for dir in os.listdir(path):
    if os.path.isdir(os.path.join(path,dir)):
        directories.append(dir)

for i in range(len(directories)):
    paths = os.path.join(path,directories[i])
    for name in os.listdir(paths):
        if name.endswith(filetypes): 
            filename = os.path.join(paths, name)	
            if filename.endswith('.mp3'):
                Easy3       = EMP3(filename)
                tag         = TinyTag.get(filename)
                mbztrackids = Easy3["musicbrainz_trackid"][0]				
                title       = Easy3["title"][0]
                tpos        = tag.track
                duration    = tag.duration
                duration    = math.ceil(duration)
                duration    = time.strftime("%M:%S", time.gmtime(duration))
                mbztrackid.append(mbztrackids)
                tracknames.append(title)
                trackpositions.append(tpos)
                trackdurations.append(duration)				
            elif filename.endswith('.flac'):
                flac = FLAC(filename)
                mbztrackids = flac.get("musicbrainz_trackid")[0]				
                title       = flac.get("title")[0]
                tpos        = flac.get("tracknumber")[0]
                duration    = flac.info.length
                duration    = math.ceil(duration)
                duration    = time.strftime("%M:%S", time.gmtime(duration))
                mbztrackid.append(mbztrackids)				
                tracknames.append(title)
                trackpositions.append(tpos)		
                trackdurations.append(duration)

    
    if filename.endswith('.mp3'):
        amp3    = MP3(filename)
        easyMP3 = EMP3(filename)		
        comment      = amp3.get("COMM::eng")
        label        = amp3.get("TPUB")
        mood         = amp3.get("TMOO")
        mbzartistid  = easyMP3["musicbrainz_artistid"][0]
        mbzalbumid   = easyMP3["musicbrainz_albumid"][0]
        releasetype  = easyMP3["musicbrainz_albumtype"][0]
    elif filename.endswith('.flac'):
        aflac    = FLAC(filename)		
        comment      = aflac.get("comment")[0]
        label        = aflac.get("label")[0]
        mood         = aflac.get('mood')
        mbzartistid  = aflac.get("musicbrainz_artistid")[0]
        mbzalbumid   = aflac.get("musicbrainz_albumid")[0]
        releasetype  = aflac.get("releasetype")[0]		

    tag     = TinyTag.get(filename)	
    album   = tag.album
    artist  = tag.artist
    genre   = tag.genre
    year    = tag.year	

    createfile = os.path.join(paths, 'album.nfo')
    exists = os.path.isfile(createfile)
    if exists:
        print("Album.nfo file exists:")
        print(createfile)
        delete = input("Would You like to replace it? y/n: ")
        if delete == 'y' or delete == 'yes':		
            os.remove(createfile)
            import shutil
            shutil.copy(template, paths)
        elif delete == 'n' or delete == 'no':
            print("Album.nfo file exists exiting script")
            sys.exit()
        else:
            print("Input Error, Script Exiting")
            sys.exit()			
    else:
        import shutil
        shutil.copy(template, paths)
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
        file.write("    <thumb>%s</thumb>\r" %image)
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
        tracknames.clear()		
        mbztrackid.clear()		
        trackpositions.clear()		
        trackdurations.clear()		
    with open(createfile, 'a+') as file:	
        file.write("    <releasetype>%s</releasetype>\r" %releasetype)	
        file.write("</album> \r")	
        file.close()






