# API 参考文档

本文档提供 3ds Max 插件开发常用 API 的快速参考。

## 目录

- [MaxScript API](#maxscript-api)
- [Python pymxs API](#python-pymxs-api)
- [C++ SDK API](#c-sdk-api)
- [事件系统](#事件系统)
- [场景管理](#场景管理)

## MaxScript API

### 场景操作

| 函数 | 描述 | 示例 |
|-----|------|------|
| `objects` | 获取所有对象 | `for obj in objects do print obj.name` |
| `selection` | 获取选中对象 | `sel = selection as array` |
| `select` | 选择对象 | `select $Box001` |
| `deselect` | 取消选择 | `deselect $*` |
| `delete` | 删除对象 | `delete $Box001` |

### 对象创建

| 函数 | 描述 | 示例 |
|-----|------|------|
| `box` | 创建盒子 | `box length:100 width:50 height:30` |
| `sphere` | 创建球体 | `sphere radius:50` |
| `cylinder` | 创建圆柱 | `cylinder radius:25 height:100` |
| `plane` | 创建平面 | `plane length:100 width:100` |
| `teapot` | 创建茶壶 | `teapot radius:25` |

### 变换操作

| 函数 | 描述 | 示例 |
|-----|------|------|
| `move` | 移动对象 | `move $ [10, 0, 0]` |
| `rotate` | 旋转对象 | `rotate $ (eulerAngles 0 0 45)` |
| `scale` | 缩放对象 | `scale $ [2, 2, 2]` |
| `in coordsys` | 坐标系统 | `in coordsys world move $ [0,0,10]` |

### 材质操作

| 函数 | 描述 | 示例 |
|-----|------|------|
| `standardMaterial` | 创建标准材质 | `m = standardMaterial()` |
| `physicalMaterial` | 创建物理材质 | `m = physicalMaterial()` |
| `meditMaterials` | 材质编辑器槽 | `meditMaterials[1] = m` |

### 动画操作

| 函数 | 描述 | 示例 |
|-----|------|------|
| `animate on` | 开启动画模式 | `animate on at time 10 (...)` |
| `at time` | 设置时间点 | `at time 50 $.pos = [0,0,0]` |
| `sliderTime` | 当前滑块时间 | `sliderTime = 50` |

### 文件操作

| 函数 | 描述 | 示例 |
|-----|------|------|
| `loadMaxFile` | 加载场景 | `loadMaxFile "path.max"` |
| `saveMaxFile` | 保存场景 | `saveMaxFile "path.max"` |
| `importFile` | 导入文件 | `importFile "path.fbx"` |
| `exportFile` | 导出文件 | `exportFile "path.fbx"` |
| `resetMaxFile` | 重置场景 | `resetMaxFile #noPrompt` |

## Python pymxs API

### 导入模块

```python
from pymxs import runtime as rt
from pymxs import attime
```

### 场景操作

| 函数 | 描述 |
|-----|------|
| `rt.objects` | 获取所有对象 |
| `rt.selection` | 获取选中对象 |
| `rt.select(obj)` | 选择对象 |
| `rt.delete(obj)` | 删除对象 |
| `rt.getNodeByName(name)` | 按名称获取对象 |

### 对象创建

```python
# 创建基本几何体
box = rt.Box(length=100, width=50, height=30)
sphere = rt.Sphere(radius=50)
cylinder = rt.Cylinder(radius=25, height=100)

# 设置位置
box.pos = rt.Point3(0, 0, 0)
```

### 数据类型

| 类型 | 描述 | 示例 |
|-----|------|------|
| `rt.Point3` | 3D 点 | `rt.Point3(10, 20, 30)` |
| `rt.Color` | 颜色 | `rt.Color(255, 0, 0)` |
| `rt.Matrix3` | 变换矩阵 | `rt.Matrix3(1)` |
| `rt.EulerAngles` | 欧拉角 | `rt.EulerAngles(0, 0, 45)` |

## C++ SDK API

### 核心类层次

```
ReferenceTarget
├── ReferenceMaker
│   ├── Object
│   │   ├── GeomObject
│   │   │   └── SimpleObject2
│   │   └── ShapeObject
│   ├── Modifier
│   ├── Material
│   └── Controller
└── INode
```

### Interface 接口

```cpp
Interface* ip = GetCOREInterface();

// 选择操作
int count = ip->GetSelNodeCount();
INode* node = ip->GetSelNode(0);

// 时间操作
TimeValue t = ip->GetTime();
ip->SetTime(100 * GetTicksPerFrame());

// 视图操作
ip->RedrawViews(t);
ip->ForceCompleteRedraw();
```

### INode 操作

```cpp
INode* node;

// 获取变换
Matrix3 tm = node->GetNodeTM(t);
Matrix3 objTM = node->GetObjectTM(t);

// 设置变换
node->SetNodeTM(t, newTM);

// 获取对象
Object* obj = node->GetObjectRef();
Object* evalObj = node->EvalWorldState(t).obj;

// 材质
Mtl* mtl = node->GetMtl();
node->SetMtl(newMtl);

// 名称
TSTR name = node->GetName();
node->SetName(_T("NewName"));
```

### Mesh 操作

```cpp
Mesh& mesh;

// 顶点操作
int numVerts = mesh.getNumVerts();
Point3 vert = mesh.getVert(i);
mesh.setVert(i, Point3(x, y, z));

// 面操作
int numFaces = mesh.getNumFaces();
Face& face = mesh.faces[i];
face.setVerts(v0, v1, v2);
face.setSmGroup(1);

// 法线
mesh.buildNormals();
Point3 normal = mesh.getFaceNormal(i);

// 更新缓存
mesh.InvalidateGeomCache();
```

## 事件系统

### MaxScript 回调

```maxscript
-- 可用回调事件
callbacks.addScript #selectionSetChanged "onSelect()" id:#myId
callbacks.addScript #nodeCreated "onNodeCreated()" id:#myId
callbacks.addScript #nodeDeleted "onNodeDeleted()" id:#myId
callbacks.addScript #timeChange "onTimeChange()" id:#myId
callbacks.addScript #filePreOpen "onFileOpen()" id:#myId
callbacks.addScript #filePostOpen "onFileOpened()" id:#myId
callbacks.addScript #systemPreNew "onNew()" id:#myId

-- 移除回调
callbacks.removeScripts id:#myId
```

### Python 回调

```python
from pymxs import runtime as rt

def on_selection_changed():
    print(f"Selection changed: {len(list(rt.selection))} objects")

rt.callbacks.addScript(
    rt.Name("selectionSetChanged"),
    "python.Execute(\"on_selection_changed()\")",
    id=rt.Name("pyCallback")
)
```

### C++ 回调

```cpp
// 节点事件回调
class MyNodeEventCallback : public INodeEventCallback {
public:
    void Added(NodeKeyTab& nodes) override {
        // 节点添加
    }
    void Deleted(NodeKeyTab& nodes) override {
        // 节点删除
    }
    void SelectionChanged() override {
        // 选择改变
    }
};

// 注册回调
INodeEventCallback* cb = new MyNodeEventCallback();
GetISceneEventManager()->RegisterCallback(cb);
```

## 场景管理

### 场景遍历

**MaxScript:**
```maxscript
fn traverseScene node = (
    print node.name
    for child in node.children do traverseScene child
)
traverseScene rootNode
```

**Python:**
```python
def traverse_scene(node=None):
    if node is None:
        for obj in rt.objects:
            print(obj.name)
    else:
        print(node.name)
        for i in range(node.numChildren):
            traverse_scene(node.children[i])
```

**C++:**
```cpp
void TraverseScene(INode* node) {
    if (!node) return;
    
    // 处理节点
    const TCHAR* name = node->GetName();
    
    // 遍历子节点
    for (int i = 0; i < node->NumberOfChildren(); i++) {
        TraverseScene(node->GetChildNode(i));
    }
}

// 从根节点开始
TraverseScene(GetCOREInterface()->GetRootNode());
```

### 图层管理

**MaxScript:**
```maxscript
-- 创建图层
newLayer = LayerManager.newLayer()
newLayer.setName "MyLayer"

-- 添加对象到图层
newLayer.addNode $Box001

-- 获取图层
layer = LayerManager.getLayerFromName "MyLayer"
```

**Python:**
```python
# 创建图层
new_layer = rt.LayerManager.newLayer()
new_layer.setName("MyLayer")

# 添加对象
new_layer.addNode(rt.selection[0])
```

## 更多资源

- [MaxScript 开发指南](../maxscript/)
- [Python 开发指南](../python/)
- [C++ SDK 开发指南](../cpp-sdk/)
