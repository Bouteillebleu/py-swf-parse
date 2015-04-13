'''
Created on 15 Oct 2011

@author: Bluebottle
'''
import os
import struct
from actions import ActionFactory
import datatypes
from log import log

class TagFactory(object):
    @staticmethod
    def new_tag(swf_version,stream,tag_type,tag_length):
        tag_class = class_from_tag_number(tag_type)
        if tag_class is not None:
            log("==Creating new tag: {0}, length {1}==".format(tag_class.__name__,tag_length))
            return tag_class(swf_version,stream,tag_type,tag_length)
        else:
            return Tag(swf_version,stream,tag_type,tag_length)

class Tag(object):
    # This isn't intended to be directly instantiated;
    # we have lots of subclasses that should be used instead.
    def __init__(self,swf_version,stream,tag_type,tag_length):
        self.swf_version = swf_version
        self._stream = stream # DEBUG
        self.type = tag_type
        self.length = tag_length
        self.parser_implemented = True
        self.parse(stream)
        
    def parse(self,stream):
        # Default parser does nothing (apart from flag that this parser
        # is not implemented). Subclasses must implement this themselves.
        self.parser_implemented = False
    
    def display(self):
        if self.parser_implemented:
            log("Display function not implemented.")
        else:
            log("Parser not implemented.")
    
    def tag_type(self):
        return tag_data[self.type]['class']
        
    # TODO: Add some output for the bit contents of the stream.
    # TODO: Check - is the stream for one of these the stream of the entire file, 
    # or just the bits in this particular tag? It really ought to be the first.

# ==== Individual tags ====

class End(Tag):
    def parse(self,stream):
        pass

    def display(self):
        pass

class ShowFrame(Tag):
    def parse(self,stream):
        pass
    
    def display(self):
        pass

class DefineShape(Tag):
    def parse(self,stream):
        self.shape_id = stream.read('uintle:16')
        log("ShapeID: {s}".format(s=self.shape_id))
        self.shape_bounds = datatypes.Rect(stream)
        log("ShapeBounds: {s}".format(s=self.shape_bounds))
        self.shape = datatypes.ShapeWithStyle(stream,'DefineShape')
    
    def display(self):
        log("ShapeID: {s}".format(s=self.shape_id))
        log("ShapeBounds: {s}".format(s=self.shape_bounds))
        # TODO: Add display output for ShapeWithStyle

class PlaceObject(Tag):
    def parse(self,stream):
        self.character_id = stream.read('uintle:16')
        self.depth = stream.read('uintle:16')
        self.matrix = datatypes.Matrix(stream)
        self.color_transform = datatypes.Cxform(stream)
    
    def display(self):
        log("CharacterId: {s}".format(s=self.character_id))
        log("Depth: {s}".format(s=self.depth))
        log("Matrix: {s}".format(s=self.matrix))
        log("ColorTransform: {s}".format(s=self.color_transform))

class RemoveObject(Tag):
    def parse(self,stream):
        self.character_id = stream.read('uintle:16')
        self.depth = stream.read('uintle:16')
    
    def display(self):
        log("CharacterId: {s}".format(s=self.character_id))
        log("Depth: {s}".format(s=self.depth))

class DefineBits(Tag):
    pass

class DefineButton(Tag):
    pass

class JPEGTables(Tag):
    pass

class SetBackgroundColor(Tag):
    def parse(self,stream):
        self.background_color = datatypes.Rgb(stream)
    
    def display(self):
        log("BackgroundColor: {s}".format(s=self.background_color))

class DefineFont(Tag):
    def parse(self,stream):
        log("DEBUG: stream length = {s} bytes".format(s=(len(stream)/8)))
        self.font_id = stream.read('uintle:16')
        starting_bytepos = stream.bytepos
        log("DEBUG: starting bytepos = {s}".format(s=starting_bytepos))
        self.n_glyphs = stream.peek('uintle:16') / 2
        self.offset_table = []
        self.glyph_shape_table = []
        for glyph_number in xrange(self.n_glyphs):
            self.offset_table.append(stream.read('uintle:16'))
            log("glyph {g}, offset = {s}".format(g=glyph_number,
                                                 s=self.offset_table[-1]))
        for glyph_number in xrange(self.n_glyphs):
            pass
            # TODO: Either DefineFont or Shape and its offshoots are wrong.
            # DefineFont at the moment reads off the end of the stream.
            #stream.bytepos = starting_bytepos + self.offset_table[glyph_number]
            #self.glyph_shape_table.append(datatypes.Shape(stream,"DefineFont"))

class DefineText(Tag):
    pass

class DoAction(Tag):
    def parse(self,stream):
        self.actions = []
        while stream.peek('uintle:8') != 0:
            action_code = stream.read('uintle:8')
            action_length = 0
            if action_code > 0x7F:
                action_length = stream.read('uintle:16')
            action_stream = stream.read('bits:{0}'.format(action_length*8))
            self.actions.append(ActionFactory.new_action(action_stream,
                                                         action_code,
                                                         action_length))        

    def display(self):
        for i, action in enumerate(self.actions):
            log("== Action {0}: {1} ==".format(i,action.__class__.__name__))
            action.display()


