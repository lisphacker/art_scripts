import csv
from collections import namedtuple
import swatch
from pprint import pprint

def find_index(l, x):
    try:
        return l.index(x)
    except:
        return -1
    
def read_csv(filename):
    colors = {}
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for i,row in enumerate(reader):
            if i == 0:
                ri = find_index(row, 'R')
                gi = find_index(row, 'G')
                bi = find_index(row, 'B')
                
                ci = find_index(row, 'C')
                mi = find_index(row, 'M')
                yi = find_index(row, 'Y')
                ki = find_index(row, 'K')
            else:
                if ri != -1 and gi != -1 and bi != -1:
                    r = float(row[ri]) / 255.0
                    g = float(row[gi]) / 255.0
                    b = float(row[bi]) / 255.0
                    rgb = (r, g, b)
                else:
                    rgb = None
                    
                if ci != -1 and ci != -1 and yi != -1 and ki != -1:
                    c = int(row[ci]) / 100.0
                    m = int(row[mi]) / 100.0
                    y = int(row[yi]) / 100.0
                    k = int(row[ki]) / 100.0
                    cmyk = (c, m, y, k)
                else:
                    cmyk = None
                    
                colors[row[0]] = (row[1], rgb, cmyk)
    return colors

def make_swatches(pencil):
    colors = read_csv(pencil + '.csv')

    rgb_swatch = None
    cmyk_swatch = None

    for code in colors:
        name, rgb, cmyk = colors[code]
        if rgb is not None and rgb_swatch is None:
            rgb_swatch = dict()
            rgb_swatch['name'] = pencil.capitalize() + ' RGB'
            rgb_swatch['swatches'] = list()
            rgb_swatch['type'] = 'Color Group'
        if rgb is not None:
            color_desc = dict()
            color_desc['data'] = dict()
            color_desc['data']['mode'] = 'RGB'
            color_desc['data']['values'] = rgb
            color_desc['name'] = code + ' ' + name
            color_desc['type'] = 'Process'
            rgb_swatch['swatches'].append(color_desc)

        if cmyk is not None and cmyk_swatch is None:
            cmyk_swatch = dict()
            cmyk_swatch['name'] = pencil.capitalize() + ' CMYK'
            cmyk_swatch['swatches'] = list()
            cmyk_swatch['type'] = 'Color Group'
        if cmyk is not None:
            color_desc = dict()
            color_desc['data'] = dict()
            color_desc['data']['mode'] = 'CMYK'
            color_desc['data']['values'] = cmyk
            color_desc['name'] = code + ' ' + name
            color_desc['type'] = 'Process'
            cmyk_swatch['swatches'].append(color_desc)

    return rgb_swatch, cmyk_swatch

def convert():
    prisma_rgb, prisma_cmyk = make_swatches('prismacolor')
    poly_rgb,   poly_cmyk   = make_swatches('polychromos')

    swatches = []

    def append(colors):
        if colors is not None:
            swatches.append(colors)

    append(prisma_rgb)
    append(prisma_cmyk)
    append(poly_rgb)
    append(poly_cmyk)

    swatch.write(swatches, 'pencil_palettes.ase')
