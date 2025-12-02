# Sample Plugin

一个展示3ds Max插件最佳实践的示例插件。
A sample plugin demonstrating best practices for 3ds Max plugin development.

## 功能特性 (Features)

- ✨ 创建参数化Box对象 (Create parametric Box objects)
- 🎨 批量修改对象颜色 (Batch modify object colors)
- 💾 保存和加载配置 (Save and load configuration)
- 🔄 支持撤销/重做 (Undo/Redo support)
- 📊 进度显示 (Progress indication)
- 🛡️ 完善的错误处理 (Comprehensive error handling)

## 系统要求 (System Requirements)

- 3ds Max 2020 或更高版本 (3ds Max 2020 or higher)
- Windows 10/11
- 最少 4GB RAM (Minimum 4GB RAM)

## 安装 (Installation)

1. 下载 `sample-plugin.ms` 文件
2. 将文件复制到以下位置之一：
   - `C:\Program Files\Autodesk\3ds Max 2024\scripts`
   - `%USERPROFILE%\Documents\3ds Max 2024\scripts`
3. 重启 3ds Max 或运行脚本

## 使用方法 (Usage)

### 方法1：通过MAXScript运行
1. 打开 3ds Max
2. 按 `F11` 打开 MAXScript Listener
3. 拖放 `sample-plugin.ms` 到 MAXScript Listener
4. 或使用菜单：`MAXScript > Run Script` 并选择文件

### 方法2：通过代码运行
```maxscript
-- 加载插件
fileIn "sample-plugin.ms"

-- 显示界面
showSamplePlugin()
```

### 基本功能

#### 创建Box对象
1. 设置 "Size" 参数（1-1000）
2. 设置 "Segments" 参数（1-20）
3. 点击 "Create Box" 按钮
4. Box对象将在场景中心创建

#### 修改选择对象颜色
1. 在场景中选择一个或多个对象
2. 在插件界面选择颜色
3. 点击 "Apply Color" 按钮
4. 所选对象的线框颜色将被更新

## 代码示例 (Code Examples)

### 通过代码创建对象
```maxscript
-- 创建插件实例
myPlugin = SamplePluginStruct()
myPlugin.initialize()

-- 创建不同大小的对象
myPlugin.createSampleObject size:20 segments:8

-- 处理选择
select $Box*
myPlugin.processSelection (color 255 0 0)
```

### 自定义配置
```maxscript
-- 启用调试模式
myPlugin = SamplePluginStruct debugMode:true
myPlugin.initialize()
```

## 配置文件 (Configuration)

配置文件自动保存在：
`%LOCALAPPDATA%\Autodesk\3ds Max\2024\en-US\plugcfg\sample_plugin_config.ini`

## 故障排除 (Troubleshooting)

### 问题1：插件无法加载
**症状**: 运行脚本后无反应或出现错误

**解决方案**:
1. 检查3ds Max版本是否为2020或更高
2. 确保文件编码为UTF-8或UTF-16
3. 查看MAXScript Listener中的错误信息
4. 尝试在干净场景中加载

### 问题2：对象创建失败
**症状**: 点击"Create Box"后无对象创建

**解决方案**:
1. 检查参数值是否在有效范围内
2. 确保场景未锁定
3. 查看是否有错误消息框
4. 检查MAXScript Listener中的日志

### 问题3：颜色应用失败
**症状**: 应用颜色时出错

**解决方案**:
1. 确保至少选择了一个对象
2. 检查所选对象是否支持wirecolor属性
3. 尝试选择几何体对象（如Box、Sphere等）

## 最佳实践展示 (Best Practices Demonstrated)

此示例插件展示了以下最佳实践：

### ✅ 代码组织
- 使用struct组织代码
- 清晰的函数命名
- 逻辑分组

### ✅ 错误处理
- try-catch块
- 输入验证
- 用户友好的错误消息

### ✅ 用户体验
- 进度指示
- 操作反馈
- 帮助文档

### ✅ 性能优化
- 批量操作
- 进度条支持取消
- 适当的undo支持

### ✅ 可维护性
- 清晰的注释
- 配置管理
- 版本信息

## 扩展建议 (Extension Ideas)

可以基于此示例添加的功能：

1. **保存预设** - 保存和加载常用参数组合
2. **批量创建** - 创建对象阵列
3. **导出功能** - 导出对象数据到文件
4. **高级UI** - 添加更多控件和选项
5. **键盘快捷键** - 为常用操作添加快捷键

## 文件结构 (File Structure)

```
sample-plugin/
├── sample-plugin.ms          # 主插件文件
├── README.md                 # 本文件
└── config/
    └── sample_plugin_config.ini  # 配置文件（自动生成）
```

## 许可证 (License)

MIT License

Copyright (c) 2025 Sample Developer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 作者 (Author)

- 示例开发者 (Sample Developer)
- Email: developer@example.com
- GitHub: https://github.com/yourusername

## 致谢 (Acknowledgments)

- Autodesk 3ds Max团队提供的优秀平台
- 社区贡献者的宝贵反馈
- 所有使用和测试此插件的用户

## 更新日志 (Changelog)

### [1.0.0] - 2025-12-02
- 初始版本发布
- 基础对象创建功能
- 颜色修改功能
- 配置管理系统

---

**版本**: 1.0.0  
**最后更新**: 2025-12-02  
**状态**: ✅ 稳定 (Stable)
