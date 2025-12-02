# 3ds Max 插件最佳实践指南
# 3ds Max Plugin Best Practices Guide

## 目录 (Table of Contents)

1. [项目结构](#项目结构)
2. [代码规范](#代码规范)
3. [错误处理](#错误处理)
4. [性能优化](#性能优化)
5. [用户体验](#用户体验)
6. [文档编写](#文档编写)
7. [版本管理](#版本管理)
8. [安全实践](#安全实践)

---

## 项目结构 (Project Structure)

### 推荐的目录结构
```
my-plugin/
├── README.md              # 项目说明文档
├── LICENSE               # 许可证文件
├── CHANGELOG.md          # 变更日志
├── plugin.ms             # 主插件文件
├── config.ini            # 配置文件
├── docs/                 # 详细文档
│   ├── user-guide.md    # 用户指南
│   ├── api-reference.md # API参考
│   └── screenshots/     # 截图
├── examples/            # 示例文件
│   └── sample-scene.max
├── tests/               # 测试文件
│   └── test_plugin.ms
├── resources/           # 资源文件
│   ├── icons/
│   └── ui/
└── scripts/             # 辅助脚本
    └── install.ms
```

### 文件命名规范

✅ **推荐**:
- `myPlugin.ms`
- `plugin_utilities.ms`
- `UI_Manager.ms`

❌ **避免**:
- `my plugin.ms` (含空格)
- `插件.ms` (非ASCII字符)
- `temp123.ms` (无意义名称)

---

## 代码规范 (Code Standards)

### MAXScript 代码规范

#### 1. 文件头部模板

```maxscript
/*******************************************************************************
 * Plugin Name: My Awesome Plugin
 * Version: 1.0.0
 * Author: Your Name
 * Email: your.email@example.com
 * Description: Brief description of what this plugin does
 * 
 * Compatible with: 3ds Max 2020-2024
 * License: MIT
 * Last Updated: 2025-12-02
 ******************************************************************************/

-- Dependencies
-- Requires: 3ds Max 2020 or higher
-- Optional: [List any optional dependencies]

-- Global Variables
global myPlugin_version = "1.0.0"
```

#### 2. 命名约定

```maxscript
-- 函数名使用驼峰命名法
fn createCustomBox boxSize = (...)
fn calculateVolume width height depth = (...)

-- 全局变量使用前缀
global g_pluginSettings
global g_currentMode

-- 局部变量使用有意义的名称
local vertexCount = polyOp.getNumVerts obj
local selectedObjects = getCurrentSelection()

-- 常量使用大写
local MAX_VERTICES = 1000000
local DEFAULT_SIZE = 10.0
```

#### 3. 代码组织

```maxscript
-- 将相关功能组织成结构体
struct MyPluginCore (
    -- 属性
    version = "1.0.0",
    settings = undefined,
    
    -- 方法
    fn initialize = (
        -- 初始化代码
    ),
    
    fn cleanup = (
        -- 清理代码
    )
)

-- 使用rollout组织UI
rollout myPluginRollout "My Plugin" (
    button btnCreate "Create"
    spinner spnSize "Size: " range:[1, 100, 10]
    
    on btnCreate pressed do (
        -- 按钮事件处理
    )
)
```

---

## 错误处理 (Error Handling)

### 1. 基本错误处理

```maxscript
fn safeOperation = (
    try (
        -- 可能出错的代码
        local result = someRiskyOperation()
        return result
    )
    catch (
        -- 错误处理
        messageBox "操作失败，请检查输入参数。\nOperation failed. Please check input parameters."
        return undefined
    )
)
```

### 2. 详细错误信息

```maxscript
fn processFile filePath = (
    try (
        if not (doesFileExist filePath) then (
            throw "文件不存在 (File does not exist): " + filePath
        )
        
        -- 处理文件
        local data = loadFile filePath
        return data
    )
    catch (e) (
        -- 记录详细错误
        local errorMsg = "处理文件时出错 (Error processing file):\n"
        errorMsg += "文件 (File): " + filePath + "\n"
        errorMsg += "错误 (Error): " + e as string
        
        format "ERROR: %\n" errorMsg
        messageBox errorMsg title:"错误 (Error)"
        return undefined
    )
)
```

### 3. 用户输入验证

```maxscript
fn validateInput value minVal maxVal = (
    if value == undefined then (
        messageBox "请输入有效值 (Please enter a valid value)"
        return false
    )
    
    if value < minVal or value > maxVal then (
        local msg = "值必须在 " + minVal as string + " 到 " + maxVal as string + " 之间\n"
        msg += "Value must be between " + minVal as string + " and " + maxVal as string
        messageBox msg
        return false
    )
    
    return true
)
```

---

## 性能优化 (Performance Optimization)

### 1. 批量操作

```maxscript
-- ❌ 错误方式：逐个处理
for obj in objects do (
    obj.wirecolor = red
    redrawViews()  -- 每次都重绘！
)

-- ✅ 正确方式：批量处理
with undo off (
    for obj in objects do (
        obj.wirecolor = red
    )
)
redrawViews()  -- 只重绘一次
```

### 2. 使用进度条

```maxscript
fn processLargeDataset data = (
    progressStart "Processing..."
    
    try (
        for i = 1 to data.count do (
            -- 更新进度
            progressUpdate (100.0 * i / data.count)
            
            -- 处理数据
            processItem data[i]
            
            -- 允许用户取消
            if getProgressCancel() then (
                progressEnd()
                return undefined
            )
        )
    )
    catch (
        progressEnd()
        throw
    )
    
    progressEnd()
    return true
)
```

### 3. 内存管理

```maxscript
fn optimizedOperation = (
    -- 禁用不必要的更新
    with redraw off (
        with undo off (
            -- 执行操作
            for obj in objects do (
                -- 处理对象
            )
        )
    )
    
    -- 清理临时对象
    gc()  -- 垃圾回收
    
    redrawViews()
)
```

---

## 用户体验 (User Experience)

### 1. 清晰的用户界面

```maxscript
rollout myPluginUI "My Plugin v1.0" width:300 (
    group "Options" (
        radioButtons rdoMode "Mode:" labels:#("Simple", "Advanced")
        spinner spnValue "Value:" range:[0, 100, 50] type:#integer
        checkbox chkAutoUpdate "Auto Update" checked:true
    )
    
    group "Actions" (
        button btnApply "Apply" width:140 height:30
        button btnReset "Reset" width:140 height:30
    )
    
    -- 提供帮助信息
    button btnHelp "?" width:20 height:20 tooltip:"Click for help"
    
    on btnHelp pressed do (
        messageBox "这是一个示例插件...\nThis is a sample plugin..." title:"Help"
    )
)
```

### 2. 操作确认

```maxscript
fn deleteAllObjects = (
    if queryBox "确定要删除所有对象吗？此操作不可撤销！\nDelete all objects? This cannot be undone!" then (
        delete objects
        messageBox "已删除所有对象 (All objects deleted)"
    )
)
```

### 3. 操作反馈

```maxscript
fn longOperation = (
    messageBox "开始处理，请稍候... (Starting process, please wait...)"
    
    -- 执行长时间操作
    processData()
    
    messageBox "处理完成！(Process completed!)" title:"成功 (Success)"
)
```

---

## 文档编写 (Documentation)

### README.md 模板

```markdown
# My Awesome Plugin

简短描述您的插件功能。
Brief description of your plugin functionality.

## 功能特性 (Features)

- ✨ 功能1 (Feature 1)
- 🚀 功能2 (Feature 2)
- 💡 功能3 (Feature 3)

## 系统要求 (System Requirements)

- 3ds Max 2020 或更高版本 (3ds Max 2020 or higher)
- Windows 10/11
- 最少 8GB RAM (Minimum 8GB RAM)

## 安装 (Installation)

1. 下载最新版本 (Download the latest release)
2. 将文件复制到：`C:\Program Files\Autodesk\3ds Max 2024\scripts`
3. 重启 3ds Max

## 使用方法 (Usage)

### 基本用法
1. 打开 3ds Max
2. 运行脚本：`MAXScript > Run Script > my_plugin.ms`
3. 使用界面进行操作

### 示例
\`\`\`maxscript
-- 代码示例
myPlugin.create size:10
\`\`\`

## 配置 (Configuration)

配置文件位置：`scripts/config.ini`

## 常见问题 (FAQ)

**Q: 问题1？**
A: 回答1

## 更新日志 (Changelog)

查看 [CHANGELOG.md](CHANGELOG.md)

## 许可证 (License)

MIT License - 查看 [LICENSE](LICENSE) 文件

## 作者 (Author)

- 姓名 (Name)
- 邮箱 (Email)
- 网站 (Website)

## 致谢 (Acknowledgments)

感谢所有贡献者和用户的支持。
```

### CHANGELOG.md 模板

```markdown
# 更新日志 (Changelog)

## [1.0.0] - 2025-12-02

### Added 新增
- 初始版本发布
- 基础功能实现

### Changed 改变
- N/A

### Fixed 修复
- N/A

### Removed 移除
- N/A
```

---

## 版本管理 (Version Management)

### 语义化版本

使用 `MAJOR.MINOR.PATCH` 格式：

- **MAJOR**: 不兼容的 API 改动
- **MINOR**: 向后兼容的功能新增
- **PATCH**: 向后兼容的问题修复

示例：
- `1.0.0` - 初始版本
- `1.1.0` - 新增功能
- `1.1.1` - 修复bug

### 版本号管理

```maxscript
-- 在代码中定义版本
global PLUGIN_VERSION = "1.0.0"
global PLUGIN_BUILD_DATE = "2025-12-02"

fn getVersionInfo = (
    return "Version: " + PLUGIN_VERSION + "\nBuild: " + PLUGIN_BUILD_DATE
)
```

---

## 安全实践 (Security Practices)

### 1. 避免危险操作

```maxscript
-- ❌ 避免直接执行用户输入
execute userInput

-- ✅ 验证和限制输入
fn safeExecute command validCommands = (
    if findItem validCommands command > 0 then (
        execute command
    ) else (
        messageBox "无效命令 (Invalid command)"
    )
)
```

### 2. 文件路径安全

```maxscript
fn safeLoadFile filePath = (
    -- 验证文件路径
    if not (doesFileExist filePath) then (
        return undefined
    )
    
    -- 检查文件扩展名
    local ext = getFilenameType filePath
    if ext != ".max" and ext != ".ms" then (
        messageBox "不支持的文件类型 (Unsupported file type)"
        return undefined
    )
    
    -- 加载文件
    return loadFile filePath
)
```

### 3. 敏感信息处理

```maxscript
-- ❌ 不要硬编码密码或密钥
global API_KEY = "secret123"

-- ✅ 从配置文件读取
fn loadAPIKey = (
    local configFile = getDir #plugcfg + "\\myconfig.ini"
    -- 从加密配置读取
    return readEncryptedConfig configFile
)
```

---

## 测试建议 (Testing Recommendations)

### 基本测试检查清单

- [ ] 在干净的3ds Max场景中测试
- [ ] 测试大场景（1000+ 对象）
- [ ] 测试边界情况（空选择、无效输入）
- [ ] 测试撤销/重做功能
- [ ] 测试多次连续执行
- [ ] 在不同的3ds Max版本中测试
- [ ] 检查内存泄漏
- [ ] 测试错误处理

---

## 附录：有用的工具和资源

### 开发工具
- MAXScript Listener - 内置调试工具
- Visual Studio Code - 代码编辑器
- Git - 版本控制

### 学习资源
- Autodesk 官方文档
- CGTalk 论坛
- ScriptSpot

### 推荐库
- struct库 - 数据结构
- fileIO库 - 文件操作
- UI库 - 界面组件

---

**版本**: 1.0.0  
**最后更新**: 2025-12-02  
**维护者**: DS Max Plugins Knowledgebase Team
