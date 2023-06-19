# coding:utf-8
# noinspection PyUnresolvedReferences
import arnold as ai

import os

import re

import ctypes

import shlex

import subprocess

import platform

from lxbasic import bsc_configure, bsc_core

import lxbasic.objects as bsc_objects

from lxutil import utl_core

import lxutil.configures as utl_configures

from lxuniverse import unr_configure

from lxarnold import and_configure

ACES_COLOR_CONFIGURE = bsc_objects.Properties(
    None, bsc_core.CfgFileMtd.get_yaml('colorspace/aces-color')
)

if platform.system().lower() == 'windows':
    # noinspection PyUnresolvedReferences
    NO_WINDOW = subprocess.STARTUPINFO()
    NO_WINDOW.dwFlags |= subprocess.STARTF_USESHOWWINDOW
else:
    NO_WINDOW = None


class AndTypeMtd(object):
    def __init__(self, type_):
        self._and_instance = type_
    @property
    def and_instance(self):
        return self._and_instance
    @property
    def name(self):
        return ai.AiParamGetTypeName(self.and_instance)

    def get_is_array(self):
        return self.and_instance == ai.AI_TYPE_ARRAY

    def get_dcc_type_args(self, is_array):
        dcc_type_name = and_configure.Type.get_name(self.and_instance)
        dcc_category_name = unr_configure.Type.get_category_name(dcc_type_name, is_array)
        return dcc_category_name, dcc_type_name

    def get_dcc_channel_names(self):
        dcc_type_name = and_configure.Type.get_name(self.and_instance)
        return unr_configure.Type.get_channel_names(dcc_type_name)


class AndArrayMtd(object):
    def __init__(self, array):
        self._and_instance = array

    @property
    def and_instance(self):
        return self._and_instance

    def get_element_count(self):
        return ai.AiArrayGetNumElements(self.and_instance)


