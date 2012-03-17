'''
Created on 20 Oct 2011

@author: Bluebottle
'''

def rgb_color_record(stream):
    # Data should be 3 bytes long: R, G and B values, each read as UI8.
    r = stream.read('uintle:8')
    g = stream.read('uintle:8')
    b = stream.read('uintle:8')
    return r,g,b

def rgba_color_record(stream):
    r = stream.read('uintle:8')
    g = stream.read('uintle:8')
    b = stream.read('uintle:8')
    a = stream.read('uintle:8')
    return r,g,b,a

def fixed_8(stream):
    low = stream.read('uintle:8')
    high = stream.read('uintle:8')
    return high,low

def fixed(stream):
    low = stream.read('uintle:16')
    high = stream.read('uintle:16')
    return high,low

def string(stream):
    new_string = ''
    while stream.peek('uintle:8') != 0:
        new_string += stream.read('bytes:1')
    stream.bytepos += 1 # Ignore the final 0 in the string.
    return stream, new_string

def rect(stream):
    # Read the Nbits field - the first 5 bits - to find the size of the next ones.
    nbits = stream.read('uint:5')
    print "nBits:",nbits
    nbits_format = 'int:%d' % nbits
    print "Xmin:",stream.read(nbits_format)
    print "Xmax:",stream.read(nbits_format)
    print "Ymin:",stream.read(nbits_format)
    print "Ymax:",stream.read(nbits_format)
    # Wherever we are now, we need to skip ahead to the next byte boundary.
    if stream.pos % 8 != 0:
        stream.pos = stream.pos + (8 - (stream.pos % 8))
    return stream

def matrix(stream):
    has_scale = stream.read('bool') #(1 << 7) & start_byte
    if has_scale:
        n_scale = stream.read('uint:5') #(start_byte >> 2) & 0x1F
        print "nScaleBits:",n_scale
        scale_format = 'uint:%d' % n_scale
        print "ScaleX:",stream.read(scale_format) # Not strictly a uint
        print "ScaleY:",stream.read(scale_format) # they're actually 16.16 fixed-point
    has_rotate = stream.read('bool')
    if has_rotate:
        n_rotate_bits = stream.read('uint:5')
        print "nRotateBits:",n_rotate_bits
        rotate_format = 'uint:%d' % n_rotate_bits
        print "RotateSkew0:",stream.read(rotate_format) # as are these - so I'll have to sort
        print "RotateSkew1:",stream.read(rotate_format) # the fixed-point stuff out later.
    n_translate_bits = stream.read('uint:5')
    print "nTranslateBits:",n_translate_bits
    if n_translate_bits > 0:
        translate_format = 'int:%d' % n_translate_bits
        print "TranslateX:",stream.read(translate_format) # Basically I need to write my own thing
        print "TranslateY:",stream.read(translate_format) # to turn however-many-bits into fixed-point.
    # BYTE ALIIIIIIGN
    if stream.pos % 8 != 0:
        stream.pos = stream.pos + (8 - (stream.pos % 8))
    return stream

def cxform(stream):
    has_add_terms = stream.read('bool')
    has_mult_terms = stream.read('bool')
    n_bits = stream.read('uint:4')
    n_bits_format = 'int:%d' % n_bits
    if has_mult_terms:
        print "RedMultTerm:",stream.read(n_bits_format)
        print "GreenMultTerm:",stream.read(n_bits_format)
        print "BlueMultTerm:",stream.read(n_bits_format)
    if has_add_terms:
        print "RedAddTerm:",stream.read(n_bits_format)
        print "GreenAddTerm:",stream.read(n_bits_format)
        print "BlueAddTerm:",stream.read(n_bits_format)
    return stream
    # BYTE ALIGN THIS THING
    # TODO: Turn this into its own function because it is that useful.
    if stream.pos % 8 != 0:
        stream.pos = stream.pos + (8 - (stream.pos % 8))
    return stream

def cxform_with_alpha(stream):
    has_add_terms = stream.read('bool')
    has_mult_terms = stream.read('bool')
    n_bits = stream.read('uint:4')
    n_bits_format = 'int:%d' % n_bits
    if has_mult_terms:
        print "RedMultTerm:",stream.read(n_bits_format)
        print "GreenMultTerm:",stream.read(n_bits_format)
        print "BlueMultTerm:",stream.read(n_bits_format)
        print "AlphaMultTerm:",stream.read(n_bits_format)
    if has_add_terms:
        print "RedAddTerm:",stream.read(n_bits_format)
        print "GreenAddTerm:",stream.read(n_bits_format)
        print "BlueAddTerm:",stream.read(n_bits_format)
        print "AlphaAddTerm:",stream.read(n_bits_format)
    return stream
    # BYTE ALIGN THIS THING
    # TODO: Turn this into its own function because it is that useful.
    if stream.pos % 8 != 0:
        stream.pos = stream.pos + (8 - (stream.pos % 8))
    return stream