class DefineFontInfo(Tag):
    pass

class DefineSound(Tag):
    pass

class StartSound(Tag):
    pass

class DefineButtonSound(Tag):
    pass

class SoundStreamHead(Tag):
    def parse(self,stream):
        stream.pos += 4
        self.playback_sound_rate = stream.read('uint:2')
        self.playback_sound_size = stream.read('uint:1')
        self.playback_sound_type = stream.read('uint:1')
        self.stream_sound_compression = stream.read('uint:4')
        self.stream_sound_rate = stream.read('uint:2')
        self.stream_sound_size = stream.read('uint:1')
        self.stream_sound_type = stream.read('uint:1')
        self.stream_sound_sample_count = stream.read('uintle:16')
        if self.stream_sound_compression == 2:
            self.latency_seek = stream.read('intle:16')

    def display(self):
        log("PlaybackSoundRate: {s}".format(s=self.playback_sound_rate))
        log("PlaybackSoundSize: {s}".format(s=self.playback_sound_size))
        log("PlaybackSoundType: {s}".format(s=self.playback_sound_type))
        log("StreamSoundCompression: {s}".format(s=self.stream_sound_compression))
        log("StreamSoundRate: {s}".format(s=self.stream_sound_rate))
        log("StreamSoundSize: {s}".format(s=self.stream_sound_size))
        log("StreamSoundType: {s}".format(s=self.stream_sound_type))
        log("StreamSoundSampleCount: {s}".format(s=self.stream_sound_sample_count))
        if self.stream_sound_compression == 2:
            log("LatencySeek: {s}".format(s=self.latency_seek))

class SoundStreamBlock(Tag):
    pass

class DefineBitsLossless(Tag):
    pass

class DefineBitsJPEG2(Tag):
    def parse(self,stream):
        self.character_id = stream.read('uintle:16')
        if stream.peek(32) == '0xffd9ffd8':
            # Some SWF versions before 8 erroneously have 
            # an extra JPEG EOI and SOI pair before the actual SOI.
            stream.read(32) # In that case, we just throw away the extra 4 bytes.
        # TODO: Convert the original JPEG extraction-to-file code,
        # as shown below, to something that'll save an image.
        #try:
        #    f = open(os.path.join("../output",filename),'wb')
        #    while stream.pos < stream.len:
        #        f.write(struct.pack('b',stream.read('int:8')))
        #finally:
        #    f.close()
        #    log("Wrote JPEG data to {s}".format(s=filename))

class DefineShape2(Tag):
    def parse(self,stream):
        self.shape_id = stream.read('uintle:16')
        log("ShapeID: {s}".format(s=self.shape_id))
        self.shape_bounds = datatypes.Rect(stream)
        log("ShapeBounds: {s}".format(s=self.shape_bounds))
        self.shape = datatypes.ShapeWithStyle(stream,'DefineShape2')
    
    def display(self):
        log("ShapeID: {s}".format(s=self.shape_id))
        log("ShapeBounds: {s}".format(s=self.shape_bounds))
        # TODO: Add display output for ShapeWithStyle

class DefineButtonCxform(Tag):
    def parse(self,stream):
        self.button_id = stream.read('uintle:16')
        self.button_color_transform = datatypes.Cxform(stream)
    
    def display(self):
        log("ButtonId: {s}".format(s=self.button_id))
        log("ButtonColorTransform: {s}".format(s=self.button_color_transform))

class Protect(Tag):
    def parse(self,stream):
        if self.length > 0:
            self.password_hash = datatypes.string(stream)

class PlaceObject2(Tag):
    def parse(self,stream):
        self.has_clip_actions = stream.read('bool')
        self.has_clip_depth = stream.read('bool')
        self.has_name = stream.read('bool')
        self.has_ratio = stream.read('bool')
        self.has_color_transform = stream.read('bool')
        self.has_matrix = stream.read('bool')
        self.has_character = stream.read('bool')
        self.move = stream.read('bool')
        self.depth = stream.read('uintle:16')
        if self.has_character:
            self.character_id = stream.read('uintle:16')
        if self.has_matrix:
            self.matrix = datatypes.Matrix(stream)
        if self.has_color_transform:
            self.color_transform = datatypes.CxformWithAlpha(stream)
        if self.has_ratio:
            self.ratio = stream.read('uintle:16')
        if self.has_name:
            self.name = datatypes.string(stream)
        if self.has_clip_depth:
            self.clip_depth = stream.read('uintle:16')
        if self.has_clip_actions:
            self.clip_actions = datatypes.ClipActions(stream,self.swf_version)

    def display(self):
        log("FlagHasClipActions: {s}".format(s=self.has_clip_actions))
        log("FlagHasClipDepth: {s}".format(s=self.has_clip_depth))
        log("FlagHasName: {s}".format(s=self.has_name))
        log("FlagHasRatio: {s}".format(s=self.has_ratio))
        log("FlagHasColorTransform: {s}".format(s=self.has_color_transform))
        log("FlagHasMatrix: {s}".format(s=self.has_matrix))
        log("FlagHasCharacter: {s}".format(s=self.has_character))
        log("FlagMove: {s}".format(s=self.move))
        log("Depth: {s}".format(s=self.depth))
        if self.has_character:
            log("CharacterId: {s}".format(s=self.character_id))
        if self.has_matrix:
            log("Matrix: {s}".format(s=self.matrix))
        if self.has_color_transform:
            log("ColorTransform: {s}".format(s=self.color_transform))
        if self.has_ratio:
            log("Ratio: {s}".format(s=self.ratio))
        if self.has_name:
            log("Name: {s}".format(s=self.name))
        if self.has_clip_depth:
            log("ClipDepth: {s}".format(s=self.clip_depth))
        if self.has_clip_actions:
            log("ClipActions: {s}".format(s=self.clip_actions))

