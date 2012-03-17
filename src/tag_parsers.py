'''
Created on 15 Oct 2011

@author: Bluebottle
'''
import os
import struct
import action_parsers
import datatypes

def define_shape(stream):
    print "ShapeId:",stream.read('uintle:16')
    print "ShapeBounds:"
    stream = datatypes.rect(stream)
    datatypes.shape_with_style(stream,"DefineShape")

def define_shape_2(stream):
    print "ShapeId:",stream.read('uintle:16')
    print "ShapeBounds:"
    stream = datatypes.rect(stream)
    #datatypes.shape_with_style(stream,"DefineShape2")
    
def remove_object(stream):
    print "CharacterId:",stream.read('uintle:16')
    print "Depth:",stream.read('uintle:16')

def remove_object_2(stream):
    print "Depth:",stream.read('uintle:16')

def set_background_color(stream):
    # Data should be an RGB color record.
    rgb = datatypes.rgb_color_record(stream)
    print "Background colour: RGB =",rgb

def define_text(stream):
    print "FontId:",stream.read('uintle:16')
    starting_bytepos = stream.bytepos
    n_glyphs = stream.peek('uintle:16') / 2
    for glyph_number in range(n_glyphs):
        stream.bytepos = starting_bytepos + (2 * glyph_number)
        glyph_offset = stream.read('uintle:16')
        stream.bytepos = starting_bytepos + glyph_offset
        datatypes.shape(stream,"DefineText")

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
        action_name = datatypes.get_action_type_name_from_number(action_code)
        print "  Action type:",action_code,action_name
        action_number += 1
        if action_length:
            print "  Action length:",action_length,"bytes"
            action_parser = get_action_parser_from_number(action_code)
            action_parser(stream.read('bits:%d' % (action_length*8)))         

def do_init_action(stream):
    print "SpriteID:",stream.read('uintle:16')
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
        action_name = datatypes.get_action_type_name_from_number(action_code)
        print "  Action type:",action_code,action_name
        action_number += 1
        if action_length:
            print "  Action length:",action_length,"bytes"
            action_parser = get_action_parser_from_number(action_code)
            action_parser(stream.read('bits:%d' % (action_length*8)))         
        
def define_bits_jpeg_2(stream):
    character_id = stream.read('uintle:16')
    print "Character ID:",character_id
    filename = "%d.jpeg" % character_id
    if stream.peek(32) == '0xffd9ffd8': # Some SWF versions before 8 erroneously have an extra JPEG EOI and SOI pair before the actual SOI.
        stream.read(32) # In that case, we just throw away the extra 4 bytes.
    try:
        f = open(os.path.join("../output",filename),'wb')
        while stream.pos < stream.len:
            f.write(struct.pack('b',stream.read('int:8')))
    finally:
        f.close()
        print "Wrote JPEG data to",filename

def place_object(stream):
    character_id = stream.read('uintle:16')
    print "CharacterID:",character_id
    depth = stream.read('uintle:16')
    print "Depth:",depth
    stream = datatypes.matrix(stream)
    stream = datatypes.cxform(stream)

def place_object_2(stream):
    flag_has_clip_actions = stream.read('bool')
    flag_has_clip_depth = stream.read('bool')
    flag_has_name = stream.read('bool')
    flag_has_ratio = stream.read('bool')
    flag_has_color_transform = stream.read('bool')
    flag_has_matrix = stream.read('bool')
    flag_has_character = stream.read('bool')
    flag_move = stream.read('bool')
    depth = stream.read('uintle:16')
    if flag_has_character:
        character_id = stream.read('uintle:16')
        print "CharacterID:",character_id
    if flag_has_matrix:
        stream = datatypes.matrix(stream)
    if flag_has_color_transform:
        stream = datatypes.cxform_with_alpha(stream)
    if flag_has_ratio:
        print "Ratio:",stream.read('uintle:16')
    if flag_has_name:
        name = ''
        while stream.peek('uintle:8') != 0:
            name += stream.read('bytes:1')
        stream.bytepos += 1 # Skip over the string's terminating 0-byte.
        print "Name:",name
    if flag_has_clip_depth:
        print "ClipDepth:",stream.read('uintle:16')
    if flag_has_clip_actions:
        pass