def gradient(stream,calling_tag):
    print "SpreadMode",stream.read('uint:2')
    print "InterpolationMode",stream.read('uint:2')
    num_gradients = stream.read('uint:4')
    print "NumGradients:",num_gradients
    for n in range(0,num_gradients):
        print "GradientRecords[%d]" % (n+1)
        print "Ratio:",stream.read('uintle:8')
        print "Color:"
        if calling_tag == "DefineShape" or calling_tag == "DefineShape2":
            print "(%d,%d,%d)" % rgb_color_record(stream)
        else:
            print "(%d,%d,%d,%d)" % rgba_color_record(stream)
    return stream

def focal_gradient(stream,calling_tag):
    stream = gradient(stream,calling_tag)
    print "FocalPoint: %d.%d" % fixed_8(stream)
    return stream

def shape(stream,calling_tag):
    num_fill_bits = stream.read('uint:4')
    print "NumFillBits:",num_fill_bits
    num_line_bits = stream.read('uint:4')
    print "NumLineBits:",num_line_bits
    # Now shaperecords.
    record_type = ''
    while record_type != 'EndShapeRecord':
        type_flag = stream.read('uint:1')
        if type_flag == 0:
            if stream.peek('uint:5') == 0:
                record_type = 'EndShapeRecord'
            else:
                record_type = 'StyleChangeRecord'
                print "RecordType: StyleChangeRecord"
                num_fill_bits,num_line_bits = style_change_record(stream,calling_tag,num_fill_bits,num_line_bits)
        else:
            straight_flag = stream.read('uint:1')
            if straight_flag == 0:
                record_type = 'CurvedEdgeRecord'
                curved_edge_record(stream)
            else:
                record_type = 'StraightEdgeRecord'
                straight_edge_record(stream)
        #print "RecordType:",record_type
        # EndShapeRecord: type_flag = 0, next 5 bits all 0
        # StyleChangeRecord: type_flag = 0, at least one of next 5 bits 1.
        # StraightEdgeRecord: type_flag = 1, next bit = 1
        # CurvedEdgeRecord: type_flat = 1, next bit = 0.

def shape_with_style(stream,calling_tag):
    stream = fill_style_array(stream,calling_tag)
    stream = line_style_array(stream,calling_tag)
    shape(stream,calling_tag)

def fill_style_array(stream,calling_tag):
    # Fill style array!
    fill_style_count = stream.read('uintle:8')
    print "FillStyleCount:",fill_style_count
    if fill_style_count == 0xff:
        fill_style_count = stream.read('uintle:16')
        print "FillStyleCountExtended:",fill_style_count
    # And the individual FillStyles!
    for n in range(0,fill_style_count):
        print "FillStyle[%d]" % (n+1)
        fill_style(stream,calling_tag)
    return stream

def fill_style(stream,calling_tag):
    fill_style_type = stream.read("uintle:8")
    print "FillStyleType",fill_style_type
    if fill_style_type == 0x00:
        print "Color:"
        if calling_tag == "DefineShape" or calling_tag == "DefineShape2":
            print "(%d,%d,%d)" % rgb_color_record(stream)
        else:
            print "(%d,%d,%d,%d)" % rgba_color_record(stream)
    if fill_style_type in (0x10,0x12,0x13):
        print "GradientMatrix:"
        stream = matrix(stream)
        print "Gradient:"
        if fill_style_type == 0x13:
            stream = focal_gradient(stream,calling_tag)
        else:
            stream = gradient(stream,calling_tag)
    if fill_style_type in (0x40,0x41,0x42,0x43):
        print "BitmapId:",stream.read("uintle:16")
        print "BitmapMatrix:"
        stream = matrix(stream)

def line_style_array(stream,calling_tag):
    # Line style array!
    line_style_count = stream.read('uintle:8')
    print "LineStyleCount:",line_style_count
    if line_style_count == 0xff:
        line_style_count = stream.read('uintle:16')
        print "LineStyleCountExtended:",line_style_count
    for n in range(0,line_style_count):
        if calling_tag in ("DefineShape","DefineShape2","DefineShape3"):
            # LineStyle!
            print "LineStyle[%d]" % (n+1)
            print "Width:",stream.read('uintle:16')
            print "Color:"
            if calling_tag == "DefineShape" or calling_tag == "DefineShape2":
                print "(%d,%d,%d)" % rgb_color_record(stream)
            else:
                print "(%d,%d,%d,%d)" % rgba_color_record(stream)
        elif calling_tag == "DefineShape4":
            #LineStyle2!
            print "LineStyle2[%d]" % (n+1)
            print "StartCapStyle:",stream.read('uintle:2')
            join_style = stream.read('uintle:2')
            print "JoinStyle:",join_style
            has_fill_flag = stream.read('bool')
            print "HasFillFlag:",has_fill_flag
            print "NoHScaleFlag:",stream.read('bool')
            print "NoVScaleFlag:",stream.read('bool')
            print "PixelHintingFlag:",stream.read('bool')
            stream.pos += 5
            print "NoClose:",stream.read('bool')
            print "EndCapStyle:",stream.read('uintle:2')
            if join_style == 2:
                miter_limit_factor = datatype.fixed_8(stream)
            if has_fill_flag:
                fill_style(stream,calling_tag)
            else:
                print "Color:"
                print "(%d,%d,%d,%d)" % rgba_color_record(stream)
    return stream