class AndPortMtd(object):
    def __init__(self, obj, port):
        self._obj = obj
        self._and_instance = port
    @property
    def obj(self):
        return self._obj
    @property
    def category(self):
        if self.get_type_is_array():
            return ai.AI_TYPE_ARRAY
        return ai.type
    @property
    def type(self):
        return ai.AiParamGetType(self.and_instance)
    @property
    def type_name(self):
        return ai.AiParamGetTypeName(self.type)
    @property
    def exact_type(self):
        if self.get_type_is_array():
            return ai.AiArrayGetType(ai.AiParamGetDefault(self.and_instance).contents.ARRAY.contents)
        return self.type
    @property
    def exact_type_name(self):
        return ai.AiParamGetTypeName(self.exact_type)
    @property
    def port(self):
        return self.and_instance
    @property
    def and_instance(self):
        return self._and_instance
    @property
    def port_name(self):
        return ai.AiParamGetName(self.and_instance)

    def get_array(self):
        return ai.AiNodeGetArray(self.obj, self.port_name)

    def get_array_element_count(self):
        return ai.AiArrayGetNumElements(self.get_array())

    def get_type_is_array(self):
        return self.type == ai.AI_TYPE_ARRAY

    def get_is_enumerate_type(self):
        return self.type == ai.AI_TYPE_ENUM

    def get_enumerate_strings(self):
        and_port = self.and_instance
        strings = []
        and_port = ai.AiParamGetEnum(and_port)
        i = 0
        t = True
        while t:
            try:
                t = ai.AiEnumGetString(and_port, i)
                if t:
                    strings.append(t)
            except UnicodeDecodeError as e:
                raise e
            i += 1
        return strings

    def get(self):
        return self._get_raw_()

    def _get_raw_(self):
        if self.get_type_is_array() is True:
            return self._get_array_raw_()
        return self._get_constant_raw_()

    def _get_constant_raw_(self):
        and_obj = self.obj
        and_type = self.type
        and_port = self.and_instance
        and_port_name = self.port_name
        if and_type in and_configure.Port.AR_VALUE_FNC_DICT:
            fnc = and_configure.Port.AR_VALUE_FNC_DICT[and_type]
            if fnc is not None:
                raw = fnc(and_obj, and_port_name)
                return self._set_raw_convert_to_dcc_style_(and_type, and_port, raw)

    def _get_array_raw_(self):
        and_port = self.and_instance
        #
        and_exact_type = self.exact_type
        if and_exact_type in and_configure.Port.AR_ARRAY_VALUE_FNC_DICT:
            lis = []
            fnc = and_configure.Port.AR_ARRAY_VALUE_FNC_DICT[and_exact_type]
            and_array = self.get_array()
            and_array_element_count = AndArrayMtd(and_array).get_element_count()
            for and_array_element_index in range(and_array_element_count):
                raw = fnc(and_array, and_array_element_index)
                lis.append(
                    self._set_raw_convert_to_dcc_style_(and_exact_type, and_port, raw)
                )
            return lis

    def get_default(self):
        return self._get_default_raw_()

    def _get_default_raw_(self):
        if self.get_type_is_array() is True:
            return self._get_default_array_raw_()
        return self._get_default_constant_raw_()

    def _get_default_constant_raw_(self):
        and_type = self.type
        and_port = self.and_instance
        if and_type in and_configure.Port.AR_DEFAULT_VALUE_FNC_DICT:
            fnc = and_configure.Port.AR_DEFAULT_VALUE_FNC_DICT[and_type]
            raw = fnc(and_port)
            return self._set_raw_convert_to_dcc_style_(and_type, and_port, raw)

    def _get_default_array_raw_(self):
        and_port = self.and_instance
        and_exact_type = self.exact_type
        if and_exact_type in and_configure.Port.AR_ARRAY_VALUE_FNC_DICT:
            lis = []
            fnc = and_configure.Port.AR_ARRAY_VALUE_FNC_DICT[and_exact_type]
            ar_array_default = ai.AiParamGetDefault(and_port).contents.ARRAY.contents
            and_array_element_count = ai.AiArrayGetNumElements(ar_array_default)
            for and_array_element_index in range(and_array_element_count):
                raw = fnc(ar_array_default, and_array_element_index)
                lis.append(
                    self._set_raw_convert_to_dcc_style_(and_exact_type, and_port, raw)
                )
            return lis
    @classmethod
    def _set_raw_convert_to_dcc_style_(cls, and_type, and_port, raw):
        # enumerate
        round_count = and_configure.Utility.ROUND
        if and_type is ai.AI_TYPE_ENUM:
            idx = raw
            return ai.AiEnumGetString(
                ai.AiParamGetEnum(and_port),
                idx
            )
        # color
        elif and_type is ai.AI_TYPE_RGB:
            rgb = raw
            _r, _g, _b = rgb.r, rgb.g, rgb.b
            _raw = round(_r, round_count), round(_g, round_count), round(_b, round_count)
        elif and_type is ai.AI_TYPE_RGBA:
            rgba = raw
            _r, _g, _b, _a = rgba.r, rgba.g, rgba.b, rgba.a
            _raw = round(_r, round_count), round(_g, round_count), round(_b, round_count), round(_a, round_count)
        # tuple/vector2
        elif and_type is ai.AI_TYPE_VECTOR2:
            vec = raw
            _x, _y = vec.x, vec.y
            _raw = round(_x, round_count), round(_y, round_count)
        # tuple/vector3
        elif and_type is ai.AI_TYPE_VECTOR:
            vec = raw
            _x, _y, _z = vec.x, vec.y, vec.z
            _raw = round(_x, round_count), round(_y, round_count), round(_z, round_count)
        # matrix44 (
        #      (float, float, float, float),
        #      (float, float, float, float),
        #      (float, float, float, float),
        #      (float, float, float, float)
        # )
        elif and_type is ai.AI_TYPE_MATRIX:
            mtx = raw
            if isinstance(mtx, ai.ai_matrix.AtMatrix) is False:
                mtx = raw[0]
            _raw = tuple([tuple([mtx[i][j] for j in xrange(4)]) for i in xrange(4)])
        # node
        elif and_type is ai.AI_TYPE_NODE:
            node = raw
            _raw = ai.AiNodeGetName(node)
        # float:
        elif and_type is ai.AI_TYPE_FLOAT:
            _raw = round(raw, round_count)
        else:
            _raw = raw
        return _raw


class AndCustomPortMtd(AndPortMtd):
    def __init__(self, obj, port):
        super(AndCustomPortMtd, self).__init__(obj, port)
    @property
    def type(self):
        return ai.AiUserParamGetType(self.and_instance)
    @property
    def exact_type(self):
        if self.get_type_is_array():
            return ai.AiUserParamGetArrayType(self.and_instance)
        return self.type
    @property
    def port_name(self):
        return ai.AiUserParamGetName(self.and_instance)

    def get(self):
        return self._get_raw_()

    def get_default(self):
        return None


class AndObjTypeMtd(object):
    def __init__(self, type_):
        self._and_instance = type_
    @property
    def and_instance(self):
        return self._and_instance
    @property
    def name(self):
        return ai.AiNodeEntryGetName(self.and_instance)
    @property
    def output_type(self):
        return ai.AiNodeEntryGetOutputType(self._and_instance)