class RemoveObject2(Tag):
    def parse(self,stream):
        self.depth = stream.read('uintle:16')
    
    def display(self):
        log("Depth: {s}".format(s=self.depth))

class DefineShape3(Tag):
    def parse(self,stream):
        self.shape_id = stream.read('uintle:16')
        log("ShapeID: {s}".format(s=self.shape_id))
        self.shape_bounds = datatypes.Rect(stream)
        log("ShapeBounds: {s}".format(s=self.shape_bounds))
        self.shape = datatypes.ShapeWithStyle(stream,'DefineShape3')
    
    def display(self):
        log("ShapeID: {s}".format(s=self.shape_id))
        log("ShapeBounds: {s}".format(s=self.shape_bounds))
        # TODO: Add display output for ShapeWithStyle
    
class DefineText2(Tag):
    pass

class DefineButton2(Tag):
    pass

class DefineBitsJPEG3(Tag):
    pass

class DefineBitsLossless2(Tag):
    pass

class DefineEditText(Tag):
    def parse(self,stream):
        self.character_id = stream.read('uintle:16')
        self.bounds = datatypes.Rect(stream)
        self.has_text = stream.read('bool')
        self.word_wrap = stream.read('bool')
        self.multiline = stream.read('bool')
        self.password = stream.read('bool')
        self.read_only = stream.read('bool')
        self.has_text_color = stream.read('bool')
        self.has_max_length = stream.read('bool')
        self.has_font = stream.read('bool')
        self.has_font_class = stream.read('bool')
        self.auto_size = stream.read('bool')
        self.has_layout = stream.read('bool')
        self.no_select = stream.read('bool')
        self.border = stream.read('bool')
        self.was_static = stream.read('bool')
        self.html = stream.read('bool')
        self.use_outlines = stream.read('bool')
        if self.has_font:
            self.font_id = stream.read('uintle:16')
        if self.has_font_class:
            self.font_class = datatypes.string(stream)
        if self.has_font:
            self.font_height = stream.read('uintle:16')
        if self.has_text_color:
            self.text_color = datatypes.Rgba(stream)
        if self.has_max_length:
            self.max_length = stream.read('uintle:16')
        if self.has_layout:
            self.align = stream.read('uintle:8')
            self.left_margin = stream.read('uintle:16')
            self.right_margin = stream.read('uintle:16')
            self.indent = stream.read('uintle:16')
            self.leading = stream.read('intle:16')
        self.variable_name = datatypes.string(stream)
        if self.has_text:
            self.initial_text = datatypes.string(stream)

    def display(self):
        log("CharacterId: {s}".format(s=self.character_id))
        log("Bounds: {s}".format(s=self.bounds))
        log("HasText: {s}".format(s=self.has_text))
        log("WordWrap: {s}".format(s=self.word_wrap))
        log("Multiline: {s}".format(s=self.multiline))
        log("Password: {s}".format(s=self.password))
        log("ReadOnly: {s}".format(s=self.read_only))
        log("HasTextColor: {s}".format(s=self.has_text_color))
        log("HasMaxLength: {s}".format(s=self.has_max_length))
        log("HasFont: {s}".format(s=self.has_font))
        log("HasFontClass: {s}".format(s=self.has_font_class))
        log("AutoSize: {s}".format(s=self.auto_size))
        log("HasLayout: {s}".format(s=self.has_layout))
        log("NoSelect: {s}".format(s=self.no_select))
        log("Border: {s}".format(s=self.border))
        log("WasStatic: {s}".format(s=self.was_static))
        log("HTML: {s}".format(s=self.html))
        log("UseOutlines: {s}".format(s=self.use_outlines))
        if self.has_font:
            log("FontId: {s}".format(s=self.font_id))
        if self.has_font_class:
            log("FontClass: {s}".format(s=self.font_class))
        if self.has_font:
            log("FontHeight: {s}".format(s=self.font_height))
        if self.has_text_color:
            log("TextColor: {s}".format(s=self.text_color))
        if self.has_max_length:
            log("MaxLength: {s}".format(s=self.max_length))
        if self.has_layout:
            log("Align: {s}".format(s=self.align))
            log("LeftMargin: {s}".format(s=self.left_margin))
            log("RightMargin: {s}".format(s=self.right_margin))
            log("Indent: {s}".format(s=self.indent))
            log("Leading: {s}".format(s=self.leading))
        log("VariableName: {s}".format(s=self.variable_name))
        if self.has_text:
            log("InitialText: {s}".format(s=self.initial_text))


