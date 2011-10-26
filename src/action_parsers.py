'''
Created on 22 Oct 2011

@author: Bluebottle
'''
import struct

def goto_frame(data):
    frame = struct.unpack('<H',data[0:2])[0]
    print "Go to frame:",frame

def constant_pool(data):
    constant_count = struct.unpack('<H',data[0:2])[0]
    print "Total constants:",constant_count
    constants_so_far = 0
    remaining_data = data[2:]
    while len(remaining_data) > 0 and constants_so_far < constant_count:
        string_so_far = ""
        while struct.unpack('<B',remaining_data[0])[0] != 0:
            string_so_far += struct.unpack("<c",remaining_data[0])[0]
            remaining_data = remaining_data[1:]
        print "Constant",constants_so_far,"is:",string_so_far
        constants_so_far += 1
        remaining_data = remaining_data[1:] #ignore the 0 at end of string.

def push(data):
    data_type = struct.unpack('<B',data[0])[0]
    remaining_data = data[1:]
    if data_type == 0:
        string_so_far = ""
        while struct.unpack('<B',remaining_data[0])[0] != 0:
            string_so_far += struct.unpack("<c",remaining_data[0])[0]
            remaining_data = remaining_data[1:]
        print "Pushed string:",string_so_far
    elif data_type == 1:
        float_pushed = struct.unpack('<f',remaining_data[0:4])[0]
        print "Pushed float:",float_pushed
    elif data_type == 4:
        register_number_pushed = struct.unpack('<B',data[0])[0]
        print "Pushed register number:",register_number_pushed
    elif data_type == 5:
        boolean_pushed = struct.unpack('<B',data[0])[0]
        print "Pushed boolean:",boolean_pushed
    elif data_type == 6:
        double_pushed = struct.unpack('<d',remaining_data[0:8])[0]
        print "Pushed double:",double_pushed
    elif data_type == 7:
        integer_pushed = struct.unpack('<i',remaining_data[0:4])[0]
        print "Pushed integer:",integer_pushed
    elif data_type == 8:
        constant_pushed = struct.unpack('<B',remaining_data[0])[0]
        print "Pushed constant:",constant_pushed
    elif data_type == 9:
        constant_pushed = struct.unpack('<H',remaining_data[0:2])[0]
        print "Pushed constant:",constant_pushed

def not_implemented(data):
    print "No parser for this action yet."
    
