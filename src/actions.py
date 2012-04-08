'''
Created on 22 Oct 2011

@author: Bluebottle
'''

class ActionFactory(object):
    @staticmethod
    def new_action(stream,action_type,action_length):
        action_class = class_from_action_number(action_type)
        if action_class is not None:
            return action_class(stream,action_type,action_length)
        else:
            return Action(stream,action_type,action_length)

class Action(object):
    # Like Tag in tags.py, this isn't intended to be instantiated directly.
    # We have lots of subclasses that should be used instead.
    def __init__(self,stream,action_type,action_length):
        self.type = action_type
        self.length = action_length
        self.parser_implemented = True
        self.parse(stream)
    
    def parse(self,stream):
        # Like Tag, the default parser does nothing other than flag that
        # the parser isn't implemented. Subclasses implement this themselves.
        self.parser_implemented = False
    
    def display(self):
        if self.parser_implemented:
            print "  Display function not implemented."
        else:
            print "  Parser not implemented."

# ==== Individual actions ====

class ActionNextFrame(Action):
    pass

class ActionPreviousFrame(Action):
    pass

class ActionPlay(Action):
    pass

class ActionStop(Action):
    pass

class ActionToggleQuality(Action):
    pass

class ActionStopSounds(Action):
    pass

class ActionAdd(Action):
    pass

class ActionSubtract(Action):
    pass

class ActionMultiply(Action):
    pass

class ActionDivide(Action):
    pass

class ActionEquals(Action):
    pass

class ActionLess(Action):
    pass

class ActionAnd(Action):
    pass

class ActionOr(Action):
    pass

class ActionNot(Action):
    pass

class ActionStringEquals(Action):
    pass

class ActionStringLength(Action):
    pass

class ActionStringExtract(Action):
    pass

class ActionPop(Action):
    pass

class ActionToInteger(Action):
    pass

class ActionGetVariable(Action):
    pass

class ActionSetVariable(Action):
    pass

class ActionSetTarget2(Action):
    pass

class ActionStringAdd(Action):
    pass

class ActionGetProperty(Action):
    pass

class ActionSetProperty(Action):
    pass

class ActionCloneSprite(Action):
    pass

class ActionRemoveSprite(Action):
    pass

class ActionTrace(Action):
    pass

class ActionStartDrag(Action):
    pass

class ActionEndDrag(Action):
    pass

class ActionStringLess(Action):
    pass

class ActionThrow(Action):
    pass

class ActionCastOp(Action):
    pass

class ActionImplementsOp(Action):
    pass

class ActionRandomNumber(Action):
    pass

class ActionMBStringLength(Action):
    pass

class ActionCharToAscii(Action):
    pass

class ActionAsciiToChar(Action):
    pass

class ActionGetTime(Action):
    pass

class ActionMBStringExtract(Action):
    pass

class ActionMBCharToAscii(Action):
    pass

class ActionMBAsciiToChar(Action):
    pass

class ActionDelete(Action):
    pass

class ActionDelete2(Action):
    pass

class ActionDefineLocal(Action):
    pass

class ActionCallFunction(Action):
    pass

class ActionReturn(Action):
    pass

class ActionModulo(Action):
    pass

class ActionNewObject(Action):
    pass

class ActionDefineLocal2(Action):
    pass

class ActionInitArray(Action):
    pass

class ActionInitObject(Action):
    pass

class ActionTypeOf(Action):
    pass

class ActionTargetPath(Action):
    pass

class ActionEnumerate(Action):
    pass

class ActionAdd2(Action):
    pass

class ActionLess2(Action):
    pass

class ActionEquals2(Action):
    pass

class ActionToNumber(Action):
    pass

class ActionToString(Action):
    pass

class ActionPushDuplicate(Action):
    pass

class ActionStackSwap(Action):
    pass

class ActionGetMember(Action):
    pass

class ActionSetMember(Action):
    pass