class DefineSprite(Tag):
    def parse(self,stream):
        self.sprite_id = stream.read('uintle:16')
        self.frame_count = stream.read('uintle:16')
        self.tags = []
        current_tag_type = None
        while stream.pos < stream.len and current_tag_type != 0:
            tag_header = stream.read('uintle:16')
            current_tag_type = tag_header >> 6 # Ignore the bottom 6 bits
            current_tag_length = tag_header & 0x3F # Only keep bottom 6 bits
            if current_tag_length == 0x3f:
                # If it's actually 63, use the long record header form instead.
                current_tag_length = stream.read('intle:32')
            tag_stream = stream.read('bits:{0}'.format(current_tag_length*8))
            log("Creating nested tag...")
            new_tag = TagFactory.new_tag(self.swf_version,
                                         tag_stream,
                                         current_tag_type,
                                         current_tag_length)
            self.tags.append(new_tag)
    
    def display(self):
        log("SpriteId: {s}".format(s=self.sprite_id))
        log("FrameCount: {s}".format(s=self.frame_count))
        log("Sprite contains the following tags:")
        for i, tag in enumerate(self.tags):
            log("tag {0}: {1}".format(i,tag.__class__.__name__))
            tag.display()

class FrameLabel(Tag):
    def parse(self,stream):
        self.name = datatypes.string(stream)
        if stream.pos < stream.length and stream.peek('uintle:8') == 1:
            self.is_named_anchor = True
        else:
            self.is_named_anchor = False
    
    def display(self):
        log("Name: {s}".format(s=self.name))
        log("Is NamedAnchor: {s}".format(s=self.is_named_anchor))

class SoundStreamHead2(Tag):
    def parse(self,stream):
        stream.pos += 4
        self.playback_sound_rate = stream.read('uint:2')
        self.playback_sound_size = stream.read('uint:1')
        self.playback_sound_type = stream.read('uint:1')
        self.stream_sound_compression = stream.read('uint:4')
        self.stream_sound_rate = stream.read('uint:2')
        self.stream_sound_size = stream.read('uint:1')
        self.stream_sound_type = stream.read('uint:1')
        self.stream_sound_sample_count = stream.read('uintle:16')
        if self.stream_sound_compression == 2:
            self.latency_seek = stream.read('intle:16')

    def display(self):
        log("PlaybackSoundRate: {s}".format(s=self.playback_sound_rate))
        log("PlaybackSoundSize: {s}".format(s=self.playback_sound_size))
        log("PlaybackSoundType: {s}".format(s=self.playback_sound_type))
        log("StreamSoundCompression: {s}".format(s=self.stream_sound_compression))
        log("StreamSoundRate: {s}".format(s=self.stream_sound_rate))
        log("StreamSoundSize: {s}".format(s=self.stream_sound_size))
        log("StreamSoundType: {s}".format(s=self.stream_sound_type))
        log("StreamSoundSampleCount: {s}".format(s=self.stream_sound_sample_count))
        if self.stream_sound_compression == 2:
            log("LatencySeek: {s}".format(s=self.latency_seek))

class DefineMorphShape(Tag):
    pass

class DefineFont2(Tag):
    pass

class ExportAssets(Tag):
    def parse(self,stream):
        count = stream.read('uintle:16')
        self.assets = []
        for x in range(0,count):
            new_asset = {'tag': stream.read('uintle:16'),
                         'name': datatypes.string(stream)}
            self.assets.append(new_asset)

class ImportAssets(Tag):
    def parse(self,stream):
        self.url = datatypes.string(stream)
        count = stream.read('uintle:16')
        self.assets = []
        for x in range(0,count):
            new_asset = {'tag': stream.read('uintle:16'),
                         'name': datatypes.string(stream)}
            self.assets.append(new_asset)

class EnableDebugger(Tag):
    def parse(self,stream):
        self.password_hash = datatypes.string(stream)

class DoInitAction(Tag):
    def parse(self,stream):
        self.sprite_id = stream.read('uintle:16')
        self.actions = []
        while stream.peek('uintle:8') != 0:
            action_code = stream.read('uintle:8')
            action_length = 0
            if action_code > 0x7F:
                action_length = stream.read('uintle:16')
            action_stream = stream.read('bits:{0}'.format(action_length*8))
            self.actions.append(ActionFactory.new_action(action_stream,
                                                         action_code,
                                                         action_length))        

    def display(self):
        for i, action in enumerate(self.actions):
            log("== Action {0}: {1} ==".format(i,action.__class__.__name__))
            action.display()

class DefineVideoStream(Tag):
    def parse(self,stream):
        self.character_id = stream.read('uintle:16')
        self.num_frames = stream.read('uintle:16')
        self.width = stream.read('uintle:16')
        self.height = stream.read('uintle:16')
        stream.pos += 4
        self.video_flags_deblocking = stream.read('uint:3') # TODO: enums!
        self.video_flags_smoothing = stream.read('uint:1') # TODO: bool?
        self.codec_id = stream.read('uintle:8') # TODO: enums!
        # TODO: Finish
        stream.bytealign()

