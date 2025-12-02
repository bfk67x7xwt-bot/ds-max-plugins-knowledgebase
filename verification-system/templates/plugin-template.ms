/*******************************************************************************
 * Plugin Name: [插件名称]
 * Version: 1.0.0
 * Author: [作者名称]
 * Email: [联系邮箱]
 * Description: [插件简短描述]
 * 
 * Compatible with: 3ds Max 2020-2024
 * License: [许可证类型，如 MIT]
 * Last Updated: YYYY-MM-DD
 ******************************************************************************/

-- ============================================================================
-- CONFIGURATION / 配置
-- ============================================================================

-- Global variables / 全局变量
global pluginName_version = "1.0.0"
global pluginName_settings

-- ============================================================================
-- PLUGIN STRUCTURE / 插件结构
-- ============================================================================

struct PluginNameStruct (
    -- Properties / 属性
    version = "1.0.0",
    debugMode = false,
    initialized = false,
    
    -- ========================================================================
    -- INITIALIZATION / 初始化
    -- ========================================================================
    
    fn initialize = (
        try (
            -- Check 3ds Max version / 检查版本
            if not this.checkVersion() then (
                return false
            )
            
            -- Load settings / 加载设置
            this.loadSettings()
            
            -- Initialize components / 初始化组件
            -- [添加您的初始化代码]
            
            this.initialized = true
            
            if this.debugMode then (
                format "% v% initialized successfully\n" "[插件名称]" this.version
            )
            
            return true
        )
        catch (e) (
            messageBox ("初始化失败 (Initialization failed):\n" + e as string)
            return false
        )
    ),
    
    fn checkVersion = (
        local minVersion = 2020
        local currentVersion = maxVersion()[1]
        
        if currentVersion < minVersion then (
            local msg = "此插件需要 3ds Max " + minVersion as string + " 或更高版本\n"
            msg += "This plugin requires 3ds Max " + minVersion as string + " or higher"
            messageBox msg title:"版本不兼容"
            return false
        )
        
        return true
    ),
    
    -- ========================================================================
    -- SETTINGS MANAGEMENT / 设置管理
    -- ========================================================================
    
    fn loadSettings = (
        local configFile = getDir #plugcfg + "\\[plugin_name]_config.ini"
        
        if doesFileExist configFile then (
            -- Load from config file / 从配置文件加载
            if this.debugMode then (
                format "Loading config from: %\n" configFile
            )
            -- [添加配置加载代码]
        ) else (
            -- Create default settings / 创建默认设置
            this.createDefaultSettings()
            this.saveSettings()
        )
    ),
    
    fn saveSettings = (
        local configFile = getDir #plugcfg + "\\[plugin_name]_config.ini"
        
        try (
            -- Save settings / 保存设置
            -- [添加配置保存代码]
            
            if this.debugMode then (
                format "Config saved to: %\n" configFile
            )
            return true
        )
        catch (e) (
            format "Failed to save config: %\n" (e as string)
            return false
        )
    ),
    
    fn createDefaultSettings = (
        -- Create default settings / 创建默认设置
        -- [添加默认设置]
    ),
    
    -- ========================================================================
    -- CORE FUNCTIONALITY / 核心功能
    -- ========================================================================
    
    fn mainFunction param1 param2 = (
        try (
            -- Validate inputs / 验证输入
            if not this.validateInputs param1 param2 then (
                return undefined
            )
            
            -- Main logic / 主要逻辑
            with undo "Plugin Action" on (
                -- [添加您的功能代码]
                
                if this.debugMode then (
                    format "Function executed with params: %, %\n" param1 param2
                )
            )
            
            return true
        )
        catch (e) (
            local errorMsg = "操作失败 (Operation failed):\n" + e as string
            messageBox errorMsg
            return undefined
        )
    ),
    
    -- ========================================================================
    -- VALIDATION / 验证
    -- ========================================================================
    
    fn validateInputs param1 param2 = (
        -- Validate param1 / 验证参数1
        if param1 == undefined then (
            messageBox "参数1无效 (Invalid parameter 1)"
            return false
        )
        
        -- Validate param2 / 验证参数2
        if param2 == undefined then (
            messageBox "参数2无效 (Invalid parameter 2)"
            return false
        )
        
        return true
    ),
    
    -- ========================================================================
    -- UTILITY FUNCTIONS / 工具函数
    -- ========================================================================
    
    fn logMessage msg = (
        if this.debugMode then (
            format "[%] %\n" localTime msg
        )
    ),
    
    -- ========================================================================
    -- CLEANUP / 清理
    -- ========================================================================
    
    fn cleanup = (
        try (
            -- Save settings before exit / 退出前保存设置
            this.saveSettings()
            
            -- Release resources / 释放资源
            -- [添加清理代码]
            
            if this.debugMode then (
                format "Cleanup completed\n"
            )
        )
        catch (e) (
            -- Silent cleanup errors / 静默清理错误
            format "Cleanup error: %\n" (e as string)
        )
    )
)

