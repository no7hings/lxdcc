# Arnold Node Definition.json

```json
{
    "aiRaySwitchRgba":
        [
            "camera",
            "shadow",
            "diffuseReflection",
            "diffuseTransmission",
            "specularReflection",
            "specularTransmission",
            "volume"
        ],
    "aiRaySwitchShader":
        [
            "camera",
            "shadow",
            "diffuseReflection",
            "diffuseTransmission",
            "specularReflection",
            "specularTransmission",
            "volume"
        ],
    "aiImage":
        [
            "filename",
            "colorSpace",
            "filter",
            "mipmapBias",
            "singleChannel",
            "startChannel",
            "swrap",
            "twrap",
            "sscale",
            "tscale",
            "sflip",
            "tflip",
            "soffset",
            "toffset",
            "swapSt",
            "uvcoords",
            "uvset",
            "multiply",
            "offset",
            "ignoreMissingTextures",
            "missingTextureColor"
        ],
    "aiNoise":
        [
            "octaves",
            "distortion",
            "lacunarity",
            "amplitude",
            "scale",
            "offset",
            "coordSpace",
            "prefName",
            "P",
            "time",
            "color1",
            "color2",
            "mode"
        ],
    "aiCellNoise":
        [
            "pattern",
            "additive",
            "octaves",
            "randomness",
            "lacunarity",
            "amplitude",
            "scale",
            "offset",
            "coordSpace",
            "prefName",
            "P",
            "time",
            "color",
            "palette",
            "density"
        ],
    "aiUtility":
        [
            "colorMode",
            "shadeMode",
            "overlayMode",
            "color",
            "aoDistance",
            "roughness",
            "normal"
        ],
    "aiWireframe":
        [
            "lineWidth",
            "fillColor",
            "lineColor",
            "rasterSpace",
            "edgeType"
        ],
    "aiMotionVector":
        [
            "raw",
            "time0",
            "time1",
            "maxDisplace"
        ],
    "aiAmbientOcclusion":
        [
            "samples",
            "spread",
            "nearClip",
            "farClip",
            "falloff",
            "black",
            "white",
            "normal",
            "invertNormals",
            "traceSet",
            "inclusive",
            "selfOnly"
        ],
    "aiRoundCorners":
        [
            "samples",
            "radius",
            "normal",
            "traceSet",
            "inclusive",
            "selfOnly",
            "objectSpace"
        ],
    "aiFlat":
        [
            "color"
        ],
    "aiToon":
        [
            "maskColor",
            "edgeColor",
            "edgeTonemap",
            "edgeOpacity",
            "edgeWidthScale",
            "silhouetteColor",
            "silhouetteTonemap",
            "silhouetteOpacity",
            "silhouetteWidthScale",
            "priority",
            "enableSilhouette",
            "ignoreThroughput",
            "enable",
            "idDifference",
            "shaderDifference",
            "uvThreshold",
            "angleThreshold",
            "normalType",
            "base",
            "baseColor",
            "baseTonemap",
            "specular",
            "specularColor",
            "specularRoughness",
            "specularAnisotropy",
            "specularRotation",
            "specularTonemap",
            "lights",
            "highlightColor",
            "highlightSize",
            "aovHighlight",
            "rimLight",
            "rimLightColor",
            "rimLightWidth",
            "aovRimLight",
            "transmission",
            "transmissionColor",
            "transmissionRoughness",
            "transmissionAnisotropy",
            "transmissionRotation",
            "sheen",
            "sheenColor",
            "sheenRoughness",
            "emission",
            "emissionColor",
            "IOR",
            "normal",
            "tangent",
            "indirectDiffuse",
            "indirectSpecular",
            "bumpMode",
            "energyConserving",
            "userId"
        ],
    "aiLambert":
        [
            "Kd",
            "KdColor",
            "opacity",
            "normal"
        ],
    "aiStandard":
        [
            "Kd",
            "KdColor",
            "diffuseRoughness",
            "Ks",
            "KsColor",
            "specularRoughness",
            "specularAnisotropy",
            "specularRotation",
            "specularDistribution",
            "Kr",
            "KrColor",
            "reflectionExitColor",
            "reflectionExitUseEnvironment",
            "Kt",
            "KtColor",
            "transmittance",
            "refractionRoughness",
            "refractionExitColor",
            "refractionExitUseEnvironment",
            "IOR",
            "dispersionAbbe",
            "Kb",
            "Fresnel",
            "Krn",
            "specularFresnel",
            "Ksn",
            "FresnelUseIOR",
            "FresnelAffectDiff",
            "emission",
            "emissionColor",
            "directSpecular",
            "indirectSpecular",
            "directDiffuse",
            "indirectDiffuse",
            "enableGlossyCaustics",
            "enableReflectiveCaustics",
            "enableRefractiveCaustics",
            "enableInternalReflections",
            "Ksss",
            "KsssColor",
            "sssRadius",
            "bounceFactor",
            "opacity",
            "normal"
        ],
    "aiStandardSurface":
        [
            "base",
            "baseColor",
            "diffuseRoughness",
            "specular",
            "specularColor",
            "specularRoughness",
            "specularIOR",
            "specularAnisotropy",
            "specularRotation",
            "metalness",
            "transmission",
            "transmissionColor",
            "transmissionDepth",
            "transmissionScatter",
            "transmissionScatterAnisotropy",
            "transmissionDispersion",
            "transmissionExtraRoughness",
            "transmitAovs",
            "subsurface",
            "subsurfaceColor",
            "subsurfaceRadius",
            "subsurfaceScale",
            "subsurfaceAnisotropy",
            "subsurfaceType",
            "sheen",
            "sheenColor",
            "sheenRoughness",
            "thinWalled",
            "normal",
            "tangent",
            "coat",
            "coatColor",
            "coatRoughness",
            "coatIOR",
            "coatAnisotropy",
            "coatRotation",
            "coatNormal",
            "coatAffectColor",
            "coatAffectRoughness",
            "thinFilmThickness",
            "thinFilmIOR",
            "emission",
            "emissionColor",
            "opacity",
            "caustics",
            "internalReflections",
            "exitToBackground",
            "indirectDiffuse",
            "indirectSpecular",
            "aovId1",
            "id1",
            "aovId2",
            "id2",
            "aovId3",
            "id3",
            "aovId4",
            "id4",
            "aovId5",
            "id5",
            "aovId6",
            "id6",
            "aovId7",
            "id7",
            "aovId8",
            "id8"
        ],
    "aiHair":
        [
            "rootcolor",
            "tipcolor",
            "opacity",
            "ambdiff",
            "spec",
            "specColor",
            "specShift",
            "specGloss",
            "spec2",
            "spec2Color",
            "spec2Shift",
            "spec2Gloss",
            "transmission",
            "transmissionColor",
            "transmissionSpread",
            "kdInd"
        ],
    "aiStandardHair":
        [
            "base",
            "baseColor",
            "melanin",
            "melaninRedness",
            "melaninRandomize",
            "roughness",
            "roughnessAzimuthal",
            "roughnessAnisotropic",
            "ior",
            "shift",
            "specularTint",
            "specular2Tint",
            "transmissionTint",
            "diffuse",
            "diffuseColor",
            "emission",
            "emissionColor",
            "opacity",
            "indirectDiffuse",
            "indirectSpecular",
            "extraDepth",
            "extraSamples",
            "aovId1",
            "id1",
            "aovId2",
            "id2",
            "aovId3",
            "id3",
            "aovId4",
            "id4",
            "aovId5",
            "id5",
            "aovId6",
            "id6",
            "aovId7",
            "id7",
            "aovId8",
            "id8"
        ],
    "aiCarPaint":
        [
            "base",
            "baseColor",
            "baseRoughness",
            "specular",
            "specularColor",
            "specularFlipFlop",
            "specularLightFacing",
            "specularFalloff",
            "specularRoughness",
            "specularIOR",
            "transmissionColor",
            "flakeColor",
            "flakeFlipFlop",
            "flakeLightFacing",
            "flakeFalloff",
            "flakeRoughness",
            "flakeIOR",
            "flakeScale",
            "flakeDensity",
            "flakeLayers",
            "flakeNormalRandomize",
            "flakeCoordSpace",
            "prefName",
            "coat",
            "coatColor",
            "coatRoughness",
            "coatIOR",
            "coatNormal"
        ],
    "aiBump2d":
        [
            "bumpMap",
            "bumpHeight",
            "normal"
        ],
    "aiBump3d":
        [
            "bumpMap",
            "bumpHeight",
            "epsilon",
            "normal"
        ],
    "aiMixShader":
        [
            "mode",
            "mix",
            "shader1",
            "shader2"
        ],
    "aiSky":
        [
            "color",
            "intensity",
            "visibility",
            "opaqueAlpha",
            "format",
            "XAngle",
            "YAngle",
            "ZAngle",
            "X",
            "Y",
            "Z"
        ],
    "aiPhysicalSky":
        [
            "turbidity",
            "groundAlbedo",
            "useDegrees",
            "elevation",
            "azimuth",
            "sunDirection",
            "enableSun",
            "sunSize",
            "sunTint",
            "skyTint",
            "intensity",
            "X",
            "Y",
            "Z"
        ],
    "aiAtmosphereVolume":
        [
            "density",
            "samples",
            "eccentricity",
            "attenuation",
            "affectCamera",
            "affectDiffuse",
            "affectSpecular",
            "rgbDensity",
            "rgbAttenuation"
        ],
    "aiFog":
        [
            "distance",
            "height",
            "color",
            "groundPoint",
            "groundNormal"
        ],
    "aiStandardVolume":
        [
            "density",
            "densityChannel",
            "scatter",
            "scatterColor",
            "scatterColorChannel",
            "scatterAnisotropy",
            "transparent",
            "transparentDepth",
            "transparentChannel",
            "emissionMode",
            "emission",
            "emissionColor",
            "emissionChannel",
            "temperature",
            "temperatureChannel",
            "blackbodyKelvin",
            "blackbodyIntensity",
            "displacement",
            "interpolation"
        ],
    "aiAbs":
        [
            "input"
        ],
    "aiAdd":
        [
            "input1",
            "input2"
        ],
    "aiAovReadFloat":
        [
            "aovName"
        ],
    "aiAovReadInt":
        [
            "aovName"
        ],
    "aiAovReadRgb":
        [
            "aovName"
        ],
    "aiAovReadRgba":
        [
            "aovName"
        ],
    "aiAovWriteFloat":
        [
            "passthrough",
            "aovInput",
            "aovName",
            "blendOpacity"
        ],
    "aiAovWriteInt":
        [
            "passthrough",
            "aovInput",
            "aovName"
        ],
    "aiAovWriteRgb":
        [
            "passthrough",
            "aovInput",
            "aovName",
            "blendOpacity"
        ],
    "aiAovWriteRgba":
        [
            "passthrough",
            "aovInput",
            "aovName",
            "blendOpacity"
        ],
    "aiAtan":
        [
            "y",
            "x",
            "units"
        ],
    "aiBlackbody":
        [
            "temperature",
            "normalize",
            "intensity"
        ],
    "aiCache":
        [
            "input"
        ],
    "aiCameraProjection":
        [
            "projectionColor",
            "offscreenColor",
            "mask",
            "camera",
            "aspectRatio",
            "frontFacing",
            "backFacing",
            "useShadingNormal",
            "coordSpace",
            "prefName",
            "P"
        ],
    "aiCheckerboard":
        [
            "color1",
            "color2",
            "uFrequency",
            "vFrequency",
            "uOffset",
            "vOffset",
            "contrast",
            "filterStrength",
            "filterOffset",
            "uvset"
        ],
    "aiClamp":
        [
            "input",
            "mode",
            "min",
            "max",
            "minColor",
            "maxColor"
        ],
    "aiClipGeo":
        [
            "intersection",
            "traceSet",
            "inclusive"
        ],
    "aiColorConvert":
        [
            "input",
            "from",
            "to"
        ],
    "aiColorCorrect":
        [
            "input",
            "alphaIsLuminance",
            "alphaMultiply",
            "alphaAdd",
            "invert",
            "invertAlpha",
            "gamma",
            "hueShift",
            "saturation",
            "contrast",
            "contrastPivot",
            "exposure",
            "multiply",
            "add",
            "mask"
        ],
    "aiColorJitter":
        [
            "input",
            "dataInput",
            "dataGainMin",
            "dataGainMax",
            "dataHueMin",
            "dataHueMax",
            "dataSaturationMin",
            "dataSaturationMax",
            "dataSeed",
            "procGainMin",
            "procGainMax",
            "procHueMin",
            "procHueMax",
            "procSaturationMin",
            "procSaturationMax",
            "procSeed",
            "objGainMin",
            "objGainMax",
            "objHueMin",
            "objHueMax",
            "objSaturationMin",
            "objSaturationMax",
            "objSeed",
            "faceGainMin",
            "faceGainMax",
            "faceHueMin",
            "faceHueMax",
            "faceSaturationMin",
            "faceSaturationMax",
            "faceSeed",
            "faceMode"
        ],
    "aiCompare":
        [
            "test",
            "input1",
            "input2"
        ],
    "aiComplement":
        [
            "input"
        ],
    "aiComplexIor":
        [
            "material",
            "mode",
            "reflectivity",
            "edgetint",
            "n",
            "k"
        ],
    "aiComposite":
        [
            "A",
            "B",
            "operation",
            "alphaOperation"
        ],
    "aiCross":
        [
            "input1",
            "input2"
        ],
    "aiCurvature":
        [
            "output",
            "samples",
            "radius",
            "spread",
            "threshold",
            "bias",
            "multiply",
            "traceSet",
            "inclusive",
            "selfOnly"
        ],
    "aiDivide":
        [
            "input1",
            "input2"
        ],
    "aiDot":
        [
            "input1",
            "input2"
        ],
    "aiExp":
        [
            "input"
        ],
    "aiFacingRatio":
        [
            "bias",
            "gain",
            "linear",
            "invert"
        ],
    "aiFlakes":
        [
            "scale",
            "density",
            "step",
            "depth",
            "IOR",
            "normalRandomize",
            "coordSpace",
            "prefName",
            "outputSpace"
        ],
    "aiFloatToInt":
        [
            "input",
            "mode"
        ],
    "aiFloatToMatrix":
        [
            "input00",
            "input01",
            "input02",
            "input03",
            "input10",
            "input11",
            "input12",
            "input13",
            "input20",
            "input21",
            "input22",
            "input23",
            "input30",
            "input31",
            "input32",
            "input33"
        ],
    "aiFloatToRgba":
        [
            "r",
            "g",
            "b",
            "a"
        ],
    "aiFloatToRgb":
        [
            "r",
            "g",
            "b"
        ],
    "aiFraction":
        [
            "input"
        ],
    "aiIsFinite":
        [
            "input"
        ],
    "aiLayerFloat":
        [
            "enable1",
            "name1",
            "input1",
            "mix1",
            "enable2",
            "name2",
            "input2",
            "mix2",
            "enable3",
            "name3",
            "input3",
            "mix3",
            "enable4",
            "name4",
            "input4",
            "mix4",
            "enable5",
            "name5",
            "input5",
            "mix5",
            "enable6",
            "name6",
            "input6",
            "mix6",
            "enable7",
            "name7",
            "input7",
            "mix7",
            "enable8",
            "name8",
            "input8",
            "mix8"
        ],
    "aiLayerRgba":
        [
            "enable1",
            "name1",
            "input1",
            "mix1",
            "operation1",
            "alphaOperation1",
            "enable2",
            "name2",
            "input2",
            "mix2",
            "operation2",
            "alphaOperation2",
            "enable3",
            "name3",
            "input3",
            "mix3",
            "operation3",
            "alphaOperation3",
            "enable4",
            "name4",
            "input4",
            "mix4",
            "operation4",
            "alphaOperation4",
            "enable5",
            "name5",
            "input5",
            "mix5",
            "operation5",
            "alphaOperation5",
            "enable6",
            "name6",
            "input6",
            "mix6",
            "operation6",
            "alphaOperation6",
            "enable7",
            "name7",
            "input7",
            "mix7",
            "operation7",
            "alphaOperation7",
            "enable8",
            "name8",
            "input8",
            "mix8",
            "operation8",
            "alphaOperation8",
            "clamp"
        ],
    "aiLayerShader":
        [
            "enable1",
            "name1",
            "input1",
            "mix1",
            "enable2",
            "name2",
            "input2",
            "mix2",
            "enable3",
            "name3",
            "input3",
            "mix3",
            "enable4",
            "name4",
            "input4",
            "mix4",
            "enable5",
            "name5",
            "input5",
            "mix5",
            "enable6",
            "name6",
            "input6",
            "mix6",
            "enable7",
            "name7",
            "input7",
            "mix7",
            "enable8",
            "name8",
            "input8",
            "mix8"
        ],
    "aiLength":
        [
            "input",
            "mode"
        ],
    "aiLog":
        [
            "input",
            "base"
        ],
    "aiMatrixInterpolate":
        [
            "type",
            "value"
        ],
    "aiMatrixMultiplyVector":
        [
            "input",
            "type",
            "matrix"
        ],
    "aiMatrixTransform":
        [
            "transformOrder",
            "rotationType",
            "units",
            "rotationOrder",
            "rotation",
            "axis",
            "angle",
            "translate",
            "scale",
            "pivot"
        ],
    "aiMatte":
        [
            "passthrough",
            "color",
            "opacity"
        ],
    "aiMax":
        [
            "input1",
            "input2"
        ],
    "aiMin":
        [
            "input1",
            "input2"
        ],
    "aiMixRgba":
        [
            "input1",
            "input2",
            "mix"
        ],
    "aiModulo":
        [
            "input",
            "divisor"
        ],
    "aiMultiply":
        [
            "input1",
            "input2"
        ],
    "aiNegate":
        [
            "input"
        ],
    "aiNormalize":
        [
            "input"
        ],
    "aiNormalMap":
        [
            "input",
            "tangent",
            "normal",
            "order",
            "invertX",
            "invertY",
            "invertZ",
            "colorToSigned",
            "tangentSpace",
            "strength"
        ],
    "aiPassthrough":
        [
            "passthrough",
            "eval1",
            "eval2",
            "eval3",
            "eval4",
            "eval5",
            "eval6",
            "eval7",
            "eval8",
            "eval9",
            "eval10",
            "eval11",
            "eval12",
            "eval13",
            "eval14",
            "eval15",
            "eval16",
            "eval17",
            "eval18",
            "eval19",
            "eval20",
            "normal"
        ],
    "aiPow":
        [
            "base",
            "exponent"
        ],
    "aiQueryShape":
        [
        ],
    "aiRampFloat":
        [
            "type",
            "input",
            "position",
            "value",
            "interpolation",
            "uvset",
            "useImplicitUvs",
            "wrapUvs"
        ],
    "aiRampRgb":
        [
            "type",
            "input",
            "position",
            "color",
            "interpolation",
            "uvset",
            "useImplicitUvs",
            "wrapUvs"
        ],
    "aiRandom":
        [
            "inputType",
            "inputInt",
            "inputFloat",
            "inputColor",
            "seed",
            "grayscale"
        ],
    "aiRange":
        [
            "input",
            "inputMin",
            "inputMax",
            "outputMin",
            "outputMax",
            "smoothstep",
            "contrast",
            "contrastPivot",
            "bias",
            "gain"
        ],
    "aiReciprocal":
        [
            "input"
        ],
    "aiRgbaToFloat":
        [
            "input",
            "mode"
        ],
    "aiRgbToFloat":
        [
            "input",
            "mode"
        ],
    "aiRgbToVector":
        [
            "input",
            "mode"
        ],
    "aiShadowMatte":
        [
            "background",
            "shadowColor",
            "shadowOpacity",
            "backgroundColor",
            "diffuseColor",
            "diffuseUseBackground",
            "diffuseIntensity",
            "backlighting",
            "indirectDiffuseEnable",
            "indirectSpecularEnable",
            "specularColor",
            "specularIntensity",
            "specularRoughness",
            "specularIOR",
            "alphaMask",
            "aovGroup",
            "aovShadow",
            "aovShadowDiff",
            "aovShadowMask"
        ],
    "aiShuffle":
        [
            "color",
            "alpha",
            "channelR",
            "channelG",
            "channelB",
            "channelA",
            "negateR",
            "negateG",
            "negateB",
            "negateA"
        ],
    "aiSign":
        [
            "input"
        ],
    "aiSkin":
        [
            "sssWeight",
            "shallowScatterColor",
            "shallowScatterWeight",
            "shallowScatterRadius",
            "midScatterColor",
            "midScatterWeight",
            "midScatterRadius",
            "deepScatterColor",
            "deepScatterWeight",
            "deepScatterRadius",
            "specularColor",
            "specularWeight",
            "specularRoughness",
            "specularIor",
            "sheenColor",
            "sheenWeight",
            "sheenRoughness",
            "sheenIor",
            "globalSssRadiusMultiplier",
            "specularInSecondaryRays",
            "fresnelAffectSss",
            "opacity",
            "opacityColor",
            "normal"
        ],
    "aiSpaceTransform":
        [
            "input",
            "type",
            "from",
            "to",
            "tangent",
            "normal",
            "normalize",
            "scale"
        ],
    "aiSqrt":
        [
            "input"
        ],
    "aiStateFloat":
        [
            "variable"
        ],
    "aiStateInt":
        [
            "variable"
        ],
    "aiStateVector":
        [
            "variable"
        ],
    "aiSubtract":
        [
            "input1",
            "input2"
        ],
    "aiSwitchRgba":
        [
            "index",
            "input0",
            "input1",
            "input2",
            "input3",
            "input4",
            "input5",
            "input6",
            "input7",
            "input8",
            "input9",
            "input10",
            "input11",
            "input12",
            "input13",
            "input14",
            "input15",
            "input16",
            "input17",
            "input18",
            "input19"
        ],
    "aiSwitchShader":
        [
            "index",
            "input0",
            "input1",
            "input2",
            "input3",
            "input4",
            "input5",
            "input6",
            "input7",
            "input8",
            "input9",
            "input10",
            "input11",
            "input12",
            "input13",
            "input14",
            "input15",
            "input16",
            "input17",
            "input18",
            "input19"
        ],
    "aiThinFilm":
        [
            "thicknessMin",
            "thicknessMax",
            "thickness",
            "iorMedium",
            "iorFilm",
            "iorInternal"
        ],
    "aiTraceSet":
        [
            "passthrough",
            "traceSet",
            "inclusive"
        ],
    "aiTrigo":
        [
            "input",
            "function",
            "units",
            "frequency",
            "phase"
        ],
    "aiTriplanar":
        [
            "input",
            "scale",
            "rotate",
            "offset",
            "coordSpace",
            "prefName",
            "blend",
            "cell",
            "cellRotate",
            "cellBlend"
        ],
    "aiTwoSided":
        [
            "front",
            "back"
        ],
    "aiUserDataFloat":
        [
            "attribute",
            "default"
        ],
    "aiUserDataInt":
        [
            "attribute",
            "default"
        ],
    "aiUserDataRgba":
        [
            "attribute",
            "default"
        ],
    "aiUserDataRgb":
        [
            "attribute",
            "default"
        ],
    "aiUserDataString":
        [
            "attribute",
            "default"
        ],
    "aiUvTransform":
        [
            "passthrough",
            "unit",
            "uvset",
            "coverage",
            "scaleFrame",
            "translateFrame",
            "rotateFrame",
            "pivotFrame",
            "wrapFrameU",
            "wrapFrameV",
            "wrapFrameColor",
            "repeat",
            "offset",
            "rotate",
            "pivot",
            "noise",
            "mirrorU",
            "mirrorV",
            "flipU",
            "flipV",
            "swapUv",
            "stagger"
        ],
    "aiUvProjection":
        [
            "projectionColor",
            "projectionType",
            "coordSpace",
            "prefName",
            "P",
            "uAngle",
            "vAngle",
            "clamp",
            "defaultColor",
            "matrix"
        ],
    "aiVectorMap":
        [
            "input",
            "tangent",
            "normal",
            "order",
            "invertX",
            "invertY",
            "invertZ",
            "colorToSigned",
            "tangentSpace",
            "scale"
        ],
    "aiVectorToRgb":
        [
            "input",
            "mode"
        ],
    "aiVolumeCollector":
        [
            "scatteringSource",
            "scattering",
            "scatteringChannel",
            "scatteringColor",
            "scatteringIntensity",
            "anisotropy",
            "attenuationSource",
            "attenuation",
            "attenuationChannel",
            "attenuationColor",
            "attenuationIntensity",
            "attenuationMode",
            "emissionSource",
            "emission",
            "emissionChannel",
            "emissionColor",
            "emissionIntensity",
            "positionOffset",
            "interpolation"
        ],
    "aiVolumeSampleFloat":
        [
            "channel",
            "positionOffset",
            "interpolation",
            "volumeType",
            "sdfOffset",
            "sdfBlend",
            "sdfInvert",
            "inputMin",
            "inputMax",
            "contrast",
            "contrastPivot",
            "bias",
            "gain",
            "outputMin",
            "outputMax",
            "clampMin",
            "clampMax"
        ],
    "aiVolumeSampleRgb":
        [
            "channel",
            "positionOffset",
            "interpolation",
            "gamma",
            "hueShift",
            "saturation",
            "contrast",
            "contrastPivot",
            "exposure",
            "multiply",
            "add"
        ],
    "aiC4dTextureTag":
        [
            "color",
            "proj",
            "lenx",
            "leny",
            "ox",
            "oy",
            "tilex",
            "tiley",
            "m",
            "camera",
            "aspectRatio",
            "usePref",
            "side"
        ],
    "aiC4dTextureTagRgba":
        [
            "color",
            "proj",
            "lenx",
            "leny",
            "ox",
            "oy",
            "tilex",
            "tiley",
            "m",
            "camera",
            "aspectRatio",
            "usePref",
            "side"
        ],
    "aiMayaLayeredShader":
        [
            "compositingFlag",
            "numInputs",
            "color0",
            "color1",
            "color2",
            "color3",
            "color4",
            "color5",
            "color6",
            "color7",
            "color8",
            "color9",
            "color10",
            "color11",
            "color12",
            "color13",
            "color14",
            "color15",
            "transparency0",
            "transparency1",
            "transparency2",
            "transparency3",
            "transparency4",
            "transparency5",
            "transparency6",
            "transparency7",
            "transparency8",
            "transparency9",
            "transparency10",
            "transparency11",
            "transparency12",
            "transparency13",
            "transparency14",
            "transparency15",
            "useTransparency0",
            "useTransparency1",
            "useTransparency2",
            "useTransparency3",
            "useTransparency4",
            "useTransparency5",
            "useTransparency6",
            "useTransparency7",
            "useTransparency8",
            "useTransparency9",
            "useTransparency10",
            "useTransparency11",
            "useTransparency12",
            "useTransparency13",
            "useTransparency14",
            "useTransparency15"
        ]
}
```

