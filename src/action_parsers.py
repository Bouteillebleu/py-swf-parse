'''
Created on 22 Oct 2011

@author: Bluebottle
'''

def goto_frame(stream):
    frame = stream.read('uintle:16')
    print "Go to frame:",frame

def get_url(stream):
    url_string = ''
    while stream.peek('uintle:8') != 0:
        url_string += stream.read('bytes:1')
    print "URLString:",url_string
    stream.bytepos += 1
    target_string = ''
    while stream.peek('uintle:8') != 0:
        target_string += stream.read('bytes:1')
    print "TargetString:",target_string
    stream.bytepos += 1

def constant_pool(stream):
    constant_count = stream.read('uintle:16')
    print "Total constants:",constant_count
    constants_so_far = 0
    while stream.pos < stream.len and constants_so_far < constant_count:
        string_so_far = ""
        while stream.peek('uintle:8') != 0:
            string_so_far += stream.read('bytes:1')
        print "Constant",constants_so_far,"is:",string_so_far
        constants_so_far += 1
        stream.bytepos += 1  #ignore the 0 at end of string.

def wait_for_frame(stream):
    print "Frame",stream.read('uintle:16')
    print "SkipCount",stream.read('uintle:8')

def set_target(stream):
    target_name = ''
    while stream.peek('uintle:8') != 0:
        target_name += stream.read('bytes:1')
    print "TargetName:",target_name
    stream.bytepos += 1

def wait_for_frame_2(stream):
    print "SkipCount",stream.read('uintle:8')

def goto_label(stream):
    label = ''
    while stream.peek('uintle:8') != 0:
        label += stream.read('bytes:1')
    print "Label:",label
    stream.bytepos += 1

def with(stream):
    print "Size:",stream.read('uintle:16')

def push(stream):
    data_type = stream.read('uintle:8')
    if data_type == 0:
        string_so_far = ""
        while stream.peek('uintle:8') != 0:
            string_so_far += stream.read('bytes:1')
        print "Pushed string:",string_so_far
        stream.bytepos += 1 #ignore the 0 at end of string.
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
    function_name = ''
    while stream.peek('uintle:8') != 0:
        function_name += stream.read('bytes:1')
    print "FunctionName:",function_name
    stream.bytepos += 1
    num_params = stream.read('uintle:16')
    for i in range(num_params):
        current_param = ''
        while stream.peek('uintle:8') != 0:
            current_param += stream.read('bytes:1')
        print "Param",i+1,":",current_param
        stream.bytepos += 1
    print "CodeSize:",stream.read('uintle:16')
    # TODO: And then there's something involving the remaining code.

def if(stream):
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
    
