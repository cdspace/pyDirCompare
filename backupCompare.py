import os
import os.path
import hashlib
import csv
import shutil

# TODO need a recursive directory follower function to get files
# perhaps yeild isn't necessary here
# it might be if we were returning the os.listdir, but we just want to return the
# hash and path, recursively, so just return it
def getFileInfo( inDir, pathDict ):
    # to get MD5
    # hashlib.md5( open( fullPath, 'rb' ).read(), ) hexDigest()

    for newDir in os.listdir( inDir ):

        fullPath = inDir + "/" + newDir
        isDir = os.path.isdir( fullPath )
        if isDir:
            getFileInfo( fullPath, pathDict )

        # else it's a file, yield the MD5
        else:
            h = ""
            with open( fullPath, 'rb' ) as f:
                h = hashlib.md5( f.read() ).hexdigest()
            pathDict.update( { h : fullPath } )


# run 1    
##dir1Name = "1_Jason SD BAK"
##dir2Name = "2_jason gs7 bak"

# run 2
##dir1Name = "1_Jason SD BAK"
##dir2Name = "3_GS4bak"

# run 3
##dir1Name = "2_jason gs7 bak"
##dir2Name = "3_GS4bak"

# run 1 to run 2 final
dir1Name = "run1_finalCopy"
dir2Name = "run2_finalCopy"

baseDir = "/Users/cdspace/Desktop/"
dir1 = baseDir + dir1Name
dir2 = baseDir + dir2Name
outDir = baseDir + "bakCompare/"
finalCopyDir = baseDir + "finalCopy/"

# we don't know the paths of the files, so let's keep a dict of lists, filename the key
# the filenames between backups should be the same
files1 = {}
files2 = {}
only1Files = {}
only2Files = {}
bothFiles = {}

# first load up the info for dir1
# recursively, and only store the file info
print( "Loading dir1..." )
getFileInfo( dir1, files1 )
print( "{} files loaded".format( len( files1 ) ) )

#for res in getFileInfo( dir1 ):
#    print( res )
#    files1.update( res )

# then load up the file info for dir2
print( "Loading dir2..." )
getFileInfo( dir2, files2 )
print( "{} files loaded".format( len( files2 ) ) )

#for res in getFileInfo( dir2 ):
#    files2.update( res )

#print( "dir1 has {} files".format( len( files1 ) ) )
#print( "dir2 has {} files".format( len( files2 ) ) )

# initialize the output files
if not os.path.exists( outDir + dir1Name.replace( " ", "_" ) + "_sameFiles.csv" ):
    sameFile = open( outDir + dir1Name.replace( " ", "_" ) + "_sameFiles.csv", 'w' )
    sameFile.close()
if not os.path.exists( outDir + dir1Name.replace( " ", "_" ) + "_onlyDir1.csv" ):
    dir1Files = open( outDir + dir1Name.replace( " ", "_" ) + "_onlyDir1.csv", 'w' )
    dir1Files.close()
if not os.path.exists( outDir + dir2Name.replace( " ", "_" ) + "_onlyDir2.csv" ):
    dir2Files = open( outDir + dir2Name.replace( " ", "_" ) + "_onlyDir2.csv", 'w' )
    dir2Files.close()

# now compare them both, by keys in the dicts
# start with dir1
print( "Begin compare..." )
for fKey1, fInfo1 in files1.items():

    # if this filename is in the second dict
    if fKey1 in files2.keys():

        # compare the file info
        # i.e. the MD5
        # what if the filesnames don't match, but the MD5's do?
        # is it the same file?
        # shouldn't the file names match if it's the same file
        # or we can check those later, once we get the real duplicates out of the way
##        print( fKey1 )
##        print( fInfo1 )
##        print( files2[ fKey1 ] )
##        print( fInfo1[ fInfo1.rindex( "/" ) + 1 : ] )
##        print( files2[ fKey1 ][ files2[ fKey1 ].rindex( "/" ) + 1 : ] )
        if fInfo1[ fInfo1.rindex( "/" ) + 1 : ] == files2[ fKey1 ][ files2[ fKey1 ].rindex( "/" ) + 1 : ]:

            # if comparable, save to compare file to look at later
            bothFiles.update( { fKey1 : [ fInfo1, files2[ fKey1 ] ] } )

        # if not
        # this might generate a lot of false negatives, maybe just if the key is there
        # but the MD5 doesn't match
        # key is there, already checked, so this is if the files don't match, so we
        # need to match by hand on these, so all good
        else:
            only1Files.update( { fKey1 : fInfo1 } )


    # if the hash isn't even there
    else:

        # save to another file to check by hand
        # save the whole path
        only1Files.update( { fKey1 : fInfo1 } )

# and lastly, check for anything in files2 that isn't in bothFiles
print( "Final check..." )
for fKey2, fInfo2 in files2.items():

    if fKey2 not in bothFiles.keys():

        only2Files.update( { fKey2 : fInfo2 } )

print( "Output results..." )
print( "Num only 1: {}".format( len( only1Files ) ) )
print( "Num only 2: {}".format( len( only2Files ) ) )
print( "Num both  : {}".format( len( bothFiles ) ) )
num1 = len( only1Files ) + len( bothFiles )
num2 = len( only2Files ) + len( bothFiles )
print( "1: {} = {}".format( num1, len( files1 ) ) )
print( "2: {} = {}".format( num2, len( files2 ) ) )
# finish up, output the final lists
# use csv
sameFile = open( outDir + dir1Name.replace( " ", "_" ) + "_sameFiles.csv", 'a' )
sameCSV = csv.writer( sameFile )
for key, value in bothFiles.items():
    sameCSV.writerow( [ key, value[ 0 ], value[ 1 ] ] )
sameFile.close()

dir1Files = open( outDir + dir1Name.replace( " ", "_" ) + "_onlyDir1.csv", 'a' )
dir1CSV = csv.writer( dir1Files )
for key, value in only1Files.items():
    dir1CSV.writerow( [ key, value ] )
dir1Files.close()

dir2Files = open( outDir + dir2Name.replace( " ", "_" ) + "_onlyDir2.csv", 'a' )
dir2CSV = csv.writer( dir2Files )
for key, value in only2Files.items():
    dir2CSV.writerow( [ key, value ] )
dir2Files.close()

print( "Copy the duplicates to an output directory..." )

# now copy the duplicates to a new directory
# preserve the path beyond dir1/2
for fKey, fName in bothFiles.items():

    # get the 1/2 input dirs, and the final output dir
    outfNameCopy = fName[ 0 ].replace( dir1, finalCopyDir[ : -1 ] )
    outDirCopy = outfNameCopy[ : outfNameCopy.rindex( "/" ) + 1 ]
    
    # if the directory isn't there, make it
    if not os.path.exists( outDirCopy ):
        os.makedirs( outDirCopy )

    # copy fName[ 0 ] into the output
    shutil.copyfile( fName[ 0 ], outfNameCopy )

    # and delete the originals
    os.remove( fName[ 0 ] )
    os.remove( fName[ 1 ] )
    
