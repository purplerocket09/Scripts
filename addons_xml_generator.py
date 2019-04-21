# *
# *  Copyright (C) 2012-2013 Garrett Brown
# *  Copyright (C) 2010      j48antialias
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with XBMC; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# *  Based on code by j48antialias:
# *  https://anarchintosh-projects.googlecode.com/files/addons_xml_generator.py
# *
 
""" addons.xml generator """
import hashlib
import os
import sys
 
# Compatibility with 3.0, 3.1 and 3.2 not supporting u"" literals
if sys.version < '3':
    import codecs
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x

class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.sha256 hash file. Must be run from the root of
        the checked-out repo. Only handles single depth folder structure.
        Also generates asha256 hash of the zip file contained in each addon folder (Leia)
    """
    def __init__(self):
        # generate files
        self.generateaddonsfile()
        self.generatesha256file("addons.xml")
        #self.generatezip256file()		
        # notify user
        print("Finished updating addons xml and sha256 files")


    def generatezip256file(self):
        # create sha256 hash for zip (Kodi Leia)
        addons = os.listdir( "." )	
        for addon_file in os.listdir(addon):
            if addon_file.endswith('.zip'):
                files = os.path.join(addon, addon_file)
                self.generatesha256file(addons_xml.encode( "UTF-8" ), file=files)        

    def generateaddonsfile(self):
        # addon list
        addons = os.listdir( "." )
        # final addons text
        addons_xml = u("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n")
        # loop thru and add each addons addon.xml file
        for addon in addons:
            try:
                # skip any file or .svn folder or .git folder
                if ( not os.path.isdir( addon ) or addon == ".svn" or addon == ".git" ): continue
                # create path
                _path = os.path.join( addon, "addon.xml" )
                # split lines for stripping
                xml_lines = open( _path, "r" ).read().splitlines()
                # new addon
                addon_xml = ""
                # loop thru cleaning each line
                for line in xml_lines:
                    # skip encoding format line
                    if ( line.find( "<?xml" ) >= 0 ): continue
                    # add line
                    if sys.version < '3':
                        addon_xml += unicode( line.rstrip() + "\n", "UTF-8" )
                    else:
                        addon_xml += line.rstrip() + "\n"
                # we succeeded so add to our final addons.xml text
                addons_xml += addon_xml.rstrip() + "\n\n"
                # create md5 hash for zip (Kodi Krypton)
                for addon_file in os.listdir(addon):
                    if addon_file.endswith('.zip'):
                        self.generatesha256file(os.path.join(addon, addon_file)) 
            except Exception as e:
                # missing or poorly formatted addon.xml
                print("Excluding %s for %s" % ( _path, e ))
        # clean and add closing tag
        addons_xml = addons_xml.strip() + u("\n</addons>\n")
        # save file
        self.savefile( addons_xml.encode( "UTF-8" ), file="addons.xml" )

    def generatesha256file(self, file):
        import hashlib 
        if file == "addons.xml":		
            sha256hash = hashlib.sha256( open( file, "r", encoding="UTF-8" ).read().encode( "UTF-8" ) ).hexdigest()
            # save file
            self.savefile( sha256hash.encode( "UTF-8" ), file="addons.xml.sha256" )
        else:
            BLOCKSIZE = 65536
            hasher = hashlib.sha256()
            
            with open(file, 'rb') as afile:
                buf = afile.read(BLOCKSIZE)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = afile.read(BLOCKSIZE)
            sha256hash = hasher.hexdigest()
            try:
                if open(file+".sha256", 'r').read() == sha256hash:
                    # Same hash, skip
                    return
            except Exception:
                pass
            self.savefile(sha256hash.encode( "UTF-8" ), file+".sha256")

    def savefile(self, data, file):
        try:
            # write data to the file (use b for Python 3)
            open(file, "wb").write(data)
        except Exception as error:
            # oops
            print("An error occurred saving %s file!\n%s" % (file, error)) 
 
if ( __name__ == "__main__" ):
    # start
    Generator()