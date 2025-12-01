-- ========================================
-- MaxScript 示例：几何体插件开发
-- ========================================
-- 描述：演示如何创建自定义几何体对象
-- 包含参数化几何体和自定义网格生成

-- ----------------------------------------
-- 示例 1：参数化星形几何体
-- ----------------------------------------
plugin simpleObject StarShape
name:"Star"
classID:#(0x12345678, 0x87654321)
category:"Custom Objects"
(
    parameters main rollout:params (
        outerRadius type:#float ui:spnOuterRadius default:50
        innerRadius type:#float ui:spnInnerRadius default:25
        points type:#integer ui:spnPoints default:5
        height type:#float ui:spnHeight default:20
    )
    
    rollout params "Star Parameters" (
        spinner spnOuterRadius "Outer Radius:" range:[0.1, 1000, 50]
        spinner spnInnerRadius "Inner Radius:" range:[0.1, 1000, 25]
        spinner spnPoints "Points:" range:[3, 100, 5] type:#integer
        spinner spnHeight "Height:" range:[0, 1000, 20]
    )
    
    on buildMesh do (
        local numVerts = points * 2 + 1
        local numFaces = points * 4
        
        setNumVerts mesh numVerts
        setNumFaces mesh numFaces
        
        -- 创建中心顶点
        setVert mesh 1 [0, 0, height/2]
        
        -- 创建星形顶点
        for i = 1 to points * 2 do (
            local angle = (360.0 / (points * 2)) * (i - 1)
            local radius = if mod i 2 == 1 then outerRadius else innerRadius
            local x = radius * cos angle
            local y = radius * sin angle
            setVert mesh (i + 1) [x, y, 0]
        )
        
        -- 创建顶部面
        local faceIdx = 1
        for i = 1 to points * 2 do (
            local next = if i == points * 2 then 2 else i + 2
            setFace mesh faceIdx [1, i + 1, next]
            faceIdx += 1
        )
        
        -- 创建底部面
        for i = 1 to points * 2 do (
            local next = if i == points * 2 then 2 else i + 2
            setFace mesh faceIdx [next, i + 1, 1]
            faceIdx += 1
        )
    )
    
    tool create (
        on mousePoint click do (
            case click of (
                1: (
                    nodeTM.translation = gridPoint
                    outerRadius = 0
                )
                2: #stop
            )
        )
        
        on mouseMove click do (
            case click of (
                1: (
                    outerRadius = length (gridDist - nodeTM.translation)
                    innerRadius = outerRadius * 0.5
                )
            )
        )
    )
)

-- ----------------------------------------
-- 示例 2：螺旋几何体
-- ----------------------------------------
plugin simpleObject HelixObject
name:"Helix"
classID:#(0x12345679, 0x97654322)
category:"Custom Objects"
(
    parameters main rollout:params (
        radius type:#float ui:spnRadius default:30
        height type:#float ui:spnHeight default:100
        turns type:#float ui:spnTurns default:3
        segments type:#integer ui:spnSegments default:50
        wireThickness type:#float ui:spnThickness default:2
    )
    
    rollout params "Helix Parameters" (
        spinner spnRadius "Radius:" range:[0.1, 1000, 30]
        spinner spnHeight "Height:" range:[0.1, 1000, 100]
        spinner spnTurns "Turns:" range:[0.1, 100, 3]
        spinner spnSegments "Segments:" range:[3, 500, 50] type:#integer
        spinner spnThickness "Thickness:" range:[0.1, 100, 2]
    )
    
    on buildMesh do (
        -- 计算螺旋点
        local helixPoints = #()
        for i = 0 to segments do (
            local t = i as float / segments
            local angle = t * turns * 360
            local h = t * height
            local x = radius * cos angle
            local y = radius * sin angle
            append helixPoints [x, y, h]
        )
        
        -- 创建管状网格
        local sides = 8
        local numVerts = (segments + 1) * sides
        local numFaces = segments * sides * 2
        
        setNumVerts mesh numVerts
        setNumFaces mesh numFaces
        
        -- 创建顶点
        local vertIdx = 1
        for i = 1 to segments + 1 do (
            local center = helixPoints[i]
            
            -- 计算切线方向
            local tangent = if i == 1 then (
                helixPoints[2] - helixPoints[1]
            ) else if i == segments + 1 then (
                helixPoints[segments + 1] - helixPoints[segments]
            ) else (
                helixPoints[i + 1] - helixPoints[i - 1]
            )
            tangent = normalize tangent
            
            -- 创建圆环顶点
            local up = [0, 0, 1]
            local right = normalize (cross tangent up)
            if length right < 0.001 do right = [1, 0, 0]
            up = normalize (cross right tangent)
            
            for j = 1 to sides do (
                local angle = (360.0 / sides) * (j - 1)
                local offset = right * wireThickness * cos angle + up * wireThickness * sin angle
                setVert mesh vertIdx (center + offset)
                vertIdx += 1
            )
        )
        
        -- 创建面
        local faceIdx = 1
        for i = 1 to segments do (
            for j = 1 to sides do (
                local v1 = (i - 1) * sides + j
                local v2 = if j == sides then (i - 1) * sides + 1 else v1 + 1
                local v3 = v1 + sides
                local v4 = v2 + sides
                
                setFace mesh faceIdx [v1, v3, v2]
                faceIdx += 1
                setFace mesh faceIdx [v2, v3, v4]
                faceIdx += 1
            )
        )
    )
)

-- ----------------------------------------
-- 示例 3：网格操作工具
-- ----------------------------------------
struct MeshHelper (
    fn getVertexPositions obj = (
        local mesh = snapshotAsMesh obj
        local verts = #()
        for i = 1 to mesh.numVerts do (
            append verts (getVert mesh i)
        )
        delete mesh
        return verts
    ),
    
    fn setVertexPositions obj positions = (
        if classOf obj.baseObject == Editable_Mesh then (
            for i = 1 to positions.count do (
                setVert obj i positions[i]
            )
            update obj
        )
    ),
    
    fn centerPivot obj = (
        local bbox = nodeLocalBoundingBox obj
        local center = (bbox[1] + bbox[2]) / 2
        obj.pivot = obj.transform * center
    ),
    
    fn weldVertices obj threshold:0.001 = (
        if classOf obj.baseObject != Editable_Mesh do (
            convertToMesh obj
        )
        meshop.weldVertsByThreshold obj #{1..obj.numVerts} threshold
    )
)

-- 使用示例
-- helper = MeshHelper()
-- verts = helper.getVertexPositions $Box001
-- helper.centerPivot $Box001
