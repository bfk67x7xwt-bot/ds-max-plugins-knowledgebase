/**
 * C++ SDK 示例：几何体插件
 * ========================================
 * 描述：演示如何创建自定义参数化几何体
 * 适用于 3ds Max 2020+
 */

#pragma once
#include <Max.h>
#include <simpobj.h>
#include <iparamb2.h>
#include <iparamm2.h>

// 插件类 ID - 必须唯一
#define PYRAMID_CLASS_ID Class_ID(0x87654321, 0xFEDCBA98)

// 参数块 ID
enum { pyramid_params };

// 参数 ID
enum {
    pb_base_size,
    pb_height,
    pb_segments
};

/**
 * 金字塔几何体类
 */
class PyramidObject : public SimpleObject2 {
public:
    PyramidObject();
    virtual ~PyramidObject();

    // SimpleObject2 接口
    void BuildMesh(TimeValue t) override;
    BOOL OKtoDisplay(TimeValue t) override { return TRUE; }
    void InvalidateUI() override;
    
    // Animatable 接口
    void BeginEditParams(IObjParam* ip, ULONG flags, Animatable* prev) override;
    void EndEditParams(IObjParam* ip, ULONG flags, Animatable* next) override;
    
    // BaseObject 接口
    const TCHAR* GetObjectName() override { return _T("Pyramid"); }
    void GetClassName(TSTR& s) override { s = _T("PyramidObject"); }
    
    // Object 接口
    CreateMouseCallBack* GetCreateMouseCallBack() override;
    
    // ReferenceTarget 接口
    RefTargetHandle Clone(RemapDir& remap) override;

    // Animatable 接口
    Class_ID ClassID() override { return PYRAMID_CLASS_ID; }
    SClass_ID SuperClassID() override { return GEOMOBJECT_CLASS_ID; }
    
    int NumParamBlocks() override { return 1; }
    IParamBlock2* GetParamBlock(int i) override { return pblock2; }
    IParamBlock2* GetParamBlockByID(BlockID id) override { return (id == pyramid_params) ? pblock2 : nullptr; }

private:
    void BuildPyramidMesh(float baseSize, float height, int segments);
};

/**
 * 类描述符
 */
class PyramidClassDesc : public ClassDesc2 {
public:
    int IsPublic() override { return TRUE; }
    void* Create(BOOL loading = FALSE) override { return new PyramidObject(); }
    const TCHAR* ClassName() override { return _T("Pyramid"); }
    SClass_ID SuperClassID() override { return GEOMOBJECT_CLASS_ID; }
    Class_ID ClassID() override { return PYRAMID_CLASS_ID; }
    const TCHAR* Category() override { return _T("Custom Geometry"); }
    const TCHAR* InternalName() override { return _T("Pyramid"); }
    HINSTANCE HInstance() override { return hInstance; }
};

// 全局实例
static PyramidClassDesc pyramidClassDesc;
extern HINSTANCE hInstance;

/**
 * 参数块描述
 */
static ParamBlockDesc2 pyramid_param_blk(
    pyramid_params, _T("params"), 0, &pyramidClassDesc, 
    P_AUTO_CONSTRUCT + P_AUTO_UI,
    0,  // 引用编号
    
    // UI 描述
    IDD_PYRAMID_PANEL, IDS_PARAMS, 0, 0, nullptr,
    
    // 参数：底边尺寸
    pb_base_size, _T("baseSize"), TYPE_FLOAT, P_ANIMATABLE, IDS_BASE_SIZE,
        p_default, 50.0f,
        p_range, 0.001f, 10000.0f,
        p_ui, TYPE_SPINNER, EDITTYPE_FLOAT, IDC_BASE_EDIT, IDC_BASE_SPIN, 1.0f,
        p_end,
    
    // 参数：高度
    pb_height, _T("height"), TYPE_FLOAT, P_ANIMATABLE, IDS_HEIGHT,
        p_default, 100.0f,
        p_range, 0.001f, 10000.0f,
        p_ui, TYPE_SPINNER, EDITTYPE_FLOAT, IDC_HEIGHT_EDIT, IDC_HEIGHT_SPIN, 1.0f,
        p_end,
    
    // 参数：分段数
    pb_segments, _T("segments"), TYPE_INT, 0, IDS_SEGMENTS,
        p_default, 1,
        p_range, 1, 100,
        p_ui, TYPE_SPINNER, EDITTYPE_INT, IDC_SEGS_EDIT, IDC_SEGS_SPIN, 1,
        p_end,
    
    p_end
);

