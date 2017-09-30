import os
import hashlib

# TODO need a recursive directory follower function to get files
def getFileInfo( inDir ):
    # to get MD5
    # hashlib.md5( open( fullPath, 'rb' ).read(), ) hexDigest()

    for newDir in os.listdir( inDir ):

        fullPath = inDir + "/" + newDir
        isDir = os.path.isdir( fullPath )
        if isDir:
            getFileInfo( fullPath )

        # else it's a file, yield the MD5
        else:
            yield { hashlib.md5( open( fullPath, 'rb' ).read() ).hexdigest() : fullPath }


    
dir1 = "/Users/cdspace/Desktop/Jason SD BAK"
dir2 = "/Users/cdspace/Desktop/jason gs7 bak"

# we don't know the paths of the files, so let's keep a dict of lists, filename the key
# the filenames between backups should be the same
files1 = {}
files2 = {}

# first load up the info for dir1
# recursively, and only store the file info
for res in getFileInfo( dir1 ):
    print( res )
    files1.update( res )

# then load up the file info for dir2
for res in getFileInfo( dir2 ):
    files2.update( res )

print( files1 )

# now compare them both, by keys in the dicts
# start with dir1
for fKey1, fInfo1 in files1.items():

    # if this filename is in the second dict
    if fKey1 in files2.keys():

        # compare the file info
        # i.e. the MD5
        # what if the filesnames don't match, but the MD5's do?
        # is it the same file?
        # shouldn't the file names match if it's the same file
        # or we can check those later, once we get the real duplicates out of the way
        if fInfo1 == files2[ fKey1 ]:
            pass

            # if comparable, save to compare file to look at later

        # if not
        # this might generate a lot of false negatives, maybe just if the key is there
        # but the MD5 doesn't match
        # key is there, already checked, so this is if the files don't match, so we
        # need to match by hand on these, so all good
        else:
            pass

            # save to another file, to compare differing files


    # if the filename isn't even there
    else:
        pass

        # save to another file to check by hand
        # save the whole path
