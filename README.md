# 3ds Max 插件知识库 (3ds Max Plugins Knowledgebase)

辅助AI创建正确的3ds Max插件的在线验证系统和知识库。  
An online verification system and knowledgebase to assist AI in creating correct 3ds Max plugins.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![3ds Max](https://img.shields.io/badge/3ds%20Max-2020--2024-blue.svg)](https://www.autodesk.com/products/3ds-max)
[![MAXScript](https://img.shields.io/badge/MAXScript-Compatible-green.svg)](https://help.autodesk.com/view/3DSMAX/2024/ENU/?guid=GUID-MAXSCRIPT-REFERENCE)

## 📋 目录 (Table of Contents)

- [概述](#概述-overview)
- [在线验证系统](#在线验证系统-online-verification-system)
- [快速开始](#快速开始-quick-start)
- [目录结构](#目录结构-directory-structure)
- [使用指南](#使用指南-usage-guide)
- [文档](#文档-documentation)
- [示例](#示例-examples)
- [贡献](#贡献-contributing)
- [许可证](#许可证-license)

## 🎯 概述 (Overview)

本知识库提供了一套完整的3ds Max插件开发验证系统，包括：

- ✅ **在线验证系统** - 自动化验证插件质量和规范性
- 📚 **最佳实践指南** - 详细的插件开发最佳实践文档
- 🔍 **验证规范** - 明确的验证标准和要求
- 📝 **模板文件** - 开箱即用的插件模板
- 🛠️ **示例插件** - 展示最佳实践的完整示例
- 🐛 **故障排除指南** - 常见问题解决方案

## 🔐 在线验证系统 (Online Verification System)

### 验证级别 (Verification Levels)

我们的验证系统包含4个级别的检查：

1. **Level 1: 基础验证 (Basic Verification)**
   - 文件结构完整性
   - 必需文件检查
   - 文档完整性
   - 代码基础规范

2. **Level 2: 功能验证 (Functional Verification)**
   - 错误处理机制
   - 代码质量检查
   - 命名规范
   - 日志功能

3. **Level 3: 兼容性验证 (Compatibility Verification)**
   - 版本兼容性
   - 系统要求声明
   - 依赖项管理
   - 多语言支持

4. **Level 4: 性能验证 (Performance Verification)**
   - 文件大小检查
   - 性能优化检测
   - 资源使用评估

### 评级标准 (Rating Criteria)

- ✅ **优秀 (Excellent)**: 95%+ 通过率
- ✔️ **良好 (Good)**: 85%+ 通过率
- ⚠️ **合格 (Pass)**: 70%+ 通过率
- ❌ **不合格 (Fail)**: < 70% 通过率

## 🚀 快速开始 (Quick Start)

### 验证您的插件 (Verify Your Plugin)

```bash
# 1. 克隆此仓库
git clone https://github.com/bfk67x7xwt-bot/ds-max-plugins-knowledgebase.git

# 2. 运行验证脚本
cd ds-max-plugins-knowledgebase/verification-system/scripts
python verify_plugin.py /path/to/your/plugin

# 3. 查看验证报告
# 报告将保存在您的插件目录中: verification-report.json
```

### 使用模板创建新插件 (Create New Plugin from Template)

```bash
# 1. 复制模板文件
cp verification-system/templates/plugin-template.ms your-plugin.ms
cp verification-system/templates/README-template.md your-plugin/README.md

# 2. 根据您的需求修改模板
# 3. 使用验证系统检查您的插件
```

## 📁 目录结构 (Directory Structure)

```
ds-max-plugins-knowledgebase/
├── README.md                          # 本文件
├── LICENSE                            # MIT许可证
└── verification-system/               # 在线验证系统
    ├── docs/                          # 文档目录
    │   ├── verification-specification.md  # 验证规范
    │   ├── verification-checklist.md      # 验证检查清单
    │   ├── best-practices.md              # 最佳实践指南
    │   └── troubleshooting.md             # 故障排除指南
    ├── scripts/                       # 验证脚本
    │   └── verify_plugin.py          # 自动验证脚本
    ├── templates/                     # 模板文件
    │   ├── plugin-template.ms        # 插件代码模板
    │   ├── README-template.md        # README模板
    │   └── CHANGELOG-template.md     # 变更日志模板
    └── examples/                      # 示例插件
        ├── sample-plugin.ms          # 示例插件代码
        └── README.md                 # 示例说明
```

## 📖 使用指南 (Usage Guide)

### 1. 验证现有插件

使用自动化验证脚本检查您的插件：

```bash
python verification-system/scripts/verify_plugin.py /path/to/plugin
```

脚本将检查：
- ✅ 文件结构和必需文件
- ✅ README文档完整性
- ✅ 代码质量和规范
- ✅ 错误处理机制
- ✅ 性能指标
- ✅ 兼容性声明

### 2. 手动验证

参考 [验证检查清单](verification-system/docs/verification-checklist.md) 进行手动验证：

- 打开检查清单文档
- 逐项检查您的插件
- 标记完成的项目
- 改进未通过的项目

### 3. 开发新插件

1. **使用模板** - 从 `verification-system/templates/` 开始
2. **参考示例** - 查看 `verification-system/examples/` 中的示例
3. **遵循最佳实践** - 阅读 [最佳实践指南](verification-system/docs/best-practices.md)
4. **定期验证** - 使用验证脚本检查进度

## 📚 文档 (Documentation)

### 核心文档

- **[验证规范](verification-system/docs/verification-specification.md)** - 详细的验证标准和要求
- **[验证检查清单](verification-system/docs/verification-checklist.md)** - 完整的检查项目列表
- **[最佳实践指南](verification-system/docs/best-practices.md)** - 插件开发最佳实践
- **[故障排除指南](verification-system/docs/troubleshooting.md)** - 常见问题和解决方案

### 模板

- **[插件代码模板](verification-system/templates/plugin-template.ms)** - MAXScript插件模板
- **[README模板](verification-system/templates/README-template.md)** - 文档模板
- **[CHANGELOG模板](verification-system/templates/CHANGELOG-template.md)** - 变更日志模板

## 💡 示例 (Examples)

### 示例插件

查看 [示例插件](verification-system/examples/sample-plugin.ms) 了解：

- 正确的代码结构
- 错误处理实现
- 用户界面设计
- 配置管理
- 性能优化技巧

### 使用示例

```maxscript
-- 在3ds Max中运行示例插件
fileIn "verification-system/examples/sample-plugin.ms"

-- 显示插件界面
showSamplePlugin()
```

## 🛠️ 验证工具 (Verification Tools)

### 自动化验证脚本

**功能特性**:
- 🔍 自动检查文件结构
- 📝 验证文档完整性
- 🔧 代码质量分析
- 📊 生成详细报告
- 💾 保存JSON格式结果

**使用方法**:

```bash
# 基本用法
python verify_plugin.py <plugin_directory>

# 查看帮助
python verify_plugin.py --help
```

**输出示例**:

```
🔍 开始验证插件: /path/to/plugin
============================================================

📋 Level 1: 基础验证 (Basic Verification)
  ✅ 主插件文件存在: 找到 1 个插件文件
  ✅ README.md 存在: README.md 文件已找到
  ✅ LICENSE 文件存在: LICENSE 文件已找到

⚙️  Level 2: 功能验证 (Functional Verification)
  ✅ 包含错误处理机制: 代码中发现try-catch或错误处理
  ✅ 包含日志记录功能: 代码中发现日志或输出语句

============================================================
📊 验证报告 (Verification Report)
============================================================
总体得分: 92.5/100
评级: 良好 (Good)
```

## 🤝 贡献 (Contributing)

我们欢迎所有形式的贡献！

### 如何贡献

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

### 贡献内容

- 📝 改进文档
- 🐛 报告和修复Bug
- ✨ 提出新功能
- 🔍 添加验证规则
- 💡 分享最佳实践
- 🌐 翻译文档

## 📄 许可证 (License)

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 👥 维护者 (Maintainers)

- **DS Max Plugins Knowledgebase Team**

## 🙏 致谢 (Acknowledgments)

- Autodesk 3ds Max 团队
- MAXScript 社区
- 所有贡献者和用户

## 📞 联系方式 (Contact)

- 🐛 问题反馈: [GitHub Issues](https://github.com/bfk67x7xwt-bot/ds-max-plugins-knowledgebase/issues)
- 💬 讨论: [GitHub Discussions](https://github.com/bfk67x7xwt-bot/ds-max-plugins-knowledgebase/discussions)

## 🗺️ 路线图 (Roadmap)

- [x] 创建基础验证系统
- [x] 编写核心文档
- [x] 提供示例插件
- [x] 开发自动化验证脚本
- [ ] 添加Web界面
- [ ] 集成CI/CD支持
- [ ] 扩展验证规则
- [ ] 多语言文档支持
- [ ] 社区插件库

---

**版本**: 1.0.0  
**最后更新**: 2025-12-02  
**状态**: ✅ 稳定 (Stable)
