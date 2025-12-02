/**
 * C++ SDK 示例：基础工具插件
 * ========================================
 * 描述：演示如何创建一个简单的工具类插件
 * 适用于 3ds Max 2020+
 */

#pragma once
#include <Max.h>
#include <istdplug.h>
#include <iparamb2.h>
#include <utilapi.h>
#include <maxscript/maxscript.h>
#include <random>  // 现代 C++ 随机数生成

// 插件类 ID - 必须唯一
#define UTILITY_PLUGIN_CLASS_ID Class_ID(0x12345678, 0xABCDEF00)

/**
 * 工具插件主类
 */
class UtilityPluginDemo : public UtilityObj {
public:
    UtilityPluginDemo();
    virtual ~UtilityPluginDemo();

    // UtilityObj 接口实现
    void BeginEditParams(Interface* ip, IUtil* iu) override;
    void EndEditParams(Interface* ip, IUtil* iu) override;
    void DeleteThis() override { delete this; }

    // 自定义方法
    void CountObjects();
    void SelectByType(Class_ID classId);
    void RandomizeColors();
    void AlignToGrid();

private:
    Interface* m_ip;
    IUtil* m_iu;
    HWND m_hPanel;

    static INT_PTR CALLBACK DlgProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
    void UpdateUI();
};

/**
 * 类描述符
 */
class UtilityPluginDemoClassDesc : public ClassDesc2 {
public:
    int IsPublic() override { return TRUE; }
    void* Create(BOOL loading = FALSE) override { return new UtilityPluginDemo(); }
    const TCHAR* ClassName() override { return _T("Utility Demo"); }
    SClass_ID SuperClassID() override { return UTILITY_CLASS_ID; }
    Class_ID ClassID() override { return UTILITY_PLUGIN_CLASS_ID; }
    const TCHAR* Category() override { return _T("Custom Utilities"); }
    const TCHAR* InternalName() override { return _T("UtilityDemo"); }
    HINSTANCE HInstance() override { return hInstance; }
};

// 全局实例
static UtilityPluginDemoClassDesc utilityPluginDesc;
extern HINSTANCE hInstance;

//================================================
// 实现文件 (UtilityPluginDemo.cpp)
//================================================

HINSTANCE hInstance = nullptr;

// DLL 入口点
BOOL WINAPI DllMain(HINSTANCE hinstDLL, ULONG fdwReason, LPVOID /*lpvReserved*/) {
    if (fdwReason == DLL_PROCESS_ATTACH) {
        hInstance = hinstDLL;
        DisableThreadLibraryCalls(hinstDLL);
    }
    return TRUE;
}

// 导出函数
extern "C" {
    __declspec(dllexport) const TCHAR* LibDescription() {
        return _T("Utility Plugin Demo");
    }

    __declspec(dllexport) int LibNumberClasses() {
        return 1;
    }

    __declspec(dllexport) ClassDesc* LibClassDesc(int i) {
        switch (i) {
            case 0: return &utilityPluginDesc;
            default: return nullptr;
        }
    }

    __declspec(dllexport) ULONG LibVersion() {
        return VERSION_3DSMAX;
    }
}

// 构造函数
UtilityPluginDemo::UtilityPluginDemo() 
    : m_ip(nullptr), m_iu(nullptr), m_hPanel(nullptr) {
}

// 析构函数
UtilityPluginDemo::~UtilityPluginDemo() {
}

// 开始编辑参数
void UtilityPluginDemo::BeginEditParams(Interface* ip, IUtil* iu) {
    m_ip = ip;
    m_iu = iu;
    
    // 创建 UI 面板
    m_hPanel = ip->AddRollupPage(
        hInstance,
        MAKEINTRESOURCE(IDD_UTILITY_PANEL),
        DlgProc,
        _T("Utility Demo"),
        reinterpret_cast<LPARAM>(this)
    );
    
    UpdateUI();
}

// 结束编辑参数
void UtilityPluginDemo::EndEditParams(Interface* ip, IUtil* iu) {
    if (m_hPanel) {
        ip->DeleteRollupPage(m_hPanel);
        m_hPanel = nullptr;
    }
    m_ip = nullptr;
    m_iu = nullptr;
}

// 对话框过程
INT_PTR CALLBACK UtilityPluginDemo::DlgProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    UtilityPluginDemo* plugin = reinterpret_cast<UtilityPluginDemo*>(
        GetWindowLongPtr(hWnd, GWLP_USERDATA)
    );

    switch (msg) {
        case WM_INITDIALOG:
            plugin = reinterpret_cast<UtilityPluginDemo*>(lParam);
            SetWindowLongPtr(hWnd, GWLP_USERDATA, lParam);
            return TRUE;

        case WM_COMMAND:
            switch (LOWORD(wParam)) {
                case IDC_BTN_COUNT:
                    plugin->CountObjects();
                    break;
                case IDC_BTN_SELECT_BOXES:
                    plugin->SelectByType(Class_ID(BOXOBJ_CLASS_ID, 0));
                    break;
                case IDC_BTN_RANDOMIZE:
                    plugin->RandomizeColors();
                    break;
                case IDC_BTN_ALIGN:
                    plugin->AlignToGrid();
                    break;
            }
            return TRUE;

        case WM_DESTROY:
            return TRUE;
    }
    return FALSE;
}

