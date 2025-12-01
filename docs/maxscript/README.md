# MaxScript 开发指南

MaxScript 是 3ds Max 内置的脚本语言，适合快速原型开发和简单工具的创建。

## 目录

- [基础入门](#基础入门)
- [脚本结构](#脚本结构)
- [常用对象操作](#常用对象操作)
- [用户界面开发](#用户界面开发)
- [工具栏自定义](#工具栏自定义)
- [事件处理](#事件处理)
- [调试技巧](#调试技巧)

## 基础入门

### 脚本文件类型

| 扩展名 | 描述 |
|-------|------|
| `.ms` | 标准 MaxScript 文件 |
| `.mcr` | 宏脚本文件（用于创建菜单和工具栏按钮） |
| `.mse` | 加密的 MaxScript 文件 |

### Hello World 示例

```maxscript
-- 第一个 MaxScript 程序
messageBox "Hello, 3ds Max!"
```

### 变量和数据类型

```maxscript
-- 变量声明
myNumber = 42
myFloat = 3.14
myString = "Hello"
myArray = #(1, 2, 3, 4, 5)
myPoint = [10, 20, 30]
myColor = color 255 0 0

-- 类型检查
classOf myNumber  -- 返回 Integer
classOf myPoint   -- 返回 Point3
```

## 脚本结构

### 结构体定义

```maxscript
struct MyPlugin (
    name = "My Plugin",
    version = 1.0,
    
    fn initialize = (
        print ("Initializing " + name)
    ),
    
    fn run = (
        -- 主要逻辑
    )
)

-- 使用结构体
plugin = MyPlugin()
plugin.initialize()
```

### 宏脚本模板

```maxscript
macroScript MyMacro
category:"My Tools"
tooltip:"My Tool Description"
buttonText:"My Tool"
(
    on execute do (
        -- 工具执行代码
        print "Tool executed!"
    )
)
```

## 常用对象操作

### 创建几何体

```maxscript
-- 创建基本几何体
myBox = box length:100 width:100 height:100 pos:[0,0,0]
mySphere = sphere radius:50 pos:[150,0,0]
myCylinder = cylinder radius:25 height:100 pos:[-150,0,0]

-- 设置属性
myBox.wirecolor = color 255 0 0
myBox.name = "RedBox"
```

### 对象选择

```maxscript
-- 选择所有对象
select $*

-- 按名称选择
select $MyBox

-- 按类型选择
select (for obj in objects where classOf obj == Box collect obj)

-- 获取当前选择
sel = selection as array
```

### 变换操作

```maxscript
-- 移动
move $ [10, 0, 0]

-- 旋转
rotate $ (eulerAngles 0 0 45)

-- 缩放
scale $ [2, 2, 2]

-- 设置绝对位置
$.pos = [100, 200, 300]
```

## 用户界面开发

### Rollout 基础

```maxscript
rollout myRollout "My Tool" (
    -- UI 控件
    button btnExecute "Execute" width:140
    spinner spnValue "Value:" range:[0,100,50]
    checkbox chkOption "Enable Option"
    dropdownlist ddlOptions "Options:" items:#("Option 1", "Option 2", "Option 3")
    
    -- 事件处理
    on btnExecute pressed do (
        print ("Value: " + spnValue.value as string)
        print ("Option enabled: " + chkOption.checked as string)
    )
    
    on spnValue changed val do (
        print ("Spinner changed to: " + val as string)
    )
)

-- 创建浮动窗口
createDialog myRollout width:200 height:150
```

### 常用 UI 控件

```maxscript
rollout uiDemo "UI Controls Demo" (
    -- 按钮
    button btn1 "Button"
    
    -- 文本框
    edittext txt1 "Text:"
    
    -- 数值输入
    spinner spn1 "Number:" range:[0,100,0]
    
    -- 滑块
    slider sld1 "Slider:" range:[0,100,50]
    
    -- 下拉列表
    dropdownlist ddl1 items:#("A", "B", "C")
    
    -- 复选框
    checkbox chk1 "Checkbox"
    
    -- 单选按钮
    radiobuttons rdo1 labels:#("Radio 1", "Radio 2")
    
    -- 颜色选择器
    colorpicker cp1 "Color:"
    
    -- 列表框
    listbox lb1 "List:" items:#("Item 1", "Item 2", "Item 3")
)
```

## 工具栏自定义

### 创建自定义工具栏按钮

```maxscript
-- 定义宏脚本
macroScript CustomTool
category:"Custom Tools"
tooltip:"Custom Tool Tooltip"
buttonText:"Custom"
icon:#("Standard", 1)
(
    on execute do (
        -- 工具逻辑
        messageBox "Custom tool executed!"
    )
    
    on isEnabled return true
    on isChecked return false
)
```

### 注册到菜单

```maxscript
-- 在 Scripting 菜单中添加项目
macroScript MyMenuItem
category:"My Scripts"
tooltip:"My Menu Item"
(
    on execute do (
        print "Menu item clicked"
    )
)
```

## 事件处理

### 场景事件回调

```maxscript
-- 选择改变回调
fn onSelectionChanged = (
    print ("Selection count: " + selection.count as string)
)

callbacks.addScript #selectionSetChanged "onSelectionChanged()" id:#myCallback

-- 移除回调
callbacks.removeScripts id:#myCallback
```

### 时间改变回调

```maxscript
-- 帧改变回调
fn onTimeChange = (
    print ("Current frame: " + currentTime as string)
)

callbacks.addScript #timeChange "onTimeChange()" id:#timeCallback
```

## 调试技巧

### 输出调试信息

```maxscript
-- 打印到监听器
print "Debug message"
format "Value: %\n" myValue

-- 显示对话框
messageBox "Debug info"

-- 使用 try-catch
try (
    -- 可能出错的代码
    result = 10 / 0
) catch (
    format "Error: %\n" (getCurrentException())
)
```

### 性能优化

```maxscript
-- 禁用重绘以提高性能
with redraw off (
    for i = 1 to 1000 do (
        box pos:[random -100 100, random -100 100, 0]
    )
)

-- 禁用撤销以提高性能
undo off (
    -- 批量操作
)

-- 使用 quiet 模式
max quiet mode
-- 操作
max quiet mode
```

## 更多资源

- [MaxScript 代码示例](../../examples/maxscript/)
- [API 参考](../api-reference/)
- [最佳实践](../best-practices/)
