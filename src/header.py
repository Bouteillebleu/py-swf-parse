# "D:/Coding/sim_original_test.swf"
# First go - using http://the-labs.com/MacromediaFlash/SWF-Spec/SWFfileformat.html as guide.
import struct

def main():
    f = open("D:/Coding/sim_original_test.swf", "rb")
    try:
#        signature = f.read(3)
#        if signature == 'FWS':
#            print "SWF file"
#        version = int(f.read(1))
#        print "Version: %d" % version
#        size = int(f.read(8))
#        print "Size: %d bytes" % size
#        # ====
#        byte = f.read(1)
#        count_so_far = 0
#        while byte != "" and count_so_far < 20:
#            byte = f.read(1)
#            print byte
#            count_so_far += 1
        print f.read(3)
        print "Version:",struct.unpack('B',f.read(1))[0]
        print "Size:",struct.unpack('L',f.read(4))[0],"bytes"
        #print "oh god what is this:",struct.unpack('B',f.read(1))[0]
        f = read_rect(f)
        print "Frame rate:",struct.unpack('B',f.read(1))[0],".",struct.unpack('B',f.read(1))[0]
        print "Frame count:",struct.unpack('H',f.read(2))[0]
        read_tag_headers(f)
    finally:
        f.close()

def read_rect(file):
    # Read the Nbits field - the first 5 bits - to find the size of the next ones.
    rect_start = struct.unpack('B',file.read(1))[0]
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
    while tag_type_name != 'End':
        print "Reading tag",tag_number
        header = struct.unpack('H',file.read(2))[0]
        tag_type = header >> 6 # Ignore the bottom 6 bits
        tag_length = header & 0x3F # Only keep the bottom 6 bits
        if tag_length == 0x3f:
            # If it's actually 63, we're using the long record header form instead.
            tag_length = struct.unpack('L',file.read(4))[0]
        tag_type_name = get_tag_type_name_from_number(tag_type)
        print "Tag type:",tag_type,tag_type_name
        print "Tag length:",tag_length,"bytes"
        tag_number += 1
        file.read(tag_length) # Skip it for now.
        
def get_tag_type_name_from_number(number):
    tags = {4:  "PlaceObject",
            26: "PlaceObject2",
            5:  "RemoveObject",
            28: "RemoveObject2",
            1:  "ShowFrame",
            9:  "SetBackgroundColor",
            43: "FrameLabel",
            24: "Protect",
            0:  "End",
            56: "ExportAssets",
            57: "ImportAssets",
            58: "EnableDebugger",
            64: "EnableDebugger2",
            12: "DoAction",
            59: "DoInitAction",
            2:  "DefineShape",
            22: "DefineShape2",
            32: "DefineShape3",
            6:  "DefineBits",
            8:  "JPEGTables",
            21: "DefineBitsJPEG2",
            35: "DefineBitsJPEG3",
            20: "DefineBitsLossless",
            36: "DefineBitsLossless2",
            46: "DefineMorphShape",
            10: "DefineFont",
            13: "DefineFontInfo",
            62: "DefineFontInfo2",
            48: "DefineFont2",
            11: "DefineText",
            33: "DefineText2",
            37: "DefineEditText",
            14: "DefineSound",
            15: "StartSound",
            18: "SoundStreamHead",
            45: "SoundStreamHead2",
            19: "SoundStreamBlock",
            7:  "DefineButton",
            34: "DefineButton2",
            23: "DefineButtonCxform",
            17: "DefineButtonSound",
            39: "DefineSprite",
            60: "DefineVideoStream",
            61: "VideoFrame"}
    if number in tags:
        return tags[number]
    else:
        return ""        
        
if __name__ == "__main__":
    main()