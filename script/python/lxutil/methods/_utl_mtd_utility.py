# coding:utf-8
import re


class String(object):
    @classmethod
    def to_number_embedded_raw(cls, string):
        pieces = re.compile(r'(\d+)').split(unicode(string))
        pieces[1::2] = map(int, pieces[1::2])
        return pieces
    @classmethod
    def to_rgb(cls, string, maximum=255):
        a = int(''.join([str(ord(i)).zfill(3) for i in string]))
        b = a % 3
        i = int(a / 256) % 3
        n = int(a % 256)
        if a % 2:
            if i == 0:
                r, g, b = 64 + 64 * b, n, 0
            elif i == 1:
                r, g, b = 0, 64 + 64 * b, n
            else:
                r, g, b = 0, n, 64 + 64 * b
        else:
            if i == 0:
                r, g, b = 0, n, 64 + 64 * b
            elif i == 1:
                r, g, b = 64 + 64 * b, 0, n
            else:
                r, g, b = 64 + 64 * b, n, 0
        return r / 255.0 * maximum, g / 255.0 * maximum, b / 255.0 * maximum
    @classmethod
    def find_spans(cls, content_str, keyword_str, match_case_flag=False, match_word_flag=False):
        lis = []
        if content_str and keyword_str:
            if match_word_flag is True:
                p = r'\b{}\b'.format(keyword_str)
            else:
                p = keyword_str

            if match_case_flag is True:
                r = re.finditer(p, content_str)
            else:
                r = re.finditer(p, content_str, re.I)
            for i in r:
                lis.append(i.span())
        return lis


class List(object):
    @classmethod
    def set_grid_to(cls, array, column_count):
        lis_ = []
        count = len(array)
        cutCount = int(count / column_count)
        for i in range(cutCount + 1):
            subLis = array[i * column_count:min((i + 1) * column_count, count)]
            if subLis:
                lis_.append(subLis)
        return lis_


class Color(object):
    @classmethod
    def rgb2hex(cls, r, g, b):
        return hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)
    @classmethod
    def hex2rgb(cls, hex_color, maximum=255):
        hex_color = int(hex_color, base=16) if isinstance(hex_color, str) else hex_color
        r, g, b = ((hex_color >> 16) & 0xff, (hex_color >> 8) & 0xff, hex_color & 0xff)
        if maximum == 255:
            return r, g, b
        elif maximum == 1.0:
            return round(float(r) / float(255), 4), round(float(g) / float(255), 4), round(float(b) / float(255), 4)
    @classmethod
    def hsv2rgb(cls, h, s, v, maximum=255):
        h = float(h % 360.0)
        s = float(max(min(s, 1.0), 0.0))
        v = float(max(min(v, 1.0), 0.0))
        #
        c = v * s
        x = c * (1 - abs((h / 60.0) % 2 - 1))
        m = v - c
        if 0 <= h < 60:
            r_, g_, b_ = c, x, 0
        elif 60 <= h < 120:
            r_, g_, b_ = x, c, 0
        elif 120 <= h < 180:
            r_, g_, b_ = 0, c, x
        elif 180 <= h < 240:
            r_, g_, b_ = 0, x, c
        elif 240 <= h < 300:
            r_, g_, b_ = x, 0, c
        else:
            r_, g_, b_ = c, 0, x
        #
        if maximum == 255:
            r, g, b = int(round((r_ + m) * maximum)), int(round((g_ + m) * maximum)), int(round((b_ + m) * maximum))
        else:
            r, g, b = float((r_ + m)), float((g_ + m)), float((b_ + m))
        return r, g, b


if __name__ == '__main__':
    # print Color.hex2rgb('BD34D1', maximum=1.0)
    print Color.rgb2hex(255, 191, 127)
