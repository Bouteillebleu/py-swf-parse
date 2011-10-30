# "D:/Coding/sim_original_test.swf"
# First go - using http://the-labs.com/MacromediaFlash/SWF-Spec/SWFfileformat.html as guide.
import tag_parsers
import datatypes
from bitstring import ConstBitStream

def main():
    f = open("D:/Coding/sim_original_test.swf", "rb")
    s = ConstBitStream(f)
    try:
        print s.read('bytes:3')
        print "Version:",s.read('uintle:8')
        print "Size:",s.read('uintle:32'),"bytes"
        #print "oh god what is this:",struct.unpack('B',f.read(1))[0]
        s = read_rect(s)
        print "Frame rate:",s.read('uintle:8'),".",s.read('uintle:8')
        print "Frame count:",s.read('uintle:16')
        read_tag_headers(s)
    finally:
        f.close()

def read_rect(bitstream):
    # Read the Nbits field - the first 5 bits - to find the size of the next ones.
    nbits = bitstream.read('uint:5')
    print "nBits:",nbits
    nbits_format = 'int:%d' % nbits
    print "Xmin:",bitstream.read(nbits_format)
    print "Xmax:",bitstream.read(nbits_format)
    print "Ymin:",bitstream.read(nbits_format)
    print "Ymax:",bitstream.read(nbits_format)
    # Wherever we are now, we need to skip ahead to the next byte boundary.
    if bitstream.pos % 8 != 0:
        bitstream.pos = bitstream.pos + (8 - (bitstream.pos % 8))
    return bitstream

def read_tag_headers(stream):
    tag_number = 0
    tag_type_name = ''
    tags_in_file = []
    while tag_type_name != 'End':
        print " == Reading tag",tag_number,"== "
        #tag_type = stream.read('uint:10')
        #tag_length = stream.read('uint:6')
        header = stream.read('uintle:16')
        tag_type = header >> 6 # Ignore the bottom 6 bits
        tag_length = header & 0x3F # Only keep the bottom 6 bits
        if tag_length == 0x3f:
            # If it's actually 63, we're using the long record header form instead.
            tag_length = stream.read('intle:32')
        tag_type_name = datatypes.get_tag_type_name_from_number(tag_type)
        if tag_type_name not in tags_in_file:
            tags_in_file.append(tag_type_name)
        print "Tag type:",tag_type,tag_type_name
        print "Tag length:",tag_length,"bytes"
        tag_number += 1
        tag_parser = get_tag_parser_from_number(tag_type)
        if tag_length > 0:
            tag_parser(stream.read('bits:%d' % (tag_length*8))) # Call an appropriate function
        else:
            tag_parser(None)
    print "==== TAGS FOUND IN FILE: ===="
    for tag in tags_in_file:
        print tag
        
def get_tag_parser_from_number(number):
    tag_functions = {9:  tag_parsers.set_background_color,
                     12: tag_parsers.do_action,
                     #21: tag_parsers.define_bits_jpeg_2,
                     26: tag_parsers.place_object_2,
                     39: tag_parsers.define_sprite
                     }
    if number in tag_functions:
        return tag_functions[number]
    else:
        return tag_parsers.not_implemented


if __name__ == "__main__":
    main()