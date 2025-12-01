# Python 开发指南

3ds Max 2022 及更高版本支持 Python 3.9+，适合复杂逻辑开发和外部库集成。

## 目录

- [环境设置](#环境设置)
- [Python 基础](#python-基础)
- [pymxs 模块](#pymxs-模块)
- [MaxPlus API](#maxplus-api)
- [用户界面开发](#用户界面开发)
- [外部库集成](#外部库集成)
- [调试和测试](#调试和测试)

## 环境设置

### Python 环境路径

3ds Max 自带 Python 解释器，位于：
```
C:\Program Files\Autodesk\3ds Max 2024\Python39\
```

### 安装第三方包

```bash
# 使用 3ds Max 自带的 pip
"C:\Program Files\Autodesk\3ds Max 2024\Python39\python.exe" -m pip install package_name
```

### 脚本放置位置

```
%USERPROFILE%\AppData\Local\Autodesk\3dsMax\2024 - 64bit\ENU\scripts\
```

## Python 基础

### Hello World

```python
# hello.py
from pymxs import runtime as rt

rt.messageBox("Hello from Python!")
```

### 在 3ds Max 中运行

```python
# 方法 1：通过菜单 Scripting > Run Script
# 方法 2：通过 MaxScript 调用
# python.ExecuteFile @"C:\path\to\script.py"
```

## pymxs 模块

### 导入 pymxs

```python
from pymxs import runtime as rt
from pymxs import attime
```

### 创建对象

```python
from pymxs import runtime as rt

# 创建几何体
box = rt.Box(length=100, width=100, height=100)
sphere = rt.Sphere(radius=50, pos=rt.Point3(150, 0, 0))
cylinder = rt.Cylinder(radius=25, height=100)

# 设置属性
box.wirecolor = rt.Color(255, 0, 0)
box.name = "PythonBox"
```

### 对象选择

```python
from pymxs import runtime as rt

# 选择所有对象
rt.select(rt.objects)

# 按名称选择
obj = rt.getNodeByName("BoxName")
if obj:
    rt.select(obj)

# 获取当前选择
selection = list(rt.selection)
print(f"Selected objects: {len(selection)}")
```

### 变换操作

```python
from pymxs import runtime as rt

obj = rt.selection[0]

# 移动
rt.move(obj, rt.Point3(10, 0, 0))

# 旋转
rt.rotate(obj, rt.EulerAngles(0, 0, 45))

# 缩放
rt.scale(obj, rt.Point3(2, 2, 2))

# 设置位置
obj.pos = rt.Point3(100, 200, 300)
```

### 材质操作

```python
from pymxs import runtime as rt

# 创建标准材质
mat = rt.StandardMaterial()
mat.name = "RedMaterial"
mat.diffuse = rt.Color(255, 0, 0)

# 应用材质
obj = rt.selection[0]
obj.material = mat
```

### 动画操作

```python
from pymxs import runtime as rt, attime

obj = rt.selection[0]

# 设置关键帧
with attime(0):
    rt.setProperty(obj, "pos", rt.Point3(0, 0, 0))
    
with attime(100):
    rt.setProperty(obj, "pos", rt.Point3(100, 100, 0))

# 启用自动关键帧
rt.animateContext = True
```

## MaxPlus API

### 场景遍历

```python
from pymxs import runtime as rt

def traverse_scene():
    """遍历场景中的所有对象"""
    for obj in rt.objects:
        print(f"Object: {obj.name}, Class: {rt.classOf(obj)}")
        
traverse_scene()
```

### 文件操作

```python
from pymxs import runtime as rt

# 导入文件
rt.importFile(r"C:\path\to\file.fbx")

# 导出文件
rt.exportFile(r"C:\path\to\output.fbx", 
              rt.Name("noPrompt"), 
              selectedOnly=True)

# 保存场景
rt.saveMaxFile(r"C:\path\to\scene.max")
```

## 用户界面开发

### 使用 PySide2/Qt

```python
from PySide2 import QtWidgets, QtCore
from pymxs import runtime as rt
import MaxPlus

class MyToolDialog(QtWidgets.QDialog):
    def __init__(self, parent=MaxPlus.GetQMaxMainWindow()):
        super().__init__(parent)
        self.setWindowTitle("My Python Tool")
        self.setMinimumSize(300, 200)
        
        layout = QtWidgets.QVBoxLayout(self)
        
        # 添加控件
        self.label = QtWidgets.QLabel("Object Count: 0")
        layout.addWidget(self.label)
        
        self.btn_count = QtWidgets.QPushButton("Count Objects")
        self.btn_count.clicked.connect(self.count_objects)
        layout.addWidget(self.btn_count)
        
        self.btn_create = QtWidgets.QPushButton("Create Box")
        self.btn_create.clicked.connect(self.create_box)
        layout.addWidget(self.btn_create)
        
    def count_objects(self):
        count = len(list(rt.objects))
        self.label.setText(f"Object Count: {count}")
        
    def create_box(self):
        rt.Box(length=100, width=100, height=100)
        self.count_objects()

# 显示对话框
dialog = MyToolDialog()
dialog.show()
```

### 使用 pymxs rollout

```python
from pymxs import runtime as rt

# 通过 MaxScript 创建 UI
rollout_code = '''
rollout pyRollout "Python Tool" (
    button btnRun "Run Python"
    on btnRun pressed do (
        python.Execute "print('Button clicked from MaxScript!')"
    )
)
createDialog pyRollout width:200
'''
rt.execute(rollout_code)
```

## 外部库集成

### NumPy 数据处理

```python
import numpy as np
from pymxs import runtime as rt

def analyze_mesh(obj):
    """分析网格顶点数据"""
    mesh = rt.snapshotAsMesh(obj)
    num_verts = rt.getNumVerts(mesh)
    
    # 获取顶点数据
    vertices = []
    for i in range(1, num_verts + 1):
        vert = rt.getVert(mesh, i)
        vertices.append([vert.x, vert.y, vert.z])
    
    # 使用 NumPy 分析
    verts_array = np.array(vertices)
    center = np.mean(verts_array, axis=0)
    bbox_min = np.min(verts_array, axis=0)
    bbox_max = np.max(verts_array, axis=0)
    
    return {
        'center': center,
        'bbox_min': bbox_min,
        'bbox_max': bbox_max,
        'vertex_count': num_verts
    }
```

### JSON 配置管理

```python
import json
import os
from pymxs import runtime as rt

class PluginConfig:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load()
        
    def load(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save(self):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        self.save()
```

## 调试和测试

### 日志记录

```python
import logging
import os

# 设置日志
log_path = os.path.join(os.environ['USERPROFILE'], 'max_python.log')
logging.basicConfig(
    filename=log_path,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def debug_function():
    logging.info("Function started")
    try:
        # 代码逻辑
        result = some_operation()
        logging.debug(f"Result: {result}")
    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)
```

### 异常处理

```python
from pymxs import runtime as rt

def safe_operation():
    try:
        obj = rt.selection[0]
        # 操作
        return True
    except IndexError:
        rt.messageBox("Please select an object first!")
        return False
    except Exception as e:
        rt.messageBox(f"Error: {str(e)}")
        return False
```

### 单元测试

```python
import unittest
from pymxs import runtime as rt

class TestBoxCreation(unittest.TestCase):
    def setUp(self):
        # 清理场景
        rt.delete(rt.objects)
        
    def test_create_box(self):
        box = rt.Box(length=100, width=100, height=100)
        self.assertIsNotNone(box)
        self.assertEqual(box.length, 100)
        
    def tearDown(self):
        rt.delete(rt.objects)

if __name__ == '__main__':
    unittest.main()
```

## 更多资源

- [Python 代码示例](../../examples/python/)
- [API 参考](../api-reference/)
- [最佳实践](../best-practices/)
