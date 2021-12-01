# coding:utf-8
from lxusd import usd_configure

j2_template = usd_configure.JinJa2.ENVIRONMENT.get_template('geometry-xml-template.j2')

ks = dict(
    option=dict(
        indent=4,
        linesep='\n'
    ),
    objs={
        "master": {
            "properties": {
                "type": "transform",
            },
            "hi": {
                "properties": {
                    "type": "transform"
                },
                "body_higrp": {
                    "properties": {
                        "type": "transform"
                    },
                    "M_body_higrp": {
                        "properties": {
                            "type": "transform"
                        },
                        "M_body_001_hi": {
                            "properties": {
                                "type": "transform"
                            },
                            "M_body_001_hiShape": {
                                "properties": {
                                    "type": "mesh",
                                    "attributes": {
                                        'edge': 10
                                    }
                                }
                            }
                        }
                    }
                }
            },
            'lo': {
                "properties": {
                    "type": "transform"
                }
            },
        }
    }
)

raw = j2_template.render(**ks)

print raw



