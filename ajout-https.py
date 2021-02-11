#!/usr/bin/env python3

import os

print("path to the domains list")
pathlist = input()

with open(pathlist) as list:
    line = list.readline()
    urllist = open("listUrl.txt", "w")
    while line:
        url = str("https://"+line)
        print(url)
        urllist.write(url)
        line = list.readline()
    list.close()
