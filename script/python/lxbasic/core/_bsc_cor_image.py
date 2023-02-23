# coding:utf-8
from ._bsc_cor_utility import *

from lxbasic.core import _bsc_cor_raw, _bsc_cor_time, _bsc_cor_process, _bsc_cor_storage


class ImgFileOpt(object):
    TIME_MARK_PATTERN = '%Y:%m:%d %H:%M:%S'
    def __init__(self, file_path):
        self._file_path = file_path
        self._file_path_opt = _bsc_cor_storage.StgFileOpt(self._file_path)

    def get_thumbnail_file_path(self, ext='.jpg'):
        return _bsc_cor_storage.StgTmpThumbnailMtd.get_file_path(self._file_path, ext)

    def get_thumbnail_file_path_(self, width=128, ext='.jpg'):
        return _bsc_cor_storage.StgTmpThumbnailMtd.get_file_path_(self._file_path, width, ext)

    def get_thumbnail(self, width=128):
        thumbnail_file_path = self.get_thumbnail_file_path()
        if os.path.isfile(self._file_path):
            if os.path.exists(thumbnail_file_path) is False:
                directory_path = os.path.dirname(thumbnail_file_path)
                if os.path.exists(directory_path) is False:
                    os.makedirs(directory_path)
                #
                cmd_args = [
                    Bin.get_oiiotool(),
                    u'-i "{}"'.format(self._file_path),
                    '--resize {}x0'.format(width),
                    '-o "{}"'.format(thumbnail_file_path)
                ]
                _bsc_cor_process.SubProcessMtd.set_run(
                    ' '.join(cmd_args)
                )
        return thumbnail_file_path

    def get_thumbnail_create_args(self, width=128, ext='.jpg'):
        thumbnail_file_path = self.get_thumbnail_file_path_(width, ext)
        if os.path.exists(thumbnail_file_path) is False:
            if os.path.exists(self._file_path):
                directory_path = os.path.dirname(thumbnail_file_path)
                if os.path.exists(directory_path) is False:
                    os.makedirs(directory_path)
                #
                cmd_args = [
                    Bin.get_oiiotool(),
                    u'-i "{}"'.format(self._file_path),
                    '--resize {}x0'.format(width),
                    '-o "{}"'.format(thumbnail_file_path)
                ]
                return thumbnail_file_path, ' '.join(cmd_args)
        return thumbnail_file_path, None

    def get_jpg_file_path(self):
        path_base, ext = os.path.splitext(self._file_path)
        return '{}{}'.format(path_base, '.jpg')

    def get_jpg(self, width=1024, block=False):
        file_path = self._file_path
        #
        jpg_file_path = self.get_jpg_file_path()
        if os.path.isfile(file_path):
            directory_path = os.path.dirname(jpg_file_path)
            if os.path.exists(directory_path) is False:
                os.makedirs(directory_path)
            #
            time_mark = _bsc_cor_time.TimestampMtd.to_string(
                self.TIME_MARK_PATTERN, _bsc_cor_storage.StgFileOpt(file_path).get_modify_timestamp()
            )
            cmd_args = [
                Bin.get_oiiotool(),
                u'-i "{}"'.format(file_path),
                '--resize {}x0'.format(width),
                '--attrib:type=string DateTime "{}"'.format(time_mark),
                '--adjust-time ',
                '--threads 2',
                u'-o "{}"'.format(jpg_file_path),
            ]
            if block is True:
                _bsc_cor_process.SubProcessMtd.set_run_with_result(
                    ' '.join(cmd_args)
                )
                return True
            else:
                s_p = _bsc_cor_process.SubProcessMtd.set_run(
                    ' '.join(cmd_args)
                )
                return s_p

    def get_create_cmd_as_ext_tgt(self, ext, directory_path=None, width=None):
        file_path_src_opt = self._file_path_opt
        file_path_tgt_opt = _bsc_cor_storage.StgFileOpt(self._file_path).set_ext_repath_to(ext)
        if file_path_src_opt.get_is_file() is True:
            file_path_tgt_opt.create_directory()
        #
        if directory_path is not None:
            file_path_tgt_opt = file_path_tgt_opt.set_directory_repath_to(directory_path)
        #
        time_mark = _bsc_cor_time.TimestampMtd.to_string(
            self.TIME_MARK_PATTERN, file_path_src_opt.get_modify_timestamp()
        )
        cmd_args = [
            Bin.get_oiiotool(),
            u'-i "{}"'.format(file_path_src_opt.path),
            '--attrib:type=string DateTime "{}"'.format(time_mark),
            '--adjust-time ',
            '--threads 1',
        ]
        if isinstance(width, (int, float)):
            cmd_args += [
                '--resize {}x0'.format(width),
            ]

        cmd_args += [
            u'-o "{}"'.format(file_path_tgt_opt.path),
        ]

        return u' '.join(cmd_args)

    def set_convert_to(self, file_path_tgt):
        file_opt_src = _bsc_cor_storage.StgFileOpt(self._file_path)
        if file_opt_src.get_is_file() is True:
            file_opt_tgt = _bsc_cor_storage.StgFileOpt(file_path_tgt)
            _ext_tgt = file_opt_tgt.get_ext()
            time_mark = _bsc_cor_time.TimestampMtd.to_string(
                self.TIME_MARK_PATTERN, file_opt_src.get_modify_timestamp()
            )
            cmd_args = [
                Bin.get_oiiotool(),
                u'-i "{}"'.format(file_opt_src.path),
                '--attrib:type=string DateTime "{}"'.format(time_mark),
                '--adjust-time ',
                '--threads 1',
                u'-o "{}"'.format(file_opt_tgt.path),
            ]
            _bsc_cor_process.SubProcessMtd.set_run_with_result(
                ' '.join(cmd_args)
            )
    @classmethod
    def r_to_rgb(cls, file_path_src, file_path_tgt):
        option = dict(
            input=file_path_src,
            output=file_path_tgt,
            time_mark=_bsc_cor_time.TimestampMtd.to_string(
                cls.TIME_MARK_PATTERN, _bsc_cor_storage.StgFileOpt(file_path_src).get_modify_timestamp()
            )
        )
        cmd_args = [
            Bin.get_oiiotool(),
            u'-i "{input}"',
            '--ch 0,0,0',
            '--attrib:type=string DateTime "{time_mark}"',
            '--adjust-time ',
            '--threads 1',
            u'-o "{output}"',
        ]
        _bsc_cor_process.SubProcessMtd.set_run_with_result(
            ' '.join(cmd_args).format(**option)
        )


