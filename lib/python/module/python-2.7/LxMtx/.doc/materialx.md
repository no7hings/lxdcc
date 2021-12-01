[TOC]

# materialx

## what?

- 基于XML格式的一种数据标准（扩展名“.mtlx”），用于记录“Graphics”（节点图， 主要是“Material”）的数据；
- MTLX文件可以是完全独立的，或拆分成多个文件以实现共用和复用。

## why?

- 解决不同生产环节/DCC软件/渲染器间的“Graphics”的数据传递；
- 解决不同部门和供应商之间的“Graphics”数据传输。

## element

- 定义了处理节点图数据的标准节点；
- 使用<nodedef>定义和扩展“BxDF Shader”（基于“BSDF”和“BRDF”算法的材质或者节点）标准节点集；
- 使用<material>定义“Shader”（材质， 如Surface Shader， Displacement Shader）实例引用的数据流；
- 使用<geominfo>定义可从节点图中引用的“Geometry”的属性；
- 使用<look>定义与“Geometry”绑定的“Material”和“Property”（特定属性， 如细分等）组合。

# reference

- [github](https://github.com/materialx)

- [arnold](https://docs.arnoldrenderer.com/display/A5AFMUG/MaterialX)

- [houdini - export](https://docs.arnoldrenderer.com/display/A5AFHUG/MaterialX+Export)

# note
- **Arnold**
    - **Geometry** 不支持“Dcc Property”
        - Maya: 存在“Maya Property”
            - 解决方案
    - **Node**：不支持“Dcc Node”；
        - Maya：存在使用“Maya Node”的情况
            - 解决方案：
                - 制作规范中禁止使用Arnold以外的节点
        - Houdini：符合规则
        
    - **Port**：不支持“Array”类型的“Port”连接
        - Maya: 存在“Ramp”类型的节点的子通道的连接
            - 解决方案:
                - 制作规范中禁止“Ramp”子通道的连接
        - Houdini: 存在“Ramp”类型的节点的子通道的连接
            - 解决方案:
                - 制作规范中禁止“Ramp”子通道的连接

    - **Output**：“Node”的“Output”为“唯一”复合型输出
        - Maya：存在多种“Output”输出。
            - 解决方案：
                - 导出的时候会转化为支持的“Output”通道
                    - OutColor
                    - OutAlpha
                - 制作规范中规定可用的“Output”通道
        - Houdini：符合规则

    - **Channel Connection**：不支持“Channel”之间的直接连接
        - Maya：存在这种连接方式
            - 解决方案：
                - 制作规范中禁止这种连接方式
        - Houdini：符合规则

    - **Color Space**：需要统一色彩空间
        - 现在Maya和Houdini的色彩空间存在问题，需要统一色彩空间的标准。

