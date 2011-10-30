'''
Created on 22 Oct 2011

@author: Bluebottle
'''

def goto_frame(stream):
    frame = stream.read('uintle:16')
    print "Go to frame:",frame

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

def push(stream):
    data_type = stream.read('uintle:8')
    if data_type == 0:
        string_so_far = ""
        while stream.peek('uintle:8') != 0:
            string_so_far += stream.read('bytes:1')
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

def not_implemented(data):
    print "No parser for this action yet."
    
