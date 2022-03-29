# coding:utf-8
import lxmaya.ssn.objects as ssn_objects

app = ssn_objects.RsvApplication()

rsv_scene_properties = app.get_rsv_scene_properties()

print rsv_scene_properties

print rsv_scene_properties.get('project')
print rsv_scene_properties.get('step')
print rsv_scene_properties.get(rsv_scene_properties.get('branch'))
print rsv_scene_properties.get('task')

stg_connector = app.get_stg_connector()

print stg_connector.get_stg_project(**rsv_scene_properties.value)
print stg_connector.get_stg_entity(**rsv_scene_properties.value)
print stg_connector.get_stg_step(**rsv_scene_properties.value)
print stg_connector.get_stg_task(**rsv_scene_properties.value)

