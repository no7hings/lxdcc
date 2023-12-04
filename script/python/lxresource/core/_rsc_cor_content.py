# coding:utf-8
import lxcontent.core as ctt_core

from ..core import _rsc_cor_base


class ResourceContent(_rsc_cor_base.AbsResource):
    """
print RscConfigure.get_yaml('database/library/resource-basic')
    """
    CACHE = {}
    ENVIRON_KEY = 'PAPER_EXTEND_CONFIGURES'

    @classmethod
    def get_yaml(cls, key):
        return cls.get('{}.yml'.format(key))

    @classmethod
    def get_as_content(cls, key):
        return ctt_core.Content(
            value=cls.get_yaml(key)
        )

    @classmethod
    def get_jinja(cls, key):
        return cls.get('{}.j2'.format(key))


class ResourceJinja(object):
    """
c = RscJinjaConfigure.get_configure_yaml(
    'test/test'
)
t = RscJinjaConfigure.get_template(
    'test/test'
)
print(
    t.render(
        name='World'
    )
)

print RscJinjaConfigure.get_template('usda/shot-asset-set')
print(
    RscJinjaConfigure.get_result(
        'katana/images',
        dict(
            images=[
                dict(
                    name='diffuse', file='test', color_r=0.0625, color_g=0.25, color_b=0.125, position_x=0,
                    position_y=0
                ),
                dict(
                    name='roughness', file='test', color_r=0.0625, color_g=0.25, color_b=0.125, position_x=0,
                    position_y=240
                )
            ]
        )
    )
)
    """

    @classmethod
    def get_configure(cls, key):
        f = ResourceContent.get_yaml(
            'jinja/{}'.format(key)
        )
        if f:
            return ctt_core.Content(
                value=f
            )

    @classmethod
    def get_template(cls, key):
        import jinja2

        f = ResourceContent.get_jinja(
            'jinja/{}'.format(key)
        )
        if f:
            return jinja2.Template(
                ctt_core.ContentFile(f).read()
            )

    @classmethod
    def get_result(cls, key, variants):
        t = ResourceJinja.get_template(key)
        return t.render(
            **variants
        )