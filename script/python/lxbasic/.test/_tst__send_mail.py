# coding:utf-8
from lxbasic import bsc_core

# bsc_core.MsgBaseMtd.send_feishu(
#     addresses=['dongchangbao@papegames.net'],
#     subject='test',
#     content='test'
# )

c = ''.join(
    map(
        lambda x: '{}: {}\n'.format(str(x[0]).rjust(16), x[1]),
        [
            ('Name', '{name}'),
            ('ID', '{id}'),
            ('User', '{user}'),
            ('Type', '{version_type}'),
            ('Folder', '{folder}'),
            ('Review', '{review}'),
            ('Description', '{description}')
        ]
    )
)

print c
