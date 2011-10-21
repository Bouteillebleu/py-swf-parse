# "D:/Coding/sim_original_test.swf"
# First go - using http://the-labs.com/MacromediaFlash/SWF-Spec/SWFfileformat.html as guide.
import struct
import tag_parsers
import datatypes

def main():
    f = open("D:/Coding/sim_original_test.swf", "rb")
    try:
        print f.read(3)
        print "Version:",struct.unpack('<B',f.read(1))[0]
        print "Size:",struct.unpack('<L',f.read(4))[0],"bytes"
        #print "oh god what is this:",struct.unpack('B',f.read(1))[0]
        f = read_rect(f)
        print "Frame rate:",struct.unpack('<B',f.read(1))[0],".",struct.unpack('B',f.read(1))[0]
        print "Frame count:",struct.unpack('<H',f.read(2))[0]
        read_tag_headers(f)
    finally:
        f.close()

def read_rect(file):
    # Read the Nbits field - the first 5 bits - to find the size of the next ones.
    rect_start = struct.unpack('<B',file.read(1))[0]
    nbits = rect_start >> 3
    print "nBits:",nbits
    # TODO: And actually, at this point I don't really care about the frame size.
    # Skip it for now.
    # For example, if nbits = 15, we skip 60 - 3 = 57 bits, which is 56 bits (7 bytes)
    # plus 1 bit, which works out to 8 bytes.
    skip_amount = (((nbits * 4) - 3) // 8) + 1
    print "Skipping",skip_amount,"bytes of RECT"
    dummy_read = file.read(skip_amount)
    return file

def read_tag_headers(file):
    tag_number = 0
    tag_type_name = ''
    tags_in_file = []
    while tag_type_name != 'End':
        print " == Reading tag",tag_number,"== "
        header = struct.unpack('<H',file.read(2))[0]
        tag_type = header >> 6 # Ignore the bottom 6 bits
        tag_length = header & 0x3F # Only keep the bottom 6 bits
        if tag_length == 0x3f:
            # If it's actually 63, we're using the long record header form instead.
            tag_length = struct.unpack('<L',file.read(4))[0]
        tag_type_name = datatypes.get_tag_type_name_from_number(tag_type)
        if tag_type_name not in tags_in_file:
            tags_in_file.append(tag_type_name)
        print "Tag type:",tag_type,tag_type_name
        print "Tag length:",tag_length,"bytes"
        tag_number += 1
        tag_parser = get_tag_parser_from_number(tag_type)
        tag_parser(file.read(tag_length)) # Call an appropriate function to 
    print "==== TAGS FOUND IN FILE: ===="
    for tag in tags_in_file:
        print tag
        
def get_tag_parser_from_number(number):
    tag_functions = {9:  tag_parsers.set_background_color,
                     21: tag_parsers.define_bits_jpeg_2,
                     26: tag_parsers.place_object_2,
                     39: tag_parsers.define_sprite}
    if number in tag_functions:
        return tag_functions[number]
    else:
        return tag_parsers.not_implemented


if __name__ == "__main__":
    main()