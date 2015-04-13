'''
Created on 20 Oct 2011

@author: Bluebottle
'''
from actions import ActionFactory
from log import log

class Rect(object):
    def __init__(self,stream):
        # Read the Nbits field - the first 5 bits - to find the size of the next ones.
        self.nbits = stream.read('uint:5')
        if self.nbits == 0:
            self.x_min = 0
            self.x_max = 0
            self.y_min = 0
            self.y_max = 0
        else:
            nbits_format = 'int:%d' % self.nbits
            self.x_min = stream.read(nbits_format)
            self.x_max = stream.read(nbits_format)
            self.y_min = stream.read(nbits_format)
            self.y_max = stream.read(nbits_format)
        stream.bytealign()
    
    def __str__(self):
        return "( XMin: {0}, XMax: {1}, YMin: {2}, YMax: {3} )".format(self.x_min,
                                                                   self.x_max,
                                                                   self.y_min,
                                                                   self.y_max)

class Fixed8(object):
    def __init__(self,stream):
        self.low = stream.read('uintle:8')
        self.high = stream.read('uintle:8')
    
    def __str__(self):
        return "{0}.{1}".format(self.high,self.low)

class Fixed(object):
    def __init__(self,stream):
        self.low = stream.read('uintle:16')
        self.high = stream.read('uintle:16')
    
    def __str__(self):
        return "{0}.{1}".format(self.high,self.low)

class EncodedU32(object):
    def __init__(self,stream):
        self.value = 0
        for byte in xrange(0,5):
            last_byte = stream.read('bool')
            byte_content = stream.read('uint:7')
            self.value += byte_content * math.pow(2,7*byte)
            if last_byte:
                break
                
    def __str__(self):
        return "{0}".format(self.value)

class Rgb(object):
    def __init__(self,stream):
        stream.bytealign()
        self.r = stream.read('uintle:8')
        self.g = stream.read('uintle:8')
        self.b = stream.read('uintle:8')
    
    def __str__(self):
        return "({0},{1},{2})".format(self.r,self.g,self.b)

class Rgba(object):
    def __init__(self,stream):
        stream.bytealign()
        self.r = stream.read('uintle:8')
        self.g = stream.read('uintle:8')
        self.b = stream.read('uintle:8')
        self.a = stream.read('uintle:8')
    
    def __str__(self):
        return "({0},{1},{2},{3})".format(self.r,self.g,self.b,self.a)

class Cxform(object):
    def __init__(self,stream):
        self.has_add_terms = stream.read('bool')
        self.has_mult_terms = stream.read('bool')
        n_bits = stream.read('uint:4')
        n_bits_format = 'int:{0}'.format(n_bits)
        if self.has_mult_terms:
            self.red_mult_term = stream.read(n_bits_format)
            self.green_mult_term = stream.read(n_bits_format)
            self.blue_mult_term = stream.read(n_bits_format)
        if self.has_add_terms:
            self.red_add_term = stream.read(n_bits_format)
            self.green_add_term = stream.read(n_bits_format)
            self.blue_add_term = stream.read(n_bits_format)
        stream.bytealign()
    
    def __str__(self):
        s = "\nHasAddTerms: {0}\nHasMultTerms: {1}".format(self.has_add_terms,
                                                           self.has_mult_terms)
        if self.has_mult_terms:
            s += "\nRedMultTerm: {0}\nGreenMultTerm: {1}\nBlueMultTerm: {2}".format(self.red_mult_term,self.green_mult_term,self.blue_mult_term)
        if self.has_add_terms:
            s += "\nRedAddTerm: {0}\nGreenAddTerm: {1}\nBlueAddTerm: {2}".format(self.red_add_term,self.green_add_term,self.blue_add_term)
        return s