class ActionIncrement(Action):
    pass

class ActionDecrement(Action):
    pass

class ActionCallMethod(Action):
    pass

class ActionNewMethod(Action):
    pass

class ActionInstanceOf(Action):
    pass

class ActionEnumerate2(Action):
    pass

class ActionBitAnd(Action):
    pass

class ActionBitOr(Action):
    pass

class ActionBitXor(Action):
    pass

class ActionBitLShift(Action):
    pass

class ActionBitRShift(Action):
    pass

class ActionBitURShift(Action):
    pass

class ActionStrictEquals(Action):
    pass

class ActionGreater(Action):
    pass

class ActionStringGreater(Action):
    pass

class ActionExtends(Action):
    pass

class ActionGotoFrame(Action):
    pass

class ActionGetURL(Action):
    pass

class ActionStoreRegister(Action):
    pass

class ActionConstantPool(Action):
    pass

class ActionWaitForFrame(Action):
    pass

class ActionSetTarget(Action):
    pass

class ActionGoToLabel(Action):
    pass

class ActionWaitForFrame2(Action):
    pass

class ActionDefineFunction2(Action):
    pass

class ActionTry(Action):
    pass

class ActionWith(Action):
    pass

class ActionPush(Action):
    pass

class ActionJump(Action):
    pass

class ActionGetURL2(Action):
    pass

class ActionDefineFunction(Action):
    pass

class ActionIf(Action):
    pass

class ActionCall(Action):
    pass

class ActionGotoFrame2(Action):
    pass

# ==== Summary data for actions ====