-- ============================================================================
-- USER INTERFACE / 用户界面
-- ============================================================================

rollout pluginNameRollout "[插件名称] v1.0" width:300 (
    local pluginInstance
    
    -- UI Controls / 界面控件
    group "Settings" (
        spinner spnValue1 "Value 1:" range:[0, 100, 50] type:#integer
        checkbox chkOption1 "Enable Option" checked:true
    )
    
    group "Actions" (
        button btnExecute "Execute" width:280 height:30
        button btnReset "Reset" width:280 height:30
    )
    
    group "Info" (
        button btnAbout "About" width:135
        button btnHelp "Help" width:135
    )
    
    -- ========================================================================
    -- EVENT HANDLERS / 事件处理
    -- ========================================================================
    
    on pluginNameRollout open do (
        -- Initialize plugin / 初始化插件
        pluginInstance = PluginNameStruct()
        if not pluginInstance.initialize() then (
            messageBox "插件初始化失败 (Plugin initialization failed)"
        )
    )
    
    on btnExecute pressed do (
        if pluginInstance != undefined and pluginInstance.initialized then (
            pluginInstance.mainFunction spnValue1.value chkOption1.checked
        )
    )
    
    on btnReset pressed do (
        -- Reset to defaults / 重置为默认值
        spnValue1.value = 50
        chkOption1.checked = true
    )
    
    on btnAbout pressed do (
        local msg = "[插件名称]\n"
        msg += "Version: " + pluginName_version + "\n"
        msg += "Author: [作者名称]\n\n"
        msg += "[插件描述]"
        messageBox msg title:"About"
    )
    
    on btnHelp pressed do (
        local msg = "使用说明 (Usage Instructions):\n\n"
        msg += "1. [步骤1]\n"
        msg += "2. [步骤2]\n"
        msg += "3. [步骤3]\n\n"
        msg += "For more information, see README.md"
        messageBox msg title:"Help"
    )
    
    on pluginNameRollout close do (
        -- Cleanup on close / 关闭时清理
        if pluginInstance != undefined then (
            pluginInstance.cleanup()
        )
    )
)

-- ============================================================================
-- ENTRY POINT / 入口点
-- ============================================================================

fn showPluginName = (
    try (
        -- Close existing dialog / 关闭已存在的对话框
        if pluginName_dialog != undefined then (
            try (DestroyDialog pluginName_dialog) catch()
        )
        
        -- Create new dialog / 创建新对话框
        global pluginName_dialog = createDialog pluginNameRollout
    )
    catch (e) (
        messageBox ("显示插件失败 (Failed to show plugin):\n" + e as string)
    )
)

-- Auto-show on load (optional) / 加载时自动显示（可选）
-- showPluginName()

-- Print success message / 打印成功消息
format "[插件名称] v% loaded successfully!\n" pluginName_version
format "Run 'showPluginName()' to show the interface\n"
