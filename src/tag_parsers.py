'''
Created on 15 Oct 2011

@author: Bluebottle
'''
import struct

def set_background_color(data):
    # Data should be an RGB color record.
    rgb = rgb_color_record(data)
    print "Background colour: RGB =",rgb

def define_sprite(data):
    #print '%r' % data
    sprite_id = struct.unpack('<H',data[0:2])[0]
    frame_count = struct.unpack('<H',data[2:4])[0]
    print "Sprite ID:",sprite_id
    print "Frame count:",frame_count
    print "Sprite contains tags:"
    remaining_data = data[4:]
    tag_name = ''
    while len(remaining_data) > 0 and tag_name != 'End':
        tag_name, tag_length = record_header(remaining_data)
        print tag_name
        remaining_data = remaining_data[tag_length:] # Trim off the tag data so far.

def not_implemented(data):
    print "No parser for this tag yet."
    
# == Data type readers (to pull out into another module?) ==

def rgb_color_record(data):
    # Data should be 3 bytes long: R, G and B values, each read as UI8.
    r = struct.unpack('<B',data[0])[0]
    g = struct.unpack('<B',data[1])[0]
    b = struct.unpack('<B',data[2])[0]
    return r,g,b

def record_header(data):
    header = struct.unpack('<H',data[0:2])[0]
    tag_type = header >> 6 # Ignore the bottom 6 bits
    tag_length = header & 0x3F # Only keep the bottom 6 bits
    if tag_length == 0x3f:
        # If it's actually 63, we're using the long record header form instead.
        tag_length = struct.unpack('<L',data[0:4])[0]
        remaining_data = data[4:]
    else:
        remaining_data = data[2:]
    tag_type_name = get_tag_type_name_from_number(tag_type)
    return tag_type_name, len(remaining_data)

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