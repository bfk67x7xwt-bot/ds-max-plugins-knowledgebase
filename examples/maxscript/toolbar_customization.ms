-- ========================================
-- MaxScript 示例：工具栏自定义
-- ========================================
-- 描述：演示如何创建自定义工具栏按钮和菜单项
-- 文件类型：保存为 .mcr 文件放入 usermacros 目录

-- ----------------------------------------
-- 示例 1：简单宏脚本
-- ----------------------------------------
macroScript QuickBox
category:"Custom Tools"
tooltip:"Quick Create Box"
buttonText:"Quick Box"
(
    -- 在鼠标位置创建盒子
    on execute do (
        local mousePos = mouse.screenPos
        local worldPos = mapScreenToWorld mouse.pos
        
        local newBox = box length:50 width:50 height:50
        newBox.pos = [0, 0, 0]
        newBox.wirecolor = random (color 0 0 0) (color 255 255 255)
        
        select newBox
        messageBox "Box created!" title:"Quick Box"
    )
    
    on isEnabled return true
)

-- ----------------------------------------
-- 示例 2：带有 UI 的工具
-- ----------------------------------------
macroScript ToolWithUI
category:"Custom Tools"
tooltip:"Tool with Dialog"
buttonText:"Tool UI"
(
    rollout toolRollout "Custom Tool" width:200 (
        group "Object Settings" (
            spinner spnSize "Size:" range:[1,1000,50]
            colorpicker cpColor "Color:" color:(color 255 0 0)
            dropdownlist ddlType "Type:" items:#("Box", "Sphere", "Cylinder")
        )
        
        group "Actions" (
            button btnCreate "Create Object" width:180
            button btnDelete "Delete Selected" width:180
            button btnRandom "Randomize Colors" width:180
        )
        
        label lblStatus ""
        
        on btnCreate pressed do (
            local obj = case ddlType.selection of (
                1: box length:spnSize.value width:spnSize.value height:spnSize.value
                2: sphere radius:(spnSize.value/2)
                3: cylinder radius:(spnSize.value/2) height:spnSize.value
            )
            obj.wirecolor = cpColor.color
            select obj
            lblStatus.text = "Created: " + obj.name
        )
        
        on btnDelete pressed do (
            local count = selection.count
            if count > 0 then (
                delete selection
                lblStatus.text = "Deleted " + count as string + " objects"
            ) else (
                lblStatus.text = "No objects selected"
            )
        )
        
        on btnRandom pressed do (
            for obj in selection do (
                obj.wirecolor = random (color 0 0 0) (color 255 255 255)
            )
            lblStatus.text = "Randomized " + selection.count as string + " objects"
        )
    )
    
    on execute do (
        createDialog toolRollout
    )
)

-- ----------------------------------------
-- 示例 3：切换开关工具
-- ----------------------------------------
macroScript ToggleTool
category:"Custom Tools"
tooltip:"Toggle Wire Display"
buttonText:"Toggle Wire"
(
    local isWireMode = false
    
    on execute do (
        isWireMode = not isWireMode
        
        for obj in objects do (
            if isWireMode then (
                obj.displayByLayer = false
                obj.boxMode = true
            ) else (
                obj.boxMode = false
            )
        )
        
        redrawViews()
    )
    
    on isChecked return isWireMode
)

-- ----------------------------------------
-- 示例 4：右键菜单扩展
-- ----------------------------------------
fn registerContextMenu = (
    rcMenu customMenu (
        menuItem miSelect "Select All Boxes"
        menuItem miDelete "Delete All Spheres"
        separator sep1
        subMenu "Transform" (
            menuItem miReset "Reset Transform"
            menuItem miCenter "Center to Origin"
        )
        
        on miSelect picked do (
            select (for obj in objects where classOf obj == Box collect obj)
        )
        
        on miDelete picked do (
            delete (for obj in objects where classOf obj == Sphere collect obj)
        )
        
        on miReset picked do (
            for obj in selection do (
                resetXForm obj
            )
        )
        
        on miCenter picked do (
            for obj in selection do (
                obj.pos = [0, 0, 0]
            )
        )
    )
    
    registerRightClickMenu #customTools customMenu
)
