# 3ds Max 插件开发知识库

本知识库旨在支持 3ds Max 插件开发，帮助开发者更高效地编写插件、解决错误并提高生产力。内容包括开发文档、代码示例、最佳实践和工具资源，同时减少使用 Copilot 时生成代码的错误。

## 📁 目录结构

```
├── docs/
│   ├── maxscript/          # MaxScript 开发指南
│   ├── python/             # Python 开发指南
│   ├── cpp-sdk/            # C++ SDK 开发指南
│   ├── api-reference/      # API 参考文档
│   └── best-practices/     # 最佳实践
├── examples/
│   ├── maxscript/          # MaxScript 代码示例
│   ├── python/             # Python 代码示例
│   └── cpp-sdk/            # C++ SDK 代码示例
└── README.md
```

## 🚀 主要功能

### 1. 多种插件开发方法指南
- **MaxScript**: 3ds Max 内置脚本语言，适合快速原型和简单工具开发
- **Python**: 支持 Python 3.x，适合复杂逻辑和外部库集成
- **C++ SDK**: 适合高性能插件和深度定制

### 2. 通用开发任务案例
- 工具栏自定义
- 命令面板扩展
- 几何体插件开发
- 材质和着色器插件
- 导入/导出插件

### 3. 详细的开发 API 参考
- 3ds Max 底层功能
- 扩展能力接口
- 事件系统
- 场景管理

### 4. 跨平台协作
- 插件更新追踪
- 版本兼容性指南
- 社区贡献和分享

## 📚 快速开始

### MaxScript 开发
查看 [MaxScript 开发指南](docs/maxscript/README.md) 了解如何使用 MaxScript 开发插件。

### Python 开发
查看 [Python 开发指南](docs/python/README.md) 了解如何使用 Python 开发插件。

### C++ SDK 开发
查看 [C++ SDK 开发指南](docs/cpp-sdk/README.md) 了解如何使用 C++ SDK 开发高性能插件。

## 🔧 开发环境要求

| 开发方式 | 要求 |
|---------|------|
| MaxScript | 3ds Max 2018 或更高版本 |
| Python | 3ds Max 2022 或更高版本（内置 Python 3.9+） |
| C++ SDK | Visual Studio 2019/2022, 3ds Max SDK |

## 🤝 贡献指南

欢迎贡献代码、文档和示例！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。