class CxformWithAlpha(object):
    def __init__(self,stream):
        self.has_add_terms = stream.read('bool')
        self.has_mult_terms = stream.read('bool')
        n_bits = stream.read('uint:4')
        n_bits_format = 'int:{0}'.format(n_bits)
        if self.has_mult_terms:
            self.red_mult_term = stream.read(n_bits_format)
            self.green_mult_term = stream.read(n_bits_format)
            self.blue_mult_term = stream.read(n_bits_format)
            self.alpha_mult_term = stream.read(n_bits_format)
        if self.has_add_terms:
            self.red_add_term = stream.read(n_bits_format)
            self.green_add_term = stream.read(n_bits_format)
            self.blue_add_term = stream.read(n_bits_format)
            self.alpha_add_term = stream.read(n_bits_format)
        stream.bytealign()
    
    def __str__(self):
        s = "\nHasAddTerms: {0}\nHasMultTerms: {1}".format(self.has_add_terms,
                                                           self.has_mult_terms)
        if self.has_mult_terms:
            s += "\nRedMultTerm: {0}\nGreenMultTerm: {1}\nBlueMultTerm: {2}\nAlphaMultTerm: {3}".format(self.red_mult_term,self.green_mult_term,self.blue_mult_term,self.alpha_mult_term)
        if self.has_add_terms:
            s += "\nRedAddTerm: {0}\nGreenAddTerm: {1}\nBlueAddTerm: {2}\nAlphaAddTerm: {3}".format(self.red_add_term,self.green_add_term,self.blue_add_term,self.alpha_add_term)
        return s

class Matrix(object):
    def __init__(self,stream):
        self.has_scale = stream.read('bool')
        if self.has_scale:
            n_scale = stream.read('uint:5')
            scale_format = 'uint:%d' % n_scale
            self.scale_x = stream.read(scale_format)
            self.scale_y = stream.read(scale_format) 
        self.has_rotate = stream.read('bool')
        if self.has_rotate:
            n_rotate_bits = stream.read('uint:5')
            rotate_format = 'uint:%d' % n_rotate_bits
            self.rotate_skew_0 = stream.read(rotate_format)
            self.rotate_skew_1 = stream.read(rotate_format)
        n_translate_bits = stream.read('uint:5')
        if n_translate_bits > 0:
            translate_format = 'int:%d' % n_translate_bits
            self.translate_x = stream.read(translate_format)
            self.translate_y = stream.read(translate_format)
        stream.bytealign()
        # Original comments say "they're actually 16.16 fixed-point"
        # for the scale/rotate/translate factors, but this doesn't seem 
        # to make any sense. Will look into this later on.
    
    def __str__(self):
        s = "\nHasScale: {0}".format(self.has_scale)
        if self.has_scale:
            s += "\nScaleX: {0}\nScaleY: {1}".format(self.scale_x,self.scale_y)
        s += "\nHasRotate: {0}".format(self.has_rotate)
        if self.has_rotate:
            s += "\nRotateSkew0: {0}\nRotateSkew1: {1}".format(self.rotate_skew_0,self.rotate_skew_1)
        if hasattr(self,"translate_x"):
            s += "\nTranslateX: {0}\nTranslateY: {1}".format(self.translate_x,self.translate_y)
        return s

class Gradient(object):
    def __init__(self,stream,calling_tag):
        self.spread_mode = stream.read('uint:2')
        self.interpolation_mode = stream.read('uint:2')
        self.num_gradients = stream.read('uint:4')
        self.gradient_records = []
        for n in range(self.num_gradients):
            new_gradient = {'ratio': stream.read('uintle:8')}
            if calling_tag == "DefineShape" or calling_tag == "DefineShape2":
                new_gradient['color'] = Rgb(stream)
            else:
                new_gradient['color'] = Rgba(stream)

class FocalGradient(object):
    def __init__(self,stream,calling_tag):
        self.spread_mode = stream.read('uint:2')
        self.interpolation_mode = stream.read('uint:2')
        self.num_gradients = stream.read('uint:4')
        self.gradient_records = []
        for n in range(num_gradients):
            new_gradient = {'ratio': stream.read('uintle:8')}
            if calling_tag == "DefineShape" or calling_tag == "DefineShape2":
                new_gradient['color'] = Rgb(stream)
            else:
                new_gradient['color'] = Rgba(stream)
        self.focal_point= Fixed8(stream)

class ClipActions(object):
    def __init__(self,stream,swf_version):
        stream.pos += 16
        self.all_event_flags = ClipEventFlags(stream,swf_version)
        if swf_version > 5:
            flag_size = 32
        else:
            flag_size = 16
        self.clip_action_records = []
        while stream.peek('uintle:{0}'.format(flag_size)) != 0:
            self.clip_action_records.append(ClipActionRecord(stream,
                                                             swf_version))
        stream.pos += flag_size
    
    def __str__(self):
        return "[no str method yet, working on it]"

