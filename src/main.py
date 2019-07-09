#!/usr/bin/env python3
import sys
from converter import DotConverter

filter_size = int(input("Filter size? >> "))
colors = int(input("Number of colors? >> "))
dtcv = DotConverter(filter_size=filter_size, colors=colors)

path = input("File name? >> ")
dtcv.input(path)
dtcv.convert()

dtcv.show()
select = input("Save this file? [y/n] >> ")
if select != 'y':
    sys.exit()
else:
    new_path = input("New file name? >> ")
    dtcv.save(new_path)