// 统计场景对象
void UtilityPluginDemo::CountObjects() {
    if (!m_ip) return;

    int count = 0;
    INode* root = m_ip->GetRootNode();
    
    // 递归统计
    std::function<void(INode*)> countNodes = [&](INode* node) {
        for (int i = 0; i < node->NumberOfChildren(); i++) {
            INode* child = node->GetChildNode(i);
            count++;
            countNodes(child);
        }
    };
    
    countNodes(root);

    TSTR msg;
    msg.printf(_T("Scene contains %d objects"), count);
    MaxMsgBox(m_ip->GetMAXHWnd(), msg, _T("Object Count"), MB_OK);
}

// 按类型选择对象
void UtilityPluginDemo::SelectByType(Class_ID classId) {
    if (!m_ip) return;

    Tab<INode*> nodes;
    INode* root = m_ip->GetRootNode();
    TimeValue t = m_ip->GetTime();

    std::function<void(INode*)> findNodes = [&](INode* node) {
        for (int i = 0; i < node->NumberOfChildren(); i++) {
            INode* child = node->GetChildNode(i);
            Object* obj = child->EvalWorldState(t).obj;
            if (obj && obj->ClassID() == classId) {
                nodes.Append(1, &child);
            }
            findNodes(child);
        }
    };

    findNodes(root);
    
    if (nodes.Count() > 0) {
        m_ip->ClearNodeSelection(FALSE);
        for (int i = 0; i < nodes.Count(); i++) {
            m_ip->SelectNode(nodes[i], TRUE);
        }
    }

    TSTR msg;
    msg.printf(_T("Selected %d objects"), nodes.Count());
    MaxMsgBox(m_ip->GetMAXHWnd(), msg, _T("Selection"), MB_OK);
}

// 随机化选中对象的颜色
void UtilityPluginDemo::RandomizeColors() {
    if (!m_ip) return;

    // 使用现代 C++ 随机数生成器
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 255);

    int count = m_ip->GetSelNodeCount();
    for (int i = 0; i < count; i++) {
        INode* node = m_ip->GetSelNode(i);
        DWORD color = RGB(dis(gen), dis(gen), dis(gen));
        node->SetWireColor(color);
    }

    m_ip->RedrawViews(m_ip->GetTime());
}

// 将选中对象对齐到网格
void UtilityPluginDemo::AlignToGrid() {
    if (!m_ip) return;

    TimeValue t = m_ip->GetTime();
    float gridSpacing = m_ip->GetGridSpacing();

    theHold.Begin();

    int count = m_ip->GetSelNodeCount();
    for (int i = 0; i < count; i++) {
        INode* node = m_ip->GetSelNode(i);
        Matrix3 tm = node->GetNodeTM(t);
        Point3 pos = tm.GetTrans();

        // 对齐到网格
        pos.x = floorf(pos.x / gridSpacing + 0.5f) * gridSpacing;
        pos.y = floorf(pos.y / gridSpacing + 0.5f) * gridSpacing;
        pos.z = floorf(pos.z / gridSpacing + 0.5f) * gridSpacing;

        tm.SetTrans(pos);
        node->SetNodeTM(t, tm);
    }

    theHold.Accept(_T("Align to Grid"));
    m_ip->RedrawViews(t);
}

// 更新 UI
void UtilityPluginDemo::UpdateUI() {
    if (!m_hPanel || !m_ip) return;

    int selCount = m_ip->GetSelNodeCount();
    TSTR text;
    text.printf(_T("Selected: %d"), selCount);
    SetDlgItemText(m_hPanel, IDC_STATIC_SELECTION, text);
}

//================================================
// 资源定义 (resource.h)
//================================================
/*
#define IDD_UTILITY_PANEL       101
#define IDC_BTN_COUNT           1001
#define IDC_BTN_SELECT_BOXES    1002
#define IDC_BTN_RANDOMIZE       1003
#define IDC_BTN_ALIGN           1004
#define IDC_STATIC_SELECTION    1005
*/

//================================================
// 资源文件 (UtilityPluginDemo.rc)
//================================================
/*
IDD_UTILITY_PANEL DIALOGEX 0, 0, 180, 120
STYLE DS_SETFONT | WS_CHILD | WS_VISIBLE
FONT 8, "Microsoft Sans Serif"
BEGIN
    PUSHBUTTON "Count Objects", IDC_BTN_COUNT, 10, 10, 160, 18
    PUSHBUTTON "Select All Boxes", IDC_BTN_SELECT_BOXES, 10, 32, 160, 18
    PUSHBUTTON "Randomize Colors", IDC_BTN_RANDOMIZE, 10, 54, 160, 18
    PUSHBUTTON "Align to Grid", IDC_BTN_ALIGN, 10, 76, 160, 18
    LTEXT "Selected: 0", IDC_STATIC_SELECTION, 10, 100, 160, 12
END
*/
