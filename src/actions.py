'''
Created on 22 Oct 2011

@author: Bluebottle
'''
import datatypes
from log import log

class ActionFactory(object):
    @staticmethod
    def new_action(stream,action_type,action_length):
        action_class = class_from_action_number(action_type)
        if action_class is not None:
            #print "  Creating new action: {0}, length {1}".format(action_class.__name__,action_length)
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
            log("Display function not implemented.")
        else:
            log("Parser not implemented.")

# ==== Individual actions ====

class ActionNextFrame(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionPreviousFrame(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionPlay(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionStop(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionToggleQuality(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionStopSounds(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionAdd(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionSubtract(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionMultiply(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionDivide(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionEquals(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionLess(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionAnd(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionOr(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionNot(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionStringEquals(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionStringLength(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionStringExtract(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionPop(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionToInteger(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionGetVariable(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionSetVariable(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionSetTarget2(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionStringAdd(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionGetProperty(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionSetProperty(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionCloneSprite(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionRemoveSprite(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionTrace(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionStartDrag(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionEndDrag(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionStringLess(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionThrow(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionCastOp(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionImplementsOp(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionRandomNumber(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionMBStringLength(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionCharToAscii(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionAsciiToChar(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionGetTime(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionMBStringExtract(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionMBCharToAscii(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionMBAsciiToChar(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionDelete(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionDelete2(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionDefineLocal(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionCallFunction(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionReturn(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionModulo(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionNewObject(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionDefineLocal2(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionInitArray(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionInitObject(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionTypeOf(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionTargetPath(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionEnumerate(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionAdd2(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionLess2(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionEquals2(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionToNumber(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionToString(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionPushDuplicate(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionStackSwap(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionGetMember(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionSetMember(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionIncrement(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionDecrement(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionCallMethod(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionNewMethod(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionInstanceOf(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionEnumerate2(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionBitAnd(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionBitOr(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionBitXor(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionBitLShift(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionBitRShift(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionBitURShift(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionStrictEquals(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionGreater(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionStringGreater(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionExtends(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionGotoFrame(Action):
    def parse(self,stream):
        self.frame = stream.read('uintle:16')
    
    def display(self):
        log("Frame: {s}".format(s=self.frame))

class ActionGetURL(Action):
    def parse(self,stream):
        self.url_string = datatypes.string(stream)
        self.target_string = datatypes.string(stream)
    
    def display(self):
        log("UrlString: {s}".format(s=self.url_string))
        log("TargetString: {s}".format(s=self.target_string))
        
class ActionStoreRegister(Action):
    def parse(self,stream):
        self.register_number = stream.read('uintle:8')
    
    def display(self):
        log("RegisterNumber: {s}".format(self.register_number))

class ActionConstantPool(Action):
    def parse(self,stream):
        self.count = stream.read('uintle:16')
        self.constant_pool = []
        for i in range(0,self.count):
            self.constant_pool.append(datatypes.string(stream))
    
    def display(self):
        log("Count: {s}".format(self.count))
        for i, item in enumerate(self.constant_pool):
            log("Constant {0}: {1}".format(i,item))

class ActionWaitForFrame(Action):
    def parse(self,stream):
        self.frame = stream.read('uintle:16')
        self.skip_count = stream.read('uintle:8')
    
    def display(self):
        log("Frame: {s}".format(s=self.frame))
        log("SkipCount: {s}".format(s=self.skip_count))

class ActionSetTarget(Action):
    def parse(self,stream):
        self.target_name = datatypes.string(stream)
    
    def display(self):
        log("TargetName: {s}".format(s=self.target_name))

class ActionGoToLabel(Action):
    def parse(self,stream):
        self.label = datatypes.string(stream)
    
    def display(self):
        log("Label: {s}".format(s=self.label))

class ActionWaitForFrame2(Action):
    def parse(self,stream):
        self.skip_count = stream.read('uintle:8')
    
    def display(self):
        log("SkipCount: {s}".format(s=self.skip_count))

class ActionDefineFunction2(Action):
    def parse(self,stream):
        self.function_name = datatypes.string(stream)
        self.num_params = stream.read('uintle:16')
        self.register_count = stream.read('uintle:8')
        self.preload_parent_flag = stream.read('bool')
        self.preload_root_flag = stream.read('bool')
        self.suppress_super_flag = stream.read('bool')
        self.preload_super_flag = stream.read('bool')
        self.suppress_arguments_flag = stream.read('bool')
        self.preload_arguments_flag = stream.read('bool')
        self.suppress_this_flag = stream.read('bool')
        self.preload_this_flag = stream.read('bool')
        stream.pos += 7
        self.preload_global_flag = stream.read('bool')
        self.parameters = []
        for i in range(0,self.num_params):
            self.parameters.append({'register': stream.read('uintle:8'),
                                    'param_name': datatypes.string(stream)
                                    })
        self.code_size = stream.read('uintle:16')
        initial_bytepos = stream.bytepos
        self.actions = []
        while stream.pos < stream.len and stream.bytepos < initial_bytepos + self.code_size:
            action_code = stream.read('uintle:8')
            action_length = 0
            if action_code > 0x7F:
                action_length = stream.read('uintle:16')
            action_stream = stream.read('bits:{0}'.format(action_length*8))
            self.actions.append(ActionFactory.new_action(action_stream,
                                                         action_code,
                                                         action_length))    

    
    def display(self):
        log("FunctionName: {s}".format(s=self.function_name))
        log("NumParams: {s}".format(s=self.num_params))
        log("RegisterCount: {s}".format(s=self.register_count))
        log("PreloadParentFlag: {s}".format(s=self.preload_parent_flag))
        log("PreloadRootFlag: {s}".format(s=self.preload_root_flag))
        log("SuppressSuperFlag: {s}".format(s=self.suppress_super_flag))
        log("PreloadSuperFlag: {s}".format(s=self.preload_super_flag))
        log("SuppressArgumentsFlag: {s}".format(s=self.suppress_arguments_flag))
        log("PreloadArgumentsFlag: {s}".format(s=self.preload_arguments_flag))
        log("SuppressThisFlag: {s}".format(s=self.suppress_this_flag))
        log("PreloadThisFlag: {s}".format(s=self.preload_this_flag))
        log("PreloadGlobalFlag: {s}".format(s=self.preload_global_flag))
        log("Parameters are:")
        for p, param in self.parameters:
            log("  Param {0}: Register {1}, ParamName {2}".format(p,param['register'],param['param_name']))
        log("CodeSize: {s}".format(s=self.code_size))
        log("Function code contains the following actions:")
        for a, action in enumerate(self.actions):
            log("  Action {0}: {1}".format(a,action.__class__.__name__))
            action.display()


class ActionTry(Action):
    def parse(self,stream):
        stream.pos += 5
        self.catch_in_register_flag = stream.read('bool')
        self.finally_block_flag = stream.read('bool')
        self.catch_block_flag = stream.read('bool')
        self.try_size = stream.read('uintle:16')
        self.catch_size = stream.read('uintle:16')
        self.finally_size = stream.read('uintle:16')
        if self.catch_in_register_flag == False:
            self.catch_name = datatypes.string(stream)
        else:
            self.catch_register = stream.read('uintle:8')
        # TryBody
        initial_bytepos = stream.bytepos
        self.try_body = []
        while stream.bytepos < initial_bytepos + self.try_size:
            action_code = stream.read('uintle:8')
            action_length = 0
            if action_code > 0x7F:
                action_length = stream.read('uintle:16')
            action_stream = stream.read('bits:{0}'.format(action_length*8))
            self.try_body.append(ActionFactory.new_action(action_stream,
                                                          action_code,
                                                          action_length))    
        # CatchBody
        initial_bytepos = stream.bytepos
        self.catch_body = []
        while stream.bytepos < initial_bytepos + self.catch_size:
            action_code = stream.read('uintle:8')
            action_length = 0
            if action_code > 0x7F:
                action_length = stream.read('uintle:16')
            action_stream = stream.read('bits:{0}'.format(action_length*8))
            self.catch_body.append(ActionFactory.new_action(action_stream,
                                                            action_code,
                                                            action_length))    

        # FinallyBody
        initial_bytepos = stream.bytepos
        self.finally_body = []
        while stream.bytepos < initial_bytepos + self.finally_size:
            action_code = stream.read('uintle:8')
            action_length = 0
            if action_code > 0x7F:
                action_length = stream.read('uintle:16')
            action_stream = stream.read('bits:{0}'.format(action_length*8))
            self.finally_body.append(ActionFactory.new_action(action_stream,
                                                              action_code,
                                                            action_length))    
            
        
                    
    def display(self):
        log("CatchInRegisterFlag: {s}".format(s=self.catch_in_register_flag))
        log("FinallyBlockFlag: {s}".format(s=self.finally_block_flag))
        log("CatchBlockFlag: {s}".format(s=self.catch_block_flag))
        log("TrySize: {s}".format(s=self.try_size))
        log("CatchSize: {s}".format(s=self.catch_size))
        log("FinallySize: {s}".format(s=self.finally_size))
        if self.catch_in_register_flag == False:
            log("CatchName: {s}".format(s=self.catch_name))
        else:
            log("CatchRegister: {s}".format(s=self.catch_register))
        log("Try block contains the following actions:")
        for a, action in enumerate(self.try_body):
            log("Action {0}: {1}".format(a,action.__class__.__name__))
            action.display()
        log("Catch block contains the following actions:")
        for a, action in enumerate(self.catch_body):
            log("Action {0}: {1}".format(a,action.__class__.__name__))
            action.display()
        log("Finally block contains the following actions:")
        for a, action in enumerate(self.finally_body):
            log("Action {0}: {1}".format(a,action.__class__.__name__))
            action.display()



class ActionWith(Action):
    def parse(self,stream):
        self.size = stream.read('uintle:16')
        initial_bytepos = stream.bytepos
        self.actions = []
        while stream.bytepos < initial_bytepos + self.code_size:
            action_code = stream.read('uintle:8')
            action_length = 0
            if action_code > 0x7F:
                action_length = stream.read('uintle:16')
            action_stream = stream.read('bits:{0}'.format(action_length*8))
            self.actions.append(ActionFactory.new_action(action_stream,
                                                         action_code,
                                                         action_length))    
    
    def display(self):
        log("Size: {s}".format(s=self.code_size))
        log("With block contains the following actions:")
        for a, action in enumerate(self.actions):
            log("Action {0}: {1}".format(a,action.__class__.__name__))
            action.display()

class ActionPush(Action):
    def parse(self,stream):
        self.type = stream.read('uintle:8')
        if self.type == 0:
            self.string = datatypes.string(stream)
        elif self.type == 1:
            self.float = stream.read('floatle:32')
        elif self.type == 4:
            self.register_number = stream.read('uintle:8')
        elif self.type == 5:
            self.boolean = stream.read('uintle:8')
        elif self.type == 6:
            self.double = stream.read('floatle:64')
        elif self.type == 7:
            self.integer = stream.read('uintle:32')
        elif self.type == 8:
            self.constant_8 = stream.read('uintle:8')
        elif self.type == 9:
            self.constant_16 = stream.read('uintle:16')
    
    def display(self):
        log("Type: {s}".format(s=self.type))
        if self.type == 0:
            log("String: {s}".format(s=self.string))
        elif self.type == 1:
            log("Float: {s}".format(s=self.float))
        elif self.type == 4:
            log("RegisterNumber: {s}".format(s=self.register_number))
        elif self.type == 5:
            log("Boolean: {s}".format(s=self.boolean))
        elif self.type == 6:
            log("Double: {s}".format(s=self.double))
        elif self.type == 7:
            log("Integer: {s}".format(s=self.integer))
        elif self.type == 8:
            log("Constant8: {s}".format(s=self.constant_8))
        elif self.type == 9:
            log("Constant16: {s}".format(s=self.constant_16))

class ActionJump(Action):
    def parse(self,stream):
        self.branch_offset = stream.read('intle:16')
    
    def display(self):
        log("BranchOffset: {s}".format(s=self.branch_offset))

class ActionGetURL2(Action):
    def parse(self,stream):
        self.send_vars_method = stream.read('uint:2')
        stream.pos += 4
        self.load_target_flag = stream.read('bool')
        self.load_variables_flag = stream.read('bool')
    
    def display(self):
        log("SendVarsMethod: {s}".format(s=self.send_vars_method))
        log("LoadTargetFlag: {s}".format(s=self.load_target_flag))
        log("LoadVariablesFlag: {s}".format(s=self.load_variables_flag))

class ActionDefineFunction(Action):
    def parse(self,stream):
        self.function_name = datatypes.string(stream)
        self.num_params = stream.read('uintle:16')
        self.params = []
        for i in range(0,self.num_params):
            self.params.append(datatypes.string(stream))
        self.code_size = stream.read('uintle:16')
        initial_bytepos = stream.bytepos
        self.actions = []
        while stream.pos < stream.len and stream.bytepos < initial_bytepos + self.code_size:
            action_code = stream.read('uintle:8')
            action_length = 0
            if action_code > 0x7F:
                action_length = stream.read('uintle:16')
            action_stream = stream.read('bits:{0}'.format(action_length*8))
            self.actions.append(ActionFactory.new_action(action_stream,
                                                         action_code,
                                                         action_length))    
            
    def display(self):
        log("FunctionName: {s}".format(s=self.function_name))
        log("NumParams: {s}".format(s=self.num_params))
        for p, param in enumerate(self.params):
            log("Param {0}: {1}".format(p,param))
        log("CodeSize: {s}".format(s=self.code_size))
        log("Function code contains the following actions:")
        for a, action in enumerate(self.actions):
            log("Action {0}: {1}".format(a,action.__class__.__name__))
            action.display()

class ActionIf(Action):
    def parse(self,stream):
        self.branch_offset = stream.read('intle:16')
    
    def display(self):
        log("BranchOffset: {s}".format(s=self.branch_offset))

class ActionCall(Action):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class ActionGotoFrame2(Action):
    def parse(self,stream):
        stream.pos += 6
        self.scene_bias_flag = stream.read('bool')
        self.play_flag = stream.read('bool')
        if self.scene_bias_flag:
            self.scene_bias = stream.read('uintle:16')
    
    def display(self):
        log("SceneBiasFlag: {s}".format(s=self.scene_bias_flag))
        log("PlayFlag: {s}".format(s=self.play_flag))
        if self.scene_bias_flag:
            log("SceneBias: {s}".format(s=self.scene_bias))

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