class VideoFrame(Tag):
    pass

class DefineFontInfo2(Tag):
    pass

class EnableDebugger2(Tag):
    def parse(self,stream):
        stream.pos += 16
        self.password_hash = datatypes.string(stream)

class ScriptLimits(Tag):
    def parse(self,stream):
        self.max_recursion_depth = stream.read('uintle:16')
        self.script_timeout_seconds = stream.read('uintle:16')
        
    def display(self):
        log("MaxRecursionDepth: {s}".format(s=self.max_recursion_depth))
        log("ScriptTimeoutSeconds: {s}".format(s=self.script_timeout_seconds))

class SetTabIndex(Tag):
    def parse(self,stream):
        self.depth = stream.read('uintle:16')
        self.tab_index = stream.read('uintle:16')
    
    def display(self):
        log("Depth: {s}".format(s=self.depth))
        log("TabIndex: {s}".format(s=self.tab_index))

class FileAttributes(Tag):
    def parse(self,stream):
        stream.pos += 1
        self.use_direct_bit = stream.read('bool')
        self.use_gpu = stream.read('bool')
        self.has_metadata = stream.read('bool')
        self.actionscript3 = stream.read('bool')
        stream.pos += 2
        self.use_network = stream.read('bool')
        stream.pos += 24
        stream.bytealign()
    
    def display(self):
        log("UseDirectBit: {s}".format(s=self.use_direct_bit))
        log("UseGPU: {s}".format(s=self.use_gpu))
        log("HasMetadata: {s}".format(s=self.has_metadata))
        log("UseNetwork: {s}".format(s=self.use_network))

class PlaceObject3(Tag):
    pass

class ImportAssets2(Tag):
    def parse(self,stream):
        self.url = datatypes.string(stream)
        stream.pos += 16
        count = stream.read('uintle:16')
        self.assets = []
        for x in range(0,count):
            new_asset = {'tag': stream.read('uintle:16'),
                         'name': datatypes.string(stream)}
            self.assets.append(new_asset)

class DefineFontAlignZones(Tag):
    def parse(self,stream):
        self.font_id = stream.read('uintle:16')
        self.csm_table_hint = stream.read('uint:2')
        stream.pos += 6
        # TODO: Use font_id to find the relevant DefineFont3 tag.
        # Then check GlyphCount from that.
        # Until we have GlyphCount, we can't do anything else with this.
        # ZoneRecords contain ZoneData, ZoneData contains FLOAT16s
        # (half-precision floats) which bitstring won't parse automatically.

class CSMTextSettings(Tag):
    def parse(self,stream):
        self.text_id = stream.read('uintle:16')
        self.use_flash_type = stream.read('int:2')
        self.grid_fit = stream.read('int:3')
        stream.pos += 3
        self.thickness = stream.read('floatle:32')
        self.sharpness = stream.read('floatle:32')
        # TODO: last 8 bits should all be 0.        

