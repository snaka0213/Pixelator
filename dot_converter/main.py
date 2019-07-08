#!/usr/bin/env python3
import sys
from converter import DotConverter

filter = int(input("Filter size? >> "))
color = int(input("Number of colors? >> "))
dtcv = DotConverter(filter=filter, color=color)

path = input("File name? >> ")
dtcv.input(path)
dtcv.convert()

dtcv.show()
select = input("Save this file? [y/n] >> ")
if select != 'y':
    sys.exit()
else:
    new_path = input("New file name? >> ")
    new_img.save(new_path)