class AndObjMtd(object):
    PORT_MTD_CLS = AndPortMtd
    CUSTOM_PORT_MTD_CLS = AndCustomPortMtd
    def __init__(self, universe, obj):
        self._universe = universe
        self._and_instance = obj
        self._and_obj_type_instance = ai.AiNodeGetNodeEntry(obj)
        self._obj_category = ai.AiNodeEntryGetType(self._and_obj_type_instance)
    @property
    def universe(self):
        return self._universe
    @property
    def obj(self):
        return self.and_instance
    @property
    def and_instance(self):
        return self._and_instance
    @property
    def name(self):
        return ai.AiNodeGetName(self.and_instance)
    @property
    def category(self):
        return self._obj_category
    @property
    def category_name(self):
        return ai.AiNodeEntryGetTypeName(self.type)
    @property
    def type(self):
        return self._and_obj_type_instance
    @property
    def type_name(self):
        return AndObjTypeMtd(self.type).name
    @property
    def output_type(self):
        return ai.AiNodeEntryGetOutputType(self.type)
    @property
    def output_type_name(self):
        return ai.AiParamGetTypeName(self.output_type)

    def get_orig_name(self):
        return ai.AiNodeGetName(self.and_instance)
    @classmethod
    def set_name_clear(cls, name):
        return re.sub(
            ur'[^\u4e00-\u9fa5a-zA-Z0-9]', '_', name
        )

    def set_name_prettify(self, index, look_pass_name=None, time_tag=None):
        type_name = self.type_name
        tags = [
            type_name, index, look_pass_name, time_tag
        ]
        return '_'.join([str(i) for i in tags if i is not None])

    def get_parent(self):
        return ai.AiNodeGetParent(self.and_instance)

    def get_port(self, port_name):
        return ai.AiNodeEntryLookUpParameter(self.type, port_name)

    def get_port_mtd(self, port_name):
        return self.PORT_MTD_CLS(self.and_instance, self.get_port(port_name))

    def get_customize_port(self, port_name):
        return ai.AiNodeLookUpUserParameter(self.and_instance, port_name)

    def get_array_port(self, port_name):
        return ai.AiNodeGetArray(self.and_instance, port_name)

    def get_port_has_source(self, port_name):
        return ai.AiNodeIsLinked(self.and_instance, port_name)
    # dcc
    def get_dcc_port_source_args(self, port_name):
        and_obj = self.and_instance
        #
        and_output_port_index = ctypes.c_int()
        and_source_obj = ai.AiNodeGetLink(and_obj, port_name, ctypes.byref(and_output_port_index))
        if and_source_obj:
            source_and_obj_mtd = self.__class__(self.universe, and_source_obj)
            source_and_obj_name = source_and_obj_mtd.name
            and_output_port_index_value = and_output_port_index.value
            and_type = source_and_obj_mtd.output_type
            #
            dcc_obj_output_name = and_configure.Node.get_output_name(and_type)
            # port-connection / element-connection
            if and_output_port_index_value == -1:
                dcc_source_port_args = (dcc_obj_output_name,)
            # channel-connection
            else:
                dcc_port_channel_names = AndTypeMtd(and_type).get_dcc_channel_names()
                dcc_source_port_args = dcc_obj_output_name, dcc_port_channel_names[and_output_port_index_value]
            return ('', source_and_obj_name), dcc_source_port_args

    def get_dcc_output_port_name(self):
        output_type = self.output_type
        return and_configure.Node.get_output_name(output_type)

    def get_input_ports(self):
        input_dict = {}

        it = ai.AiNodeEntryGetParamIterator(ai.AiNodeGetNodeEntry(self._and_instance))
        while not ai.AiParamIteratorFinished(it):
            i_and_input_port = ai.AiParamIteratorGetNext(it)
            # OSL parameters start with "param_"
            if str(ai.AiParamGetName(i_and_input_port)).startswith("param_"):
                paramName = ai.AiParamGetName(i_and_input_port)
                i_and_input_port_opt = AndPortMtd(self._and_instance, i_and_input_port)
                input_dict[paramName] = {}
                input_dict[paramName]['paramName'] = i_and_input_port_opt.port_name
                input_dict[paramName]['paramType'] = i_and_input_port_opt.type_name
                input_dict[paramName]['paramDefaultValue'] = i_and_input_port_opt.get_default()
        return input_dict


