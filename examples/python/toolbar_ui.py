"""
Python 示例：工具栏和 UI 开发
========================================
描述：演示如何使用 PySide2 创建自定义用户界面
适用于 3ds Max 2022+ (Python 3.9+)
"""

from PySide2 import QtWidgets, QtCore, QtGui
from pymxs import runtime as rt

# 获取 3ds Max 主窗口
# 注意：MaxPlus 在新版本中已弃用，使用 QApplication.activeWindow()
def get_max_main_window():
    """获取 3ds Max 主窗口，兼容不同版本"""
    try:
        # 尝试使用 MaxPlus（旧版本）
        import MaxPlus
        return MaxPlus.GetQMaxMainWindow()
    except ImportError:
        pass
    
    # 使用 QApplication.activeWindow()（新版本推荐）
    app = QtWidgets.QApplication.instance()
    if app:
        return app.activeWindow()
    return None

MAX_MAIN_WINDOW = get_max_main_window()


class ObjectCreatorDialog(QtWidgets.QDialog):
    """对象创建工具对话框"""
    
    def __init__(self, parent=MAX_MAIN_WINDOW):
        super().__init__(parent)
        self.setWindowTitle("Object Creator")
        self.setMinimumSize(350, 400)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Tool)
        
        self._setup_ui()
        self._connect_signals()
        self._update_object_count()
    
    def _setup_ui(self):
        """设置 UI 布局"""
        layout = QtWidgets.QVBoxLayout(self)
        
        # 对象类型选择
        type_group = QtWidgets.QGroupBox("Object Type")
        type_layout = QtWidgets.QVBoxLayout(type_group)
        
        self.type_combo = QtWidgets.QComboBox()
        self.type_combo.addItems(["Box", "Sphere", "Cylinder", "Plane", "Teapot"])
        type_layout.addWidget(self.type_combo)
        
        layout.addWidget(type_group)
        
        # 尺寸参数
        size_group = QtWidgets.QGroupBox("Size Parameters")
        size_layout = QtWidgets.QFormLayout(size_group)
        
        self.size_spin = QtWidgets.QDoubleSpinBox()
        self.size_spin.setRange(1, 10000)
        self.size_spin.setValue(50)
        size_layout.addRow("Size:", self.size_spin)
        
        self.segments_spin = QtWidgets.QSpinBox()
        self.segments_spin.setRange(1, 100)
        self.segments_spin.setValue(32)
        size_layout.addRow("Segments:", self.segments_spin)
        
        layout.addWidget(size_group)
        
        # 位置参数
        pos_group = QtWidgets.QGroupBox("Position")
        pos_layout = QtWidgets.QFormLayout(pos_group)
        
        self.pos_x = QtWidgets.QDoubleSpinBox()
        self.pos_x.setRange(-10000, 10000)
        pos_layout.addRow("X:", self.pos_x)
        
        self.pos_y = QtWidgets.QDoubleSpinBox()
        self.pos_y.setRange(-10000, 10000)
        pos_layout.addRow("Y:", self.pos_y)
        
        self.pos_z = QtWidgets.QDoubleSpinBox()
        self.pos_z.setRange(-10000, 10000)
        pos_layout.addRow("Z:", self.pos_z)
        
        layout.addWidget(pos_group)
        
        # 颜色选择
        color_group = QtWidgets.QGroupBox("Color")
        color_layout = QtWidgets.QHBoxLayout(color_group)
        
        self.color_btn = QtWidgets.QPushButton()
        self.color_btn.setStyleSheet("background-color: red")
        self.color_btn.setFixedHeight(30)
        self.selected_color = QtGui.QColor(255, 0, 0)
        color_layout.addWidget(self.color_btn)
        
        self.random_color_check = QtWidgets.QCheckBox("Random Color")
        color_layout.addWidget(self.random_color_check)
        
        layout.addWidget(color_group)
        
        # 操作按钮
        btn_layout = QtWidgets.QHBoxLayout()
        
        self.create_btn = QtWidgets.QPushButton("Create Object")
        self.create_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        btn_layout.addWidget(self.create_btn)
        
        self.delete_btn = QtWidgets.QPushButton("Delete Selected")
        self.delete_btn.setStyleSheet("background-color: #f44336; color: white;")
        btn_layout.addWidget(self.delete_btn)
        
        layout.addLayout(btn_layout)
        
        # 批量创建
        batch_group = QtWidgets.QGroupBox("Batch Create")
        batch_layout = QtWidgets.QHBoxLayout(batch_group)
        
        self.batch_count = QtWidgets.QSpinBox()
        self.batch_count.setRange(1, 100)
        self.batch_count.setValue(10)
        batch_layout.addWidget(QtWidgets.QLabel("Count:"))
        batch_layout.addWidget(self.batch_count)
        
        self.batch_btn = QtWidgets.QPushButton("Batch Create")
        batch_layout.addWidget(self.batch_btn)
        
        layout.addWidget(batch_group)
        
        # 状态栏
        self.status_label = QtWidgets.QLabel("Ready")
        self.status_label.setStyleSheet("color: gray;")
        layout.addWidget(self.status_label)
        
        # 对象计数
        self.count_label = QtWidgets.QLabel("Scene objects: 0")
        layout.addWidget(self.count_label)
    
    def _connect_signals(self):
        """连接信号槽"""
        self.create_btn.clicked.connect(self._create_object)
        self.delete_btn.clicked.connect(self._delete_selected)
        self.color_btn.clicked.connect(self._pick_color)
        self.batch_btn.clicked.connect(self._batch_create)
    
    def _pick_color(self):
        """选择颜色"""
        color = QtWidgets.QColorDialog.getColor(self.selected_color, self)
        if color.isValid():
            self.selected_color = color
            self.color_btn.setStyleSheet(f"background-color: {color.name()}")
    
    def _get_color(self):
        """获取当前颜色"""
        if self.random_color_check.isChecked():
            import random
            return rt.Color(random.randint(0, 255), 
                           random.randint(0, 255), 
                           random.randint(0, 255))
        return rt.Color(self.selected_color.red(),
                       self.selected_color.green(),
                       self.selected_color.blue())
    
    def _create_object(self):
        """创建对象"""
        obj_type = self.type_combo.currentText()
        size = self.size_spin.value()
        pos = rt.Point3(self.pos_x.value(), self.pos_y.value(), self.pos_z.value())
        
        try:
            if obj_type == "Box":
                obj = rt.Box(length=size, width=size, height=size)
            elif obj_type == "Sphere":
                obj = rt.Sphere(radius=size / 2, segs=self.segments_spin.value())
            elif obj_type == "Cylinder":
                obj = rt.Cylinder(radius=size / 2, height=size)
            elif obj_type == "Plane":
                obj = rt.Plane(length=size, width=size)
            elif obj_type == "Teapot":
                obj = rt.Teapot(radius=size / 2)
            else:
                obj = rt.Box(length=size, width=size, height=size)
            
            obj.pos = pos
            obj.wirecolor = self._get_color()
            rt.select(obj)
            
            self.status_label.setText(f"Created: {obj.name}")
            self._update_object_count()
            
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
    
    def _delete_selected(self):
        """删除选中对象"""
        try:
            selection_list = list(rt.selection)
        except (TypeError, ValueError):
            selection_list = []
        count = len(selection_list)
        if count > 0:
            rt.delete(rt.selection)
            self.status_label.setText(f"Deleted {count} objects")
            self._update_object_count()
        else:
            self.status_label.setText("No objects selected")
    
    def _batch_create(self):
        """批量创建对象"""
        import random
        
        count = self.batch_count.value()
        obj_type = self.type_combo.currentText()
        size = self.size_spin.value()
        
        # 禁用重绘以提高性能
        rt.disableSceneRedraw()
        
        try:
            for _ in range(count):
                pos = rt.Point3(
                    random.uniform(-200, 200),
                    random.uniform(-200, 200),
                    random.uniform(0, 100)
                )
                
                if obj_type == "Box":
                    obj = rt.Box(length=size, width=size, height=size)
                elif obj_type == "Sphere":
                    obj = rt.Sphere(radius=size / 2)
                else:
                    obj = rt.Box(length=size, width=size, height=size)
                
                obj.pos = pos
                obj.wirecolor = self._get_color()
            
            self.status_label.setText(f"Created {count} objects")
            
        finally:
            rt.enableSceneRedraw()
            rt.redrawViews()
            self._update_object_count()
    
    def _update_object_count(self):
        """更新对象计数"""
        count = len(list(rt.objects))
        self.count_label.setText(f"Scene objects: {count}")


