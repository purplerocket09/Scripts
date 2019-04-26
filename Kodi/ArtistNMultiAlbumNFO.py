#Creates Kodi Compatable NFO file for Artist N Their Albums.
#Also Downloads Artwork for Artists N Albums.
#Gets Album description from theaudiodb and a fallback of Wikipedia
#Writes the description to the comment Tag.
#Still only supports mp3 N Flac to add others soon
import os
import sys
import datetime
import math
import time
import shutil
import wikipedia
import urllib.request
import json
import mutagen
from tinytag import TinyTag
from mutagen.mp3 import MP3
from mutagen.mp3 import EasyMP3 as EMP3
from mutagen.id3 import ID3, COMM
from mutagen.flac import FLAC
from colorama import init 
from termcolor import colored  
init()

#print('This Script is for Albums only NOT including Compolations')
#print('If path is network location please use UNC path \\\servername\\\path')
path = input("Enter Location of Artist Folders: ")
path2 = input("Enter Artist Name (Folder) to Scrap: ")

path = os.path.join(path, path2)

directories = []
tracknames = []
trackpositions = []
trackdurations = []
mbztrackid = []

filetypes = ('.mp3', '.flac')
artworktype = ('.jpg', '.png')
template = 'template.nfo'
compilation = 'false'
image = 'none'

#Artwork Area
source = "Artwork/"
cd = source + "cdart.png"
backcover = source + "back.jpg"
frontcover = source + "cover.jpg"
sidecover = source + "spine.jpg"

#---------------------------------------
#Albums Scrapper and Album.nfo Creation
#---------------------------------------

for dir in os.listdir(path):
    if os.path.isdir(os.path.join(path,dir)):
        directories.append(dir)