def define_edit_text(stream):
    character_id = stream.read('uintle:16')
    print "Character ID",character_id
    print "Bounds:"
    stream = datatypes.rect(stream)
    has_text = stream.read('bool')
    print "HasText:",has_text
    word_wrap = stream.read('bool')
    print "WordWrap:",word_wrap
    multiline = stream.read('bool')
    print "Multiline:",multiline
    password = stream.read('bool')
    print "Password:",password
    read_only = stream.read('bool')
    print "ReadOnly:",read_only
    has_text_color = stream.read('bool')
    print "HasTextColor:",has_text_color
    has_max_length = stream.read('bool')
    print "HasMaxLength:",has_max_length
    has_font = stream.read('bool')
    print "HasFont:",has_font
    has_font_class = stream.read('bool')
    print "HasFontClass:",has_font_class
    auto_size = stream.read('bool')
    print "AutoSize:",auto_size
    has_layout = stream.read('bool')
    print "HasLayout:",has_layout
    no_select = stream.read('bool')
    print "NoSelect:",no_select
    border = stream.read('bool')
    print "Border:",border
    was_static = stream.read('bool')
    print "WasStatic:",was_static
    html = stream.read('bool')
    print "HTML:",html
    use_outlines = stream.read('bool')
    print "UseOutlines:",use_outlines
    if has_font:
        print "FontID:",stream.read('uintle:16')
    if has_font_class:
        font_class = ''
        while stream.peek('uintle:8') != 0:
            font_class += stream.read('bytes:1')
        print "FontClass:",font_class
    if has_font:
        print "FontHeight:",stream.read('uintle:16')
    if has_text_color:
        rgba = datatypes.rgba_color_record(stream)
        print "TextColor:",rgba
    if has_max_length:
        print "MaxLength:",stream.read('uintle:16')
    if has_layout:
        print "Align:",stream.read('uintle:8')
        print "LeftMargin:",stream.read('uintle:16')
        print "RightMargin:",stream.read('uintle:16')
        print "Indent:",stream.read('uintle:16')
        print "Leading:",stream.read('intle:16')
    variable_name = ''
    while stream.peek('uintle:8') != 0:
        variable_name += stream.read('bytes:1')
    print "VariableName:",variable_name
    if has_text:
        initial_text = ''
        while stream.peek('uintle:8') != 0:
            initial_text += stream.read('bytes:1')
        print "InitialText:",initial_text

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
        tag_name, tag_length, is_long_header = datatypes.record_header(stream)
        print tag_name,"- length",tag_length,"bytes"
        if is_long_header:
            stream.pos = current_pos + (tag_length*8) + 48
        else:
            stream.pos = current_pos + (tag_length*8) + 16
        
def frame_label(stream):
    name = ''
    while stream.peek('uintle:8') != 0:
        name += stream.read('bytes:1')
    print "Name:",name

def script_limits(stream):
    print "MaxRecursionDepth:",stream.read('uintle:16')
    print "ScriptTimeoutSeconds:",stream.read('uintle:16')

def set_tab_index(stream):
    print "Depth:",stream.read('uintle:16')
    print "TabIndex:",stream.read('uintle:16')

def not_implemented(data):
    print "No parser for this tag yet."
    
# == The list of action parser functions ==

def get_action_parser_from_number(number):
    action_functions = {0x81: action_parsers.goto_frame,
                        0x83: action_parsers.get_url,
                        0x88: action_parsers.constant_pool,
                        0x8a: action_parsers.wait_for_frame,
                        0x8b: action_parsers.set_target,
                        0x8c: action_parsers.goto_label,
                        0x8d: action_parsers.wait_for_frame_2,
                        0x94: action_parsers.with,
                        0x96: action_parsers.push,
                        0x99: action_parsers.jump,
                        0x9a: action_parsers.get_url_2,
                        0x9b: action_parsers.define_function,
                        0x9d: action_parsers.if,
                        0x9f: action_parsers.goto_frame_2,
                        }
    if number in action_functions:
        return action_functions[number]
    else:
        return action_parsers.not_implemented

