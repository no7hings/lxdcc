# coding:utf-8
import re


s = 'A@_aaaaa.'


print re.findall(
    r'[^a-zA-Z0-9_]',
    s
)
