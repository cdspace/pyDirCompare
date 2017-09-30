import os
import csv
import hashlib

baseDir = "/Users/cdspace/Desktop/phoneBAK_FINAL/"
subDirs = [ "other",
            "photos",
            "videos" ]



def getFileInfo( inDir, pathList ):
    # to get MD5
    # hashlib.md5( open( fullPath, 'rb' ).read(), ) hexDigest()

    for newDir in os.listdir( inDir ):

        fullPath = inDir + "/" + newDir
        isDir = os.path.isdir( fullPath )
        if isDir:
            getFileInfo( fullPath, pathList )

        # else it's a file, yield the MD5
        else:
            h = ""
            with open( fullPath, 'rb' ) as f:
                h = hashlib.md5( f.read() ).hexdigest()
            pathList.append( [ h, fullPath ] )



for subD in subDirs:

    files1 = []
    files2 = []
    dupes = []

    # first load up the info for dir1
    # recursively, and only store the file info
    print( "Loading dir1..." + subD )
    getFileInfo( baseDir + subD, files1 )
    print( "{} files loaded".format( len( files1 ) ) )

    # make a copy to compare to
    files2 = files1[:]

    # loop and check
    for f1 in files1:

        for f2 in files2:

            if f1[ 0 ] == f2[ 0 ] and f1[ 1 ] != f2[ 1 ]:
                dupes.append( [ f1, f2 ] )


    # and output if we have anything
    if len( dupes ) >= 0:

        with open( baseDir + "dupes_" + subD + ".csv", 'w' ) as fOut:
            fOutCSV = csv.writer( fOut )
            for d in dupes:
                fOutCSV.writerow( d )

                
            
