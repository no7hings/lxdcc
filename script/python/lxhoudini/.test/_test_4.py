# coding:utf-8
import hou

from PySide2 import QtWidgets

w = hou.qt.mainWindow()
print '*' * 100


def rcs(w):
    if w.__class__.__name__ == 'QMenu':
        print w

    for i in w.children():
        if isinstance(i, QtWidgets.QLayout):
            layout = i
            count = layout.count()
            for j in range(0, count):
                item = layout.itemAt(j)
                if item:
                    widget = item.widget()
                    for k in widget.children():
                        rcs(k)
        else:
            for k in i.children():
                rcs(k)


rcs(w)