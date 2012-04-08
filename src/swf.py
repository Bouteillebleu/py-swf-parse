# "D:/Coding/sim_original_test.swf"
# First go - using http://the-labs.com/MacromediaFlash/SWF-Spec/SWFfileformat.html as guide.
import sys, os, zlib
import datatypes
from tags import TagFactory
from bitstring import ConstBitStream

class Swf(object):
    def __init__(self,filename):
        # For now, when we get the file we want to parse it right away.
        self.filename = filename
        self.parse()
    
    def parse(self):
        f = open(self.filename,"rb")
        self._bitstream = ConstBitStream(f)
        try:
            self.parse_header()
            self.parse_tags()
        finally:
            f.close()
    
    def parse_header(self):
        file_type = self._bitstream.read('bytes:3')
        self.version = self._bitstream.read('uintle:8')
        self.size = self._bitstream.read('uintle:32')
        if file_type == "FWS":
            self.compressed = False
        elif file_type == "CWS":
            self.compressed = True
            # Decompress what's after version and size, and rejoin.
            start_section = self._bitstream[:64]
            to_decompress = self._bitstream[64:].tobytes()
            self._bitstream = start_section + ConstBitStream(bytes=zlib.decompress(to_decompress))
            self._bitstream.pos = 64
        self.framesize = datatypes.Rect(self._bitstream)
        self.framerate = datatypes.Fixed8(self._bitstream)
        self.framecount = self._bitstream.read('uintle:16')

        self.display_header() # DEBUG

    def display_header(self):
        print "Compressed:",self.compressed
        print "Version:",self.version
        print "Size:",self.size,"bytes"
        print "FrameSize:",self.framesize
        print "FrameRate:",self.framerate
        print "FrameCount:",self.framecount
        
    def parse_tags(self):
        self.tags = []
        current_tag_type = -1
        while current_tag_type != 0:
            tag_header = self._bitstream.read('uintle:16')
            current_tag_type = tag_header >> 6 # Ignore the bottom 6 bits
            current_tag_length = tag_header & 0x3F # Only keep bottom 6 bits
            if current_tag_length == 0x3f:
                # If it's actually 63, use the long record header form instead.
                current_tag_length = self._bitstream.read('intle:32')
            #print "Current tag type:",current_tag_type
            #print "Current tag length:",current_tag_length
            tag_stream = self._bitstream.read('bits:{0}'.format(current_tag_length*8))
            new_tag = TagFactory.new_tag(self.version,
                                         tag_stream,
                                         current_tag_type,
                                         current_tag_length)
            self.tags.append(new_tag)
            
    def display_tags(self):
        for i, tag in enumerate(self.tags):
            print "== Tag {0}: {1} ==".format(i,tag.__class__.__name__)
            tag.display()

# ========

def main():
    test_file = sys.argv[1]
    f = open(os.path.join(os.getcwd(),test_file), "rb")
    s = ConstBitStream(f)
    try:
        file_type = s.read('bytes:3')
        if file_type == "FWS":
            print "Standard SWF"
            print "Version:",s.read('uintle:8')
            print "Size:",s.read('uintle:32'),"bytes"
            s = datatypes.rect(s)
            print "Frame rate: %d.%d" % datatypes.fixed_8(s)
            print "Frame count:",s.read('uintle:16')
            read_tag_headers(s)
        elif file_type == "CWS":
            print "Compressed SWF"
            print "Version:",s.read('uintle:8')
            print "Uncompressed size:",s.read('uintle:32'),"bytes"
            to_decompress = s[64:].tobytes()
            s = ConstBitStream(bytes=zlib.decompress(to_decompress))
            s = datatypes.rect(s)
            print "Frame rate: %d.%d" % datatypes.fixed_8(s)
            print "Frame count:",s.read('uintle:16')
            read_tag_headers(s)
            #print "[Cannot currently parse]"
    finally:
        f.close()

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
    tag_functions = {#2:  tag_parsers.define_shape,
                     4:  tag_parsers.place_object,
                     5:  tag_parsers.remove_object,
                     9:  tag_parsers.set_background_color,
                     #10: tag_parsers.define_font,
                     12: tag_parsers.do_action,
                     21: tag_parsers.define_bits_jpeg_2,
                     #22: tag_parsers.define_shape_2,
                     26: tag_parsers.place_object_2,
                     28: tag_parsers.remove_object_2,
                     32: tag_parsers.define_shape_3,
                     37: tag_parsers.define_edit_text,
                     39: tag_parsers.define_sprite,
                     43: tag_parsers.frame_label,
                     59: tag_parsers.do_init_action,
                     65: tag_parsers.script_limits,
                     66: tag_parsers.set_tab_index,
                     }
    if number in tag_functions:
        return tag_functions[number]
    else:
        return tag_parsers.not_implemented


if __name__ == "__main__":
    swf_object = Swf(sys.argv[1])
    swf_object.display_header()
    swf_object.display_tags()