//================================================
// 创建鼠标回调
//================================================

class PyramidCreateCallBack : public CreateMouseCallBack {
public:
    PyramidObject* obj;
    Point3 p0, p1;
    IPoint2 sp0;
    
    int proc(ViewExp* vpt, int msg, int point, int flags, IPoint2 m, Matrix3& mat) override;
};

int PyramidCreateCallBack::proc(ViewExp* vpt, int msg, int point, int flags, IPoint2 m, Matrix3& mat) {
    if (!vpt || !vpt->IsAlive()) {
        DbgAssert(!_T("Invalid viewport"));
        return CREATE_ABORT;
    }

    switch (msg) {
        case MOUSE_POINT:
            switch (point) {
                case 0:
                    sp0 = m;
                    p0 = vpt->SnapPoint(m, m, nullptr, SNAP_IN_3D);
                    mat.SetTrans(p0);
                    break;
                case 1:
                    p1 = vpt->SnapPoint(m, m, nullptr, SNAP_IN_3D);
                    {
                        float dist = Length(p1 - p0);
                        obj->pblock2->SetValue(pb_base_size, 0, dist);
                        obj->pblock2->SetValue(pb_height, 0, dist * 2.0f);
                    }
                    break;
                case 2:
                    return CREATE_STOP;
            }
            break;
            
        case MOUSE_MOVE:
            switch (point) {
                case 1:
                    p1 = vpt->SnapPoint(m, m, nullptr, SNAP_IN_3D);
                    {
                        float dist = Length(p1 - p0);
                        obj->pblock2->SetValue(pb_base_size, 0, dist);
                        obj->pblock2->SetValue(pb_height, 0, dist * 2.0f);
                    }
                    break;
            }
            break;
            
        case MOUSE_ABORT:
            return CREATE_ABORT;
    }
    
    return CREATE_CONTINUE;
}

static PyramidCreateCallBack pyramidCreateCB;

//================================================
// PyramidObject 实现
//================================================

PyramidObject::PyramidObject() {
    pyramidClassDesc.MakeAutoParamBlocks(this);
}

PyramidObject::~PyramidObject() {
}

CreateMouseCallBack* PyramidObject::GetCreateMouseCallBack() {
    pyramidCreateCB.obj = this;
    return &pyramidCreateCB;
}

void PyramidObject::BeginEditParams(IObjParam* ip, ULONG flags, Animatable* prev) {
    SimpleObject2::BeginEditParams(ip, flags, prev);
    pyramidClassDesc.BeginEditParams(ip, this, flags, prev);
}

void PyramidObject::EndEditParams(IObjParam* ip, ULONG flags, Animatable* next) {
    SimpleObject2::EndEditParams(ip, flags, next);
    pyramidClassDesc.EndEditParams(ip, this, flags, next);
}

void PyramidObject::InvalidateUI() {
    pyramid_param_blk.InvalidateUI();
}

RefTargetHandle PyramidObject::Clone(RemapDir& remap) {
    PyramidObject* newObj = new PyramidObject();
    newObj->ReplaceReference(0, remap.CloneRef(pblock2));
    BaseClone(this, newObj, remap);
    return newObj;
}

void PyramidObject::BuildMesh(TimeValue t) {
    float baseSize, height;
    int segments;
    
    pblock2->GetValue(pb_base_size, t, baseSize, FOREVER);
    pblock2->GetValue(pb_height, t, height, FOREVER);
    pblock2->GetValue(pb_segments, t, segments, FOREVER);
    
    BuildPyramidMesh(baseSize, height, segments);
}