# Albums and Artwork		
for i in range(len(directories)):
    try:
        shutil.rmtree(source)    
    except:
        pass
    album = directories[i].replace(' ', '+') 
    query = path2 + ' ' + directories[i]
    paths = os.path.join(path,directories[i])
    print("Working On:", query)
    url = "http://www.theaudiodb.com/api/v1/json/1/searchalbum.php?&a={0}".format(album)
    response = urllib.request.urlopen(url)
    response = response.read().decode('utf-8')
    json_obj = json.loads(response)
    try:
        list = (json_obj['album'][0])
        comment = list['strDescriptionEN']			
    except:
        try:
            comment = wikipedia.summary(query, sentences=4)
            comment = comment + "Wikipedia"
        except wikipedia.exceptions.PageError:
            print(colored('NO', 'red') + ',Album Description. Please Check')
            comment = "Please Add Information"
    for name in os.listdir(paths):
        if name.endswith(filetypes): 
            filename = os.path.join(paths, name)			
            if filename.endswith('.mp3'):
                #Write Comment To MP3
                audio = ID3(filename)
                audio.add(COMM(encoding=3, text=comment))
                audio.save() 			
                Easy3       = EMP3(filename)
                tag         = TinyTag.get(filename)
                albumid     = Easy3["musicbrainz_releasegroupid"][0]				
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
                #Write Comment To Flac				
                flac["comment"] = comment
                flac.save() 
                albumid     = flac.get("musicbrainz_releasegroupid")[0]				
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
        #comment      = amp3.get("COMM::eng")
        label        = amp3.get("TPUB")
        mood         = amp3.get("TMOO")
        mbzartistid  = easyMP3["musicbrainz_artistid"][0]
        mbzalbumid   = easyMP3["musicbrainz_albumid"][0]
        releasetype  = easyMP3["musicbrainz_albumtype"][0]
    elif filename.endswith('.flac'):
        aflac    = FLAC(filename)		
        #comment      = aflac.get("comment")[0]
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
        os.remove(createfile)
        #print("Album.nfo file exists:")
        #print(createfile)
        #delete = input("Would You like to replace it? y/n: ")
        #if delete == 'y' or delete == 'yes':		
        #    os.remove(createfile)
        #    import shutil
        #    shutil.copy(template, paths)
        #elif delete == 'n' or delete == 'no':
        #    print("Album.nfo file exists exiting script")
        #    sys.exit()
        #else:
        #    print("Input Error, Script Exiting")
        #    sys.exit()			
    else:
        shutil.copy2(template, createfile)		
        #shutil.copy(template, paths)
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
    #Make Directory
    try:
        os.mkdir("Artwork")
    except:
        pass	
    #Get and move artwork
    try:	
        list = (json_obj['album'][0])
        cdart = list['strAlbumCDart']
        back = list['strAlbumThumbBack']
        cover = list['strAlbumThumb']
        spine = list['strAlbumSpine']
        urllib.request.urlretrieve(cdart, cd)
        urllib.request.urlretrieve(back, backcover)
        urllib.request.urlretrieve(cover, frontcover)
        urllib.request.urlretrieve(spine, sidecover)
        coverexists = os.path.isfile(frontcover)
        print("Cover", coverexists)
        cdexists = os.path.isfile(cd)
        print("cdart", cdexists)
        artworks = os.listdir(source)
        for f in artworks:
            shutil.copy(source+f, paths)
    except:	
        url = "http://webservice.fanart.tv/v3/music/albums/{0}?api_key=639191cb0774661597f28a47e7e2bad5".format(albumid)
        response = urllib.request.urlopen(url)
        response = response.read().decode('utf-8')
        list = json.loads(response)["albums"]
        list = list[albumid]
        if 'albumcover' in list:
            albumcover = list["albumcover"]
            for num in albumcover:
                list = num["url"]
                try:
                    urllib.request.urlretrieve(list, frontcover)
                except:
                    pass
            Cexists = os.path.isfile(frontcover)
            print("Cover", Cexists)
        else:
            fexists = os.path.isfile(frontcover)
            print("Cover", fexists)
        if 'cdart' in list:
            cdart = list["cdart"]
            for num in cdart:
                list = num["url"]
                try:
                    urllib.request.urlretrieve(list, cd)
                except:
                    pass
            exists1 = os.path.isfile(cd)
            print("cdart", exists1)
        else:
            exists2 = os.path.isfile(cd)
            if exists2:
                print('CDArt', exists2)
            else:
                print('CDArt' + ' ' + colored(exists2, 'red'))
        artworks = os.listdir(source)
        for f in artworks:
            shutil.copy(source+f, paths)
    print(' ')

#---------------------------------------
#Artist Scrapper and Artist.nfo Creation
#---------------------------------------
print("Moving ON-TO Artist")
print(" ")
atsdestpath = os.path.join(path, path2)
		
artist = path2.replace(' ', '+')

template = 'template.nfo'
#ArtistArt Area
Aistsource = "ArtistArt/"
logo = Aistsource + "logo.png"
folder = Aistsource + "folder.jpg"
fanart = Aistsource + "fanart.jpg"
fanart2 = Aistsource + "fanart2.jpg"
banner = Aistsource + "banner.jpg"

try:
    shutil.rmtree(Aistsource)    
except:
    pass

artisturl = "http://www.theaudiodb.com/api/v1/json/1/search.php?s={0}".format(artist)
response = urllib.request.urlopen(artisturl)
response = response.read().decode('utf-8')
artistinfo = json.loads(response)
try:
    list = (artistinfo['artists'][0])
except:
    print("No Artist Results")
    sys.exit()

sthumb      = list['strArtistThumb']
slogo       = list['strArtistLogo']
sfanart     = list['strArtistFanart']
sfanart2    = list['strArtistFanart2']
sbanner     = list['strArtistBanner']

name       = list['strArtist']
bio        = list['strBiographyEN']
if bio == "None":
    print("NO BIO")
    bio = 'Please update Bio'
