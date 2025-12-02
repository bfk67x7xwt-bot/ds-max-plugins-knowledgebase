# 在线验证系统使用指南
# Online Verification System User Guide

## 快速开始 (Quick Start)

本指南帮助您快速开始使用3ds Max插件在线验证系统。

### 系统要求 (System Requirements)

- Python 3.6 或更高版本
- 任何操作系统 (Windows, macOS, Linux)
- 无需额外Python依赖包

### 基本使用 (Basic Usage)

#### 1. 验证现有插件

```bash
# 进入验证脚本目录
cd verification-system/scripts

# 运行验证
python verify_plugin.py /path/to/your/plugin

# 示例：验证示例插件
python verify_plugin.py ../examples/
```

#### 2. 查看验证报告

验证完成后，会在插件目录生成 `verification-report.json` 文件：

```json
{
  "plugin_name": "Your Plugin",
  "version": "1.0.0",
  "overall_score": 85.5,
  "rating": "良好 (Good)",
  "recommendations": [...]
}
```

#### 3. 理解评级系统

| 评级 | 分数范围 | 说明 |
|------|---------|------|
| ✅ 优秀 (Excellent) | 95-100 | 所有检查几乎完美通过 |
| ✔️ 良好 (Good) | 85-94 | 大部分检查通过，少量改进空间 |
| ⚠️ 合格 (Pass) | 70-84 | 基本要求满足，需要改进 |
| ❌ 不合格 (Fail) | < 70 | 需要重大改进 |

## 验证级别详解 (Verification Levels Explained)

### Level 1: 基础验证 (35% 权重)

**必须100%通过才能继续**

检查项目：
- ✅ 主插件文件存在 (.ms, .mse, .dlu, .dlx, .dlo)
- ✅ README.md 文件存在
- ✅ LICENSE 文件存在
- ✅ README 包含完整信息（名称、版本、作者、安装说明、使用示例）
- ✅ 代码包含文件头部注释

**为什么重要？**
基础文件和文档是插件可用性和可维护性的基础。

### Level 2: 功能验证 (30% 权重)

**必须90%以上通过**

检查项目：
- ✅ 包含错误处理机制 (try-catch)
- ✅ 包含日志记录功能
- ✅ 遵循命名规范
- ✅ 代码质量良好

**为什么重要？**
这些确保插件能够稳定运行并易于调试。

### Level 3: 兼容性验证 (20% 权重)

**建议80%以上通过**

检查项目：
- ✅ 3ds Max 版本兼容性已声明
- ✅ 系统要求已声明
- ✅ 依赖项已文档化（可选）

**为什么重要？**
帮助用户了解插件是否适用于他们的环境。

### Level 4: 性能验证 (15% 权重)

**建议70%以上通过**

检查项目：
- ✅ 插件文件大小合理
- ✅ 包含性能优化代码

**为什么重要？**
影响插件的用户体验和系统性能。

## 常见问题解答 (FAQ)

### Q1: 为什么我的插件评分低？

**A**: 检查验证报告中的 `recommendations` 部分，它会列出需要改进的具体项目。

### Q2: 如何提高评分？

**A**: 按优先级：
1. 确保 Level 1 100% 通过（添加缺失文件）
2. 改进 Level 2 项目（添加错误处理）
3. 补充 Level 3 信息（文档化兼容性）
4. 优化 Level 4 指标（性能优化）

### Q3: LICENSE 文件是必需的吗？

**A**: 是的。LICENSE 文件对于：
- 保护您的权利
- 告知用户使用条款
- 开源合规性
都是必需的。

推荐使用 MIT License（宽松）或 GPL（开源）。

### Q4: 如何添加文件头部注释？

**A**: 参考模板：

```maxscript
/*******************************************************************************
 * Plugin Name: Your Plugin Name
 * Version: 1.0.0
 * Author: Your Name
 * Description: Brief description
 * Compatible with: 3ds Max 2020-2024
 * License: MIT
 ******************************************************************************/
```

### Q5: 验证报告可以自定义吗？

**A**: 当前版本输出固定格式的 JSON 报告。如需自定义，可以修改 `verify_plugin.py` 脚本的 `save_report` 方法。

## 最佳实践建议 (Best Practice Tips)

### 开发前 (Before Development)

1. ✅ 使用提供的模板开始
2. ✅ 阅读最佳实践指南
3. ✅ 规划插件结构

### 开发中 (During Development)

1. ✅ 定期运行验证脚本
2. ✅ 及时修复发现的问题
3. ✅ 保持文档更新

### 发布前 (Before Release)

1. ✅ 确保评级至少为"良好"
2. ✅ 所有 Level 1-2 检查通过
3. ✅ 测试所有声明的功能
4. ✅ 更新 CHANGELOG

## 验证脚本高级用法 (Advanced Usage)

### 脚本参数

```bash
# 显示帮助
python verify_plugin.py --help

# 基本验证
python verify_plugin.py /path/to/plugin

# 验证多个插件
for dir in plugin1 plugin2 plugin3; do
    python verify_plugin.py $dir
done
```

### 集成到 CI/CD

将验证集成到持续集成流程：

```yaml
# GitHub Actions 示例
name: Verify Plugin
on: [push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Verification
        run: |
          python verification-system/scripts/verify_plugin.py .
      - name: Check Score
        run: |
          # 检查评分是否达标
          # 从 verification-report.json 读取
```

### 自定义验证规则

您可以通过修改脚本添加自定义检查：

```python
# 在 PluginVerifier 类中添加新方法
def _verify_custom_check(self):
    checks = []
    
    # 添加您的检查逻辑
    custom_check = {
        'name': '自定义检查',
        'passed': True/False,
        'details': '检查详情'
    }
    checks.append(custom_check)
    
    return checks
```

## 获取帮助 (Getting Help)

### 文档资源

1. **[验证规范](docs/verification-specification.md)** - 详细的验证标准
2. **[检查清单](docs/verification-checklist.md)** - 完整检查项目
3. **[最佳实践](docs/best-practices.md)** - 开发指南
4. **[故障排除](docs/troubleshooting.md)** - 常见问题解决

### 社区支持

- GitHub Issues: 报告问题和建议
- GitHub Discussions: 讨论和交流
- 示例代码: 查看 examples/ 目录

## 更新和维护 (Updates and Maintenance)

### 系统更新

验证系统会定期更新以包含：
- 新的检查规则
- 改进的验证逻辑
- 更多最佳实践
- Bug 修复

### 保持同步

```bash
# 更新到最新版本
git pull origin main

# 查看更新日志
git log --oneline verification-system/
```

## 贡献验证规则 (Contributing Verification Rules)

欢迎贡献新的验证规则！

### 贡献步骤

1. Fork 仓库
2. 添加新检查到 `verify_plugin.py`
3. 更新文档
4. 提交 Pull Request

### 规则要求

- ✅ 清晰的检查目的
- ✅ 准确的实现逻辑
- ✅ 完善的文档说明
- ✅ 示例和测试

---

**版本**: 1.0.0  
**最后更新**: 2025-12-02  
**维护者**: DS Max Plugins Knowledgebase Team

如有问题或建议，请在 GitHub Issues 中反馈。
