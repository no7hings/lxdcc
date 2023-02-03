# coding:utf-8
import types

_objectStore = {}


#
def pyToMelProc(pyObj, args=(), returnType=None, procName=None, useName=False, procPrefix='pyToMel_'):
    melParams = []
    pyParams = []
    melReturn = returnType if returnType else ''
    #
    for t, n in args:
        melParams.append('%s $%s' % (t, n))
        #
        if t == 'string':
            pyParams.append(r"""'"+$%s+"'""" % n)
        else:
            pyParams.append(r'"+$%s+"' % n)
    #
    objId = id(pyObj)
    #
    d = {}
    #
    if procName:
        d['procName'] = procName
    elif useName:
        d['procName'] = pyObj.__name__
    else:
        if isinstance(pyObj, types.LambdaType):
            procPrefix += '_lambda'
        elif isinstance(pyObj, (types.FunctionType, types.BuiltinFunctionType)):
            try:
                procPrefix += '_' + pyObj.__name__
            except (AttributeError, TypeError):
                pass
        elif isinstance(pyObj, types.MethodType):
            try:
                procPrefix += '_' + pyObj.im_class.__name__ + '_' + pyObj.__name__
            except (AttributeError, TypeError):
                pass
        d['procName'] = '%s%s' % (procPrefix, objId)
    #
    d['procName'] = d['procName'].replace('<', '_').replace('>', '_').replace('-', '_')
    d['melParams'] = ', '.join(melParams)
    d['pyParams'] = ', '.join(pyParams)
    d['melReturn'] = melReturn
    d['thisModule'] = __name__
    d['id'] = objId
    #
    contents = '''global proc %(melReturn)s %(procName)s(%(melParams)s){'''
    if melReturn:
        contents += 'return '
    contents += '''python("import %(thisModule)s;%(thisModule)s._objectStore[%(id)s](%(pyParams)s)");}'''
    # mel.eval(contents % d)
    print contents % d
    _objectStore[objId] = pyObj
    return d['procName']


def test():
    pass


pyToMelProc(
    test
)
