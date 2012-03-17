'''
Created on 22 Oct 2011

@author: Bluebottle
'''

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
    # TIME TO BYTE ALIGN
    if stream.pos % 8 != 0:
        stream.pos = stream.pos + (8 - (stream.pos % 8))
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
    