class ImgOiioMtd(object):
    @classmethod
    def set_fit_to(cls, file_path_src, file_path_tgt, size):
        option = dict(
            input=file_path_src,
            output=file_path_tgt,
            size='{}x{}'.format(*size)
        )
        cmd_args = [
            Bin.get_oiiotool(),
            u'-i "{input}"',
            '--fit {size}',
            u'-o "{output}"',
        ]
        _bsc_cor_process.SubProcessMtd.set_run_with_result(
            ' '.join(cmd_args).format(**option)
        )
    @classmethod
    def set_create_as_flat_color(cls, file_path_tgt, size, rgba):
        option = dict(
            size='{}x{}'.format(*size),
            color='{},{},{},{}'.format(*rgba),
            output=file_path_tgt
        )
        cmd_args = [
            Bin.get_oiiotool(),
            '--create {size} 4',
            '--fill:color={color} {size}',
            # u'-i "{}"'.format(file_path_src),
            u'-o "{output}"',
        ]
        _bsc_cor_process.SubProcessMtd.set_run_with_result(
            ' '.join(cmd_args).format(**option)
        )
    @classmethod
    def set_over_by(cls, file_path_fgd, file_path_bgd, file_path_tgt, offset_fgd):
        option = dict(
            foreground=file_path_fgd,
            background=file_path_bgd,
            output=file_path_tgt,
            offset_foreground='-{}-{}'.format(*offset_fgd)
        )
        cmd_args = [
            Bin.get_oiiotool(),
            u'"{foreground}" --originoffset {offset_foreground}',
            u'"{background}"',
            '--over',
            u'-o "{output}"',
        ]
        _bsc_cor_process.SubProcessMtd.set_run_with_result(
            ' '.join(cmd_args).format(**option)
        )
    @classmethod
    def set_guide_create(cls):
        file_path_tgt = '/data/f/test_rvio/test_6.exr'
        guide_data = [
            ('primary', 8),
            ('object-color', 8),
            ('wire', 8),
            ('density', 8)
        ]
        size = 2048, 2048
        w, h = size
        g_w, g_h = w, 48
        rgba = .18, .18, .18, 1
        option = dict(
            size='{}x{}'.format(*size),
            color='{},{},{},{}'.format(*rgba),
            output=file_path_tgt,
        )
        box_args = []
        border_rgb = 1, 1, 1
        max_c = sum([i[1] for i in guide_data])
        i_x_0, i_y_0 = 0, h - g_h
        for i in guide_data:
            i_text, i_c = i
            i_background_rgb = _bsc_cor_raw.RawTextOpt(i_text).to_rgb(maximum=1)
            # background
            box_args.append(
                '--box:color={},{},{},1:fill=1'.format(*i_background_rgb)
            )
            i_p = i_c / float(max_c)
            i_x_1, i_y_1 = int(i_x_0 + i_p * w), h - 1
            box_args.append(
                '{},{},{},{}'.format(i_x_0, i_y_0, i_x_1, i_y_1)
            )
            # border
            box_args.append(
                '--box:color={},{},{},1'.format(*border_rgb)
            )
            i_p = i_c / float(max_c)
            i_x_1, i_y_1 = int(i_x_0 + i_p * w), h - 1
            box_args.append(
                '{},{},{},{}'.format(i_x_0, i_y_0, i_x_1, i_y_1)
            )
            i_x_0 = i_x_1

        option['box'] = ' '.join(box_args)
        cmd_args = [
            Bin.get_oiiotool(),
            '--create {size} 4',
            '--fill:color={color} {size}',
            '{box}',
            # '--text:x=100:y=200:font="Arial":color=1,0,0:size=60 "Go Big Red!"',
            u'-o "{output}"',
        ]
        # print ' '.join(cmd_args).format(**option)
        _bsc_cor_process.SubProcessMtd.set_run_with_result(
            ' '.join(cmd_args).format(**option)
        )
    @classmethod
    def test(cls):
        file_path_tgt = '/data/f/test_rvio/test_6.exr'
        guide_data = [
            ('primary', 8),
            ('object-color', 8),
            ('wire', 8),
            ('density', 8)
        ]
        size = 2048, 2048
        w, h = size
        g_w, g_h = w, 48
        rgba = .18, .18, .18, 1
        option = dict(
            size='{}x{}'.format(*size),
            color='{},{},{},{}'.format(*rgba),
            output=file_path_tgt,
        )
        box_args = []
        border_rgb = 1, 1, 1
        max_c = sum([i[1] for i in guide_data])
        i_x_0, i_y_0 = 0, h-g_h
        for i in guide_data:
            i_text, i_c = i
            i_background_rgb = _bsc_cor_raw.RawTextOpt(i_text).to_rgb(maximum=1)
            # background
            box_args.append(
                '--box:color={},{},{},1:fill=1'.format(*i_background_rgb)
            )
            i_p = i_c/float(max_c)
            i_x_1, i_y_1 = int(i_x_0+i_p*w), h-1
            box_args.append(
                '{},{},{},{}'.format(i_x_0, i_y_0, i_x_1, i_y_1)
            )
            # border
            box_args.append(
                '--box:color={},{},{},1'.format(*border_rgb)
            )
            i_p = i_c / float(max_c)
            i_x_1, i_y_1 = int(i_x_0 + i_p * w), h - 1
            box_args.append(
                '{},{},{},{}'.format(i_x_0, i_y_0, i_x_1, i_y_1)
            )
            i_x_0 = i_x_1

        option['box'] = ' '.join(box_args)
        cmd_args = [
            Bin.get_oiiotool(),
            '--create {size} 4',
            '--fill:color={color} {size}',
            '{box}',
            # '--text:x=100:y=200:font="Arial":color=1,0,0:size=60 "Go Big Red!"',
            u'-o "{output}"',
        ]
        # print ' '.join(cmd_args).format(**option)
        _bsc_cor_process.SubProcessMtd.set_run_with_result(
            ' '.join(cmd_args).format(**option)
        )
    @classmethod
    def set_convert_to(cls, file_path_src, file_path_tgt):
        option = dict(
            input=file_path_src,
            output=file_path_tgt,
        )
        cmd_args = [
            Bin.get_oiiotool(),
            u'-i "{input}"',
            '--ch R,G,B,A=1.0',
            u'-o "{output}"',
        ]
        _bsc_cor_process.SubProcessMtd.set_run_with_result(
            ' '.join(cmd_args).format(**option)
        )
    @classmethod
    def set_color_space_convert_to(cls, file_path_src, file_path_tgt, color_space_src, color_space_tgt):
        option = dict(
            input=file_path_src,
            output=file_path_tgt,
            from_color_space=color_space_src,
            to_color_space=color_space_tgt,
        )
        cmd_args = [
            Bin.get_oiiotool(),
            u'-i "{input}"',
            # '--colorconfig "{}"'.format('/l/packages/pg/third_party/ocio/aces/1.2/config.ocio'),
            # '--iscolorspace "{from_color_space}"',
            # '--tocolorspace "{to_color_space}"',
            '--colorconvert "{from_color_space}" "{to_color_space}"',
            u'-o "{output}"',
        ]
        _bsc_cor_process.SubProcessMtd.set_run_with_result(
            ' '.join(cmd_args).format(**option)
        )


