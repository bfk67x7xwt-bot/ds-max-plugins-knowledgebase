/*******************************************************************************
 * Plugin Name: Sample 3ds Max Plugin
 * Version: 1.0.0
 * Author: Sample Developer
 * Email: developer@example.com
 * Description: This is a sample plugin demonstrating best practices
 * 
 * Compatible with: 3ds Max 2020-2024
 * License: MIT
 * Last Updated: 2025-12-02
 ******************************************************************************/

-- Global Variables
global samplePlugin_version = "1.0.0"
global samplePlugin_settings

-- Plugin Structure
struct SamplePluginStruct (
    -- Properties
    version = "1.0.0",
    debugMode = false,
    
    -- Initialize function
    fn initialize = (
        try (
            -- Load settings
            this.loadSettings()
            
            if debugMode then (
                format "Sample Plugin v% initialized\n" version
            )
            
            return true
        )
        catch (e) (
            messageBox ("初始化失败 (Initialization failed): " + e as string)
            return false
        )
    ),
    
    -- Load settings from config file
    fn loadSettings = (
        local configFile = getDir #plugcfg + "\\sample_plugin_config.ini"
        
        if doesFileExist configFile then (
            -- Load configuration
            if debugMode then (
                format "Loading config from: %\n" configFile
            )
        ) else (
            -- Create default config
            this.saveSettings()
        )
    ),
    
    -- Save settings to config file
    fn saveSettings = (
        local configFile = getDir #plugcfg + "\\sample_plugin_config.ini"
        
        try (
            -- Save configuration
            if debugMode then (
                format "Saving config to: %\n" configFile
            )
            return true
        )
        catch (
            return false
        )
    ),
    
    -- Main plugin function
    fn createSampleObject size: 10 segments: 4 = (
        try (
            -- Validate inputs
            if not this.validateInput size 1 1000 then (
                return undefined
            )
            
            -- Create object with undo support
            with undo "Create Sample Object" on (
                local obj = Box length:size width:size height:size \
                              lengthsegs:segments widthsegs:segments heightsegs:segments
                
                obj.name = uniqueName "SampleBox"
                obj.wirecolor = color 100 150 255
                
                select obj
                
                if debugMode then (
                    format "Created object: % (size: %)\n" obj.name size
                )
                
                return obj
            )
        )
        catch (e) (
            messageBox ("创建对象失败 (Failed to create object): " + e as string)
            return undefined
        )
    ),
    
    -- Validate input values
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
    ),
    
    -- Process selected objects
    fn processSelection colorValue = (
        if selection.count == 0 then (
            messageBox "请先选择对象 (Please select objects first)"
            return false
        )
        
        try (
            progressStart "Processing objects..."
            
            with undo "Process Selection" on (
                for i = 1 to selection.count do (
                    -- Update progress
                    progressUpdate (100.0 * i / selection.count)
                    
                    -- Process object
                    selection[i].wirecolor = colorValue
                    
                    -- Check for cancel
                    if getProgressCancel() then (
                        progressEnd()
                        messageBox "操作已取消 (Operation cancelled)"
                        return false
                    )
                )
            )
            
            progressEnd()
            
            local msg = "已处理 " + selection.count as string + " 个对象\n"
            msg += "Processed " + selection.count as string + " objects"
            messageBox msg title:"成功 (Success)"
            
            return true
        )
        catch (e) (
            progressEnd()
            messageBox ("处理失败 (Processing failed): " + e as string)
            return false
        )
    ),
    
    -- Cleanup function
    fn cleanup = (
        try (
            this.saveSettings()
            
            if debugMode then (
                format "Sample Plugin cleanup completed\n"
            )
        )
        catch (
            -- Silent cleanup errors
        )
    )
)

-- User Interface
rollout samplePluginRollout "Sample Plugin v1.0" width:280 (
    local pluginInstance
    
    group "Create Objects" (
        spinner spnSize "Size:" range:[1, 1000, 10] type:#integer
        spinner spnSegments "Segments:" range:[1, 20, 4] type:#integer
        button btnCreate "Create Box" width:250 height:30
    )
    
    group "Process Selection" (
        colorpicker cpColor "Color:" color:(color 255 100 100)
        button btnProcess "Apply Color" width:250 height:30
    )
    
    group "Tools" (
        button btnAbout "About" width:120
        button btnHelp "Help" width:120
    )
    
    -- Initialize on open
    on samplePluginRollout open do (
        pluginInstance = SamplePluginStruct()
        pluginInstance.initialize()
    )
    
    -- Create button handler
    on btnCreate pressed do (
        if pluginInstance != undefined then (
            pluginInstance.createSampleObject size:spnSize.value segments:spnSegments.value
        )
    )
    
    -- Process button handler
    on btnProcess pressed do (
        if pluginInstance != undefined then (
            pluginInstance.processSelection cpColor.color
        )
    )
    
    -- About button handler
    on btnAbout pressed do (
        local msg = "Sample Plugin\n"
        msg += "Version: " + samplePlugin_version + "\n"
        msg += "Author: Sample Developer\n\n"
        msg += "This is a demonstration plugin showing best practices."
        messageBox msg title:"About"
    )
    
    -- Help button handler
    on btnHelp pressed do (
        local msg = "使用说明 (Usage Instructions):\n\n"
        msg += "1. 设置参数 (Set parameters)\n"
        msg += "2. 点击'Create Box'创建对象 (Click 'Create Box' to create)\n"
        msg += "3. 选择对象并应用颜色 (Select objects and apply color)\n\n"
        msg += "For more information, see README.md"
        messageBox msg title:"Help"
    )
    
    -- Cleanup on close
    on samplePluginRollout close do (
        if pluginInstance != undefined then (
            pluginInstance.cleanup()
        )
    )
)

-- Create floating dialog
fn showSamplePlugin = (
    try (
        -- Check if dialog already exists
        if samplePlugin_dialog != undefined then (
            try (DestroyDialog samplePlugin_dialog) catch()
        )
        
        -- Create new dialog
        global samplePlugin_dialog = createDialog samplePluginRollout
    )
    catch (e) (
        messageBox ("显示插件失败 (Failed to show plugin): " + e as string)
    )
)

-- Entry point
showSamplePlugin()

-- Print success message
format "Sample Plugin v% loaded successfully!\n" samplePlugin_version
format "Run 'showSamplePlugin()' to show the interface\n"
