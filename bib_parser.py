#! /usr/bin/python3

import sys

# replace_chars = ["&", "%", "_", "$"]
replace_chars = ["&", "%", "$"]

def find_all(source, search):
    occurances = [] # list of indexes where character has occured in the string provided
    start = 0
    while True:
        index = source.find(search, start)
        if index == -1:
            return occurances
        else:
            start = index + 1
            if source[index - 1] == '\\':
                continue
            occurances.append(index)
            

def replace_all(locations, source):
    for index in locations:
        source = source[:index] + '\\' + source[index:]
    return source

try:
    file = sys.argv[1]
    with open(file, 'r+') as bib:
        read_bib = bib.read()
        for char in replace_chars:
            replace_index = find_all(read_bib, char)
            read_bib = replace_all(replace_index, read_bib)
        bib.seek(0)
        bib.write(read_bib)
        bib.truncate()
        
except IndexError:
    print("not enough parameters for script")
# except:
#     print("Something went bung")