class ImgFileOiioOpt(object):
    """
    oiiotool -- simple image processing operations
    OpenImageIO-Arnold 2.2.1 http://www.openimageio.org
    Usage:  oiiotool [filename|command]...

    Important usage tips:
      * The oiiotool command line is processed in order, LEFT to
        RIGHT.
      * The command line consists of image NAMES ('image.tif') and
        COMMANDS ('--over'). Commands start with dashes (one or two
        dashes are equivalent). Some commands have required arguments
        which must follow on the command line. For example, the '-o'
        command is followed by a filename.
      * oiiotool is STACK-based: naming an image pushes it on the
        stack, and most commands pop the top image (or sometimes more
        than one image), perform a calculation, and push the result
        image back on the stack. For example, the '--over' command pops
        the top two images off the stack, composites them, then pushes
        the result back onto the stack.
      * Some commands allow one or more optional MODIFIERS in the
        form 'name=value', which are appended directly to the command
        itself (no spaces), separated by colons ':'. For example,
           oiiotool in.tif --text:x=100:y=200:color=1,0,0 "Hello" -o out.tif
      * Using numerical wildcards will run the whole command line
        on each of several sequentially-named files, for example:
           oiiotool fg.#.tif bg.#.tif -over -o comp.#.tif
        See the manual for info about subranges, number of digits,
        etc.
      * Command line arguments containing substrings enclosed in
        braces {} are replaced by evaluating their contents as
        expressions. Simple math is allowed as well as retrieving
        metadata such as {TOP.'foo:bar'}, {IMG[0].filename}, or
        {FRAME_NUMBER/24.0}.

    Options (general):
        --help                        Print help message
        -v                            Verbose status messages
        -q                            Quiet mode (turn verbose off)
        -n                            No saved output (dry run)
        -a                            Do operations on all subimages/miplevels
        --debug                       Debug mode
        --runstats                    Print runtime statistics
        --info                        Print resolution and basic info on all inputs, detailed metadata if -v is also used (options: format=xml:verbose=1)
        --echo TEXT                   Echo message to console (options: newline=0)
        --metamatch REGEX             Which metadata is printed with -info -v
        --no-metamatch REGEX          Which metadata is excluded with -info -v
        --stats                       Print pixel statistics on all inputs
        --dumpdata                    Print all pixel data values (options: empty=0)
        --hash                        Print SHA-1 hash of each input image
        --colorcount COLORLIST        Count of how many pixels have the given color (argument: color;color;...) (options: eps=color)
        --rangecheck MIN MAX          Count of how many pixels are outside the min/max color range (each is a comma-separated color value list)
        --no-clobber                  Do not overwrite existing files
        --threads N                   Number of threads (default 0 == #cores)
        --frames FRAMERANGE           Frame range for '#' or printf-style wildcards
        --framepadding NDIGITS        Frame number padding digits (ignored when using printf-style wildcards)
        --views VIEWNAMES             Views for %V/%v wildcards (comma-separated, defaults to "left,right")
        --wildcardoff                 Disable numeric wildcard expansion for subsequent command line arguments
        --wildcardon                  Enable numeric wildcard expansion for subsequent command line arguments
        --evaloff                     Disable {expression} evaluation for subsequent command line arguments
        --evalon                      Enable {expression} evaluation for subsequent command line arguments
        --no-autopremult              Turn off automatic premultiplication of images with unassociated alpha
        --autopremult                 Turn on automatic premultiplication of images with unassociated alpha
        --autoorient                  Automatically --reorient all images upon input
        --autocc                      Automatically color convert based on filename
        --noautocc                    Turn off automatic color conversion
        --native                      Keep native pixel data type (bypass cache if necessary)
        --cache MB                    ImageCache size (in MB: default=4096)
        --autotile TILESIZE           Autotile enable for cached images (the argument is the tile size, default 0 means no autotile)
        --metamerge                   Always merge metadata of all inputs into output
    Commands that read images:
        -i FILENAME                   Input file (options: now=, printinfo=, autocc=, type=, ch=)
        --iconfig NAME VALUE          Sets input config attribute (options: type=...)
    Commands that write images:
        -o FILENAME                   Output the current image to the named file
        -otex FILENAME                Output the current image as a texture
        -oenv FILENAME                Output the current image as a latlong env map
        -obump FILENAME               Output the current bump texture map as a 6 channels texture including the first and second moment of the bump slopes (options: bumpformat=height|normal|auto)
    Options that affect subsequent image output:
        -d TYPE                       '-d TYPE' sets the output data format of all channels, '-d CHAN=TYPE' overrides a single named channel (multiple -d args are allowed). Data types include: uint8, sint8, uint10, uint12, uint16, sint16, uint32, sint32, half, float, double
        --scanline                    Output scanline images
        --tile WIDTH HEIGHT           Output tiled images with this tile size
        --compression NAME            Set the compression method (in the form "name" or "name:quality")
        --dither                      Add dither to 8-bit output
        --planarconfig CONFIG         Force planarconfig (contig, separate, default)
        --adjust-time                 Adjust file times to match DateTime metadata
        --noautocrop                  Do not automatically crop images whose formats don't support separate pixel data and full/display windows
        --autotrim                    Automatically trim black borders upon output to file formats that support separate pixel data and full/display windows
    Options that change current image metadata (but not pixel values):
        --attrib NAME VALUE           Sets metadata attribute (options: type=...)
        --sattrib NAME VALUE          Sets string metadata attribute
        --eraseattrib REGEX           Erase attributes matching regex
        --caption TEXT                Sets caption (ImageDescription metadata)
        --keyword KEYWORD             Add a keyword
        --clear-keywords              Clear all keywords
        --nosoftwareattrib            Do not write command line into Exif:ImageHistory, Software metadata attributes
        --sansattrib                  Write command line into Software & ImageHistory but remove --sattrib and --attrib options
        --orientation ORIENT          Set the assumed orientation
        --orientcw                    Rotate orientation metadata 90 deg clockwise
        --orientccw                   Rotate orientation metadata 90 deg counter-clockwise
        --orient180                   Rotate orientation metadata 180 deg
        --origin +X+Y                 Set the pixel data window origin (e.g. +20+10, -16-16)
        --originoffset +X+Y           Offset the pixel data window origin from its current position (e.g. +20+10, -16-16)
        --fullsize GEOM               Set the display window (e.g., 1920x1080, 1024x768+100+0, -20-30)
        --fullpixels                  Set the 'full' image range to be the pixel data window
        --chnames NAMELIST            Set the channel names (comma-separated)
    Options that affect subsequent actions:
        --fail THRESH                 Failure threshold difference (0.000001)
        --failpercent PCNT            Allow this percentage of failures in diff (0)
        --hardfail THRESH             Fail diff if any one pixel exceeds this error (infinity)
        --warn THRESH                 Warning threshold difference (0.00001)
        --warnpercent PCNT            Allow this percentage of warnings in diff (0)
        --hardwarn THRESH             Warn if any one pixel difference exceeds this error (infinity)
    Actions:
        --create GEOM NCHANS          Create a blank image
        --pattern NAME GEOM NCHANS    Create a patterned image. Pattern name choices: black, constant, fill, checker, noise
        --kernel NAME GEOM            Create a centered convolution kernel
        --capture                     Capture an image (options: camera=%d)
        --diff                        Print report on the difference of two images (modified by --fail, --failpercent, --hardfail, --warn, --warnpercent --hardwarn)
        --pdiff                       Print report on the perceptual difference of two images (modified by --fail, --failpercent, --hardfail, --warn, --warnpercent --hardwarn)
        --add                         Add two images
        --addc VAL                    Add to all channels a scalar or per-channel constants (e.g.: 0.5 or 1,1.25,0.5)
        --sub                         Subtract two images
        --subc VAL                    Subtract from all channels a scalar or per-channel constants (e.g.: 0.5 or 1,1.25,0.5)
        --mul                         Multiply two images
        --mulc VAL                    Multiply the image values by a scalar or per-channel constants (e.g.: 0.5 or 1,1.25,0.5)
        --div                         Divide first image by second image
        --divc VAL                    Divide the image values by a scalar or per-channel constants (e.g.: 0.5 or 1,1.25,0.5)
        --mad                         Multiply two images, add a third
        --invert                      Take the color inverse (subtract from 1)
        --abs                         Take the absolute value of the image pixels
        --absdiff                     Absolute difference between two images
        --absdiffc VAL                Absolute difference versus a scalar or per-channel constant (e.g.: 0.5 or 1,1.25,0.5)
        --powc VAL                    Raise the image values to a scalar or per-channel power (e.g.: 2.2 or 2.2,2.2,2.2,1.0)
        --noise                       Add noise to an image (options: type=gaussian:mean=0:stddev=0.1, type=uniform:min=0:max=0.1, type=salt:value=0:portion=0.1, seed=0
        --chsum                       Turn into 1-channel image by summing channels (options: weight=r,g,...)
        --colormap MAPNAME            Color map based on channel 0 (arg: "inferno", "viridis", "magma", "turbo", "plasma", "blue-red", "spectrum", "heat", or comma-separated list of RGB triples)
        --crop GEOM                   Set pixel data resolution and offset, cropping or padding if necessary (WxH+X+Y or xmin,ymin,xmax,ymax)
        --croptofull                  Crop or pad to make pixel data region match the "full" region
        --trim                        Crop to the minimal ROI containing nonzero pixel values
        --cut GEOM                    Cut out the ROI and reposition to the origin (WxH+X+Y or xmin,ymin,xmax,ymax)
        --paste +X+Y                  Paste fg over bg at the given position (e.g., +100+50; '-' or 'auto' indicates using the data window position as-is; options: all=%d, mergeroi=%d)
        --mosaic WxH                  Assemble images into a mosaic (arg: WxH; options: pad=0)
        --over                        'Over' composite of two images
        --zover                       Depth composite two images with Z channels (options: zeroisinf=%d)
        --deepmerge                   Merge/composite two deep images
        --deepholdout                 Hold out one deep image by another
        --histogram BINSxHEIGHT CHAN  Histogram one channel (options: cumulative=0)
        --rotate90                    Rotate the image 90 degrees clockwise
        --rotate180                   Rotate the image 180 degrees
        --rotate270                   Rotate the image 270 degrees clockwise (or 90 degrees CCW)
        --flip                        Flip the image vertically (top<->bottom)
        --flop                        Flop the image horizontally (left<->right)
        --reorient                    Rotate and/or flop the image to transform the pixels to match the Orientation metadata
        --transpose                   Transpose the image
        --cshift +X+Y                 Circular shift the image (e.g.: +20-10)
        --resample GEOM               Resample (640x480, 50%) (options: interp=0)
        --resize GEOM                 Resize (640x480, 50%) (options: filter=%s)
        --fit GEOM                    Resize to fit within a window size (options: filter=%s, pad=%d, exact=%d)
        --pixelaspect ASPECT          Scale up the image's width or height to match the given pixel aspect ratio (options: filter=%s)
        --rotate DEGREES              Rotate pixels (degrees clockwise) around the center of the display window (options: filter=%s, center=%f,%f, recompute_roi=%d
        --warp MATRIX                 Warp pixels (argument is a 3x3 matrix, separated by commas) (options: filter=%s, recompute_roi=%d)
        --convolve                    Convolve with a kernel
        --blur WxH                    Blur the image (options: kernel=name)
        --median WxH                  Median filter the image
        --dilate WxH                  Dilate (area maximum) the image
        --erode WxH                   Erode (area minimum) the image
        --unsharp                     Unsharp mask (options: kernel=gaussian, width=3, contrast=1, threshold=0)
        --laplacian                   Laplacian filter the image
        --fft                         Take the FFT of the image
        --ifft                        Take the inverse FFT of the image
        --polar                       Convert complex (real,imag) to polar (amplitude,phase)
        --unpolar                     Convert polar (amplitude,phase) to complex (real,imag)
        --fixnan STRATEGY             Fix NaN/Inf values in the image (choices: none, black, box3, error)
        --fillholes                   Fill in holes (where alpha is not 1)
        --max                         Pixel-by-pixel max of two images
        --maxc VAL                    Max all values with a scalar or per-channel constants (e.g.: 0.5 or 1,1.25,0.5)
        --min                         Pixel-by-pixel min of two images
        --minc VAL                    Min all values with a scalar or per-channel constants (e.g.: 0.5 or 1,1.25,0.5)
        --clamp                       Clamp values (options: min=..., max=..., clampalpha=0)
        --contrast                    Remap values (options: black=0..., white=1..., sthresh=0.5..., scontrast=1.0..., gamma=1, clamp=0|1)
        --rangecompress               Compress the range of pixel values with a log scale (options: luma=0|1)
        --rangeexpand                 Un-rangecompress pixel values back to a linear scale (options: luma=0|1)
        --line X1,Y1,X2,Y2,...        Render a poly-line (options: color=)
        --box X1,Y1,X2,Y2             Render a box (options: color=)
        --fill GEOM                   Fill a region (options: color=)
        --text TEXT                   Render text into the current image (options: x=, y=, size=, color=)
    Manipulating channels or subimages:
        --ch CHANLIST                 Select or shuffle channels (e.g., "R,G,B", "B,G,R", "2,3,4")
        --chappend                    Append the channels of the last two images
        --unmip                       Discard all but the top level of a MIPmap
        --selectmip MIPLEVEL          Select just one MIP level (0 = highest res)
        --subimage SUBIMAGEINDEX      Select just one subimage (by index or name)
        --sisplit                     Split the top image's subimges into separate images
        --siappend                    Append the last two images into one multi-subimage image
        --siappendall                 Append all images on the stack into a single multi-subimage image
        --deepen                      Deepen normal 2D image to deep
        --flatten                     Flatten deep image to non-deep
    Image stack manipulation:
        --dup                         Duplicate the current image (push a copy onto the stack)
        --swap                        Swap the top two images on the stack.
        --pop                         Throw away the current image
        --label %s                    Label the top image
    Color management:
        --colorconfig FILENAME        Explicitly specify an OCIO configuration file
        --iscolorspace COLORSPACE     Set the assumed color space (without altering pixels)
        --tocolorspace COLORSPACE     Convert the current image's pixels to a named color space
        --colorconvert SRC DST        Convert pixels from 'src' to 'dst' color space (options: key=, value=, unpremult=, strict=)
        --ccmatrix MATRIXVALS         Color convert pixels with a 3x3 or 4x4 matrix (options: unpremult=,transpose=)
        --ociolook LOOK               Apply the named OCIO look (options: from=, to=, inverse=, key=, value=, unpremult=)
        --ociodisplay DISPLAY VIEW    Apply the named OCIO display and view (options: from=, looks=, key=, value=, unpremult=)
        --ociofiletransform FILENAME  Apply the named OCIO filetransform (options: inverse=, unpremult=)
        --unpremult                   Divide all color channels of the current image by the alpha to "un-premultiply"
        --premult                     Multiply all color channels of the current image by the alpha

    Input formats supported: bmp, cineon, dds, dpx, fits, hdr, ico, iff, jpeg, null, openexr, png, pnm, psd, rla, sgi, socket, softimage, targa, tiff, zfile
    Output formats supported: bmp, dpx, fits, hdr, ico, iff, jpeg, null, openexr, png, pnm, rla, sgi, socket, targa, tiff, zfile
    Color configuration: built-in
    Known color spaces: "linear", "default", "rgb", "RGB", "sRGB", "Rec709"
    No OpenColorIO support was enabled at build time.
    Filters available: box, triangle, gaussian, sharp-gaussian, catmull-rom, blackman-harris, sinc, lanczos3, radial-lanczos3, nuke-lanczos6, mitchell, bspline, disk, cubic, keys, simon, rifman
    Dependent libraries: jpeglib 9.2, null 1.0, IlmBase , libpng 1.6.29, LIBTIFF Version 4.0.8
    OIIO 2.2.1 built sse2,sse3,ssse3,sse41,sse42, running on 12 cores 62.7GB sse2,sse3,ssse3,sse41,sse42,avx,avx2,fma,f16c,popcnt,rdrand
    Full OIIO documentation can be found at
        https://openimageio.readthedocs.io
    """
    #
    INFO_PATTERN = '{path} : {width} x {height}, {channel_count} channel, {type} {format}'
    #
    BIT_DICT = {
        'uint8': 8, 'uint10': 10, 'uint12': 12, 'uint16': 16, 'uint32': 32,
        'sint8': 8, 'sint16': 16, 'sint32': 32,
        'half': 16, 'float': 32, 'double': 64
    }
    TYPE_DICT = {
        'uint8': 'uint', 'uint10': 'uint', 'uint12': 'uint', 'uint16': 'uint', 'uint32': 'uint',
        'sint16': 'sint', 'sint8': 'sint', 'sint32': 'sint',
        'half': 'half',  'float': 'float', 'double': 'double'
    }
    @classmethod
    def _get_info_(cls, file_path):
        cmd_args = [
            Bin.get_oiiotool(),
            '--info:verbose=1 "{}"'.format(file_path),
        ]
        p = _bsc_cor_process.SubProcessMtd.set_run(' '.join(cmd_args))
        _ = p.stdout.readlines()
        if _:
            p = parse.parse(cls.INFO_PATTERN, _[0])
            if p:
                return p.named
    @classmethod
    def _get_metadata_(cls, file_path):
        cmd_args = [
            Bin.get_oiiotool(),
            '--info:verbose=1 "{}"'.format(file_path),
        ]
        p = _bsc_cor_process.SubProcessMtd.set_run(' '.join(cmd_args))
        _ = p.stdout.readlines()
        print _
    #
    def __init__(self, file_path):
        if os.path.isfile(file_path):
            self._file_path = file_path
            self._info = self._get_info_(self._file_path)
        else:
            raise OSError()
    @property
    def info(self):
        return self._info
    #
    @property
    def path(self):
        return self._file_path

    def get_size(self):
        return int(self._info['width']), int(self._info['height'])
    size = property(get_size)

    @property
    def bit(self):
        return self.BIT_DICT[self._info['type']]
    @property
    def type(self):
        return self.TYPE_DICT[self._info['type']]
    @property
    def format(self):
        return self

    def set_convert_to(self, output_file_path):
        if os.path.exists(self.path):
            if SystemMtd.get_is_windows():
                pass
            elif SystemMtd.get_is_linux():
                if os.path.exists(output_file_path) is False:
                    subprocess.Popen(
                        u'ffmpeg -framerate 1 -i "{}" -c:v libx264 -r 30 -pix_fmt yuv420p "{}"'.format(
                            self.path, output_file_path
                        ),
                        shell=True
                    )

    def get_metadata(self):
        pass

    def __str__(self):
        return 'image(path="{}", width={}, height={})'.format(
            self._file_path,
            self._info['width'], self._info['height']
        )


class ImgTextureOiioOpt(ImgFileOiioOpt):
    def __init__(self, *args, **kwargs):
        super(ImgTextureOiioOpt, self).__init__(*args, **kwargs)

    def get_is_srgb(self):
        bit = self.BIT_DICT[self._info['type']]
        type_ = self.TYPE_DICT[self._info['type']]
        return bit <= 16 and type_ in ('uint', 'sint')

    def get_is_linear(self):
        return not self.get_is_srgb()

    def get_color_space(self):
        if self.get_is_srgb():
            return bsc_configure.ColorSpace.SRGB
        else:
            return bsc_configure.ColorSpace.LINEAR
