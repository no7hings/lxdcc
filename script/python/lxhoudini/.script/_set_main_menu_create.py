# coding:utf-8
import os

import shutil

from lxutil import utl_setup

file_path = os.path.dirname(__file__)

c = utl_setup.HoudiniSetupCreator(file_path)

main_menu_xml_file = c.set_main_menu_xml_create()
print main_menu_xml_file

shutil.copy2(
    main_menu_xml_file,
    '/data/e/myworkspace/td/lynxi/script/python/.setup/houdini/MainMenuCommon.xml'
)
