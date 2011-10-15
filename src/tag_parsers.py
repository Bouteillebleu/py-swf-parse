'''
Created on 15 Oct 2011

@author: Bluebottle
'''
import struct

def set_background_color(data):
    # Data should be an RGB color record.
    rgb = rgb_color_record(data)
    print "Background colour: RGB =",rgb

def not_implemented(data):
    print "No parser for this tag yet."
    
# == Data type readers (to pull out into another module?) ==

def rgb_color_record(data):
    # Data should be 3 bytes long: R, G and B values, each read as UI8.
    r = struct.unpack('B',data[0])[0]
    g = struct.unpack('B',data[1])[0]
    b = struct.unpack('B',data[2])[0]
    return r,g,b