action_data = { 0x04: {'class': ActionNextFrame },
                0x05: {'class': ActionPreviousFrame },
                0x06: {'class': ActionPlay },
                0x07: {'class': ActionStop },
                0x08: {'class': ActionToggleQuality },
                0x09: {'class': ActionStopSounds },
                0x0A: {'class': ActionAdd },
                0x0B: {'class': ActionSubtract },
                0x0C: {'class': ActionMultiply },
                0x0D: {'class': ActionDivide },
                0x0E: {'class': ActionEquals },
                0x0F: {'class': ActionLess },
                0x10: {'class': ActionAnd },
                0x11: {'class': ActionOr },
                0x12: {'class': ActionNot },
                0x13: {'class': ActionStringEquals },
                0x14: {'class': ActionStringLength },
                0x15: {'class': ActionStringExtract },
                0x17: {'class': ActionPop },
                0x18: {'class': ActionToInteger },
                0x1C: {'class': ActionGetVariable },
                0x1D: {'class': ActionSetVariable },
                0x20: {'class': ActionSetTarget2 },
                0x21: {'class': ActionStringAdd },
                0x22: {'class': ActionGetProperty },
                0x23: {'class': ActionSetProperty },
                0x24: {'class': ActionCloneSprite },
                0x25: {'class': ActionRemoveSprite },
                0x26: {'class': ActionTrace },
                0x27: {'class': ActionStartDrag },
                0x28: {'class': ActionEndDrag },
                0x29: {'class': ActionStringLess },
                0x2A: {'class': ActionThrow },
                0x2B: {'class': ActionCastOp },
                0x2C: {'class': ActionImplementsOp },
                0x30: {'class': ActionRandomNumber },
                0x31: {'class': ActionMBStringLength },
                0x32: {'class': ActionCharToAscii },
                0x33: {'class': ActionAsciiToChar },
                0x34: {'class': ActionGetTime },
                0x35: {'class': ActionMBStringExtract },
                0x36: {'class': ActionMBCharToAscii },
                0x37: {'class': ActionMBAsciiToChar },
                0x3A: {'class': ActionDelete },
                0x3B: {'class': ActionDelete2 },
                0x3C: {'class': ActionDefineLocal },
                0x3D: {'class': ActionCallFunction },
                0x3E: {'class': ActionReturn },
                0x3F: {'class': ActionModulo },
                0x40: {'class': ActionNewObject },
                0x41: {'class': ActionDefineLocal2 },
                0x42: {'class': ActionInitArray },
                0x43: {'class': ActionInitObject },
                0x44: {'class': ActionTypeOf },
                0x45: {'class': ActionTargetPath },
                0x46: {'class': ActionEnumerate },
                0x47: {'class': ActionAdd2 },
                0x48: {'class': ActionLess2 },
                0x49: {'class': ActionEquals2 },
                0x4A: {'class': ActionToNumber },
                0x4B: {'class': ActionToString },
                0x4C: {'class': ActionPushDuplicate },
                0x4D: {'class': ActionStackSwap },
                0x4E: {'class': ActionGetMember },
                0x4F: {'class': ActionSetMember },
                0x50: {'class': ActionIncrement },
                0x51: {'class': ActionDecrement },
                0x52: {'class': ActionCallMethod },
                0x53: {'class': ActionNewMethod },
                0x54: {'class': ActionInstanceOf },
                0x55: {'class': ActionEnumerate2 },
                0x60: {'class': ActionBitAnd },
                0x61: {'class': ActionBitOr },
                0x62: {'class': ActionBitXor },
                0x63: {'class': ActionBitLShift },
                0x64: {'class': ActionBitRShift },
                0x65: {'class': ActionBitURShift },
                0x66: {'class': ActionStrictEquals },
                0x67: {'class': ActionGreater },
                0x68: {'class': ActionStringGreater },
                0x69: {'class': ActionExtends },
                0x81: {'class': ActionGotoFrame }, # small t (yes, they differ)
                0x83: {'class': ActionGetURL },
                0x87: {'class': ActionStoreRegister },
                0x88: {'class': ActionConstantPool },
                0x8A: {'class': ActionWaitForFrame },
                0x8B: {'class': ActionSetTarget },
                0x8C: {'class': ActionGoToLabel }, # capital T (in the spec)
                0x8D: {'class': ActionWaitForFrame2 },
                0x8E: {'class': ActionDefineFunction2 },
                0x8F: {'class': ActionTry },
                0x94: {'class': ActionWith },
                0x96: {'class': ActionPush },
                0x99: {'class': ActionJump },
                0x9A: {'class': ActionGetURL2 },
                0x9B: {'class': ActionDefineFunction },
                0x9D: {'class': ActionIf },
                0x9E: {'class': ActionCall },
                0x9F: {'class': ActionGotoFrame2 }, # small t
              }

def class_from_action_number(number):
    if number in action_data:
        return action_data[number]['class']
    else:
        return None


# ==== Old-style action parsers ====

def goto_frame(stream):
    frame = stream.read('uintle:16')
    print "Go to frame:",frame

def get_url(stream):
    stream, url_string = datatypes.string(stream)
    print "URLString:",url_string
    stream, target_string = datatypes.string(stream)
    print "TargetString:",target_string

def constant_pool(stream):
    constant_count = stream.read('uintle:16')
    print "Total constants:",constant_count
    constants_so_far = 0
    while stream.pos < stream.len and constants_so_far < constant_count:
        stream, string_so_far = datatypes.string(stream)
        print "Constant",constants_so_far,"is:",string_so_far
        constants_so_far += 1

def wait_for_frame(stream):
    print "Frame",stream.read('uintle:16')
    print "SkipCount",stream.read('uintle:8')

def set_target(stream):
    stream, target_name = datatypes.string(stream)
    print "TargetName:",target_name

def wait_for_frame_2(stream):
    print "SkipCount",stream.read('uintle:8')

def goto_label(stream):
    stream, label = datatypes.string(stream)
    print "Label:",label

def action_with(stream):
    print "Size:",stream.read('uintle:16')

