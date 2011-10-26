'''
Created on 15 Oct 2011

@author: Bluebottle
'''
import struct
import action_parsers
from datatypes import record_header, rgb_color_record, get_action_type_name_from_number

def set_background_color(data):
    # Data should be an RGB color record.
    rgb = rgb_color_record(data)
    print "Background colour: RGB =",rgb

def do_action(data):
    action_number = 0
    action_name = ''
    remaining_data = data
    print "DEBUG: len(data) is",len(remaining_data)
    while action_name != 'ActionEndFlag':
        print "   == Reading action",action_number,"== "
        action_code = struct.unpack('<B',remaining_data[0])[0]
        if action_code >= 0x80:
            # If it's actually 63, we're using the long record header form instead.
            action_length = struct.unpack('<H',remaining_data[1:3])[0]
            remaining_data = remaining_data[3:]
        else:
            action_length = None
            remaining_data = remaining_data[1:]
        action_name = get_action_type_name_from_number(action_code)
        print "  Action type:",action_code,action_name
        action_number += 1
        if action_length:
            print "  Action length:",action_length,"bytes"
            action_parser = get_action_parser_from_number(action_code)
            action_parser(remaining_data[0:action_length])
            remaining_data = remaining_data[action_length:]
         
        
def define_bits_jpeg_2(data):
    character_id = struct.unpack('<H',data[0:2])[0]
    print "Character ID:",character_id
    filename = "%d.jpeg" % character_id
    try:
        f = open(filename,'wb')
        remaining_data = data[2:]
        while len(remaining_data) > 0:
            #print repr(remaining_data[0:4])
            #chunk = struct.pack('<c',remaining_data[0])
            f.write(remaining_data[0])
            remaining_data = remaining_data[1:]
        #else:
        #    format_string = "<" + ("c" * len(remaining_data))
        #    chunk = struct.pack(format_string,*(b for b in remaining_data))
        #    f.write(chunk)
    finally:
        f.close()
        print "Wrote JPEG data to",filename

def place_object_2(data):
    flags = struct.unpack('<B',data[0])[0]
    flag_has_clip_actions = (1 << 7) & flags
    flag_has_clip_depth = (1 << 6) & flags
    flag_has_name = (1 << 5) & flags
    flag_has_ratio = (1 << 4) & flags
    flag_has_color_transform = (1 << 3) & flags
    flag_has_matrix = (1 << 2) & flags
    flag_has_character = (1 << 1) & flags
    flag_move = (1 << 0) & flags
    depth = struct.unpack('<H',data[1:3])[0]
    remaining_data = data[3:]
    if flag_has_character:
        character_id = struct.unpack('<H',data[0:2])[0]
        print "CharacterID:",character_id
        remaining_data = remaining_data[2:]
    if flag_has_matrix:
        pass
    if flag_has_color_transform:
        pass
    if flag_has_ratio:
        pass
    if flag_has_name:
        pass
    if flag_has_clip_depth:
        pass
    if flag_has_clip_actions:
        pass

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
    
# == The list of action parser functions ==

def get_action_parser_from_number(number):
    action_functions = {0x81: action_parsers.goto_frame,
                        0x88: action_parsers.constant_pool,
                        0x96: action_parsers.push,
                        }
    if number in action_functions:
        return action_functions[number]
    else:
        return action_parsers.not_implemented