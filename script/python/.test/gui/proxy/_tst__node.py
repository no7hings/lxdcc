# coding:utf-8
import os

import six

import lxbasic.storage as bsc_storage

import fnmatch

import lxgui.proxy.widgets as prx_widgets

y_f = '{}.yml'.format(os.path.splitext(__file__)[0])

c = bsc_storage.StgFileOpt(y_f).set_read()


class TestWindow(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self.set_definition_window_size([720, 720])
        self._test_()

    def _value_completion_gain_fnc_(self, *args, **kwargs):
        k = args[0]
        if isinstance(k, six.text_type):
            k = k.encode('utf-8')
        return fnmatch.filter(
            ['test'], '*{}*'.format(k)
        )

    def _test_(self):
        tab_view = prx_widgets.PrxTabView()
        self.add_widget(tab_view)
        self.set_main_style_mode(1)
        for i in [
            'constant',
            'tuple',
            'array',
            'shotgun',
            'storage',
            'storages',
        ]:
            i_s = prx_widgets.PrxVScrollArea()
            tab_view.add_widget(i_s, name=i)
            i_n = prx_widgets.PrxNode(i)
            i_s.add_widget(i_n)
            i_n.create_ports_by_data(
                c.get(i)
            )
            # print i_n.get_all_ports()

        # n.get_port('files.list').set_root('/data/e/workspace/lynxi/script/python/.resources/icons')
        # n.set('files.list', ['/data/e/workspace/lynxi/script/python/.resources/icons/add.svg'])
        #
        # n.get_port('files.tree').set_root('/data/e/workspace/lynxi/script/python/.resources/icons')
        # n.set('files.tree', ['/data/e/workspace/lynxi/script/python/.resources/icons/add.svg'])


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    w = TestWindow()
    #
    w.set_window_show()
    #
    sys.exit(app.exec_())
