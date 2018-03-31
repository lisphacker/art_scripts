#!/usr/bin/env python

from PIL import Image
import numpy as np
import sys
import glob
import os
import os.path as pth

def convert_file(infile, outfile):
    g1 = Image.open(infile).convert('L')
    size = g1.size

    grey = np.array(g1.getdata(0), dtype='float32')
    white = grey > 200
    alpha = np.ones_like(grey) * 255
    alpha[white] = 0

    a = Image.new('L', g1.size)
    a.putdata(alpha)

    g2 = g1.convert('LA')
    g2.putalpha(a)
    
    
    g2.save(outfile)

def main():
    indir = sys.argv[1]
    outdir = sys.argv[2]

    indir_len = len(indir)

    infiles = glob.glob(indir + '/**', recursive=True)
    for infile in infiles:
        rel_path = infile[indir_len:]
        p, ext = pth.splitext(rel_path)
        rel_path = p + '.png'

        if ext == '.png' or ext == '.jpg' or ext == '.jpeg':
            outfile = outdir + rel_path
            os.makedirs(pth.dirname(outfile), exist_ok = True)
            print('Converting {} to {}'.format(infile, outfile))
            convert_file(infile, outfile)

if __name__ == '__main__':
    main()