class ClipActionRecord(object):
    def __init__(self,stream,swf_version):
        self.event_flags = ClipEventFlags(stream,swf_version)
        self.action_record_size = stream.read('uintle:32')
        initial_bytepos = stream.bytepos
        if hasattr(self.event_flags,"clip_event_key_press") and self.event_flags.clip_event_key_press == True:
            self.key_code = stream.read('uintle:8')
        self.actions = []
        while stream.bytepos < initial_bytepos + self.action_record_size:
            action_code = stream.read('uintle:8')
            action_length = 0
            if action_code > 0x7F:
                action_length = stream.read('uintle:16')
            action_stream = stream.read('bits:{0}'.format(action_length*8))
            self.actions.append(ActionFactory.new_action(action_stream,
                                                         action_code,
                                                         action_length) )
    
class ClipEventFlags(object):
    def __init__(self,stream,swf_version):
        self.clip_event_key_up = stream.read('bool')
        self.clip_event_key_down = stream.read('bool')
        self.clip_event_mouse_up = stream.read('bool')
        self.clip_event_mouse_down = stream.read('bool')
        self.clip_event_mouse_move = stream.read('bool')
        self.clip_event_unload = stream.read('bool')
        self.clip_event_enter_frame = stream.read('bool')
        self.clip_event_load = stream.read('bool')
        if swf_version > 5:
            self.clip_event_drag_over = stream.read('bool')
            self.clip_event_roll_out = stream.read('bool')
            self.clip_event_roll_over = stream.read('bool')
            self.clip_event_release_outside = stream.read('bool')
            self.clip_event_release = stream.read('bool')
            self.clip_event_press = stream.read('bool')
            self.clip_event_initialize = stream.read('bool')
        else:
            stream.pos += 7
        self.clip_event_data = stream.read('bool')
        if swf_version > 5:
            stream.pos += 5
            self.clip_event_construct = stream.read('bool')
            self.clip_event_key_press = stream.read('bool')
            self.clip_event_drag_out = stream.read('bool')
        stream.pos += 8
    
    def __str__(self):
        items = ["\nClipEventKeyUp: {0}".format(self.clip_event_key_up),
                 "ClipEventKeyDown: {0}".format(self.clip_event_key_down),
                 "ClipEventMouseUp: {0}".format(self.clip_event_mouse_up),
                 "ClipEventMouseDown: {0}".format(self.clip_event_mouse_down),
                 "ClipEventUnload: {0}",format(self.clip_event_unload),
                 "ClipEventEnterFrame: {0}".format(self.clip_event_enter_frame),
                 "ClipEventLoad: {0}".format(self.clip_event_load) ]
        if hasattr(self,"clip_event_drag_over"):
            items.append("ClipEventDragOver: {0}".format(self.clip_event_drag_over))
            items.append("ClipEventRollOut: {0}".format(self.clip_event_roll_out))
            items.append("ClipEventRollOver: {0}".format(self.clip_event_roll_over))
            items.append("ClipEventReleaseOutside: {0}".format(self.clip_event_release_outside))
            items.append("ClipEventRelease: {0}".format(self.clip_event_release))
            items.append("ClipEventPress: {0}".format(self.clip_event_press))
            items.append("ClipEventInitialize: {0}".format(self.clip_event_initialize))
        items.append("ClipEventData: {0}".format(self.clip_event_data))
        if hasattr(self,"clip_event_construct"):
            items.append("ClipEventConstruct: {0}".format(self.clip_event_construct))
            items.append("ClipEventKeyPress: {0}".format(self.clip_event_key_press))
            items.append("ClipEventDragOut: {0}".format(self.clip_event_drag_out))
        return "\n".join(items)

class Shape(object):
    def __init__(self,stream,calling_tag):
        print "Creating new Shape"
        print "stream.bytepos =",stream.bytepos
        self.num_fill_bits = stream.read('uint:4')
        print "NumFillBits:",self.num_fill_bits
        self.num_line_bits = stream.read('uint:4')
        print "NumLineBits:",self.num_line_bits
        self.shaperecords = []
        # Note from the v10 spec: "Each individual shape is byte-aligned
        # within an array of shape records; one shape record is padded to
        # a byte boundary before the next shape record begins."
        # https://github.com/timknip/pyswf/blob/master/swf/data.py points out
        # that this isn't true; and this note is not in the v19 spec.
        # So they aren't byte-aligned, they just run together.
        # Although this may be trickier than I thought:
        # * 4chan_pokemon.swf, which I've been using for testing, parses if 
        #   they're not byte-aligned.
        # * sim_test_original.swf falls over horribly if they're not,
        #   but doesn't parse properly even if they are. Argh.
        record = None
        while type(record) != EndShapeRecord:
            # TODO: track fill_bits and line_bits
            record = (ShapeRecordFactory.new_shape_record(stream,
                                         self,
                                         calling_tag))
            self.shape_records.append(record)

