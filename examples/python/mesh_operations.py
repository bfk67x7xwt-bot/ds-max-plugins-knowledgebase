"""
Python 示例：网格操作工具
========================================
描述：演示如何使用 Python 操作网格数据
适用于 3ds Max 2022+ (Python 3.9+)
"""

from pymxs import runtime as rt
from typing import List, Tuple, Optional
import math


class MeshOperations:
    """网格操作工具类"""
    
    @staticmethod
    def get_vertex_positions(node) -> List[Tuple[float, float, float]]:
        """
        获取网格顶点位置
        
        Args:
            node: 3ds Max 节点对象
            
        Returns:
            顶点位置列表 [(x, y, z), ...]
        """
        mesh = rt.snapshotAsMesh(node)
        vertices = []
        
        num_verts = rt.getNumVerts(mesh)
        for i in range(1, num_verts + 1):
            vert = rt.getVert(mesh, i)
            vertices.append((vert.x, vert.y, vert.z))
        
        rt.delete(mesh)
        return vertices
    
    @staticmethod
    def get_face_indices(node) -> List[Tuple[int, int, int]]:
        """
        获取网格面索引
        
        Args:
            node: 3ds Max 节点对象
            
        Returns:
            面索引列表 [(v1, v2, v3), ...]
        """
        mesh = rt.snapshotAsMesh(node)
        faces = []
        
        num_faces = rt.getNumFaces(mesh)
        for i in range(1, num_faces + 1):
            face = rt.getFace(mesh, i)
            # 注意：MaxScript 面的顶点索引从 1 开始，转换为从 0 开始 (vertex indices, not coordinates)
            faces.append((int(face.x) - 1, int(face.y) - 1, int(face.z) - 1))
        
        rt.delete(mesh)
        return faces
    
    @staticmethod
    def get_bounding_box(node) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        """
        获取对象边界框
        
        Args:
            node: 3ds Max 节点对象
            
        Returns:
            (min_point, max_point)
        """
        bbox = rt.nodeLocalBoundingBox(node)
        min_pt = bbox[0]
        max_pt = bbox[1]
        return (
            (min_pt.x, min_pt.y, min_pt.z),
            (max_pt.x, max_pt.y, max_pt.z)
        )
    
    @staticmethod
    def calculate_surface_area(node) -> float:
        """
        计算网格表面积
        
        Args:
            node: 3ds Max 节点对象
            
        Returns:
            表面积
        """
        mesh = rt.snapshotAsMesh(node)
        total_area = 0.0
        
        num_faces = rt.getNumFaces(mesh)
        for i in range(1, num_faces + 1):
            area = rt.meshop.getFaceArea(mesh, i)
            total_area += area
        
        rt.delete(mesh)
        return total_area
    
    @staticmethod
    def calculate_volume(node) -> float:
        """
        计算网格体积（假设网格封闭）
        
        Args:
            node: 3ds Max 节点对象
            
        Returns:
            体积
        """
        vertices = MeshOperations.get_vertex_positions(node)
        faces = MeshOperations.get_face_indices(node)
        
        volume = 0.0
        for f in faces:
            v0 = vertices[f[0]]
            v1 = vertices[f[1]]
            v2 = vertices[f[2]]
            
            # 使用有符号体积公式
            volume += (
                v0[0] * (v1[1] * v2[2] - v2[1] * v1[2]) +
                v1[0] * (v2[1] * v0[2] - v0[1] * v2[2]) +
                v2[0] * (v0[1] * v1[2] - v1[1] * v0[2])
            ) / 6.0
        
        return abs(volume)
    
    @staticmethod
    def center_pivot(node):
        """
        将枢轴点移动到对象中心
        
        Args:
            node: 3ds Max 节点对象
        """
        rt.CenterPivot(node)
    
    @staticmethod
    def reset_transform(node):
        """
        重置对象变换
        
        Args:
            node: 3ds Max 节点对象
        """
        rt.ResetXForm(node)
        rt.collapseStack(node)


