# 最佳实践

本文档汇总 3ds Max 插件开发的最佳实践和常见问题解决方案。

## 目录

- [代码组织](#代码组织)
- [性能优化](#性能优化)
- [错误处理](#错误处理)
- [用户体验](#用户体验)
- [版本兼容性](#版本兼容性)
- [测试和调试](#测试和调试)
- [常见问题](#常见问题)

## 代码组织

### 模块化设计

**推荐的项目结构:**

```
my_plugin/
├── __init__.py          # Python 入口
├── core/                # 核心逻辑
│   ├── operations.py
│   └── utils.py
├── ui/                  # 用户界面
│   ├── main_dialog.py
│   └── widgets.py
├── config/              # 配置
│   └── settings.json
└── resources/           # 资源文件
    └── icons/
```

### 命名规范

| 类型 | 规范 | 示例 |
|-----|------|------|
| 类名 | PascalCase | `MyPlugin`, `GeometryHelper` |
| 函数名 | camelCase/snake_case | `createBox`, `create_box` |
| 变量名 | camelCase/snake_case | `myObject`, `my_object` |
| 常量 | UPPER_SNAKE_CASE | `MAX_VERTICES`, `DEFAULT_SIZE` |

### 配置管理

```python
import json
import os

class PluginSettings:
    """插件配置管理类"""
    
    DEFAULT_SETTINGS = {
        "auto_save": True,
        "default_size": 100.0,
        "last_used_path": ""
    }
    
    def __init__(self, config_path):
        self.config_path = config_path
        self.settings = self._load()
    
    def _load(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return {**self.DEFAULT_SETTINGS, **json.load(f)}
        return self.DEFAULT_SETTINGS.copy()
    
    def save(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def get(self, key, default=None):
        return self.settings.get(key, default)
    
    def set(self, key, value):
        self.settings[key] = value
        self.save()
```

## 性能优化

### MaxScript 性能

```maxscript
-- ❌ 不推荐：频繁重绘
for i = 1 to 1000 do (
    box pos:[i*10, 0, 0]
)

-- ✅ 推荐：禁用重绘
with redraw off (
    for i = 1 to 1000 do (
        box pos:[i*10, 0, 0]
    )
)
redrawViews()

-- ✅ 推荐：禁用撤销
undo off (
    for i = 1 to 1000 do (
        box pos:[i*10, 0, 0]
    )
)
```

### Python 性能

```python
from pymxs import runtime as rt

# ❌ 不推荐：逐个处理
for obj in rt.objects:
    rt.select(obj)
    # 处理

# ✅ 推荐：批量处理
objects_list = list(rt.objects)
rt.select(objects_list)
```

### C++ 性能

```cpp
// ❌ 不推荐：频繁获取接口
for (int i = 0; i < 1000; i++) {
    Interface* ip = GetCOREInterface();  // 避免重复调用
    // ...
}

// ✅ 推荐：缓存接口
Interface* ip = GetCOREInterface();
for (int i = 0; i < 1000; i++) {
    // 使用缓存的 ip
}

// ✅ 推荐：暂停视图更新
ip->DisableSceneRedraw();
// 批量操作
ip->EnableSceneRedraw();
ip->RedrawViews(ip->GetTime());
```

### 大型网格处理

```cpp
// 预分配内存
mesh.setNumVerts(vertexCount, FALSE);
mesh.setNumFaces(faceCount, FALSE);

// 批量设置顶点
for (int i = 0; i < vertexCount; i++) {
    mesh.setVert(i, vertices[i]);
}

// 最后更新缓存
mesh.InvalidateGeomCache();
mesh.buildNormals();
```

## 错误处理

### MaxScript 错误处理

```maxscript
fn safeOperation = (
    try (
        -- 可能出错的代码
        result = someFunction()
        return result
    ) catch (
        -- 获取错误信息
        errorMsg = getCurrentException()
        format "Error: %\n" errorMsg
        
        -- 通知用户
        messageBox ("操作失败: " + errorMsg) title:"错误"
        
        return undefined
    )
)
```

### Python 错误处理

```python
import logging
from pymxs import runtime as rt

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def safe_operation(obj):
    """安全的对象操作"""
    try:
        if obj is None:
            raise ValueError("Object cannot be None")
        
        # 操作逻辑
        result = process_object(obj)
        logger.info(f"Successfully processed {obj.name}")
        return result
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        rt.messageBox(str(e), title="Validation Error")
        
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        rt.messageBox(f"An error occurred: {e}", title="Error")
        
    return None
```

### C++ 错误处理

```cpp
bool SafeOperation(INode* node) {
    if (!node) {
        // 记录错误
        MaxMsgBox(nullptr, _T("Node is null"), _T("Error"), MB_OK);
        return false;
    }
    
    try {
        // 操作逻辑
        Object* obj = node->GetObjectRef();
        if (!obj) {
            throw std::runtime_error("Object reference is null");
        }
        
        // 处理对象
        ProcessObject(obj);
        return true;
        
    } catch (const std::exception& e) {
        // 转换错误消息
        TSTR msg;
        msg.printf(_T("Error: %hs"), e.what());
        MaxMsgBox(nullptr, msg, _T("Error"), MB_OK);
        return false;
    }
}
```

## 用户体验

### 进度反馈

**MaxScript:**
```maxscript
fn processWithProgress items = (
    progressStart "Processing..."
    local total = items.count
    
    for i = 1 to total do (
        -- 更新进度
        progressUpdate (100.0 * i / total)
        
        -- 检查取消
        if keyboard.escPressed do (
            progressEnd()
            return false
        )
        
        -- 处理逻辑
        processItem items[i]
    )
    
    progressEnd()
    return true
)
```

**Python:**
```python
from PySide2 import QtWidgets
from pymxs import runtime as rt

def process_with_progress(items):
    progress = QtWidgets.QProgressDialog(
        "Processing...", "Cancel", 0, len(items)
    )
    progress.setWindowModality(QtCore.Qt.WindowModal)
    
    for i, item in enumerate(items):
        if progress.wasCanceled():
            break
        
        progress.setValue(i)
        process_item(item)
    
    progress.close()
```

### 撤销支持

**MaxScript:**
```maxscript
fn myOperation = (
    undo "My Operation" on (
        -- 可撤销的操作
        $.pos = [100, 0, 0]
    )
)
```

**C++:**
```cpp
void MyOperation(INode* node) {
    theHold.Begin();
    
    // 可撤销的操作
    // ...
    
    theHold.Accept(_T("My Operation"));
}
```

## 版本兼容性

### 检测 3ds Max 版本

**MaxScript:**
```maxscript
fn getMaxVersion = (
    local ver = maxVersion()
    local major = ver[1] / 1000
    return major
)

if getMaxVersion() >= 24 then (
    -- 3ds Max 2022+ 特定代码
) else (
    -- 旧版本兼容代码
)
```

**Python:**
```python
from pymxs import runtime as rt

def get_max_version():
    ver = rt.maxVersion()
    return ver[0] // 1000

if get_max_version() >= 24:
    # 3ds Max 2022+ 特定代码
    pass
else:
    # 旧版本兼容代码
    pass
```

**C++:**
```cpp
DWORD maxVersion = Get3DSMAXVersion();
int majorVersion = GET_MAX_RELEASE(maxVersion);

if (majorVersion >= MAX_RELEASE_R24) {
    // 3ds Max 2022+ 特定代码
} else {
    // 旧版本兼容代码
}
```

### API 兼容性包装

```python
class MaxVersionCompat:
    """版本兼容性包装类"""
    
    def __init__(self):
        self.version = self._get_version()
    
    def _get_version(self):
        from pymxs import runtime as rt
        ver = rt.maxVersion()
        return ver[0] // 1000
    
    def create_physical_material(self):
        from pymxs import runtime as rt
        if self.version >= 24:
            return rt.PhysicalMaterial()
        else:
            return rt.StandardMaterial()
```

## 测试和调试

### 单元测试

```python
import unittest
from pymxs import runtime as rt

class TestPluginOperations(unittest.TestCase):
    
    def setUp(self):
        """测试前清理场景"""
        rt.delete(rt.objects)
    
    def tearDown(self):
        """测试后清理场景"""
        rt.delete(rt.objects)
    
    def test_create_box(self):
        """测试创建盒子"""
        box = rt.Box(length=100, width=100, height=100)
        self.assertIsNotNone(box)
        self.assertEqual(box.length, 100)
    
    def test_selection(self):
        """测试选择功能"""
        box = rt.Box()
        rt.select(box)
        self.assertEqual(len(list(rt.selection)), 1)

if __name__ == '__main__':
    unittest.main()
```

### 调试技巧

```python
# 使用断点调试
import pdb

def debug_function():
    pdb.set_trace()  # 设置断点
    # 代码继续...

# 使用日志
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def logged_function(value):
    logger.debug(f"Input value: {value}")
    result = process(value)
    logger.debug(f"Output result: {result}")
    return result
```

## 常见问题

### Q: 脚本运行缓慢

**A:** 检查以下优化点：
1. 使用 `with redraw off` 禁用重绘
2. 使用 `undo off` 禁用撤销
3. 缓存频繁访问的对象引用
4. 使用批量操作替代循环操作

### Q: 内存泄漏

**A:** 确保：
1. 正确释放不再使用的对象
2. 移除不再需要的回调
3. 关闭打开的文件句柄

### Q: 插件无法加载

**A:** 检查：
1. 编译配置是否正确（Release/Debug）
2. Visual Studio 版本是否匹配
3. SDK 版本是否与 3ds Max 版本匹配
4. def 文件导出函数是否正确

### Q: 回调未触发

**A:** 确保：
1. 回调 ID 唯一
2. 回调函数语法正确
3. 回调未被意外移除

## 更多资源

- [MaxScript 开发指南](../maxscript/)
- [Python 开发指南](../python/)
- [C++ SDK 开发指南](../cpp-sdk/)
- [API 参考](../api-reference/)
