# "D:/Coding/sim_original_test.swf"
# First go - using http://the-labs.com/MacromediaFlash/SWF-Spec/SWFfileformat.html as guide.
import sys, os, zlib
import datatypes
from tags import TagFactory, Tag
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

    def display_header(self):
        print "Compressed:",self.compressed
        print "Version:",self.version
        print "Size:",self.size,"bytes"
        print "FrameSize:",self.framesize
        print "FrameRate:",self.framerate
        print "FrameCount:",self.framecount
        
    def parse_tags(self):
        self.tags = []
        self.dictionary = {}
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
            if hasattr(new_tag,'character_id'):
                print "A NEW DICTIONARY ENTRY (not nested)"
                self.dictionary[new_tag.character_id] = {'nested': False,
                                                         'num': len(self.tags)-1}
            elif hasattr(new_tag,'tags'):
                for t in new_tag.tags:
                    if hasattr(t,'character_id'):
                        print "A NEW DICTIONARY ENTRY (nested)"
                        self.dictionary[t.character_id]={'nested': True,
                                                         'num':len(new_tag.tags)-1,
                                                         'parent_num':len(self.tags)-1}
            
    def display_tags(self):
        for i, tag in enumerate(self.tags):
            print "== Tag {0}: {1} ==".format(i,tag.__class__.__name__)
            tag.display()

    def included_tags(self):
        # This doesn't include tags that are part of DefineSprite.
        # Not yet, at least.
        print "Tags in this file:"
        tag_classes = [tag.__class__ for tag in self.tags]
        tag_instances = dict((c, tag_classes.count(c)) for c in tag_classes)
        for tag_class, number in sorted(tag_instances.items(),
                                        key=lambda x: x[1],
                                        reverse=True):
            print "{0}: {1} time{2}".format(tag_class.__name__,
                                            number,
                                            "s"[number==1:])
            if tag_class.parse == Tag.parse:
                print "  parser not implemented"
            else:
                print "  parser implemented"
        
    def display_dictionary(self):
        if len(self.dictionary.keys()) == 0:
            print "Dictionary currently empty."
        else:
            for char_id in sorted(self.dictionary.keys()):
                if self.dictionary[char_id]['nested']:
                    print "CharacterID {0}: {1}, tag {2} in {3}, tag {4}".format(char_id,
                        self.tags[self.dictionary[char_id]['parent_num']].tags[self.dictionary[char_id]['num']].__class__.__name__,
                        self.dictionary[char_id]['num'],
                        self.tags[self.dictionary[char_id]['parent_num']].__class__.__name__,
                        self.dictionary[char_id]['parent_num'])
                else:
                    print "CharacterID {0}: {1}, tag {2}".format(char_id,
                        self.tags[self.dictionary[char_id]['num']].__class__.__name__,
                        self.dictionary[char_id]['num'])

# ========

if __name__ == "__main__":
    swf_object = Swf(sys.argv[1])
    swf_object.display_header()
    #swf_object.display_tags()
    swf_object.display_dictionary()
    #swf_object.included_tags()