class AndShapeObjMtd(AndObjMtd):
    def __init__(self, universe, obj):
        super(AndShapeObjMtd, self).__init__(universe, obj)

    def get_maya_path(self):
        return AndCustomPortMtd(self.and_instance, self.get_customize_port('maya_full_name')).get()

    def get_surface_shader_objs(self):
        and_obj_type_name = self.type_name
        if and_obj_type_name in [and_configure.ObjType.AND_MESH_NAME, and_configure.ObjType.AND_CURVE_NAME]:
            shader_names = self.get_port_mtd('shader').get() or []
            return [AndUniverseMtd(self.universe).get_obj(i) for i in shader_names]
        elif and_obj_type_name in [and_configure.ObjType.AND_XGEN_NAME]:
            shader_names = AndCustomPortMtd(self.and_instance, self.get_customize_port('xgen_shader')).get() or []
            if shader_names:
                return [AndUniverseMtd(self.universe).get_obj(i) for i in shader_names]
            #
            shader_names = self.get_port_mtd('shader').get() or []
            return [AndUniverseMtd(self.universe).get_obj(i) for i in shader_names]

    def get_displacement_shader_objs(self):
        and_obj_type_name = self.type_name
        if and_obj_type_name in [and_configure.ObjType.AND_MESH_NAME, and_configure.ObjType.AND_CURVE_NAME]:
            shader_names = self.get_port_mtd('disp_map').get() or []
            return [AndUniverseMtd(self.universe).get_obj(i) for i in shader_names]
        elif and_obj_type_name in [and_configure.ObjType.AND_XGEN_NAME]:
            shader_names = AndCustomPortMtd(self.and_instance, self.get_customize_port('xgen_disp_map')).get() or []
            if shader_names:
                return [AndUniverseMtd(self.universe).get_obj(i) for i in shader_names]
            #
            shader_names = self.get_port_mtd('disp_map').get() or []
            return [AndUniverseMtd(self.universe).get_obj(i) for i in shader_names]

    def get_visibility_port(self):
        return self.get_port('visibility')

    def get_sidedness_port(self):
        return self.get_port('sidedness')

    def get_visibility_raw(self):
        return self.get_port_mtd('visibility').get()

    def get_visibility_dict(self):
        return self._set_visibility_unpack_(self.get_visibility_raw())
    @classmethod
    def _set_visibility_unpack_(cls, raw):
        ar_rays = and_configure.Visibility.AR_RAY_ALL
        dic = {}
        for v in ar_rays:
            n = and_configure.Visibility.get_name(v)
            dic[n] = True
        comp = ai.AI_RAY_ALL
        if raw < comp:
            for v in reversed([v for v in ar_rays]):
                comp &= ~v
                if raw <= comp:
                    n = and_configure.Visibility.get_name(v)
                    dic[n] = False
                else:
                    comp += v
        return dic

    def get_sidedness_row(self):
        return self.get_port_mtd('sidedness').get()


class AndShaderObjMtd(AndObjMtd):
    def __init__(self, universe, obj):
        super(AndShaderObjMtd, self).__init__(universe, obj)


class AndUniverseMtd(object):
    OBJ_MTD_CLS = AndObjMtd
    def __init__(self, universe):
        self._and_instance = universe
    @property
    def and_instance(self):
        return self._and_instance

    def get_obj(self, obj_name):
        return ai.AiNodeLookUpByName(self.and_instance, obj_name)


def _set_ar_universe_only_begin():
    if not ai.AiUniverseIsActive():
        ai.AiBegin()
        ai.AiMsgSetConsoleFlags(ai.AI_LOG_NONE)
        return True
    return False


def _set_ar_universe_end():
    if ai.AiUniverseIsActive():
        if ai.AiRendering():
            ai.AiRenderInterrupt()
        if ai.AiRendering():
            ai.AiRenderAbort()
        ai.AiEnd()


