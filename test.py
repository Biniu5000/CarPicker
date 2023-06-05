def convertTuple(tup):
    # initialize an empty string
    str = ''
    for item in tup:
        str = str + " " + item
    return str

# Driver code
tuple = ('g', 'e', 'e', 'k', 's')
str = convertTuple(tuple)
print(str)