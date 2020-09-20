#!/usr/bin/env python3

from time import *
from subprocess import *
from sys import *

fileName = argv[1]

# unbuffer (part of expect package) allows pipe from subprocess without any buffering for real-time reading
process = Popen(['unbuffer', 'python3', '-m', 'trace', '-t', fileName], bufsize=0, encoding='utf8', stderr=STDOUT, stdout=PIPE)
startTime = clock_gettime(CLOCK_MONOTONIC)
while True:
    line = process.stdout.readline()
    if line:
        if line.startswith(fileName):
            parenOpenIndex = line.find('(')
            if parenOpenIndex != -1:
                parenCloseIndex = line.find(')', parenOpenIndex + 1)
                now = clock_gettime(CLOCK_MONOTONIC)
                print(str(now - startTime) + ',' + line[parenOpenIndex + 1:parenCloseIndex])
    else:
        break