class MeshModifier:
    """网格修改工具类"""
    
    @staticmethod
    def noise_deform(node, strength: float = 10.0, seed: int = 0):
        """
        添加噪波变形
        
        Args:
            node: 3ds Max 节点对象
            strength: 噪波强度
            seed: 随机种子
        """
        import random
        random.seed(seed)
        
        # 转换为可编辑网格
        if rt.classOf(node.baseObject) != rt.Editable_Mesh:
            rt.convertToMesh(node)
        
        mesh = node.mesh
        num_verts = rt.getNumVerts(mesh)
        
        for i in range(1, num_verts + 1):
            vert = rt.getVert(mesh, i)
            offset = rt.Point3(
                random.uniform(-strength, strength),
                random.uniform(-strength, strength),
                random.uniform(-strength, strength)
            )
            rt.setVert(mesh, i, vert + offset)
        
        rt.update(node)
    
    @staticmethod
    def smooth_mesh(node, iterations: int = 1):
        """
        平滑网格（拉普拉斯平滑）
        
        Args:
            node: 3ds Max 节点对象
            iterations: 迭代次数
        """
        # 添加 TurboSmooth 修改器
        smooth_mod = rt.TurboSmooth()
        smooth_mod.iterations = iterations
        rt.addModifier(node, smooth_mod)
    
    @staticmethod
    def subdivide_mesh(node, levels: int = 1):
        """
        细分网格
        
        Args:
            node: 3ds Max 节点对象
            levels: 细分级别
        """
        meshsmooth = rt.MeshSmooth()
        meshsmooth.subdivisionLevel = levels
        rt.addModifier(node, meshsmooth)
    
    @staticmethod
    def add_bend(node, angle: float = 90.0, axis: int = 2):
        """
        添加弯曲修改器
        
        Args:
            node: 3ds Max 节点对象
            angle: 弯曲角度
            axis: 弯曲轴 (0=X, 1=Y, 2=Z)
        """
        bend = rt.Bend()
        bend.angle = angle
        bend.BendAxis = axis
        rt.addModifier(node, bend)
    
    @staticmethod
    def add_twist(node, angle: float = 180.0, axis: int = 2):
        """
        添加扭曲修改器
        
        Args:
            node: 3ds Max 节点对象
            angle: 扭曲角度
            axis: 扭曲轴 (0=X, 1=Y, 2=Z)
        """
        twist = rt.Twist()
        twist.angle = angle
        twist.axis = axis
        rt.addModifier(node, twist)


class MeshAnalyzer:
    """网格分析工具类"""
    
    @staticmethod
    def analyze_mesh(node) -> dict:
        """
        分析网格属性
        
        Args:
            node: 3ds Max 节点对象
            
        Returns:
            包含网格信息的字典
        """
        mesh = rt.snapshotAsMesh(node)
        
        info = {
            'name': node.name,
            'vertex_count': rt.getNumVerts(mesh),
            'face_count': rt.getNumFaces(mesh),
            'edge_count': rt.meshop.getNumEdges(mesh),
            'surface_area': MeshOperations.calculate_surface_area(node),
            'bounding_box': MeshOperations.get_bounding_box(node)
        }
        
        # 计算边界框尺寸
        bbox = info['bounding_box']
        info['dimensions'] = (
            bbox[1][0] - bbox[0][0],
            bbox[1][1] - bbox[0][1],
            bbox[1][2] - bbox[0][2]
        )
        
        rt.delete(mesh)
        return info
    
    @staticmethod
    def find_isolated_vertices(node) -> List[int]:
        """
        查找孤立顶点
        
        Args:
            node: 3ds Max 节点对象
            
        Returns:
            孤立顶点索引列表
        """
        mesh = rt.snapshotAsMesh(node)
        isolated = []
        
        num_verts = rt.getNumVerts(mesh)
        for i in range(1, num_verts + 1):
            faces = rt.meshop.getPolysUsingVert(mesh, i)
            if len(faces) == 0:
                isolated.append(i)
        
        rt.delete(mesh)
        return isolated
    
    @staticmethod
    def check_manifold(node) -> bool:
        """
        检查网格是否为流形
        
        Args:
            node: 3ds Max 节点对象
            
        Returns:
            是否为流形
        """
        mesh = rt.snapshotAsMesh(node)
        
        # 检查每条边是否只被两个面共享
        num_edges = rt.meshop.getNumEdges(mesh)
        for i in range(1, num_edges + 1):
            faces = rt.meshop.getPolysUsingEdge(mesh, i)
            if len(faces) > 2:
                rt.delete(mesh)
                return False
        
        rt.delete(mesh)
        return True


def demo_mesh_operations():
    """演示网格操作"""
    # 创建测试对象
    box = rt.Box(length=100, width=100, height=100)
    rt.select(box)
    
    # 分析网格
    analyzer = MeshAnalyzer()
    info = analyzer.analyze_mesh(box)
    
    print("=== Mesh Analysis ===")
    for key, value in info.items():
        print(f"{key}: {value}")
    
    # 应用修改
    modifier = MeshModifier()
    modifier.add_bend(box, angle=45)
    
    print("\nBend modifier added.")
    
    return box


if __name__ == "__main__":
    demo_mesh_operations()