class ShapeWithStyle(object):
    def __init__(self,stream,calling_tag):
        log("Parsing ShapeWithStyle")
        self.fill_styles = FillStyleArray(stream,calling_tag)
        self.line_styles = LineStyleArray(stream,calling_tag)
        # The rest of this is / should be the same as for Shape.
        self.num_fill_bits = stream.read('uint:4')
        self.num_line_bits = stream.read('uint:4')
        log("NumFillBits: {s}".format(s=self.num_fill_bits))
        log("NumLineBits: {s}".format(s=self.num_line_bits))
        self.shape_records = []
        record = None
        while type(record) != EndShapeRecord:
            # TODO: track fill_bits and line_bits
            record = (ShapeRecordFactory.new_shape_record(stream,
                                         self,
                                         calling_tag))
            self.shape_records.append(record)

class ShapeRecordFactory(object):
    @staticmethod
    def new_shape_record(stream,shape_object,calling_tag):
        type_flag = stream.read('uint:1')
        if type_flag == 0:
            if stream.peek('uint:5') == 0:
                # EndShapeRecord: type_flag = 0, next 5 bits all 0
                stream.pos += 5
                return EndShapeRecord(stream)
            else:
                # StyleChangeRecord: type_flag = 0, at least one of next 5 bits 1.
                # For this, we need to know the most recent numbers for fill/line
                # index bits to pass into StyleChangeRecord.
                for shape_record in reversed(shape_object.shape_records):
                    if (hasattr(shape_record,"state_new_styles") and 
                        shape_record.state_new_styles == True):
                        # This is the most recent fill/line bit setting. Use this!
                        fill_bits = shape_record.num_fill_bits
                        line_bits = shape_record.num_line_bits
                        break
                else:
                    # We end up here if there aren't any records,
                    # or if none of them define new fill/line bits.
                    # So we use the ones defined on the Shape or
                    # ShapeWithStyle object at the start.
                    fill_bits = shape_object.num_fill_bits
                    line_bits = shape_object.num_line_bits
                return StyleChangeRecord(stream,
                                         calling_tag,
                                         fill_bits,line_bits)
        else:
            straight_flag = stream.read('uint:1')
            if straight_flag == 0:
                # CurvedEdgeRecord: type_flag = 1, next bit = 0.
                return CurvedEdgeRecord(stream)
            else:
                # StraightEdgeRecord: type_flag = 1, next bit = 1
                return StraightEdgeRecord(stream)
        #record_type = self.shaperecords[-1].__class__

   
class EndShapeRecord(object):
    def __init__(self,stream):
        log("Parsing EndShapeRecord")
        self.type_flag = 0
        self.end_of_shape = 0
        # Based on the demo on p232 of v19 of the spec,
        # I think we should be byte-aligning at the end of
        # a set of Shape Records? (i.e. at the end of
        # an EndShapeRecord).
        stream.bytealign()
    
