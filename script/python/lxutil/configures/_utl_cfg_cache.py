# coding:utf-8
from lxutil import utl_configure
#
from lxutil.configures import _utl_cfg_product
#
TEXTURE_COLOR_SPACE_CONFIGURE = None
TEXTURE_ACES_COLOR_SPACE_CONFIGURE = None


def get_color_space_configure():
    global TEXTURE_COLOR_SPACE_CONFIGURE
    #
    _ = TEXTURE_COLOR_SPACE_CONFIGURE
    if _ is None:
        _ = _utl_cfg_product.TextureColorSpaceConfigure(
            utl_configure.MainData.get_as_configure('utility/product/texture')
        )
        TEXTURE_COLOR_SPACE_CONFIGURE = _
    return _


def get_aces_color_space_configure():
    """
    cache the color space configure
    :return:
    """
    global TEXTURE_ACES_COLOR_SPACE_CONFIGURE
    #
    _ = TEXTURE_ACES_COLOR_SPACE_CONFIGURE
    if _ is None:
        _ = _utl_cfg_product.TextureAcesColorSpaceConfigure(
            utl_configure.MainData.get_as_configure('utility/product/color-space')
        )
        TEXTURE_ACES_COLOR_SPACE_CONFIGURE = _
    return _
