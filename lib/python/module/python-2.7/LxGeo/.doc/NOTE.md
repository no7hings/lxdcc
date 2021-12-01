# 2020-0806

## maya&houdini geometry data

### maya
- geometry
    - face vertex counts
        - code
        ```
        OpenMaya.MFnMesh(*args).getVertices() -> (MIntArray, MIntArray)
        
        Returns the mesh-relative/global vertex IDs for all of the mesh's
        polygons as a tuple of two int arrays. The first array contains the
        number of vertices for each polygon and the second contains the mesh-
        relative IDs for each polygon-vertex. These IDs can be used to index
        into the arrays returned by getPoints() and getFloatPoints().
        ```
        - data
        ```
        [3, 3]
        ```
    - face vertex indices
        - code
        ```
         OpenMaya.MFnMesh(*args).getVertices() -> (MIntArray, MIntArray)
        ```
        - data
        ```
        [0, 1, 2, 2, 1, 3]
        ```
    - points
        - code
        ```
        OpenMaya.MFnMesh(*args).getPoints(space=MSpace.kObject) -> MPointArray
      
        Returns a copy of the mesh's vertex positions as an MPointArray.
        ```
        - data
        ```
        [(-0.5, -1.1102230246251565e-16, 0.5), (0.5, -1.1102230246251565e-16, 0.5), (-0.5, 1.1102230246251565e-16, -0.5), (0.5, 1.1102230246251565e-16, -0.5)]
        ```
- map
    - uv counts
    ```
    [3, 3]
    ```
    - uv indices
    ```
    [0, 1, 2, 2, 1, 3]
    ```
    - us
    ```
    [1.0, 2.0, 1.0, 2.0]
    ```
    - vs
    ```
    [0.0, 0.0, 1.0, 1.0]
    ```

### houdini
- geometry
    - face vertex counts
    ```
    [3, 3]
    ```
    - face vertex indices
    ```
    [2, 1, 0, 3, 1, 2]
    ```
- map
    - uvs
    ```
    [1.0, 0.0, 2.0, 0.0, 1.0, 1.0, 2.0, 1.0]
    ```