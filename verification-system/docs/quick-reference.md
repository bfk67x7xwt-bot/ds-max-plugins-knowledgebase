# 快速参考指南
# Quick Reference Guide

## 命令速查 (Command Quick Reference)

### 验证插件
```bash
python verify_plugin.py /path/to/plugin
```

### 查看帮助
```bash
python verify_plugin.py --help
```

## 文件要求速查 (File Requirements)

### 必需文件 (Required)
- [ ] `plugin.ms` (或 .mse, .dlu, .dlx, .dlo)
- [ ] `README.md`
- [ ] `LICENSE`

### 推荐文件 (Recommended)
- [ ] `CHANGELOG.md`
- [ ] `docs/` 目录
- [ ] `examples/` 目录
- [ ] `tests/` 目录

## README.md 必需内容 (Required README Content)

```markdown
# Plugin Name
Brief description

## Features
- Feature list

## System Requirements
- 3ds Max version
- OS requirements
- RAM requirements

## Installation
Installation steps

## Usage
Usage instructions with examples

## Author
Author information

## License
License type
```

## 代码模板速查 (Code Template)

### 文件头部
```maxscript
/*******************************************************************************
 * Plugin Name: [Name]
 * Version: X.Y.Z
 * Author: [Author]
 * Description: [Description]
 * Compatible with: 3ds Max 2020-2024
 * License: [License]
 ******************************************************************************/
```

### 错误处理
```maxscript
try (
    -- Your code
)
catch (e) (
    messageBox ("Error: " + e as string)
)
```

### 进度条
```maxscript
progressStart "Processing..."
for i = 1 to count do (
    progressUpdate (100.0 * i / count)
    -- Process
)
progressEnd()
```

### 输入验证
```maxscript
if value == undefined then (
    messageBox "Invalid input"
    return undefined
)
```

## 评级速查 (Rating Quick Reference)

| 分数 | 评级 | 说明 |
|------|------|------|
| 95+ | ✅ 优秀 | 准备发布 |
| 85-94 | ✔️ 良好 | 少量改进 |
| 70-84 | ⚠️ 合格 | 需要改进 |
| <70 | ❌ 不合格 | 重大问题 |

## 验证级别权重 (Level Weights)

- Level 1 (基础): 35%
- Level 2 (功能): 30%
- Level 3 (兼容): 20%
- Level 4 (性能): 15%

## 常见问题快速解决 (Quick Fixes)

### 问题：缺少 LICENSE
```bash
# 复制 MIT License 模板
cp templates/LICENSE ./LICENSE
# 编辑并填写年份和作者
```

### 问题：缺少 README
```bash
# 复制 README 模板
cp templates/README-template.md ./README.md
# 按模板填写内容
```

### 问题：缺少错误处理
```maxscript
-- 在所有函数中添加 try-catch
fn myFunction = (
    try (
        -- 原有代码
    )
    catch (e) (
        messageBox ("Error: " + e as string)
        return undefined
    )
)
```

### 问题：缺少文件头部
```maxscript
-- 在文件最开始添加注释块
/*******************************************************************************
 * Plugin Name: My Plugin
 * Version: 1.0.0
 * ... (其他信息)
 ******************************************************************************/
```

## 验证流程 (Verification Workflow)

```
1. 开发插件
   ↓
2. 运行验证脚本
   ↓
3. 查看报告
   ↓
4. 修复问题
   ↓
5. 重新验证
   ↓
6. 达到"良好"评级
   ↓
7. 准备发布
```

## 文档路径速查 (Documentation Paths)

- 验证规范: `docs/verification-specification.md`
- 检查清单: `docs/verification-checklist.md`
- 最佳实践: `docs/best-practices.md`
- 故障排除: `docs/troubleshooting.md`
- 用户指南: `docs/user-guide.md`

## 模板路径速查 (Template Paths)

- 插件模板: `templates/plugin-template.ms`
- README模板: `templates/README-template.md`
- CHANGELOG模板: `templates/CHANGELOG-template.md`

## 示例路径速查 (Example Paths)

- 示例插件: `examples/sample-plugin.ms`
- 示例README: `examples/README.md`

## 验证脚本路径 (Script Path)

- 验证脚本: `scripts/verify_plugin.py`

## 最低通过标准 (Minimum Pass Criteria)

- Level 1: 100% ✅
- Level 2: 90% ✅
- Level 3: 80% ⚠️
- Level 4: 70% ⚠️
- 总分: 70% ⚠️

## MAXScript 常用模式 (Common Patterns)

### 结构体定义
```maxscript
struct MyStruct (
    property1 = defaultValue,
    fn method1 = ( ... )
)
```

### UI 定义
```maxscript
rollout myRollout "Title" (
    button btn "Click"
    on btn pressed do ( ... )
)
```

### 全局变量
```maxscript
global g_myVariable = value
```

### Undo 支持
```maxscript
with undo "Action Name" on (
    -- Your code
)
```

## 性能优化技巧 (Performance Tips)

```maxscript
-- 禁用重绘
with redraw off ( ... )

-- 禁用 undo (谨慎使用)
with undo off ( ... )

-- 垃圾回收
gc()

-- 批量操作
for obj in objects do ( ... )
-- 而不是逐个处理
```

## 获取帮助 (Get Help)

- 📚 文档: 查看 `docs/` 目录
- 💡 示例: 查看 `examples/` 目录
- 🐛 Issues: GitHub Issues
- 💬 讨论: GitHub Discussions

---

**提示**: 将此页面加入书签以便快速查阅！
