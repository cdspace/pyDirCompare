# yielding a one key dictionary example

def oneKeyYieldRecursive( inDict, newKey ):

    # let's just yield a key that isn't in the inDict

    # try an if/else with a yield
    if newKey not in inDict.keys():
        yield { newKey : str( newKey ) }

    else:
        oneKeyYieldRecursive( inDict, newKey + 1 )



def oneKeyYieldRecursive2( inDict, newKey ):

    # let's just yield a key that isn't in the inDict

    # try an if/else with a yield
    if newKey in inDict.keys():
        oneKeyYieldRecursive( inDict, newKey + 1 )

    else:
        yield { newKey : str( newKey ) }


# init the dict
outDict = {}
print( outDict )
i = 1
for i in range( 5 ):
    outDict.update( { str( i ) : str( i ) } )

# second test
outDict2 = outDict.copy()

print( outDict )
print( outDict2 )

# now lets try the yeild
#for q in range( 2, 31 ):
#    ret = oneKeyYieldRecursive( outDict, q )
#    # here 'ret' is a generator, how to we get the single element dict out to use it?
#    outDict.update( ret )


# instead of getting the yield return to use it, loop over it
for y in range( 2, 30 ):
    for r in oneKeyYieldRecursive( outDict, y ):
        print( r )
        outDict.update( r )

print( outDict )

# and try the second one, should be the same
for y in range( 2, 30 ):
    print( y )
    for r in oneKeyYieldRecursive2( outDict2, y ):
        print( r )
        outDict2.update( r )

print( outDict2 )

# yup, results are the same