class SceneAnalyzerDialog(QtWidgets.QDialog):
    """场景分析工具对话框"""
    
    def __init__(self, parent=MAX_MAIN_WINDOW):
        super().__init__(parent)
        self.setWindowTitle("Scene Analyzer")
        self.setMinimumSize(400, 500)
        
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        
        # 分析按钮
        self.analyze_btn = QtWidgets.QPushButton("Analyze Scene")
        layout.addWidget(self.analyze_btn)
        
        # 结果表格
        self.result_table = QtWidgets.QTableWidget()
        self.result_table.setColumnCount(2)
        self.result_table.setHorizontalHeaderLabels(["Object Type", "Count"])
        self.result_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.result_table)
        
        # 对象列表
        self.object_list = QtWidgets.QListWidget()
        layout.addWidget(self.object_list)
        
        # 选择按钮
        btn_layout = QtWidgets.QHBoxLayout()
        self.select_btn = QtWidgets.QPushButton("Select in Scene")
        btn_layout.addWidget(self.select_btn)
        layout.addLayout(btn_layout)
    
    def _connect_signals(self):
        self.analyze_btn.clicked.connect(self._analyze_scene)
        self.select_btn.clicked.connect(self._select_object)
        self.object_list.itemDoubleClicked.connect(self._select_object)
    
    def _analyze_scene(self):
        """分析场景"""
        # 统计对象类型
        type_count = {}
        self.object_list.clear()
        
        for obj in rt.objects:
            obj_class = str(rt.classOf(obj))
            type_count[obj_class] = type_count.get(obj_class, 0) + 1
            self.object_list.addItem(f"{obj.name} ({obj_class})")
        
        # 更新表格
        self.result_table.setRowCount(len(type_count))
        for i, (obj_type, count) in enumerate(sorted(type_count.items())):
            self.result_table.setItem(i, 0, QtWidgets.QTableWidgetItem(obj_type))
            self.result_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(count)))
    
    def _select_object(self):
        """在场景中选择对象"""
        current = self.object_list.currentItem()
        if current:
            name = current.text().split(" (")[0]
            obj = rt.getNodeByName(name)
            if obj:
                rt.select(obj)


def show_object_creator():
    """显示对象创建工具"""
    dialog = ObjectCreatorDialog()
    dialog.show()
    return dialog


def show_scene_analyzer():
    """显示场景分析工具"""
    dialog = SceneAnalyzerDialog()
    dialog.show()
    return dialog


# 如果直接运行此脚本
if __name__ == "__main__":
    dialog = show_object_creator()
