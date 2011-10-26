'''
Created on 20 Oct 2011

@author: Bluebottle
'''
import struct

def rgb_color_record(data):
    # Data should be 3 bytes long: R, G and B values, each read as UI8.
    r = struct.unpack('<B',data[0])[0]
    g = struct.unpack('<B',data[1])[0]
    b = struct.unpack('<B',data[2])[0]
    return r,g,b

def matrix(data):
    start_byte = struct.unpack('<B',data[0])[0]
    has_scale = (1 << 7) & start_byte
    if has_scale:
        n_scale = (start_byte >> 2) & 0x1F
    # Thoughts: could we have a UB-reader that took:
    # - current data, active byte as data[0]
    # - current bit to focus on (the last one processed is the previous one)
    # and returned:
    # - field as requested, in some appropriate form
    # - current data, active byte as data[0]
    # - current bit to focus on (as in input, the last one processed is the previous one)
    
    

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