class DefineFont3(Tag):
    def parse(self,stream):
        self.font_id = stream.read('uintle:16')
        log("DEBUG: FontID: {s}".format(s=self.font_id))
        self.font_flags_has_layout = stream.read('bool')
        log("DEBUG: FontFlagsHasLayout: {s}".format(s=self.font_flags_has_layout))
        self.font_flags_shiftJIS = stream.read('bool')
        log("DEBUG: FontFlagsShiftJIS: {s}".format(s=self.font_flags_shiftJIS))
        self.font_flags_small_text = stream.read('bool')
        log("DEBUG: FontFlagsSmallText: {s}".format(s=self.font_flags_small_text))
        self.font_flags_ansi = stream.read('bool')
        log("DEBUG: FontFlagsANSI: {s}".format(s=self.font_flags_ansi))
        self.font_flags_wide_offsets = stream.read('bool')
        log("DEBUG: FontFlagsWideOffsets: {s}".format(s=self.font_flags_wide_offsets))
        self.font_flags_wide_codes = stream.read('bool')
        log("DEBUG: FontFlagsWideCodes: {s}".format(s=self.font_flags_wide_codes))
        self.font_flags_italic = stream.read('bool')
        log("DEBUG: FontFlagsItalic: {s}".format(s=self.font_flags_italic))
        self.font_flags_bold = stream.read('bool')
        log("DEBUG: FontFlagsBold: {s}".format(s=self.font_flags_bold))
        self.language_code = stream.read('uintle:8') # TODO: enum?
        log("DEBUG: LanguageCode: {s}".format(s=self.language_code))
        self.font_name_len = stream.read('uintle:8')
        log("DEBUG: FontNameLen: {s}".format(s=self.font_name_len))
        self.font_name = [] # TODO: change this to be stored as a string instead
        for x in range(0,self.font_name_len):
            self.font_name.append(chr(stream.read('uintle:8')))
        log("DEBUG: FontName: {s}".format(s="".join(self.font_name)))
        self.num_glyphs = stream.read('uintle:16')
        log("DEBUG: NumGlyphs: {s}".format(s=self.num_glyphs))
        self.offset_table = []
        if self.font_flags_wide_offsets:
            for x in range(0,self.num_glyphs):
                self.offset_table.append(stream.read('uintle:32'))
            self.code_table_offset = stream.read('uintle:32')
        else:
            for x in range(0,self.num_glyphs):
                self.offset_table.append(stream.read('uintle:16'))
            self.code_table_offset = stream.read('uintle:16')
        log("DEBUG: CodeTableOffset: {s}".format(s=self.code_table_offset))
        self.glyph_shape_table = []
        for x in range(0,self.num_glyphs):
            log("DEBUG: Reading shape for glyph {x}".format(x=x))
            self.glyph_shape_table.append(datatypes.Shape(stream,'DefineFont3'))
            # TODO: parse SHAPE[NumGlyphs], "same as in DefineFont"
        self.code_table = []
        for x in range(0,self.num_glyphs):
            self.code_table.append(stream.read('uintle:16'))
        if self.font_flags_has_layout:
            self.font_ascent = stream.read('uintle:16')
            log("DEBUG: FontAscent: {s}".format(s=self.font_ascent))
            self.font_descent = stream.read('uintle:16')
            log("DEBUG: FontDescent: {s}".format(s=self.font_descent))
            self.font_leading = stream.read('intle:16')
            log("DEBUG: FontLeading: {s}".format(s=self.font_leading))
            self.font_advance_table = []
            for x in range(0,self.num_glyphs):
                self.font_advance_table.append(stream.read('intle:16'))
            self.font_bounds_table = []
            for x in range(0,self.num_glyphs):
                self.font_bounds_table.append(datatypes.Rect(stream))
            self.kerning_count = stream.read('uintle:16')
            self.font_kerning_table = []
            for x in range(0,self.kerning_count):
                self.font_kerning_table.append(datatypes.KerningRecord(stream,
                                               self.font_flags_wide_codes))

    def display(self):
        log("FontID: {s}".format(s=self.font_id))
        log("FontFlagsHasLayout: {s}".format(s=self.font_flags_has_layout))
        log("FontFlagsShiftJIS: {s}".format(s=self.font_flags_shiftJIS))
        log("FontFlagsSmallText: {s}".format(s=self.font_flags_small_text))
        log("FontFlagsANSI: {s}".format(s=self.font_flags_ansi))
        log("FontFlagsWideOffsets: {s}".format(s=self.font_flags_wide_offsets))
        log("FontFlagsWideCodes: {s}".format(s=self.font_flags_wide_codes))
        log("FontFlagsItalic: {s}".format(s=self.font_flags_italic))
        log("FontFlagsBold: {s}".format(s=self.font_flags_bold))
        log("LanguageCode: {s}".format(s=self.language_code))
        log("FontNameLen: {s}".format(s=self.font_name_len))
        # TODO: Remaining

    
class SymbolClass(Tag):
    def parse(self,stream):
        num_symbols = stream.read('uintle:16')
        self.symbols = []
        for x in range(0,num_symbols):
            new_symbol = {'tag': stream.read('uintle:16'),
                         'name': datatypes.string(stream)}
            self.symbols.append(new_symbol)

class Metadata(Tag):
    def parse(self,stream):
        self.metadata = datatypes.string(stream)

class DefineScalingGrid(Tag):
    def parse(self,stream):
        self.character_id = stream.read('uintle:16')
        self.splitter = datatypes.Rect(stream)

class DoABC(Tag):
    pass

class DefineShape4(Tag):
    def parse(self,stream):
        self.shape_id = stream.read('uintle:16')
        self.shape_bounds = datatypes.Rect(stream)
        self.edge_bounds = datatypes.Rect(stream)
        stream.pos += 5
        self.uses_fill_winding_rule = stream.read('bool')
        self.uses_non_scaling_strokes = stream.read('bool')
        self.uses_scaling_strokes = stream.read('bool')
        self.shape = datatypes.ShapeWithStyle(stream,'DefineShape4')
    
    def display(self):
        log("ShapeID: {s}".format(s=self.shape_id))
        log("ShapeBounds: {s}".format(s=self.shape_bounds))
        log("EdgeBounds: {s}".format(s=self.edge_bounds))
        log("UsesFillWindingRule: {s}".format(s=self.uses_fill_winding_rule))
        log("UsesNonScalingStrokes: {s}".format(s=self.uses_non_scaling_strokes))
        log("UsesScalingStrokes: {s}".format(s=self.uses_scaling_strokes))
        # TODO: Add display output for ShapeWithStyle

class DefineMorphShape2(Tag):
    pass

class DefineSceneAndFrameLabelData(Tag):
    def parse(self,stream):
        self.scene_count = datatypes.EncodedU32(stream)
        self.scenes = []
        for x in xrange(0,scene_count):
            offset_data = {'offset' : datatypes.EncodedU32(stream),
                           'name' : datatypes.string(stream) }
            self.scenes.append(offset_data)
        self.frame_label_count = datatypes.EncodedU32(stream)
        self.frame_labels = []
        for x in xrange(0,scene_count):
            label_data = {'frame_number' : datatypes.EncodedU32(stream),
                          'frame_label' : datatypes.string(stream) }
            self.frame_labels.append(label_data)
        

