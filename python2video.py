#!/usr/bin/env python3

import os
from time import *
from subprocess import *
from sys import *
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
from PIL import Image, ImageDraw, ImageFont

fileName = argv[1]
frameDirName = 'frames'
fps = 30
fadeFrames = 20
startTime = clock_gettime(CLOCK_MONOTONIC)
executionStats = []

# unbuffer (part of expect package) allows pipe from subprocess without any buffering for real-time reading
process = Popen(['unbuffer', 'python3', '-m', 'trace', '-t', fileName], bufsize=0, encoding='utf8', stderr=STDOUT, stdout=PIPE)
while True:
    line = process.stdout.readline()
    if line:
        if line.startswith(fileName):
            parenOpenIndex = line.find('(')
            if parenOpenIndex != -1:
                parenCloseIndex = line.find(')', parenOpenIndex + 1)
                now = clock_gettime(CLOCK_MONOTONIC)
                lineNumber = int(line[parenOpenIndex + 1:parenCloseIndex])
                secondsFromStart = now - startTime
                executionStats.append((secondsFromStart, lineNumber))
                print(str(secondsFromStart) + ': executing line ' + str(lineNumber))
    else:
        break

class FadingLinesImageFormatter(ImageFormatter):
    def __init__(self, **options):
        ImageFormatter.__init__(self, **options)
        self.fade_lines = options.get('fade_lines', {})

    def format(self, tokensource, outfile):
        """
        TODO
        """
        self._create_drawables(tokensource)
        self._draw_line_numbers()
        im = Image.new(
            'RGB',
            self._get_image_size(self.maxcharno, self.maxlineno),
            self.background_color
        )
        self._paint_line_number_bg(im)
        draw = ImageDraw.Draw(im)
        # Highlight
        if self.fade_lines:
            x = self.image_pad + self.line_number_width - self.line_number_pad + 1
            recth = self._get_line_height()
            rectw = im.size[0] - x
            for linenumber, intensity in self.fade_lines.items():
                y = self._get_line_y(linenumber - 1)
                draw.rectangle([(x, y), (x + rectw, y + recth)],
                               fill=(47 + intensity, 30 + intensity, 46 + intensity))
        for pos, value, font, kw in self.drawables:
            draw.text(pos, value, font=font, **kw)
        im.save(outfile, self.image_format.upper())

#run(['rm', '-rf', frameDirName])
os.makedirs(os.path.join(frameDirName), exist_ok=True)
with open(fileName, 'r') as file:
    code = file.read()
    frameNumber = 1
    executedLines = {}
    lastLine = 0
    while executionStats:
        for line, value in executedLines.items():
            if value > 0 and line != lastLine:
                executedLines[line] = value - 1
        frameEndTime = frameNumber / fps
        print(str(frameEndTime) + ': generating frame ' + str(frameNumber))
        while executionStats and executionStats[0][0] < frameEndTime:
            lastLine = executionStats.pop(0)[1]
            executedLines[lastLine] = fadeFrames
        with open(frameDirName + '/' + str(frameNumber).zfill(8) + '.png', 'wb+') as image:
            image.write(highlight(code, PythonLexer(), FadingLinesImageFormatter(style='paraiso-dark', fade_lines=executedLines)))
        frameNumber = frameNumber + 1

run(['ffmpeg', '-y', '-framerate', str(fps), '-pattern_type', 'glob', '-i', frameDirName + '/*.png', 'test.mp4'])
