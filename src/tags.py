'''
Created on 15 Oct 2011

@author: Bluebottle
'''
import os
import struct
from actions import ActionFactory
import datatypes

class TagFactory(object):
    @staticmethod
    def new_tag(swf_version,stream,tag_type,tag_length):
        tag_class = class_from_tag_number(tag_type)
        if tag_class is not None:
            print "  Creating new tag: {0}, length {1}".format(tag_class.__name__,tag_length)
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
            print "Display function not implemented."
        else:
            print "Parser not implemented."

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
    pass

class PlaceObject(Tag):
    def parse(self,stream):
        self.character_id = stream.read('uintle:16')
        self.depth = stream.read('uintle:16')
        self.matrix = datatypes.Matrix(stream)
        self.color_transform = datatypes.Cxform(stream)
    
    def display(self):
        print "CharacterId:",self.character_id
        print "Depth:",self.depth
        print "Matrix:",self.matrix
        print "ColorTransform:",self.color_transform

class RemoveObject(Tag):
    def parse(self,stream):
        self.character_id = stream.read('uintle:16')
        self.depth = stream.read('uintle:16')
    
    def display(self):
        print "CharacterId:",self.character_id
        print "Depth:",self.depth

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
        print "BackgroundColor:",self.background_color

class DefineFont(Tag):
    pass

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
            print "  == Action {0}: {1} ==".format(i,action.__class__.__name__)
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
        print "PlaybackSoundRate:",self.playback_sound_rate
        print "PlaybackSoundSize:",self.playback_sound_size
        print "PlaybackSoundType:",self.playback_sound_type
        print "StreamSoundCompression:",self.stream_sound_compression
        print "StreamSoundRate:",self.stream_sound_rate
        print "StreamSoundSize:",self.stream_sound_size
        print "StreamSoundType:",self.stream_sound_type
        print "StreamSoundSampleCount:",self.stream_sound_sample_count
        if self.stream_sound_compression == 2:
            print "LatencySeek:",self.latency_seek

class SoundStreamBlock(Tag):
    pass

class DefineBitsLossless(Tag):
    pass

class DefineBitsJPEG2(Tag):
    pass

class DefineShape2(Tag):
    pass

class DefineButtonCxform(Tag):
    def parse(self,stream):
        self.button_id = stream.read('uintle:16')
        self.button_color_transform = datatypes.Cxform(stream)
    
    def display(self):
        print "ButtonId:",self.button_id
        print "ButtonColorTransform:",self.button_color_transform

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
        print "FlagHasClipActions:",self.has_clip_actions
        print "FlagHasClipDepth:",self.has_clip_depth
        print "FlagHasName:",self.has_name
        print "FlagHasRatio:",self.has_ratio
        print "FlagHasColorTransform:",self.has_color_transform
        print "FlagHasMatrix:",self.has_matrix
        print "FlagHasCharacter:",self.has_character
        print "FlagMove:",self.move
        print "Depth:",self.depth
        if self.has_character:
            print "CharacterId:",self.character_id
        if self.has_matrix:
            print "Matrix:",self.matrix
        if self.has_color_transform:
            print "ColorTransform:",self.color_transform
        if self.has_ratio:
            print "Ratio:",self.ratio
        if self.has_name:
            print "Name:",self.name
        if self.has_clip_depth:
            print "ClipDepth:",self.clip_depth
        if self.has_clip_actions:
            print "ClipActions:",self.clip_actions

class RemoveObject2(Tag):
    def parse(self,stream):
        self.depth = stream.read('uintle:16')
    
    def display(self):
        print "Depth:",self.depth

class DefineShape3(Tag):
    pass

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
        print "CharacterId:",self.character_id
        print "Bounds:",self.bounds
        print "HasText:",self.has_text
        print "WordWrap:",self.word_wrap
        print "Multiline:",self.multiline
        print "Password:",self.password
        print "ReadOnly:",self.read_only
        print "HasTextColor:",self.has_text_color
        print "HasMaxLength:",self.has_max_length
        print "HasFont:",self.has_font
        print "HasFontClass:",self.has_font_class
        print "AutoSize:",self.auto_size
        print "HasLayout:",self.has_layout
        print "NoSelect:",self.no_select
        print "Border:",self.border
        print "WasStatic:",self.was_static
        print "HTML:",self.html
        print "UseOutlines:",self.use_outlines
        if self.has_font:
            print "FontId:",self.font_id
        if self.has_font_class:
            print "FontClass:",self.font_class
        if self.has_font:
            print "FontHeight:",self.font_height
        if self.has_text_color:
            print "TextColor:",self.text_color
        if self.has_max_length:
            print "MaxLength:",self.max_length
        if self.has_layout:
            print "Align:",self.align
            print "LeftMargin:",self.left_margin
            print "RightMargin:",self.right_margin
            print "Indent:",self.indent
            print "Leading:",self.leading
        print "VariableName:",self.variable_name
        if self.has_text:
            print "InitialText:",self.initial_text