def style_change_record(stream,calling_tag,num_fill_bits,num_line_bits):
    #if calling_tag == "DefineShape2" or calling_tag == "DefineShape3":
    state_new_styles = stream.read('bool')
    print "StateNewStyles:",state_new_styles
    state_line_style = stream.read('bool')
    print "StateLineStyle:",state_line_style
    state_fill_style_1 = stream.read('bool')
    state_fill_style_0 = stream.read('bool')
    print "StateFillStyles - 0:",state_fill_style_0,", 1:",state_fill_style_1
    state_move_to = stream.read('bool')
    print "StateMoveTo:",state_move_to
    if state_move_to:
        move_bits = stream.read('uint:5')
        move_bits_format = 'int:%d' % move_bits
        move_delta_x = stream.read(move_bits_format)
        move_delta_y = stream.read(move_bits_format)
        print "MoveDelta:",(move_delta_x,move_delta_y)
    # TODO: Are we getting FillBits and LineBits from the original Shape parsing? (Yes.)
    if num_fill_bits > 0:
        fill_bits_format = 'uint:%d' % num_fill_bits
        if state_fill_style_0:
            print "FillStyle0:",stream.read(fill_bits_format)
        if state_fill_style_1:
            print "FillStyle1:",stream.read(fill_bits_format)
    line_bits_format = 'uint:%d' % num_line_bits
    if state_line_style and num_line_bits > 0:
        print "LineStyle:",stream.read(line_bits_format)
    # TIME TO BYTE ALIGN
    if stream.pos % 8 != 0:
        stream.pos = stream.pos + (8 - (stream.pos % 8))
    if state_new_styles: # and calling_tag != "DefineShape":
        stream = fill_style_array(stream,calling_tag)
        stream = line_style_array(stream,calling_tag)
        num_fill_bits = stream.read('uint:4')
        print "NumFillBits:",num_fill_bits
        num_line_bits = stream.read('uint:4')
        print "NumLineBits:",num_line_bits
    return num_fill_bits,num_line_bits

def straight_edge_record(stream):
    num_bits = stream.read('uint:4')
    print "NumBits:",num_bits
    num_bits_format = 'int:%d' % (num_bits+2)
    general_line_flag = stream.read('bool')
    if general_line_flag:
        print "DeltaX:",stream.read(num_bits_format)
        print "DeltaY:",stream.read(num_bits_format)
    else:
        vert_line_flag = stream.read('bool')
        if vert_line_flag:
            print "DeltaY:",stream.read(num_bits_format)
        else:
            print "DeltaX:",stream.read(num_bits_format)
    # NB: this is really badly documented in the specs.
    # I'm going by the worked example on page 266 of the v10 spec,
    # which is closer to what the comments for STRAIGHTEDGERECORD say
    # than what the value column actually says.

def curved_edge_record(stream):
    num_bits = stream.read('uint:4')
    num_bits_format = 'int:%d' % (num_bits+2)
    print "ControlDeltaX:",stream.read(num_bits_format)
    print "ControlDeltaY:",stream.read(num_bits_format)
    print "AnchorDeltaX:",stream.read(num_bits_format)
    print "AnchorDeltaY:",stream.read(num_bits_format)

def record_header(stream):
    header = stream.read('uintle:16')
    is_long_header = False
    tag_type = header >> 6 # Ignore the bottom 6 bits
    tag_length = header & 0x3F # Only keep the bottom 6 bits
    if tag_length == 0x3f:
        # If it's actually 63, we're using the long record header form instead.
        is_long_header = True
        tag_length = stream.read('intle:32')
    tag_type_name = get_tag_type_name_from_number(tag_type)
    return tag_type_name, tag_length, is_long_header

