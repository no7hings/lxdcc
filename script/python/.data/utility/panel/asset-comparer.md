# Rule
## mesh is "non-changed"
- do nothing
## mesh is "addition"
- remove the mesh
## mesh is "deletion"
- create the mesh
## mesh has "path-changed"
- repath the mesh
## mesh has "path-exchanged"
- exchange the mesh and "keep look + keep geometry-uv-map"
## mesh has "face-vertices"
- replace the mesh and "keep look + keep geometry-uv-map"
## mesh has "points-changed"
- update the mesh's points