class DefineSprite(Tag):
    def parse(self,stream):
        self.sprite_id = stream.read('uintle:16')
        self.frame_count = stream.read('uintle:16')
        self.tags = []
        current_tag_type = -1
        while stream.pos < stream.len and current_tag_type != 0:
            tag_header = stream.read('uintle:16')
            current_tag_type = tag_header >> 6 # Ignore the bottom 6 bits
            current_tag_length = tag_header & 0x3F # Only keep bottom 6 bits
            if current_tag_length == 0x3f:
                # If it's actually 63, use the long record header form instead.
                current_tag_length = stream.read('intle:32')
            tag_stream = stream.read('bits:{0}'.format(current_tag_length*8))
            new_tag = TagFactory.new_tag(self.swf_version,
                                         tag_stream,
                                         current_tag_type,
                                         current_tag_length)
            self.tags.append(new_tag)
    
    def display(self):
        print "SpriteId:",self.sprite_id
        print "FrameCount:",self.frame_count
        print "Sprite contains the following tags:"
        for i, tag in enumerate(self.tags):
            print "tag {0}: {1}".format(i,tag.__class__.__name__)
            tag.display()



class FrameLabel(Tag):
    def parse(self,stream):
        self.name = datatypes.string(stream)
        if stream.pos < stream.length and stream.peek('uintle:8') == 1:
            self.is_named_anchor = True
        else:
            self.is_named_anchor = False
    
    def display(self):
        print "Name:",self.name
        print "Is NamedAnchor:",self.is_named_anchor

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
        print "PlaybackSoundRate:",self.playback_sound_rate
        print "PlaybackSoundSize:",self.playback_sound_size
        print "PlaybackSoundType:",self.playback_sound_type
        print "StreamSoundCompression:",self.stream_sound_compression
        print "StreamSoundRate:",self.stream_sound_rate
        print "StreamSoundSize:",self.stream_sound_size
        print "StreamSoundType:",self.stream_sound_type
        print "StreamSoundSampleCount:",self.stream_sound_sample_count
        if self.stream_sound_compression == 2:
            print "LatencySeek:",self.latency_seek

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
            print "  == Action {0}: {1} ==".format(i,action.__class__.__name__)
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
        self.pos += 16
        self.password_hash = datatypes.string(stream)

class ScriptLimits(Tag):
    def parse(self,stream):
        self.max_recursion_depth = stream.read('uintle:16')
        self.script_timeout_seconds = stream.read('uintle:16')
        
    def display(self):
        print "MaxRecursionDepth:",self.max_recursion_depth
        print "ScriptTimeoutSeconds:",self.script_timeout_seconds

class SetTabIndex(Tag):
    def parse(self,stream):
        self.depth = stream.read('uintle:16')
        self.tab_index = stream.read('uintle:16')
    
    def display(self):
        print "Depth:",self.depth
        print "TabIndex:",self.tab_index

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
        print "UseDirectBit:",self.use_direct_bit
        print "UseGPU:",self.use_gpu
        print "HasMetadata:",self.has_metadata
        print "UseNetwork:",self.use_network

class PlaceObject3(Tag):
    pass

class ImportAssets2(Tag):
    def parse(self,stream):
        self.url = datatypes.string(stream)
        self.pos += 16
        count = stream.read('uintle:16')
        self.assets = []
        for x in range(0,count):
            new_asset = {'tag': stream.read('uintle:16'),
                         'name': datatypes.string(stream)}
            self.assets.append(new_asset)

class DefineFontAlignZones(Tag):
    pass

class CSMTextSettings(Tag):
    pass

class DefineFont3(Tag):
    pass

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
    pass

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

# ========

def define_shape(stream):
    print "ShapeId:",stream.read('uintle:16')
    print "ShapeBounds:"
    stream = datatypes.rect(stream)
    datatypes.shape_with_style(stream,"DefineShape")