def push(stream):
    data_type = stream.read('uintle:8')
    if data_type == 0:
        stream, string_so_far = datatypes.string(stream)
        print "Pushed string:",string_so_far
    elif data_type == 1:
        float_pushed = stream.read('floatle:32')
        print "Pushed float:",float_pushed
    elif data_type == 4:
        register_number_pushed = stream.read('uintle:8')
        print "Pushed register number:",register_number_pushed
    elif data_type == 5:
        boolean_pushed = stream.read('uintle:8')
        print "Pushed boolean:",boolean_pushed
    elif data_type == 6:
        double_pushed = stream.read('floatle:64')
        print "Pushed double:",double_pushed
    elif data_type == 7:
        integer_pushed = stream.read('uintle:32')
        print "Pushed integer:",integer_pushed
    elif data_type == 8:
        constant_pushed = stream.read('uintle:8')
        print "Pushed constant:",constant_pushed
    elif data_type == 9:
        constant_pushed = stream.read('uintle:16')
        print "Pushed constant:",constant_pushed

def jump(stream):
    print "BranchOffset:",stream.read('intle:16')

def get_url_2(stream):
    print "SendVarsMethod:",stream.read('uintle:2')
    stream.read(4)
    print "LoadTargetFlag:",stream.read('bool')
    print "LoadVariablesFlag:",stream.read('bool')

def define_function(stream):
    stream, function_name = datatypes.string(stream)
    print "FunctionName:",function_name
    num_params = stream.read('uintle:16')
    for i in range(num_params):
        stream, current_param = datatypes.string(stream)
        print "Param",i+1,":",current_param
    print "CodeSize:",stream.read('uintle:16')
    # TODO: And then there's something involving the remaining code.

def define_function_2(stream):
    stream, function_name = datatypes.string(stream)
    print "FunctionName:",function_name
    num_params = stream.read('uintle:16')
    print "NumParams:",num_params
    print "RegisterCount:",stream.read('uintle:8')
    print "PreloadParentFlag:",stream.read('bool')
    print "PreloadRootFlag:",stream.read('bool')
    print "SuppressSuperFlag:",stream.read('bool')
    print "PreloadSuperFlag:",stream.read('bool')
    print "SuppressArgumentsFlag:",stream.read('bool')
    print "PreloadArgumentsFlag:",stream.read('bool')
    print "SuppressThisFlag:",stream.read('bool')
    print "PreloadThisFlag:",stream.read('bool')
    stream.pos += 7
    print "PreloadGlobalFlag:",stream.read('bool')
    stream.bytealign()
    for i in range(num_params):
        print "For parameter",i+1
        register = stream.read('uintle:8')
        print "Using register:",register
        stream, param_name = datatypes.string(stream)
        print "ParamName:",param_name
    # TODO: And then there's something involving the remaining code.

def action_try(stream):
    stream.pos += 5
    catch_in_register_flag = stream.read('bool')
    print "CatchInRegisterFlag:",catch_in_register_flag
    print "FinallyBlockFlag:",stream.read('bool')
    print "CatchBlockFlag:",stream.read('bool')
    print "TrySize:",stream.read('uintle:16')
    print "CatchSize:",stream.read('uintle:16')
    print "FinallySize:",stream.read('uintle:16')
    if catch_in_register_flag:
        print "CatchRegister:",stream.read('uintle:8')
    else:
        stream, catch_name = datatypes.string(stream)
        print "CatchName:",catch_name
    # TODO: And then there's the TryBody, CatchBody and FinallyBody.

def action_if(stream):
    print "BranchOffset:",stream.read('intle:16')

def goto_frame_2(stream):
    stream.read(6)
    scene_bias_flag = stream.read('bool')
    print "SceneBiasFlag:",scene_bias_flag
    print "PlayFlag:",stream.read('bool')
    if scene_bias_flag:
        print "SceneBias:",stream.read('uintle:16')

def not_implemented(data):
    print "No parser for this action yet."
    
