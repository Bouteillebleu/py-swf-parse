'''
Created on 15 Oct 2011

@author: Bluebottle
'''
import struct
import action_parsers
from datatypes import record_header, rgb_color_record, matrix, get_action_type_name_from_number

def set_background_color(stream):
    # Data should be an RGB color record.
    rgb = rgb_color_record(stream)
    print "Background colour: RGB =",rgb

def do_action(stream):
    action_number = 0
    action_name = ''
    while action_name != 'ActionEndFlag':
        print "   == Reading action",action_number,"== "
        action_code = stream.read('uintle:8')
        if action_code >= 0x80:
            # If it's actually 63, we're using the long record header form instead.
            action_length = stream.read('uintle:16')
        else:
            action_length = None
        action_name = get_action_type_name_from_number(action_code)
        print "  Action type:",action_code,action_name
        action_number += 1
        if action_length:
            print "  Action length:",action_length,"bytes"
            action_parser = get_action_parser_from_number(action_code)
            action_parser(stream.read('bits:%d' % (action_length*8)))         
        
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

def place_object_2(stream):
    #flags = struct.unpack('<B',data[0])[0]
    flag_has_clip_actions = stream.read('bool') #(1 << 7) & flags
    flag_has_clip_depth = stream.read('bool') #(1 << 6) & flags
    flag_has_name = stream.read('bool') #(1 << 5) & flags
    flag_has_ratio = stream.read('bool') #(1 << 4) & flags
    flag_has_color_transform = stream.read('bool') #(1 << 3) & flags
    flag_has_matrix = stream.read('bool') #(1 << 2) & flags
    flag_has_character = stream.read('bool') #(1 << 1) & flags
    flag_move = stream.read('bool') #(1 << 0) & flags
    depth = stream.read('uintle:16') #struct.unpack('<H',data[1:3])[0]
    #remaining_data = data[3:]
    if flag_has_character:
        character_id = stream.read('uintle:16') #struct.unpack('<H',data[0:2])[0]
        print "CharacterID:",character_id
        #remaining_data = remaining_data[2:]
    if flag_has_matrix:
        stream = matrix(stream)
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

def define_sprite(stream):
    #print '%r' % data
    sprite_id = stream.read('uintle:16')
    frame_count = stream.read('uintle:16')
    print "Sprite ID:",sprite_id
    print "Frame count:",frame_count
    print "Sprite contains tags:"
    tag_name = ''
    while stream.pos < stream.len and tag_name != 'End':
        current_pos = stream.pos
        tag_name, tag_length, is_long_header = record_header(stream)
        print tag_name,"- length",tag_length,"bytes"
        if is_long_header:
            stream.pos = current_pos + (tag_length*8) + 48
        else:
            stream.pos = current_pos + (tag_length*8) + 16
        
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