bzArtistID = list['strMusicBrainzID']
genre      = list['strGenre']
style      = list['strStyle']
mood       = list['strMood']
active     = list['intFormedYear']
if active == "None":
    active = 'UnKnown'
activeend  = list['strDisbanded']
if activeend == "None":
    activeend = ''
born       = list['intBornYear']
if born == "None":
    born =''
bornplace  = list['strCountry']
died       = list['intDiedYear']

albumsurl = "http://www.theaudiodb.com/api/v1/json/1/discography.php?s={0}".format(artist)
response  = urllib.request.urlopen(albumsurl)
response  = response.read().decode('utf-8')

try:
    albslist = []
    albsyears = []
    list = json.loads(response)["album"]
    for i in list:
        album = i["strAlbum"]
        year = i["intYearReleased"]
        if year == "None":
            year = 'UnKnown'
        albslist.append(album)
        albsyears.append(year)	
except:
    print("No Results for Artist Albums")
    pass

createfile = os.path.join(atsdestpath, 'artist.nfo')
exists = os.path.isfile(createfile)
if exists:
    os.remove(createfile)
else:
    shutil.copy2(template, createfile)
with open(createfile, 'a+') as file:
    file.seek(0, 2)
    file.write("<artist> \r")    
    file.write("    <name>%s</name>\r" % name)
    file.write("    <musicBrainzArtistID>%s</musicBrainzArtistID>\r" %bzArtistID)
    file.write("    <genre>%s</genre>\r" %genre)
    file.write("    <style>%s</style>\r" %style)
    file.write("    <mood>%s</mood>\r" %mood)
    file.write("    <yearsactive>%s - %s</yearsactive>\r" %(active, activeend))
    file.write("    <born>%s  %s</born>\r" %(born, bornplace))
    file.write("    <formed>%s</formed>\r" %active)
    file.write("    <biography>%s</biography>\r" %bio)
    file.write("    <died>%s</died>\r" %died)
    file.write("    <disbanded>%s</disbanded>\r" %activeend)
    file.close()   
try:
    with open(createfile, 'a+') as file:
        for i in range(len(albslist)):	
            file.write("    <album>\r")
            file.write("        <title>%s</title>\r" %albslist[i])	
            file.write("        <year>%s</year>\r" %albsyears[i])
            file.write("    </album>\r")
        file.close()
except:
    pass
with open(createfile, 'a+') as file:	
    file.write("</artist> \r")	
    file.close()
#Make Directory
try:
    os.mkdir("ArtistArt")
except:
    pass
try:
    urllib.request.urlretrieve(slogo, logo)
    urllib.request.urlretrieve(sthumb, folder)
    urllib.request.urlretrieve(sfanart, fanart)
    urllib.request.urlretrieve(sfanart2, fanart2)
    urllib.request.urlretrieve(sbanner, banner)
    existlogo = os.path.isfile(logo)
    existfolder = os.path.isfile(folder)
    existfanart = os.path.isfile(fanart)
    existfanart2 = os.path.isfile(fanart2)
    existbanner = os.path.isfile(banner)
    if existlogo:
        print('LogoArt', existlogo)
    else:
        print('LogoArt' + ' ' + colored(existlogo, 'red'))	
    if existfolder:
        print('ThumbArt', existfolder)
    else:
        print('ThumbArt' + ' ' + colored(existfolder, 'red'))
    if existfanart:
        print('FanartArt', existfanart)
    else:
        print('FanartArt' + ' ' + colored(existfanart, 'red'))
    if existfanart2:
        print('Fanart2Art', existfanart2)
    else:
        print('Fanart2Art' + ' ' + colored(existfanart2, 'red'))
    if existbanner:
        print('BannerArt', existbanner)
    else:
        print('BannerArt' + ' ' + colored(existbanner, 'red'))			
    ArtistArt = os.listdir(Aistsource)    
    for f in ArtistArt:
        shutil.copy(Aistsource+f, atsdestpath)
except:
    print("Art Error")