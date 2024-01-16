#!/usr/bin/env bash
/job/PLE/support/wrappers/paper-bin paper_cosmos@master-52 pyqt4@4.11.4 pyqt5@5.6.0 3rdmodules@wrap-1.0.0 paper_qtside@master-5 deadline_stubs@10.1.19.4 paper_prod_tools@master-46 paper_extend_shotgun@master-3 aces@1.2 maya@2019.2 paper_wrap_maya@master-5 paper_extend_maya@/home/dongchangbao/packages/paper_extend_maya/9.99.99 lxdcc@/home/dongchangbao/packages/lxdcc/9.9.99 lxdcc_gui@/home/dongchangbao/packages/lxdcc_gui/9.9.99 lxdcc_lib@/home/dongchangbao/packages/lxdcc_lib/9.9.99 lxdcc_rsc@/home/dongchangbao/packages/lxdcc_rsc/9.9.99 paper_extend_usd@master-3 --join-cmd maya -command "python(\"import lxmaya.dcc.objects as mya_dcc_objects; mya_dcc_objects.Scene.set_file_open_as_project(\\\"/data/f/test_osl/test_osl.ma\\\")\")"
