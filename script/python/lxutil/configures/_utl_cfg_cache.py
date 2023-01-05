# coding:utf-8
from lxutil import utl_configure
#
from lxutil.configures import _utl_cfg_product
#
TEXTURE_TX = None
ACES_COLOR_SPACE = None


def get_texture_tx_configure():
    global TEXTURE_TX
    #
    _ = TEXTURE_TX
    if _ is None:
        _ = _utl_cfg_product.TextureTxCfg(
            utl_configure.MainData.get_as_configure('utility/product/texture')
        )
        TEXTURE_TX = _
    return _


def get_aces_color_space_configure():
    global ACES_COLOR_SPACE
    #
    _ = ACES_COLOR_SPACE
    if _ is None:
        _ = _utl_cfg_product.AcesColorSpaceConfigure(
            utl_configure.MainData.get_as_configure('utility/product/color-space')
        )
        ACES_COLOR_SPACE = _
    return _
