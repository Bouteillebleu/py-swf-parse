# "D:/Coding/sim_original_test.swf"
# First go - using http://the-labs.com/MacromediaFlash/SWF-Spec/SWFfileformat.html as guide.
import struct
import tag_parsers

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
        print " == Reading tag",tag_number,"== "
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
        tag_parser = get_tag_parser_from_number(tag_type)
        tag_parser(file.read(tag_length)) # Call an appropriate function to 
        
def get_tag_type_name_from_number(number):
    tags = {0:  "End",
            1:  "ShowFrame",
            2:  "DefineShape",
            4:  "PlaceObject",
            5:  "RemoveObject",
            6:  "DefineBits",
            7:  "DefineButton",
            8:  "JPEGTables",
            9:  "SetBackgroundColor",
            10: "DefineFont",
            11: "DefineText",
            12: "DoAction",
            13: "DefineFontInfo",
            14: "DefineSound",
            15: "StartSound",
            17: "DefineButtonSound",
            18: "SoundStreamHead",
            19: "SoundStreamBlock",
            20: "DefineBitsLossless",
            21: "DefineBitsJPEG2",
            22: "DefineShape2",
            23: "DefineButtonCxform",
            24: "Protect",
            26: "PlaceObject2",
            28: "RemoveObject2",
            32: "DefineShape3",
            33: "DefineText2",
            34: "DefineButton2",
            35: "DefineBitsJPEG3",
            36: "DefineBitsLossless2",
            37: "DefineEditText",
            39: "DefineSprite",
            43: "FrameLabel",
            45: "SoundStreamHead2",
            46: "DefineMorphShape",
            48: "DefineFont2",
            56: "ExportAssets",
            57: "ImportAssets",
            58: "EnableDebugger",
            59: "DoInitAction",
            60: "DefineVideoStream",
            61: "VideoFrame",
            62: "DefineFontInfo2",
            64: "EnableDebugger2"}
    # 65: "ScriptLimits",
    # 66: "SetTabIndex",
    # 69: "FileAttributes",
    # 70: "PlaceObject3",
    # 71: "ImportAssets2",
    # 73: "DefineFontAlignZones",
    # 74: "CSMTextSettings",
    # 75: "DefineFont3",
    # 76: "SymbolClass",
    # 77: "Metadata",
    # 78: "DefineScalingGrid",
    # 82: "DoABC",
    # 83: "DefineShape4",
    # 84: "DefineMorphShape2",
    # 86: "DefineSceneAndFrameLabelData",
    # 87: "DefineBinaryData",
    # 88: "DefineFontName",
    # 89: "StartSound2",
    # 90: "DefineBitJPEG4",
    # 91: "DefineFont4"
    # 73 is DefineFontAlignZones, allegedly v8 or later.
    # 74 is CSMTextSettings, also v8 or later.
    # 75 is DefineFont3, also also v8 or later. Weird.
    # Worth checking whether their descriptions in the v10 spec match the fields here.
    if number in tags:
        return tags[number]
    else:
        return ""        

def get_tag_parser_from_number(number):
    tag_functions = {9: tag_parsers.set_background_color}
    if number in tag_functions:
        return tag_functions[number]
    else:
        return tag_parsers.not_implemented



if __name__ == "__main__":
    main()