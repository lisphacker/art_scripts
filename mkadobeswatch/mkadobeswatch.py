#!/usr/bin/env python

import sys
import csv
from pprint import pprint
import swatch
import matplotlib.pyplot as plt
import numpy as np
import colorsys
import math

def rgb(c):
    return c['data']['values'][0], c['data']['values'][1], c['data']['values'][2]

def sort_colors(colors):
    #return sort_colors_by_name(colors)
    return sort_colors_by_step(colors)
    
def sort_colors_by_name(colors):
    colors.sort(key=lambda c: int(c['name'].split(' ')[1]))
    return colors
          
def sort_colors_by_step(colors):
    gray = []
    notgray = []

    for color in colors:
        r, g, b = rgb(color)
        c = color['name'].lower()
        if c.find('grey') >= 0 or c.find('white') >= 0 or c.find('black') >= 0 or c.find('gray') >= 0:
            print(r, b, g, color['name'])
            gray.append(color)
        else:
            notgray.append(color)

    gray.sort(key=lambda c: rgb(c)[0])
    
    def step(r, g, b, repetitions=1):
        lum = math.sqrt( .241 * r + .691 * g + .068 * b )
 
        h, s, v = colorsys.rgb_to_hsv(r,g,b)
 
        h2 = int(h * repetitions)
        lum2 = int(lum * repetitions)
        v2 = int(v * repetitions)
 
        if h2 % 2 == 1:
            v2 = repetitions - v2
            lum = repetitions - lum

        return (h2, lum, v2)
            
    notgray.sort(key=lambda c: step(c['data']['values'][0], c['data']['values'][1], c['data']['values'][2], 8))

    return gray + notgray
    
def display(name, colors):
    N = 100
    
    ca = np.empty((len(colors), N, 3), dtype='float32')

    for i, c in enumerate(colors):
        ca[i, :, 0] = c['data']['values'][0]
        ca[i, :, 1] = c['data']['values'][1]
        ca[i, :, 2] = c['data']['values'][2]

    plt.figure()
    plt.title(name)
    plt.imshow(ca)
    plt.show()

def convert(name, csv_path, swatch_file):
    colors = []
    
    with open(csv_path, 'r') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            r = float(row['R']) / 255.0
            g = float(row['G']) / 255.0
            b = float(row['B']) / 255.0
            
            color = dict()
            color['name'] = str(row['Code'] + ' - ' + row['Name'])
            color['type'] = u'Process'
            color['data'] = {
                'mode':   u'RGB',
                'values': [r, g, b]
                }

            colors.append(color)

    colors = sort_colors(colors)
    display(name, colors)

    cg = {
        'name': str(name),
        'type': u'Color Group',
        'swatches': colors
        }

    swatch.write([cg], swatch_file)

def main():
    if len(sys.argv) != 4:
        print('SYNTAX: {} <name> <csv file> <swatch file>')
        return
        
    convert(sys.argv[1], sys.argv[2], sys.argv[3])
    
if __name__ == '__main__':
    main()
