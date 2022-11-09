# coding:utf-8
if __name__ == '__main__':
    import lxresolver.commands as rsv_commands

    r = rsv_commands.get_resolver()

    rsv_project = r.get_rsv_project(project='cgm')

    rsv_entity = rsv_project.get_rsv_resource(
        shot='z88320'
    )
    print rsv_entity.get_available_rsv_unit(
        task=['final_layout', 'animation', 'blocking', 'rough_layout'], keyword='shot-maya-scene-file'
    )