class AndTextureOpt(object):
    """
    maketx -- convert images to tiled, MIP-mapped textures
    OpenImageIO-Arnold 2.2.1 http://www.openimageio.org
    Usage:  maketx [options] file...
        --help                   Print help message
        -v                       Verbose status messages
        -o %s                    Output filename
        --threads %d             Number of threads (default: #cores)
        -u                       Update mode
        --format %s              Specify output file format (default: guess from extension)
        --nchannels %d           Specify the number of output image channels.
        --chnames %s             Rename channels (comma-separated)
        -d %s                    Set the output data format to one of: uint8, sint8, uint16, sint16, half, float
        --tile %d %d             Specify tile size
        --separate               Use planarconfig separate (default: contiguous)
        --compression %s         Set the compression method (default = zip, if possible)
        --fovcot %f              Override the frame aspect ratio. Default is width/height.
        --wrap %s                Specify wrap mode (black, clamp, periodic, mirror)
        --swrap %s               Specific s wrap mode separately
        --twrap %s               Specific t wrap mode separately
        --resize                 Resize textures to power of 2 (default: no)
        --noresize               Do not resize textures to power of 2 (deprecated)
        --filter %s              Select filter for resizing (choices: box triangle gaussian sharp-gaussian catmull-rom blackman-harris sinc lanczos3 radial-lanczos3 nuke-lanczos6 mitchell bspline disk cubic keys simon rifman, default=box)
        --hicomp                 Compress HDR range before resize, expand after.
        --sharpen %f             Sharpen MIP levels (default = 0.0 = no)
        --nomipmap               Do not make multiple MIP-map levels
        --checknan               Check for NaN/Inf values (abort if found)
        --fixnan %s              Attempt to fix NaN/Inf values in the image (options: none, black, box3)
        --fullpixels             Set the 'full' image range to be the pixel data window
        --Mcamera %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f
                                 Set the camera matrix
        --Mscreen %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f
                                 Set the screen matrix
        --prman-metadata         Add prman specific metadata
        --attrib %s %s           Sets metadata attribute (name, value)
        --sattrib %s %s          Sets string metadata attribute (name, value)
        --sansattrib             Write command line into Software & ImageHistory but remove --sattrib and --attrib options
        --constant-color-detect  Create 1-tile textures from constant color inputs
        --monochrome-detect      Create 1-channel textures from monochrome inputs
        --opaque-detect          Drop alpha channel that is always 1.0
        --no-compute-average     Don't compute and store average color
        --ignore-unassoc         Ignore unassociated alpha tags in input (don't autoconvert)
        --runstats               Print runtime statistics
        --mipimage %s            Specify an individual MIP level
    Basic modes (default is plain texture):
        --shadow                 Create shadow map
        --envlatl                Create lat/long environment map
        --lightprobe             Create lat/long environment map from a light probe
        --bumpslopes             Create a 6 channels bump-map with height, derivatives and square derivatives from an height or a normal map
        --bumpformat %s          Specify the interpretation of a 3-channel input image for --bumpslopes: "height", "normal" or "auto" (default).
    Color Management Options (OpenColorIO DISABLED)
        --colorconfig %s         Explicitly specify an OCIO configuration file
        --colorconvert %s %s     Apply a color space conversion to the image. If the output color space is not the same bit depth as input color space, it is your responsibility to set the data format to the proper bit depth using the -d option.  (choices: sRGB, linear)
        --unpremult              Unpremultiply before color conversion, then premultiply after the color conversion.  You'll probably want to use this flag if your image contains an alpha channel.
    Configuration Presets
        --prman                  Use PRMan-safe settings for tile size, planarconfig, and metadata.
        --oiio                   Use OIIO-optimized settings for tile size, planarconfig, metadata.
    Arnold Extensions
        --colorengine            Select the color processor engine to use: ocio or syncolor
                                 (default: ocio, available: ocio, syncolor)
        --colorconfig            For OCIO, set the OCIO config (leave empty to use OCIO
                                 environment variable).
                                 For synColor, use this flag twice to set the native and
                                 the custom catalog paths.
    """
    TX_EXT = '.tx'
    def __init__(self, file_path):
        self._file_path = file_path

    def get_is_exists(self):
        return os.path.exists(self._file_path)

    def get_info(self):
        info = {}
        #
        file_path = self._file_path

        info['filename'] = file_path
        if os.path.isfile(file_path):
            info['bit_depth'] = ai.AiTextureGetBitDepth(file_path)
            info['format'] = ai.AiTextureGetFormat(file_path)
        else:
            info['bit_depth'] = 8
            info['format'] = "unknown"
        return info
    @utl_core.Modifier.debug_trace
    def get_resolution(self):
        return ai.AiTextureGetResolution(self._file_path)
    @utl_core.Modifier.debug_trace
    def get_bit_depth(self):
        return ai.AiTextureGetBitDepth(self._file_path)

    def get_type(self):
        return ai.AiTextureGetFormat(self._file_path)

    def get_color_space(self, use_aces=False):
        bit_depth = ai.AiTextureGetBitDepth(self._file_path)
        type_ = ai.AiTextureGetFormat(self._file_path)
        # noinspection PyBroadException
        try:
            is_srgb = bit_depth <= 16 and type_ in (ai.AI_TYPE_BYTE, ai.AI_TYPE_INT, ai.AI_TYPE_UINT)
            condition = use_aces, is_srgb
            if condition == (True, True):
                return 'Utility - sRGB - Texture'
            elif condition == (False, True):
                return 'sRGB'
            elif condition == (True, False):
                return 'Utility - Linear - sRGB'
            elif condition == (False, False):
                return 'linear'
            else:
                raise TypeError()
        except:
            bsc_core.LogMtd.trace_method_warning(
                'color-space-guess',
                u'file-obj="{}" guess color-space error'.format(self._file_path)
            )
            return 'linear'

    def get_modify_timestamp(self):
        if self.get_is_exists() is True:
            return os.stat(self._file_path).st_mtime

    def get_is_srgb(self):
        bit_depth = ai.AiTextureGetBitDepth(self._file_path)
        type_ = ai.AiTextureGetFormat(self._file_path)
        return bit_depth <= 16 and type_ in (ai.AI_TYPE_BYTE, ai.AI_TYPE_INT, ai.AI_TYPE_UINT)

    def get_is_linear(self):
        return not self.get_is_srgb()

    def get_is_8_bit(self):
        return self.get_bit_depth() <= 8

    def get_is_16_bit(self):
        return self.get_bit_depth() <= 16

    def get_path_as_tx(self):
        name = os.path.basename(self._file_path)
        name_base, ext = os.path.splitext(name)
        directory_path = os.path.dirname(self._file_path)
        return '{}/{}{}'.format(directory_path, name_base, self.TX_EXT)

    def get_is_exists_as_tx(self):
        tx_file_path = self.get_path_as_tx()
        if os.path.exists(tx_file_path) is True:
            timestamp = self.get_modify_timestamp()
            tx_timestamp = self.__class__(tx_file_path).get_modify_timestamp() or 0
            return timestamp == tx_timestamp
        else:
            return False


@utl_core.Modifier.debug_trace
def _get_resolution_(file_path):
    return ai.AiTextureGetResolution(file_path)


@utl_core.Modifier.debug_trace
def _get_bit_(file_path):
    return ai.AiTextureGetBitDepth(file_path)


@utl_core.Modifier.debug_trace
def _get_type_(file_path):
    return ai.AiTextureGetFormat(file_path)