class StyleChangeRecord(object):
    def __init__(self,stream,calling_tag,fill_bits,line_bits,first_glyph=False):
        # p127 in v19 spec
        # also p228 in v19 spec
        # Docs say this is "used by DefineShape2 and DefineShape3 only",
        # but (based on test files) it is still present for DefineShape.
        # (It's presumably just always false then.)
        log("Parsing StyleChangeRecord")
        log("Calling tag: {s}".format(s=calling_tag))
        self.type_flag = 0
        #if calling_tag in ("DefineShape2","DefineShape3"):
        self.state_new_styles = stream.read('bool')
        log("StateNewStyles: {s}".format(s=self.state_new_styles))
        self.state_line_style = stream.read('bool')
        log("StateLineStyle: {s}".format(s=self.state_line_style))
        self.state_fill_style_1 = stream.read('bool')
        log("StateFillStyle1: {s}".format(s=self.state_fill_style_1))
        self.state_fill_style_0 = stream.read('bool')
        log("StateFillStyle0: {s}".format(s=self.state_fill_style_0))
        self.state_move_to = stream.read('bool')
        log("StateMoveTo: {s}".format(s=self.state_move_to))
        if self.state_move_to:
            self.move_bits = stream.read('uint:5')
            if self.move_bits == 0:
                self.move_delta_x = 0
                self.move_delta_y = 0
            else:
                move_bits_format = 'int:%d' % self.move_bits
                self.move_delta_x = stream.read(move_bits_format)
                self.move_delta_y = stream.read(move_bits_format)
            log("MoveDeltaX: {s}".format(s=self.move_delta_x))
            log("MoveDeltaY: {s}".format(s=self.move_delta_y))
        if fill_bits > 0:
            fill_bits_format = 'uint:%d' % fill_bits
            if self.state_fill_style_0:
                self.fill_style_0 = stream.read(fill_bits_format)
                log("FillStyle0: {s}".format(s=self.fill_style_0))
            if self.state_fill_style_1:
                self.fill_style_1 = stream.read(fill_bits_format)
                log("FillStyle1: {s}".format(s=self.fill_style_1))
        if self.state_line_style and line_bits > 0:
            line_bits_format = 'uint:%d' % line_bits
            self.line_style = stream.read(line_bits_format)
            log("LineStyle: {s}".format(s=self.line_style))
        # TODO: Whether this is byte-aligned depends on whether:
        # (a) state_new_styles is set and True (if not, byte-align at the end)
        # (b) FillStyles and/or LineStyles have byte-aligned fields at start
        if hasattr(self,"state_new_styles") and self.state_new_styles:
            # TODO: Fix this up, probably turn these into lists.
            self.fill_styles = FillStyleArray(stream,calling_tag)
            self.line_styles = LineStyleArray(stream,calling_tag)
            self.num_fill_bits = stream.read('uint:4')
            self.num_line_bits = stream.read('uint:4')
        #stream.bytealign()
        # And whether *this* needs byte-aligning depends on similar things.

class StraightEdgeRecord(object):
    def __init__(self,stream):
        log("Parsing StraightEdgeRecord")
        self.type_flag = 1
        self.straight_flag = 1
        self.num_bits = stream.read('uint:4')
        num_bits_format = 'int:%d' % (self.num_bits+2)
        self.general_line_flag = stream.read('bool')
        log("GeneralLineFlag: {s}".format(s=self.general_line_flag))
        if not self.general_line_flag:
            self.vert_line_flag = stream.read('bool')
            log("VertLineFlag: {s}".format(s=self.vert_line_flag))
        if self.general_line_flag or not self.vert_line_flag:    
            self.delta_x = stream.read(num_bits_format)
            log("DeltaX: {s}".format(s=self.delta_x))
        if self.general_line_flag or self.vert_line_flag:
            self.delta_y = stream.read(num_bits_format)
            log("DeltaY: {s}".format(s=self.delta_y))

class CurvedEdgeRecord(object):
    def __init__(self,stream):
        log("Parsing CurvedEdgeRecord")
        self.type_flag = 1
        self.straight_flag = 0
        self.num_bits = stream.read('uint:4')
        num_bits_format = 'int:%d' % (self.num_bits+2)
        self.control_delta_x = stream.read(num_bits_format)
        self.control_delta_y = stream.read(num_bits_format)
        self.anchor_delta_x = stream.read(num_bits_format)
        self.anchor_delta_y = stream.read(num_bits_format)
        #stream.bytealign()
        # Whether this should be byte-aligned depends on what comes next.

class FillStyleArray(object):
    def __init__(self,stream,calling_tag):
        stream.bytealign() # because FillStyleArray starts with UI8.
        self.fill_style_count = stream.read('uintle:8')
        log("DEBUG: FillStyleCount: {s}".format(s=self.fill_style_count))
        total = self.fill_style_count
        if self.fill_style_count == 0xFF and calling_tag in ('DefineShape2',
                                                             'DefineShape3'):
            self.fill_style_count_extended = stream.read('uintle:16')
            log("DEBUG: FillStyleCountExtended: {s}".format(s=self.fill_style_count_extended))
            total = self.fill_style_count_extended
        self.fill_styles = []
        for x in xrange(total):
            self.fill_styles.append(FillStyle(stream,calling_tag))
    
    def __str__(self):
        log("FillStyleArray, length {l}:".format(l=len(self.fill_styles)))
        for fs in self.fill_styles:
            log("FillStyle: {s}".format(s=fs))