def get_tag_type_name_from_number(number):
    tags = {0:  "End",
            1:  "ShowFrame",
            2:  "DefineShape",
            4:  "PlaceObject",
            5:  "RemoveObject",
            6:  "DefineBits",
            7:  "DefineButton", # can contain actionrecords
            8:  "JPEGTables",
            9:  "SetBackgroundColor",
            10: "DefineFont",
            11: "DefineText",
            12: "DoAction", # can contain actionrecords
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
            26: "PlaceObject2", # Can contain actionrecords
            28: "RemoveObject2",
            32: "DefineShape3",
            33: "DefineText2",
            34: "DefineButton2", # can contain actionrecords
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
            64: "EnableDebugger2",
            65: "ScriptLimits",
            66: "SetTabIndex",
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
    }
    if number in tags:
        return tags[number]
    else:
        return str(number)

def get_action_type_name_from_number(number):
    actions = {0x00:'ActionEndFlag',
               0x04:'ActionNextFrame',
               0x05:'ActionPreviousFrame',
               0x06:'ActionPlay',
               0x07:'ActionStop',
               0x08:'ActionToggleQuality',
               0x09:'ActionStopSounds',
               0x0A:'ActionAdd',
               0x0B:'ActionSubtract',
               0x0C:'ActionMultiply',
               0x0D:'ActionDivide',
               0x0E:'ActionEquals',
               0x0F:'ActionLess',
               0x10:'ActionAnd',
               0x11:'ActionOr',
               0x12:'ActionNot',
               0x13:'ActionStringEquals',
               0x14:'ActionStringLength',
               0x15:'ActionStringExtract',
               0x17:'ActionPop',
               0x18:'ActionToInteger',
               0x1C:'ActionGetVariable',
               0x1D:'ActionSetVariable',
               0x20:'ActionSetTarget2',
               0x21:'ActionStringAdd',
               0x22:'ActionGetProperty',
               0x23:'ActionSetProperty',
               0x24:'ActionCloneSprite',
               0x25:'ActionRemoveSprite',
               0x26:'ActionTrace',
               0x27:'ActionStartDrag',
               0x28:'ActionEndDrag',
               0x29:'ActionStringLess',
               0x2A:'ActionThrow',
               0x2B:'ActionCastOp',
               0x2C:'ActionImplementsOp',
               0x30:'ActionRandomNumber',
               0x31:'ActionMBStringLength',
               0x32:'ActionCharToAscii',
               0x33:'ActionAsciiToChar',
               0x34:'ActionGetTime',
               0x35:'ActionMBStringExtract',
               0x36:'ActionMBCharToAscii',
               0x37:'ActionMBAsciiToChar',
               0x3A:'ActionDelete',
               0x3B:'ActionDelete2',
               0x3C:'ActionDefineLocal',
               0x3D:'ActionCallFunction',
               0x3E:'ActionReturn',
               0x3F:'ActionModulo',
               0x40:'ActionNewObject',
               0x41:'ActionDefineLocal2',
               0x42:'ActionInitArray',
               0x43:'ActionInitObject',
               0x44:'ActionTypeOf',
               0x45:'ActionTargetPath',
               0x46:'ActionEnumerate',
               0x47:'ActionAdd2',
               0x48:'ActionLess2',
               0x49:'ActionEquals2',
               0x4A:'ActionToNumber',
               0x4B:'ActionToString',
               0x4C:'ActionPushDuplicate',
               0x4D:'ActionStackSwap',
               0x4E:'ActionGetMember',
               0x4F:'ActionSetMember',
               0x50:'ActionIncrement',
               0x51:'ActionDecrement',
               0x52:'ActionCallMethod',
               0x53:'ActionNewMethod',
               0x54:'ActionInstanceOf',
               0x55:'ActionEnumerate2',
               0x60:'ActionBitAnd',
               0x61:'ActionBitOr',
               0x62:'ActionBitXor',
               0x63:'ActionbitLShift',
               0x64:'ActionBitRShift',
               0x65:'ActionBitURShift',
               0x66:'ActionStrictEquals',
               0x67:'ActionGreater',
               0x68:'ActionStringGreater',
               0x69:'ActionExtends',
               0x81:'ActionGotoFrame',
               0x83:'ActionGetURL',
               0x87:'ActionStoreRegister',
               0x88:'ActionConstantpool',
               0x8A:'ActionWaitForFrame',
               0x8B:'ActionSetTarget',
               0x8C:'ActionGoToLabel',
               0x8D:'ActionWaitForFrame2',
               0x8E:'ActionDefineFunction2',
               0x8F:'ActionTry',
               0x94:'ActionWith',
               0x96:'ActionPush',
               0x99:'ActionJump',
               0x9A:'ActionGetURL2',
               0x9B:'ActionDefineFunction',
               0x9D:'ActionIf',
               0x9E:'ActionCall',
               0x9F:'ActionGotoFrame2',         
               }
    # Bug in v6 spec: both ActionIf and ActionGetUrl2 are listed as 0x9A.
    # v10 spec has ActionIf as 0x9D, so I'm going with that.
    if number in actions:
        return actions[number]
    else:
        return ""