@utl_core.Modifier.debug_trace
def _get_channels_count_(file_path):
    return ai.AiTextureGetNumChannels(file_path)


class AndImageOpt(object):
    @classmethod
    def _get_info_(cls, file_path):
        _f = file_path.encode("UTF8")
        width, height = _get_resolution_(_f) or (0, 0)
        dic = dict(
            bit=cls._get_bit_(file_path) or 0,
            type=cls._get_type_(_f),
            channel_count=_get_channels_count_(_f),
            width=width,
            height=height
        )
        return dic
    @staticmethod
    def _get_bit_(file_path):
        return ai.AiTextureGetBitDepth(file_path)
    @staticmethod
    def _get_type_(file_path):
        return ai.AiTextureGetFormat(file_path)
    @staticmethod
    def _get_channel_count_(file_path):
        return ai.AiTextureGetNumChannels(file_path)
    @classmethod
    def _get_is_srgb_(cls, file_path):
        return (
            cls._get_bit_(file_path) <= 16
            and cls._get_type_(file_path) in (ai.AI_TYPE_BYTE, ai.AI_TYPE_INT, ai.AI_TYPE_UINT)
        )
    @classmethod
    def _get_is_linear_(cls, file_path):
        return not cls._get_is_srgb_(file_path)
    @classmethod
    def _get_is_8_bit_(cls, file_path):
        return cls._get_bit_(file_path) <= 8
    @classmethod
    def _get_is_16_bit_(cls, file_path):
        return cls._get_bit_(file_path) <= 16
    #
    def __init__(self, file_path):
        self._file_path = file_path
        if os.path.isfile(file_path):
            self._file_path = file_path
            self._info = self._get_info_(
                self._file_path
            )
        else:
            raise OSError()

    @property
    def path(self):
        return self._file_path
    @property
    def size(self):
        return int(self._info['width']), int(self._info['height'])
    @property
    def bit(self):
        return self._info['bit']
    @property
    def type(self):
        return self._info['type']
    @property
    def channel_count(self):
        return self._info['channel_count']

    def get_is_8_bit(self):
        return self.bit <= 8

    def get_is_16_bit(self):
        return self.bit <= 16