class DefineBinaryData(Tag):
    pass

class DefineFontName(Tag):
    def parse(self,stream):
        self.font_id = stream.read('uintle:16')
        self.font_name = datatypes.string(stream)
        self.font_copyright = datatypes.string(stream)

class StartSound2(Tag):
    pass

class DefineBitsJPEG4(Tag):
    pass

class DefineFont4(Tag):
    pass


# ==== Summary data for tags ====

# 'datatypes' is mainly for reference when implementing;
# it gives me an idea how annoying the parser will be to get working.

tag_data =  { 0: {'class': End,
                  'min_version': 1,
                  'datatypes': [] },
              1: {'class': ShowFrame,
                  'min_version': 1,
                  'datatypes': [] },
              2: {'class': DefineShape,
                  'min_version': 1,
                  'datatypes': ['rect','shapewithstyle'] },
              4: {'class': PlaceObject,
                  'min_version': 1,
                  'datatypes': ['matrix',
                                'cxform'] },
              5: {'class': RemoveObject,
                  'min_version': 1,
                  'datatypes': [] },
              6: {'class': DefineBits,
                  'min_version': 1,
                  'datatypes': ['UI8[image size] (JPEG data)'] },
              7: {'class': DefineButton,
                  'min_version': 1,
                  'datatypes': ['buttonrecord[]','actionrecord[]'] },
              8: {'class': JPEGTables,
                  'min_version': 1,
                  'datatypes': ['UI8[encoding size] (JPEG enc. table)'] },
              9: {'class': SetBackgroundColor,
                  'min_version': 1,
                  'datatypes': ['rgb'] },
             10: {'class': DefineFont,
                  'min_version': 1,
                  'datatypes': ['UI16[nGlyphs] (array of offsets)',
                                'SHAPE[nGlyphs] (array of shapes)'] },
             11: {'class': DefineText,
                  'min_version': 1,
                  'datatypes': ['rect','matrix','textrecord[]'] },
             12: {'class': DoAction,
                  'min_version': 3,
                  'datatypes': ['actionrecord'] },
             13: {'class': DefineFontInfo,
                  'min_version': 1,
                  'datatypes': ['UI8[FontNameLen] (font name)',
                                'UI16/8[nGlyphs] (glyph->code table)'] },
             14: {'class': DefineSound,
                  'min_version': 1,
                  'datatypes': ['UI8[size of sound data]'] },
             15: {'class': StartSound,
                  'min_version': 1,
                  'datatypes': ['soundinfo'] },
             17: {'class': DefineButtonSound,
                  'min_version': 2,
                  'datatypes': ['soundinfo'] },
             18: {'class': SoundStreamHead,
                  'min_version': 1,
                  'datatypes': [] },
             19: {'class': SoundStreamBlock,
                  'min_version': 1,
                  'datatypes': ['UI8[size of compressed data]'] },
             20: {'class': DefineBitsLossless,
                  'min_version': 2,
                  'datatypes': ['colormapdata','bitmapdata'] },
             21: {'class': DefineBitsJPEG2,
                  'min_version': 2,
                  'datatypes': ['UI8[data size] (JPEG/PNG/GIF data)'] },
             22: {'class': DefineShape2,
                  'min_version': 2,
                  'datatypes': ['rect','shapewithstyle'] },
             23: {'class': DefineButtonCxform,
                  'min_version': 2,
                  'datatypes': ['cxform'] },
             24: {'class': Protect,
                  'min_version': 2,
                  'datatypes': ['string'] }, # sometimes
             26: {'class': PlaceObject2,
                  'min_version': 3,
                  'datatypes': ['matrix',
                                'cxformwithalpha',
                                'string',
                                'clipactions'] },
             28: {'class': RemoveObject2,
                  'min_version': 3,
                  'datatypes': [] },
             32: {'class': DefineShape3,
                  'min_version': 3,
                  'datatypes': ['rect','shapewithstyle'] },
             33: {'class': DefineText2,
                  'min_version': 3,
                  'datatypes': ['rect','matrix','textrecord[]'] },
             34: {'class': DefineButton2,
                  'min_version': 3,
                  'datatypes': ['buttonrecord[]','buttoncondaction[]'] },
             35: {'class': DefineBitsJPEG3,
                  'min_version': 2,
                  'datatypes': ['UI8[data size] (JPEG/PNG/GIF data)',
                                'UI8[alpha size] (alpha data)'] },
             36: {'class': DefineBitsLossless2,
                  'min_version': 3,
                  'datatypes': ['alphacolormapdata','alphabitmapdata'] },
             37: {'class': DefineEditText,
                  'min_version': 4,
                  'datatypes': ['rect','string','rgba'] },
             39: {'class': DefineSprite,
                  'min_version': 3,
                  'datatypes': ['tag[]'] },
             43: {'class': FrameLabel,
                  'min_version': 3,
                  'datatypes': ['string'] }, # TODO: Deal with NamedAnchor (p.54)
             45: {'class': SoundStreamHead2,
                  'min_version': 3, # TODO: a guess
                  'datatypes': [] },
             46: {'class': DefineMorphShape,
                  'min_version': 3,
                  'datatypes': ['rect',
                                'morphfillstylearray',
                                'morphlinestylearray',
                                'shape'] }, # TODO: Also shapewithstyle?
             48: {'class': DefineFont2,
                  'min_version': 3,
                  'datatypes': ['langcode',
                                'UI8[FontNameLen] (font name)',
                                'UI32/16[nGlyphs] (array of offsets)',
                                'SHAPE[nGlyphs] (array of shapes)',
                                'RECT[nGlyphs]',
                                'kerningrecord[KerningCount]'] },
             56: {'class': ExportAssets,
                  'min_version': 5,
                  'datatypes': ['string'] },
             57: {'class': ImportAssets,
                  'min_version': 5,
                  'datatypes': ['string'] },
             58: {'class': EnableDebugger,
                  'min_version': 5,
                  'datatypes': ['string'] },
             59: {'class': DoInitAction,
                  'min_version': 6,
                  'datatypes': ['actionrecord'] },
             60: {'class': DefineVideoStream,
                  'min_version': 6,
                  'datatypes': [] },
             61: {'class': VideoFrame,
                  'min_version': 6,
                  'datatypes': ['h263videopacket',
                                'screenvideopacket',
                                'vp6swfvideopacket',
                                'vp6swfalphavideopacket',
                                'screenv2videopacket'] },
             62: {'class': DefineFontInfo2,
                  'min_version': 6,
                  'datatypes': ['UI8[FontNameLen] (font name)',
                                'langcode',
                                'UI16[nGlyphs] (glyph->code table)'] },
             64: {'class': EnableDebugger2,
                  'min_version': 6,
                  'datatypes': ['string'] },
             65: {'class': ScriptLimits,
                  'min_version': 7,
                  'datatypes': [] },
             66: {'class': SetTabIndex,
                  'min_version': 7,
                  'datatypes': [] },
             69: {'class': FileAttributes,
                  'min_version': 8,
                  'datatypes': [] },
             70: {'class': PlaceObject3,
                  'min_version': 8,
                  'datatypes': ['string',
                                'matrix',
                                'cxformwithalpha',
                                'filterlist',
                                'clipactions'] },
             71: {'class': ImportAssets2,
                  'min_version': 8,
                  'datatypes': ['string'] },
             73: {'class': DefineFontAlignZones,
                  'min_version': 8,
                  'datatypes': ['zonerecord[GlyphCount]'] },
             74: {'class': CSMTextSettings,
                  'min_version': 8,
                  'datatypes': ['f32 (32-bit float, I think)'] },
             75: {'class': DefineFont3,
                  'min_version': 8,
                  'datatypes': ['langcode',
                                'UI8[FontNameLen] (font name)',
                                'UI32/16[nGlyphs] (array of offsets)',
                                'SHAPE[nGlyphs] (array of shapes)',
                                'RECT[nGlyphs]',
                                'kerningrecord[KerningCount]'] },
             76: {'class': SymbolClass,
                  'min_version': 10, # TODO: This is a guess, it's not in the v10 spec. Check which version AS3 is introduced in.
                  'datatypes': ['string'] },
             77: {'class': Metadata,
                  'min_version': 1, # TODO: I think it should be 10, but the spec says 1...
                  'datatypes': ['string'] },
             78: {'class': DefineScalingGrid,
                  'min_version': 10, # TODO: Also a guess.
                  'datatypes': ['rect'] },
             82: {'class': DoABC,
                  'min_version': 9,
                  'datatypes': ['string','byte[] (AS3 bytecode)'] },
             83: {'class': DefineShape4,
                  'min_version': 8,
                  'datatypes': ['rect','shapewithstyle'] },
             84: {'class': DefineMorphShape2,
                  'min_version': 8,
                  'datatypes': ['rect',
                                'morphfillstylearray',
                                'morphlinestylearray',
                                'shape'] }, # TODO: Also shapewithstyle?
             86: {'class': DefineSceneAndFrameLabelData,
                  'min_version': 10, # TODO: Also a guess.
                  'datatypes': ['string','encodedU32'] },
             87: {'class': DefineBinaryData,
                  'min_version': 9,
                  'datatypes': ['binary'] },
             88: {'class': DefineFontName,
                  'min_version': 9,
                  'datatypes': ['string'] },
             89: {'class': StartSound2,
                  'min_version': 9,
                  'datatypes': ['string','soundinfo'] },
             90: {'class': DefineBitsJPEG4,
                  'min_version': 10,
                  'datatypes': ['UI8[data size] (JPEG/PNG/GIF data)',
                                'UI8[alpha size] (alpha data)'] },
             91: {'class': DefineFont4,
                  'min_version': 10,
                  'datatypes': ['string','fontdata'] },
             }

def class_from_tag_number(number):
    if number in tag_data:
        return tag_data[number]['class']
    else:
        return None