void PyramidObject::BuildPyramidMesh(float baseSize, float height, int segments) {
    // 网格常量定义
    const DWORD SMOOTH_GROUP_SIDES = 1;    // 侧面平滑组
    const DWORD SMOOTH_GROUP_BOTTOM = 2;   // 底面平滑组
    const int EDGE_VISIBLE = 1;            // 边可见
    const int EDGE_INVISIBLE = 0;          // 边不可见
    
    // 简单金字塔：5个顶点，4个侧面 + 1个底面
    int numVerts = 5;
    int numFaces = 6;  // 4个三角形侧面 + 2个三角形底面
    
    mesh.setNumVerts(numVerts);
    mesh.setNumFaces(numFaces);
    
    float halfSize = baseSize / 2.0f;
    
    // 设置顶点
    // 底面四个角
    mesh.setVert(0, Point3(-halfSize, -halfSize, 0));
    mesh.setVert(1, Point3(halfSize, -halfSize, 0));
    mesh.setVert(2, Point3(halfSize, halfSize, 0));
    mesh.setVert(3, Point3(-halfSize, halfSize, 0));
    // 顶点
    mesh.setVert(4, Point3(0, 0, height));
    
    // 设置侧面（4个三角形）
    mesh.faces[0].setVerts(0, 1, 4);
    mesh.faces[0].setSmGroup(SMOOTH_GROUP_SIDES);
    mesh.faces[0].setEdgeVisFlags(EDGE_VISIBLE, EDGE_VISIBLE, EDGE_INVISIBLE);
    
    mesh.faces[1].setVerts(1, 2, 4);
    mesh.faces[1].setSmGroup(SMOOTH_GROUP_SIDES);
    mesh.faces[1].setEdgeVisFlags(EDGE_VISIBLE, EDGE_VISIBLE, EDGE_INVISIBLE);
    
    mesh.faces[2].setVerts(2, 3, 4);
    mesh.faces[2].setSmGroup(SMOOTH_GROUP_SIDES);
    mesh.faces[2].setEdgeVisFlags(EDGE_VISIBLE, EDGE_VISIBLE, EDGE_INVISIBLE);
    
    mesh.faces[3].setVerts(3, 0, 4);
    mesh.faces[3].setSmGroup(SMOOTH_GROUP_SIDES);
    mesh.faces[3].setEdgeVisFlags(EDGE_VISIBLE, EDGE_VISIBLE, EDGE_INVISIBLE);
    
    // 设置底面（2个三角形）
    mesh.faces[4].setVerts(0, 3, 1);
    mesh.faces[4].setSmGroup(SMOOTH_GROUP_BOTTOM);
    mesh.faces[4].setEdgeVisFlags(EDGE_VISIBLE, EDGE_INVISIBLE, EDGE_VISIBLE);
    
    mesh.faces[5].setVerts(1, 3, 2);
    mesh.faces[5].setSmGroup(SMOOTH_GROUP_BOTTOM);
    mesh.faces[5].setEdgeVisFlags(EDGE_INVISIBLE, EDGE_VISIBLE, EDGE_VISIBLE);
    
    // 更新缓存
    mesh.InvalidateGeomCache();
    mesh.buildNormals();
}

//================================================
// 资源定义 (resource.h)
//================================================
/*
#define IDD_PYRAMID_PANEL       101
#define IDS_PARAMS              102
#define IDS_BASE_SIZE           103
#define IDS_HEIGHT              104
#define IDS_SEGMENTS            105
#define IDC_BASE_EDIT           1001
#define IDC_BASE_SPIN           1002
#define IDC_HEIGHT_EDIT         1003
#define IDC_HEIGHT_SPIN         1004
#define IDC_SEGS_EDIT           1005
#define IDC_SEGS_SPIN           1006
*/

//================================================
// 资源文件 (PyramidObject.rc)
//================================================
/*
STRINGTABLE
BEGIN
    IDS_PARAMS      "Parameters"
    IDS_BASE_SIZE   "Base Size"
    IDS_HEIGHT      "Height"
    IDS_SEGMENTS    "Segments"
END

IDD_PYRAMID_PANEL DIALOGEX 0, 0, 108, 80
STYLE DS_SETFONT | WS_CHILD | WS_VISIBLE
FONT 8, "Microsoft Sans Serif"
BEGIN
    LTEXT "Base Size:", -1, 4, 8, 40, 10
    EDITTEXT IDC_BASE_EDIT, 44, 6, 40, 12, ES_AUTOHSCROLL
    CONTROL "", IDC_BASE_SPIN, "SpinnerControl", WS_TABSTOP, 86, 6, 7, 10
    
    LTEXT "Height:", -1, 4, 24, 40, 10
    EDITTEXT IDC_HEIGHT_EDIT, 44, 22, 40, 12, ES_AUTOHSCROLL
    CONTROL "", IDC_HEIGHT_SPIN, "SpinnerControl", WS_TABSTOP, 86, 22, 7, 10
    
    LTEXT "Segments:", -1, 4, 40, 40, 10
    EDITTEXT IDC_SEGS_EDIT, 44, 38, 40, 12, ES_AUTOHSCROLL
    CONTROL "", IDC_SEGS_SPIN, "SpinnerControl", WS_TABSTOP, 86, 38, 7, 10
END
*/