class AndTextureOpt_(AndImageOpt):
    """
    maketx -- convert images to tiled, MIP-mapped textures
    OpenImageIO-Arnold 2.2.1 http://www.openimageio.org
    Usage:  maketx [options] file...
        --help                   Print help message
        -v                       Verbose status messages
        -o %s                    Output filename
        --threads %d             Number of threads (default: #cores)
        -u                       Update mode
        --format %s              Specify output file format (default: guess from extension)
        --nchannels %d           Specify the number of output image channels.
        --chnames %s             Rename channels (comma-separated)
        -d %s                    Set the output data format to one of: uint8, sint8, uint16, sint16, half, float
        --tile %d %d             Specify tile size
        --separate               Use planarconfig separate (default: contiguous)
        --compression %s         Set the compression method (default = zip, if possible)
        --fovcot %f              Override the frame aspect ratio. Default is width/height.
        --wrap %s                Specify wrap mode (black, clamp, periodic, mirror)
        --swrap %s               Specific s wrap mode separately
        --twrap %s               Specific t wrap mode separately
        --resize                 Resize textures to power of 2 (default: no)
        --noresize               Do not resize textures to power of 2 (deprecated)
        --filter %s              Select filter for resizing (choices: box triangle gaussian sharp-gaussian catmull-rom blackman-harris sinc lanczos3 radial-lanczos3 nuke-lanczos6 mitchell bspline disk cubic keys simon rifman, default=box)
        --hicomp                 Compress HDR range before resize, expand after.
        --sharpen %f             Sharpen MIP levels (default = 0.0 = no)
        --nomipmap               Do not make multiple MIP-map levels
        --checknan               Check for NaN/Inf values (abort if found)
        --fixnan %s              Attempt to fix NaN/Inf values in the image (options: none, black, box3)
        --fullpixels             Set the 'full' image range to be the pixel data window
        --Mcamera %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f
                                 Set the camera matrix
        --Mscreen %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f
                                 Set the screen matrix
        --prman-metadata         Add prman specific metadata
        --attrib %s %s           Sets metadata attribute (name, value)
        --sattrib %s %s          Sets string metadata attribute (name, value)
        --sansattrib             Write command line into Software & ImageHistory but remove --sattrib and --attrib options
        --constant-color-detect  Create 1-tile textures from constant color inputs
        --monochrome-detect      Create 1-channel textures from monochrome inputs
        --opaque-detect          Drop alpha channel that is always 1.0
        --no-compute-average     Don't compute and store average color
        --ignore-unassoc         Ignore unassociated alpha tags in input (don't autoconvert)
        --runstats               Print runtime statistics
        --mipimage %s            Specify an individual MIP level
    Basic modes (default is plain texture):
        --shadow                 Create shadow map
        --envlatl                Create lat/long environment map
        --lightprobe             Create lat/long environment map from a light probe
        --bumpslopes             Create a 6 channels bump-map with height, derivatives and square derivatives from an height or a normal map
        --bumpformat %s          Specify the interpretation of a 3-channel input image for --bumpslopes: "height", "normal" or "auto" (default).
    Color Management Options (OpenColorIO DISABLED)
        --colorconfig %s         Explicitly specify an OCIO configuration file
        --colorconvert %s %s     Apply a color space conversion to the image. If the output color space is not the same bit depth as input color space, it is your responsibility to set the data format to the proper bit depth using the -d option.  (choices: sRGB, linear)
        --unpremult              Unpremultiply before color conversion, then premultiply after the color conversion.  You'll probably want to use this flag if your image contains an alpha channel.
    Configuration Presets
        --prman                  Use PRMan-safe settings for tile size, planarconfig, and metadata.
        --oiio                   Use OIIO-optimized settings for tile size, planarconfig, metadata.
    Arnold Extensions
        --colorengine            Select the color processor engine to use: ocio or syncolor
                                 (default: ocio, available: ocio, syncolor)
        --colorconfig            For OCIO, set the OCIO config (leave empty to use OCIO
                                 environment variable).
                                 For synColor, use this flag twice to set the native and
                                 the custom catalog paths.
    """
    #
    TX_EXT = '.tx'
    TEXTURE_ACES_COLOR_SPACE_CONFIGURE = utl_configures.get_aces_color_space_configure()
    def __init__(self, *args, **kwargs):
        super(AndTextureOpt_, self).__init__(*args, **kwargs)

    def get_is_srgb(self):
        return (
            self._info['bit'] <= 16
            and self._info['type'] in (ai.AI_TYPE_BYTE, ai.AI_TYPE_INT, ai.AI_TYPE_UINT)
        )

    def get_is_linear(self):
        return not self.get_is_srgb()

    def get_color_space(self):
        if self.get_is_srgb():
            return bsc_configure.ColorSpace.SRGB
        else:
            return bsc_configure.ColorSpace.LINEAR

    def get_path_as_tx(self, search_directory_path=None):
        file_path_src = self._file_path
        #
        name = os.path.basename(file_path_src)
        name_base, ext = os.path.splitext(name)
        directory_path = os.path.dirname(file_path_src)
        if search_directory_path:
            return '{}/{}{}'.format(search_directory_path, name_base, self.TX_EXT)
        return '{}/{}{}'.format(directory_path, name_base, self.TX_EXT)

    def set_unit_tx_create(self, color_space, use_aces, aces_file, aces_color_spaces, aces_render_color_space, search_directory_path=None, block=False):
        cmd = self.get_unit_tx_create_cmd(
            color_space,
            use_aces,
            aces_file,
            aces_color_spaces,
            aces_render_color_space,
            search_directory_path
        )
        #
        if block is True:
            bsc_core.SubProcessMtd.set_run_with_result(
                cmd
            )
            return True
        else:
            return bsc_core.SubProcessMtd.set_run(
                cmd
            )

    def get_unit_tx_create_cmd(self, color_space_src, use_aces, aces_file, aces_color_spaces, aces_render_color_space, search_directory_path=None):
        file_path_src = self._file_path
        cmd_args = [
            'maketx',
            '-v',
            '-u',
            '--unpremult',
            '--threads 2',
            '--oiio'
        ]
        if use_aces is True:
            if color_space_src in aces_color_spaces:
                if color_space_src != aces_render_color_space:
                    cmd_args += [
                        '--colorengine ocio',
                        '--colorconfig "{}"'.format(aces_file),
                        #
                        '--colorconvert "{}" "{}"'.format(color_space_src, aces_render_color_space),
                    ]
            else:
                raise TypeError(
                    u'file="{}", aces color-space="{}" is not available'.format(
                        file_path_src, color_space_src
                    )
                )
        #
        if search_directory_path:
            file_path_src_tgt = self.get_path_as_tx(
                search_directory_path
            )
            cmd_args += [
                u'-o "{}"'.format(file_path_src_tgt)
            ]
        # etc. jpg to exr
        if self.get_is_srgb() and self.get_is_8_bit():
            cmd_args += [
                '--format exr',
                '-d half',
                '--compression dwaa'
            ]
        #
        cmd_args += [
            u'"{}"'.format(file_path_src)
        ]
        #
        return ' '.join(cmd_args)
    @classmethod
    def get_format_convert_as_aces_command(cls, file_path_src, file_path_tgt, color_space_src, color_space_tgt):
        option = dict(
            file_src=file_path_src,
            file_tgt=file_path_tgt,
            color_space_src=color_space_src,
            color_space_tgt=color_space_tgt,
            format_tgt=os.path.splitext(file_path_tgt)[-1][1:],
            aces_file=cls.TEXTURE_ACES_COLOR_SPACE_CONFIGURE.get_ocio_file()
            # channel_count_src=_get_channels_count_(file_path_src)
        )
        cmd_args = [
            'maketx',
            # verbose status messages
            '-v',
            # update mode
            '-u',
            # number of output image channels
            # '--nchannels {channel_count_src}',
            '--unpremult',
            '--threads 2',
            '--oiio',
            # do not mip map
            '--nomipmap',
            # color convert
            '--colorengine ocio',
            # '--colorconfig "{}"'.format('/l/packages/pg/third_party/ocio/aces/1.2/config.ocio'),
            '--colorconvert "{color_space_src}" "{color_space_tgt}"',
            '--format {format_tgt}',
            '"{file_src}"',
            '-o "{file_tgt}"'
        ]
        cmd = ' '.join(cmd_args).format(**option)
        return cmd
    @classmethod
    def get_create_exr_as_acescg_command(cls, file_path_src, file_path_tgt, color_space_src, color_space_tgt, use_update_mode=True):
        option = dict(
            file_src=file_path_src,
            file_tgt=file_path_tgt,
            color_space_src=color_space_src,
            color_space_tgt=color_space_tgt,
            format_tgt=os.path.splitext(file_path_tgt)[-1][1:],
            aces_file=cls.TEXTURE_ACES_COLOR_SPACE_CONFIGURE.get_ocio_file()
            # channel_count_src=_get_channels_count_(file_path_src)
        )
        cmd_args = [
            'maketx',
            '"{file_src}"',
            '-o "{file_tgt}"',
            # verbose status messages
            '-v',
            '--unpremult',
            '--threads 2',
            '--oiio',
        ]
        # use update mode
        if use_update_mode is True:
            cmd_args += [
                '-u'
            ]
        # convert color
        if color_space_src != color_space_tgt:
            cmd_args += [
                '--colorengine ocio',
                '--colorconfig "{}"'.format(cls.TEXTURE_ACES_COLOR_SPACE_CONFIGURE.get_ocio_file()),
                '--colorconvert "{color_space_src}" "{color_space_tgt}"',
            ]
        # format args, etc. jpg to exr
        if cls._get_is_srgb_(file_path_src) and cls._get_is_8_bit_(file_path_src):
            cmd_args += [
                '--format exr',
                '-d half',
                '--compression dwaa',
            ]
        else:
            cmd_args += [
                '--format exr',
            ]
        cmd = ' '.join(cmd_args).format(**option)
        return cmd
    @classmethod
    def get_create_tx_as_acescg_command(cls, file_path_src, file_path_tgt, color_space_src, color_space_tgt, use_update_mode=True):
        cmd_args = [
            'maketx',
            u'"{}"'.format(file_path_src),
            u'-o "{}"'.format(file_path_tgt),
            '-v',
            '-u',
            '--unpremult',
            '--threads 4',
            '--oiio'
        ]
        # color space args
        if color_space_src != color_space_tgt:
            aces_color_spaces = cls.TEXTURE_ACES_COLOR_SPACE_CONFIGURE.get_all_color_spaces()
            if color_space_src in aces_color_spaces:
                cmd_args += [
                    '--colorengine ocio',
                    '--colorconfig "{}"'.format(cls.TEXTURE_ACES_COLOR_SPACE_CONFIGURE.get_ocio_file()),
                    '--colorconvert "{}" "{}"'.format(color_space_src, color_space_tgt),
                ]
            else:
                raise TypeError(
                    u'file="{}", aces color-space="{}" is not available'.format(
                        file_path_src, color_space_src
                    )
                )
        # format args, etc. jpg to exr
        if cls._get_is_srgb_(file_path_src) and cls._get_is_8_bit_(file_path_src):
            cmd_args += [
                '--format exr',
                '-d half',
                '--compression dwaa'
            ]
        #
        return ' '.join(cmd_args)


