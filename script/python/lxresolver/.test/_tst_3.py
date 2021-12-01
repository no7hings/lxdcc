# coding:utf-8
from lxresolver import commands


r = commands.get_resolver()

o = {
    "task": "surfacing",
    "branch": "asset",
    "dcc": {
        "root": "|master"
    },
    "project": "shl",
    "platform": "linux",
    "step": "srf",
    "version": "v008",
    "role": "chr",
    "asset": "nn_gongshifu",
    "workspace": "work",
    "root": "/l/prod",
    "option": {
        "scheme": "publish"
    }
}

t = r.get_rsv_task(**o)
