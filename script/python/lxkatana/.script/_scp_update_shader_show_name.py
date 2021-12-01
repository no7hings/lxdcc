# coding:utf-8


if __name__ == '__main__':
    for i in NodegraphAPI.GetAllNodesByType('ArnoldShadingNode'):
        atrs = i.getAttributes()
        obj_name = i.getName()
        show_name = atrs.get('ns_displayName')
        if show_name is not None:
            if show_name != obj_name:
                atrs['ns_displayName'] = obj_name
                i.setAttributes(atrs)


