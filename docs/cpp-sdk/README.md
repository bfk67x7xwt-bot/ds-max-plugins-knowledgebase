# C++ SDK 开发指南

C++ SDK 适合开发高性能插件和深度定制功能，提供对 3ds Max 底层 API 的完整访问。

## 目录

- [开发环境配置](#开发环境配置)
- [项目设置](#项目设置)
- [插件架构](#插件架构)
- [常见插件类型](#常见插件类型)
- [编译和调试](#编译和调试)
- [API 常用类](#api-常用类)

## 开发环境配置

### 系统要求

| 3ds Max 版本 | Visual Studio 版本 | SDK 路径 |
|-------------|-------------------|---------|
| 2024 | VS 2022 | `C:\Program Files\Autodesk\3ds Max 2024 SDK\` |
| 2023 | VS 2019/2022 | `C:\Program Files\Autodesk\3ds Max 2023 SDK\` |
| 2022 | VS 2019 | `C:\Program Files\Autodesk\3ds Max 2022 SDK\` |

### SDK 目录结构

```
3ds Max 2024 SDK/
├── maxsdk/
│   ├── include/           # 头文件
│   ├── lib/               # 库文件
│   │   ├── x64/
│   │   │   ├── Release/
│   │   │   └── Debug/
│   └── samples/           # 示例代码
└── howto/                 # 教程文档
```

### 环境变量配置

```batch
set MAXSDK_PATH=C:\Program Files\Autodesk\3ds Max 2024 SDK\maxsdk
set 3DSMAX_PATH=C:\Program Files\Autodesk\3ds Max 2024
```

## 项目设置

### 创建新项目

1. 创建 Visual Studio DLL 项目
2. 配置项目属性

### 项目属性配置

**C/C++ > 常规 > 附加包含目录：**
```
$(MAXSDK_PATH)\include
```

**链接器 > 常规 > 附加库目录：**
```
$(MAXSDK_PATH)\lib\x64\Release
```

**链接器 > 输入 > 附加依赖项：**
```
core.lib
geom.lib
mesh.lib
maxutil.lib
maxscrpt.lib
paramblk2.lib
```

### def 文件

创建 `plugin.def` 文件：

```def
LIBRARY MyPlugin
EXPORTS
    LibDescription     @1
    LibNumberClasses   @2
    LibClassDesc       @3
    LibVersion         @4
```

## 插件架构

### 基本插件结构

```cpp
// MyPlugin.h
#pragma once
#include <Max.h>
#include <iparamb2.h>

// 插件类 ID
#define MYPLUGIN_CLASS_ID Class_ID(0x12345678, 0x87654321)

// 插件类声明
class MyPlugin : public UtilityObj {
public:
    MyPlugin();
    ~MyPlugin();
    
    // 必须实现的方法
    void BeginEditParams(Interface* ip, IUtil* iu) override;
    void EndEditParams(Interface* ip, IUtil* iu) override;
    void DeleteThis() override { delete this; }
    
private:
    Interface* ip;
    IUtil* iu;
};

// 类描述符
class MyPluginClassDesc : public ClassDesc2 {
public:
    int IsPublic() override { return TRUE; }
    void* Create(BOOL loading = FALSE) override { return new MyPlugin(); }
    const TCHAR* ClassName() override { return _T("My Plugin"); }
    SClass_ID SuperClassID() override { return UTILITY_CLASS_ID; }
    Class_ID ClassID() override { return MYPLUGIN_CLASS_ID; }
    const TCHAR* Category() override { return _T("Custom Tools"); }
};
```

### 入口点实现

```cpp
// MyPlugin.cpp
#include "MyPlugin.h"

// 全局实例
static MyPluginClassDesc myPluginDesc;

// DLL 入口点
BOOL WINAPI DllMain(HINSTANCE hinstDLL, ULONG fdwReason, LPVOID lpvReserved) {
    switch (fdwReason) {
        case DLL_PROCESS_ATTACH:
            DisableThreadLibraryCalls(hinstDLL);
            break;
    }
    return TRUE;
}

// 导出函数
extern "C" {

__declspec(dllexport) const TCHAR* LibDescription() {
    return _T("My Plugin Description");
}

__declspec(dllexport) int LibNumberClasses() {
    return 1;
}

__declspec(dllexport) ClassDesc* LibClassDesc(int i) {
    switch (i) {
        case 0: return &myPluginDesc;
        default: return nullptr;
    }
}

__declspec(dllexport) ULONG LibVersion() {
    return VERSION_3DSMAX;
}

}  // extern "C"
```

## 常见插件类型

### 几何体插件

```cpp
// GeomPlugin.h
class GeomPlugin : public SimpleObject2 {
public:
    // 构造函数
    GeomPlugin();
    
    // 基本方法
    void BuildMesh(TimeValue t) override;
    BOOL OKtoDisplay(TimeValue t) override { return TRUE; }
    void InvalidateUI() override;
    
    // 参数块
    IParamBlock2* pblock2;
    
    // 类 ID
    Class_ID ClassID() override { return GEOM_PLUGIN_CLASS_ID; }
    SClass_ID SuperClassID() override { return GEOMOBJECT_CLASS_ID; }
    
    // 名称
    void GetClassName(TSTR& s) override { s = _T("GeomPlugin"); }
    const TCHAR* GetObjectName() override { return _T("Geom Plugin"); }
};

// 参数块枚举
enum { geom_params };
enum { 
    pb_radius,
    pb_segments
};

// 参数块描述
static ParamBlockDesc2 geom_param_blk(
    geom_params, _T("params"), 0, &geomPluginClassDesc, P_AUTO_CONSTRUCT + P_AUTO_UI,
    0,  // ref number
    IDD_PANEL, IDS_PARAMS, 0, 0, NULL,
    
    pb_radius, _T("radius"), TYPE_FLOAT, P_ANIMATABLE, IDS_RADIUS,
        p_default, 50.0f,
        p_range, 0.0f, 1000.0f,
        p_ui, TYPE_SPINNER, EDITTYPE_FLOAT, IDC_RADIUS_EDIT, IDC_RADIUS_SPIN, 1.0f,
        p_end,
    
    pb_segments, _T("segments"), TYPE_INT, 0, IDS_SEGMENTS,
        p_default, 12,
        p_range, 3, 100,
        p_ui, TYPE_SPINNER, EDITTYPE_INT, IDC_SEGS_EDIT, IDC_SEGS_SPIN, 1,
        p_end,
    p_end
);

// BuildMesh 实现
void GeomPlugin::BuildMesh(TimeValue t) {
    float radius = pblock2->GetFloat(pb_radius, t);
    int segs = pblock2->GetInt(pb_segments, t);
    
    // 创建网格顶点和面
    mesh.setNumVerts(segs + 1);
    mesh.setNumFaces(segs);
    
    // 设置顶点
    mesh.setVert(0, Point3(0, 0, 0));
    for (int i = 0; i < segs; i++) {
        float angle = 2.0f * PI * i / segs;
        float x = radius * cos(angle);
        float y = radius * sin(angle);
        mesh.setVert(i + 1, Point3(x, y, 0));
    }
    
    // 设置面
    for (int i = 0; i < segs; i++) {
        int next = (i + 1) % segs;
        mesh.faces[i].setVerts(0, i + 1, next + 1);
        mesh.faces[i].setSmGroup(1);
        mesh.faces[i].setEdgeVisFlags(1, 1, 1);
    }
    
    mesh.InvalidateGeomCache();
}
```

### 修改器插件

```cpp
// ModifierPlugin.h
class ModifierPlugin : public Modifier {
public:
    // 通道
    ChannelMask ChannelsUsed() override { return GEOM_CHANNEL; }
    ChannelMask ChannelsChanged() override { return GEOM_CHANNEL; }
    
    // 修改方法
    void ModifyObject(TimeValue t, ModContext& mc, ObjectState* os, INode* node) override;
    
    // 类信息
    Class_ID ClassID() override { return MODIFIER_PLUGIN_CLASS_ID; }
    SClass_ID SuperClassID() override { return OSM_CLASS_ID; }
    
    // 有效性
    Interval LocalValidity(TimeValue t) override;
    
    // 创建实例
    RefTargetHandle Clone(RemapDir& remap) override;
};

// 修改实现
void ModifierPlugin::ModifyObject(TimeValue t, ModContext& mc, ObjectState* os, INode* node) {
    if (!os->obj) return;
    
    // 获取网格
    Mesh* mesh = nullptr;
    if (os->obj->IsSubClassOf(triObjectClassID)) {
        TriObject* triObj = static_cast<TriObject*>(os->obj);
        mesh = &triObj->GetMesh();
    }
    
    if (!mesh) return;
    
    // 修改顶点
    int numVerts = mesh->getNumVerts();
    for (int i = 0; i < numVerts; i++) {
        Point3& vert = mesh->verts[i];
        // 应用修改
        vert.z += sin(vert.x * 0.1f) * 10.0f;
    }
    
    mesh->InvalidateGeomCache();
}
```

### 导入导出插件

```cpp
// ExporterPlugin.h
class ExporterPlugin : public SceneExport {
public:
    // 文件扩展名
    int ExtCount() override { return 1; }
    const TCHAR* Ext(int n) override { return _T("myf"); }
    const TCHAR* LongDesc() override { return _T("My Format File"); }
    const TCHAR* ShortDesc() override { return _T("My Format"); }
    const TCHAR* AuthorName() override { return _T("Author Name"); }
    const TCHAR* CopyrightMessage() override { return _T("Copyright 2024"); }
    unsigned int Version() override { return 100; }
    
    // 导出方法
    int DoExport(const TCHAR* name, ExpInterface* ei, Interface* ip, 
                 BOOL suppressPrompts = FALSE, DWORD options = 0) override;
};

// 导出实现
int ExporterPlugin::DoExport(const TCHAR* name, ExpInterface* ei, Interface* ip,
                              BOOL suppressPrompts, DWORD options) {
    // 打开文件
    FILE* file = _tfopen(name, _T("wb"));
    if (!file) return FALSE;
    
    // 遍历场景节点
    INode* root = ip->GetRootNode();
    for (int i = 0; i < root->NumberOfChildren(); i++) {
        INode* node = root->GetChildNode(i);
        ExportNode(file, node);
    }
    
    fclose(file);
    return TRUE;
}
```

## 编译和调试

### 编译配置

1. **Release 配置**：用于发布
2. **Debug 配置**：用于调试

### 调试设置

**调试 > 命令：**
```
C:\Program Files\Autodesk\3ds Max 2024\3dsmax.exe
```

### 插件安装

将编译后的 `.dlu`、`.dlm` 或 `.dlo` 文件复制到：
```
C:\Program Files\Autodesk\3ds Max 2024\plugins\
```

或自定义插件目录：
```
%LOCALAPPDATA%\Autodesk\3dsMax\2024 - 64bit\ENU\plugins\
```

## API 常用类

### 核心类

| 类名 | 描述 |
|-----|------|
| `Interface` | 3ds Max 主接口 |
| `INode` | 场景节点 |
| `Object` | 对象基类 |
| `Modifier` | 修改器基类 |
| `Mesh` | 网格数据 |
| `Matrix3` | 3x4 变换矩阵 |
| `Point3` | 3D 点/向量 |
| `Interval` | 时间间隔 |

### 常用操作

```cpp
// 获取接口
Interface* ip = GetCOREInterface();

// 获取选中节点
int numSelected = ip->GetSelNodeCount();
for (int i = 0; i < numSelected; i++) {
    INode* node = ip->GetSelNode(i);
    // 处理节点
}

// 获取当前时间
TimeValue t = ip->GetTime();

// 刷新视图
ip->RedrawViews(t);
```

## 更多资源

- [C++ SDK 代码示例](../../examples/cpp-sdk/)
- [API 参考](../api-reference/)
- [最佳实践](../best-practices/)
