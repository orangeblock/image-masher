#!/usr/bin/python
###
#   A simple script to mash images together in horizontal or vertical strips. 
#   The visible part of each image depends on its position in the sequence.
# 
#   Copyright (C) 2017 orangeblock
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
###
import os
import PIL
import urllib2
import argparse

from PIL import Image

HORIZONTAL = 1
VERTICAL = 2

DEFAULT_SIZE = (500, 500)
DEFAULT_SAMPLER = PIL.Image.BICUBIC
DEFAULT_SAVE = False
DEFAULT_OUT = '.'


def _load_images(locations):
    images = []
    for location in locations:
        try:
            images.append(Image.open(location))
        except IOError:
            images.append(Image.open(urllib2.urlopen(location)))
    return images


def _crop_images(images, final_size, direction):
    max_x, max_y = final_size
    step = max_x / len(images) if direction == VERTICAL else max_y / len(images)
    imgXpos = []
    for i, image in enumerate(images):
        if i == (len(images) - 1):
            # The last image is cropped to the edge to fill missing pixels due to imperfect division
            if direction == VERTICAL:
                box_position = (i*step, 0, max_x, max_y)
            else:
                box_position = (0, i*step, max_x, max_y)
        else:
            if direction == VERTICAL:
                box_position = (i*step, 0, (i+1)*step, max_y)
            else:
                box_position = (0, i*step, max_x, (i+1)*step)
        imgXpos.append((image.crop(box_position), box_position))
    return imgXpos


def mash(img_locations, size=DEFAULT_SIZE, direction=VERTICAL, sampler=DEFAULT_SAMPLER, save=DEFAULT_SAVE, out=DEFAULT_OUT, out_name='mashed'):
    if len(img_locations) < 2:
        raise Exception("You need at least 2 images")
    if direction not in (VERTICAL, HORIZONTAL):
        raise Exception("Not a supported direction")
    if len(size) != 2 or size[0] <= 0 or size[1] <= 0:
        raise Exception("Invalid size")

    resized = [image.resize(size, sampler) for image in _load_images(img_locations)]
    croppedXpos = _crop_images(resized, size, direction)
    
    canvas = Image.new('RGB', size)
    for image, position in croppedXpos:
        canvas.paste(image, position)
    if save:
        canvas.save(os.path.join(out, '%s.jpg' % out_name), 'JPEG')
    return canvas




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mash images together in vertical strips')
    parser.add_argument('--horizontal', action='store_true', help='Mash horizontally instead')
    parser.add_argument('-x', metavar='<pixels>', default=DEFAULT_SIZE[0], type=int, help='Size of final image on the X axis; default=%d' % DEFAULT_SIZE[0])
    parser.add_argument('-y', metavar='<pixels>', default=DEFAULT_SIZE[1], type=int, help='Size of final image on the Y axis; default=%d' % DEFAULT_SIZE[1])
    parser.add_argument('-d', '--dest', metavar='<path>', default=DEFAULT_OUT, help='Specify output directory; default=%s' % DEFAULT_OUT)
    parser.add_argument('images', nargs='*', help='A list of descriptors to image files. Can be file paths or URLs')

    args = parser.parse_args()
    direction = HORIZONTAL if args.horizontal else VERTICAL
    mashed = mash(args.images, size=(args.x, args.y), direction=direction, save=True, out=args.dest)