class AndOslShaderMtd(object):
    @classmethod
    def get_data(cls, code):
        input_dict = {}
        errors = ''
        isActive = ai.AiUniverseIsActive()
        if not isActive:
            ai.AiBegin()

        # create a universe dedicated to OSL node compilation
        # for parameter/output type introspection and error checking
        compilation_universe = ai.AiUniverse()

        and_obj = ai.AiNode(compilation_universe, "osl", "test_node")
        and_obj_opt = AndObjMtd(compilation_universe, and_obj)

        ai.AiNodeSetStr(and_obj, "code", code)

        if ai.AiNodeLookUpUserParameter(and_obj, "compilation_errors"):
            compilation_errors = ai.AiNodeGetArray(and_obj, "compilation_errors")
        else:
            compilation_errors = None

        if compilation_errors is None or ai.AiArrayGetNumElements(compilation_errors) == 0:
            compileState = True
            input_dict = and_obj_opt.get_input_ports()
        else:
            compileState = False
            for i in range(ai.AiArrayGetNumElements(compilation_errors)):
                errors += ai.AiArrayGetStr(compilation_errors, i) + "\n"
        # cleanup the node
        ai.AiUniverseDestroy(compilation_universe)

        if not isActive:
            ai.AiEnd()
        return input_dict


class AndMayaAeTemplateMtd(object):
    pass