class FillStyle(object):
    fill_styles = {0x00 : 'solid',
                   0x10 : 'linear gradient',
                   0x12 : 'radial gradient',
                   0x13 : 'focal radial gradient',
                   0x40 : 'repeating bitmap',
                   0x41 : 'clipped bitmap',
                   0x42 : 'non-smoothed repeating bitmap',
                   0x43 : 'non-smoothed clipped bitmap' }

    def __init__(self,stream,calling_tag):
        stream.bytealign()
        self.fill_style_type = stream.read("uintle:8")
        if self.fill_style_type == 0x00: # solid
            if calling_tag == "DefineShape" or calling_tag == "DefineShape2":
                self.color = Rgb(stream)
            else:
                self.color = Rgba(stream)
        if self.fill_style_type in (0x10,0x12,0x13): # gradient
            self.gradient_matrix = Matrix(stream)
            if self.fill_style_type == 0x13: # focal radial gradient
                self.gradient = FocalGradient(stream,calling_tag)
            else:
                self.gradient = Gradient(stream,calling_tag)
        if self.fill_style_type in (0x40,0x41,0x42,0x43): # bitmap
            stream.bytealign()
            self.bitmap_id = stream.read("uintle:16")
            self.bitmap_matrix = Matrix(stream)

class LineStyleArray(object):
    def __init__(self,stream,calling_tag):
        stream.bytealign()
        self.line_style_count = stream.read('uintle:8')
        log("DEBUG: LineStyleCount: {s}".format(s=self.line_style_count))
        total = self.line_style_count
        if self.line_style_count == 0xFF:
            self.line_style_count_extended = stream.read('uintle:16')
            log("DEBUG: LineStyleCountExtended: {s}".format(s=self.line_style_count_extended))
            total = self.line_style_count_extended
        self.line_styles = []
        if calling_tag in ('DefineShape1','DefineShape2','DefineShape3'):
            linestyle_class = LineStyle
        else:
            linestyle_class = LineStyle2
        for x in xrange(total):
            self.line_styles.append(linestyle_class(stream,calling_tag))

class LineStyle(object):
    def __init__(self,stream,calling_tag):
        self.width = stream.read("uintle:16")
        if calling_tag == "DefineShape" or calling_tag == "DefineShape2":
            self.color = Rgb(stream)
        else:
            self.color = Rgba(stream)

class LineStyle2(object):
    def __init__(self,stream,calling_tag):
        self.width = stream.read("uintle:16")
        self.start_cap_style = stream.read("uint:2")
        self.join_style = stream.read("uint:2")
        self.has_fill_flag = stream.read("bool")
        self.no_h_scale_flag = stream.read("bool")
        self.no_v_scale_flag = stream.read("bool")
        self.pixel_hinting_flag = stream.read("bool")
        stream.pos += 5
        self.no_close = stream.read("bool")
        self.end_cap_style = stream.read("uint:2")
        if self.join_style == 2:
            self.miter_limit_factor = Fixed8(stream)
        if self.has_fill_flag:
            self.fill_type = FillStyle(stream,calling_tag)
        else:
            self.color = Rgba(stream)

class KerningRecord(object):
    def __init__(self,stream,font_flags_wide_codes):
        if font_flags_wide_codes:
            self.font_kerning_code_1 = stream.read('uintle:16')
            self.font_kerning_code_2 = stream.read('uintle:16')
        else:
            self.font_kerning_code_1 = stream.read('uintle:8')
            self.font_kerning_code_2 = stream.read('uintle:8')
        self.font_kerning_adjustment = stream.read('intle:16')
            
            
# ========

def string(stream):
    # Not a new class; produces a Python 2.x string.
    new_string = []
    while stream.peek('uintle:8') != 0:
        new_string.append(stream.read('bytes:1'))
    stream.bytepos += 1 # Ignore the final 0 in the string.
    return ''.join(new_string)

# ======== Old-style datatype parsing functions
# ======== that haven't been implemented as classes yet

def shape_with_style(stream,calling_tag):
    stream = fill_style_array(stream,calling_tag)
    stream = line_style_array(stream,calling_tag)
    shape(stream,calling_tag)