def define_shape_2(stream):
    print "ShapeId:",stream.read('uintle:16')
    print "ShapeBounds:"
    stream = datatypes.rect(stream)
    datatypes.shape_with_style(stream,"DefineShape2")

def define_shape_3(stream):
    print "ShapeId:",stream.read('uintle:16')
    print "ShapeBounds:"
    stream = datatypes.rect(stream)
    datatypes.shape_with_style(stream,"DefineShape3")
    
def define_shape_4(stream):
    print "ShapeId:",stream.read('uintle:16')
    print "ShapeBounds:"
    stream = datatypes.rect(stream)
    print "EdgeBounds:"
    stream = datatypes.rect(stream)
    stream.pos += 5
    print "UsesFillWindingRule:",stream.read('bool')
    print "UsesNonScalingStrokes:",stream.read('bool')
    print "UsesScalingStrokes:",stream.read('bool')
    datatypes.shape_with_style(stream,"DefineShape4")
    
def define_text(stream):
    print "FontId:",stream.read('uintle:16')
    starting_bytepos = stream.bytepos
    n_glyphs = stream.peek('uintle:16') / 2
    for glyph_number in range(n_glyphs):
        stream.bytepos = starting_bytepos + (2 * glyph_number)
        glyph_offset = stream.read('uintle:16')
        stream.bytepos = starting_bytepos + glyph_offset
        datatypes.shape(stream,"DefineText")

def do_init_action(stream):
    print "SpriteID:",stream.read('uintle:16')
    action_number = 0
    action_name = ''
    while action_name != 'ActionEndFlag':
        print "   == Reading action",action_number,"== "
        action_code = stream.read('uintle:8')
        if action_code >= 0x80:
            # If it's actually 63, we're using the long record header form instead.
            action_length = stream.read('uintle:16')
        else:
            action_length = None
        action_name = datatypes.get_action_type_name_from_number(action_code)
        print "  Action type:",action_code,action_name
        action_number += 1
        if action_length:
            print "  Action length:",action_length,"bytes"
            action_parser = get_action_parser_from_number(action_code)
            action_parser(stream.read('bits:%d' % (action_length*8)))         
        
def define_bits_jpeg_2(stream):
    character_id = stream.read('uintle:16')
    print "Character ID:",character_id
    filename = "%d.jpeg" % character_id
    if stream.peek(32) == '0xffd9ffd8': # Some SWF versions before 8 erroneously have an extra JPEG EOI and SOI pair before the actual SOI.
        stream.read(32) # In that case, we just throw away the extra 4 bytes.
    try:
        f = open(os.path.join("../output",filename),'wb')
        while stream.pos < stream.len:
            f.write(struct.pack('b',stream.read('int:8')))
    finally:
        f.close()
        print "Wrote JPEG data to",filename

def define_sprite(stream):
    #print '%r' % data
    sprite_id = stream.read('uintle:16')
    frame_count = stream.read('uintle:16')
    print "Sprite ID:",sprite_id
    print "Frame count:",frame_count
    print "Sprite contains tags:"
    tag_name = ''
    while stream.pos < stream.len and tag_name != 'End':
        current_pos = stream.pos
        tag_name, tag_length, is_long_header = datatypes.record_header(stream)
        print tag_name,"- length",tag_length,"bytes"
        if is_long_header:
            stream.pos = current_pos + (tag_length*8) + 48
        else:
            stream.pos = current_pos + (tag_length*8) + 16
        
def not_implemented(data):
    print "No parser for this tag yet."
    
# == The list of action parser functions ==

def get_action_parser_from_number(number):
    action_functions = {0x81: action_parsers.goto_frame,
                        0x83: action_parsers.get_url,
                        0x88: action_parsers.constant_pool,
                        0x8a: action_parsers.wait_for_frame,
                        0x8b: action_parsers.set_target,
                        0x8c: action_parsers.goto_label,
                        0x8d: action_parsers.wait_for_frame_2,
                        0x8e: action_parsers.define_function_2,
                        0x8f: action_parsers.action_try,
                        0x94: action_parsers.action_with,
                        0x96: action_parsers.push,
                        0x99: action_parsers.jump,
                        0x9a: action_parsers.get_url_2,
                        0x9b: action_parsers.define_function,
                        0x9d: action_parsers.action_if,
                        0x9f: action_parsers.goto_frame_2,
                        }
    if number in action_functions:
        return action_functions[number]
    else:
        return action_parsers.not_implemented

