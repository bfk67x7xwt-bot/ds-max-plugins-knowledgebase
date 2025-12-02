#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3ds Max Plugin Online Verification Script
在线验证3ds Max插件的自动化脚本

This script automates the verification of 3ds Max plugins according to
the verification specification.

Usage:
    python verify_plugin.py <plugin_directory>
    python verify_plugin.py --help
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class PluginVerifier:
    """3ds Max插件验证器"""
    
    def __init__(self, plugin_dir: str):
        self.plugin_dir = Path(plugin_dir)
        self.results = {
            'plugin_name': '',
            'version': '',
            'timestamp': datetime.now().isoformat(),
            'levels': {
                'level1': {'name': 'Basic Verification', 'checks': [], 'score': 0},
                'level2': {'name': 'Functional Verification', 'checks': [], 'score': 0},
                'level3': {'name': 'Compatibility Verification', 'checks': [], 'score': 0},
                'level4': {'name': 'Performance Verification', 'checks': [], 'score': 0},
            },
            'overall_score': 0,
            'rating': '',
            'issues': [],
            'recommendations': []
        }
        
    def verify(self) -> Dict:
        """执行完整验证流程"""
        print(f"🔍 开始验证插件: {self.plugin_dir}")
        print("=" * 60)
        
        if not self.plugin_dir.exists():
            print(f"❌ 错误: 目录不存在: {self.plugin_dir}")
            sys.exit(1)
            
        # Level 1: 基础验证
        print("\n📋 Level 1: 基础验证 (Basic Verification)")
        self._verify_level1()
        
        # Level 2: 功能验证
        print("\n⚙️  Level 2: 功能验证 (Functional Verification)")
        self._verify_level2()
        
        # Level 3: 兼容性验证
        print("\n🔌 Level 3: 兼容性验证 (Compatibility Verification)")
        self._verify_level3()
        
        # Level 4: 性能验证
        print("\n⚡ Level 4: 性能验证 (Performance Verification)")
        self._verify_level4()
        
        # 计算总分和评级
        self._calculate_overall_score()
        
        # 生成报告
        self._print_report()
        
        return self.results
    
    def _verify_level1(self):
        """Level 1: 基础验证"""
        checks = []
        
        # 检查主插件文件
        plugin_files = list(self.plugin_dir.glob('*.ms')) + \
                      list(self.plugin_dir.glob('*.mse')) + \
                      list(self.plugin_dir.glob('*.dlu')) + \
                      list(self.plugin_dir.glob('*.dlx')) + \
                      list(self.plugin_dir.glob('*.dlo'))
        
        checks.append({
            'name': '主插件文件存在',
            'passed': len(plugin_files) > 0,
            'details': f"找到 {len(plugin_files)} 个插件文件"
        })
        
        # 检查README.md
        readme_exists = (self.plugin_dir / 'README.md').exists()
        checks.append({
            'name': 'README.md 存在',
            'passed': readme_exists,
            'details': 'README.md 文件' + ('已找到' if readme_exists else '未找到')
        })
        
        # 检查LICENSE
        license_exists = (self.plugin_dir / 'LICENSE').exists() or \
                        (self.plugin_dir / 'LICENSE.txt').exists() or \
                        (self.plugin_dir / 'LICENSE.md').exists()
        checks.append({
            'name': 'LICENSE 文件存在',
            'passed': license_exists,
            'details': 'LICENSE 文件' + ('已找到' if license_exists else '未找到')
        })
        
        # 检查README内容
        if readme_exists:
            readme_checks = self._check_readme_content()
            checks.extend(readme_checks)
        
        # 检查代码文件头部
        if plugin_files:
            header_checks = self._check_file_headers(plugin_files)
            checks.extend(header_checks)
        
        self.results['levels']['level1']['checks'] = checks
        self.results['levels']['level1']['score'] = self._calculate_score(checks)
        
        for check in checks:
            status = "✅" if check['passed'] else "❌"
            print(f"  {status} {check['name']}: {check['details']}")
    
    def _verify_level2(self):
        """Level 2: 功能验证"""
        checks = []
        
        # 检查错误处理
        plugin_files = list(self.plugin_dir.glob('*.ms')) + \
                      list(self.plugin_dir.glob('*.mse'))
        
        if plugin_files:
            error_handling = self._check_error_handling(plugin_files)
            checks.append(error_handling)
            
            # 检查日志功能
            logging_check = self._check_logging(plugin_files)
            checks.append(logging_check)
            
            # 检查函数命名
            naming_check = self._check_naming_conventions(plugin_files)
            checks.append(naming_check)
        
        self.results['levels']['level2']['checks'] = checks
        self.results['levels']['level2']['score'] = self._calculate_score(checks)
        
        for check in checks:
            status = "✅" if check['passed'] else "⚠️"
            print(f"  {status} {check['name']}: {check['details']}")
    
    def _verify_level3(self):
        """Level 3: 兼容性验证"""
        checks = []
        
        # 检查版本兼容性声明
        readme_path = self.plugin_dir / 'README.md'
        if readme_path.exists():
            content = readme_path.read_text(encoding='utf-8', errors='ignore')
            
            # 检查3ds Max版本声明
            version_declared = bool(re.search(r'3ds\s*Max\s*\d{4}', content, re.IGNORECASE))
            checks.append({
                'name': '3ds Max版本兼容性已声明',
                'passed': version_declared,
                'details': '在README中' + ('找到' if version_declared else '未找到') + '版本信息'
            })
            
            # 检查系统要求
            system_req = bool(re.search(r'(系统要求|system\s+requirements?|windows)', content, re.IGNORECASE))
            checks.append({
                'name': '系统要求已声明',
                'passed': system_req,
                'details': '在README中' + ('找到' if system_req else '未找到') + '系统要求'
            })
        
        # 检查依赖项文档
        deps_file = (self.plugin_dir / 'requirements.txt').exists() or \
                   (self.plugin_dir / 'dependencies.txt').exists()
        checks.append({
            'name': '依赖项已文档化',
            'passed': deps_file,
            'details': '依赖项文件' + ('已找到' if deps_file else '未找到（可选）')
        })
        
        self.results['levels']['level3']['checks'] = checks
        self.results['levels']['level3']['score'] = self._calculate_score(checks)
        
        for check in checks:
            status = "✅" if check['passed'] else "⚠️"
            print(f"  {status} {check['name']}: {check['details']}")
    
    def _verify_level4(self):
        """Level 4: 性能验证"""
        checks = []
        
        # 检查文件大小
        plugin_files = list(self.plugin_dir.glob('*.ms')) + \
                      list(self.plugin_dir.glob('*.mse')) + \
                      list(self.plugin_dir.glob('*.dlu')) + \
                      list(self.plugin_dir.glob('*.dlx')) + \
                      list(self.plugin_dir.glob('*.dlo'))
        
        if plugin_files:
            total_size = sum(f.stat().st_size for f in plugin_files)
            size_mb = total_size / (1024 * 1024)
            size_ok = size_mb < 50  # 假设合理大小为50MB以下
            
            checks.append({
                'name': '插件文件大小合理',
                'passed': size_ok,
                'details': f'总大小: {size_mb:.2f} MB'
            })
            
            # 检查是否有性能优化标识
            performance_aware = False
            for pf in plugin_files[:5]:  # 检查前5个文件
                if pf.suffix in ['.ms', '.mse']:
                    content = pf.read_text(encoding='utf-8', errors='ignore')
                    if re.search(r'(performance|optimize|efficient|cache)', content, re.IGNORECASE):
                        performance_aware = True
                        break
            
            checks.append({
                'name': '包含性能优化代码',
                'passed': performance_aware,
                'details': '代码中' + ('发现' if performance_aware else '未发现') + '性能优化相关内容'
            })
        
        self.results['levels']['level4']['checks'] = checks
        self.results['levels']['level4']['score'] = self._calculate_score(checks)
        
        for check in checks:
            status = "✅" if check['passed'] else "⚠️"
            print(f"  {status} {check['name']}: {check['details']}")
    
    def _check_readme_content(self) -> List[Dict]:
        """检查README内容完整性"""
        checks = []
        readme_path = self.plugin_dir / 'README.md'
        content = readme_path.read_text(encoding='utf-8', errors='ignore')
        
        # 提取插件名称和版本
        name_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if name_match:
            self.results['plugin_name'] = name_match.group(1).strip()
        
        version_match = re.search(r'(version|版本)[\s:：]+(\d+\.\d+\.\d+)', content, re.IGNORECASE)
        if version_match:
            self.results['version'] = version_match.group(2)
        
        # 检查各个必需部分
        required_sections = [
            ('安装说明', r'(install|安装)', 'Installation instructions'),
            ('使用示例', r'(usage|example|使用|示例)', 'Usage examples'),
            ('作者信息', r'(author|作者|developer|开发)', 'Author information'),
        ]
        
        for name, pattern, eng_name in required_sections:
            found = bool(re.search(pattern, content, re.IGNORECASE))
            checks.append({
                'name': f'README包含{name}',
                'passed': found,
                'details': f'{eng_name} ' + ('found' if found else 'not found')
            })
        
        return checks
    
    def _check_file_headers(self, files: List[Path]) -> List[Dict]:
        """检查文件头部注释"""
        checks = []
        
        for pfile in files[:3]:  # 检查前3个文件
            if pfile.suffix not in ['.ms', '.mse']:
                continue
                
            try:
                content = pfile.read_text(encoding='utf-8', errors='ignore')
                first_100_lines = '\n'.join(content.split('\n')[:100])
                
                has_header = bool(re.search(r'(Plugin\s+Name|Author|Version|Description)', 
                                           first_100_lines, re.IGNORECASE))
                
                checks.append({
                    'name': f'文件头部注释完整 ({pfile.name})',
                    'passed': has_header,
                    'details': '包含必要的元信息' if has_header else '缺少插件元信息'
                })
                break  # 只检查第一个有效文件
            except Exception as e:
                continue
        
        return checks
    
    def _check_error_handling(self, files: List[Path]) -> Dict:
        """检查错误处理机制"""
        has_error_handling = False
        
        for pfile in files[:5]:
            try:
                content = pfile.read_text(encoding='utf-8', errors='ignore')
                if re.search(r'(try|catch|error|exception)', content, re.IGNORECASE):
                    has_error_handling = True
                    break
            except:
                continue
        
        return {
            'name': '包含错误处理机制',
            'passed': has_error_handling,
            'details': '代码中' + ('发现' if has_error_handling else '未发现') + 'try-catch或错误处理'
        }
    
    def _check_logging(self, files: List[Path]) -> Dict:
        """检查日志功能"""
        has_logging = False
        
        for pfile in files[:5]:
            try:
                content = pfile.read_text(encoding='utf-8', errors='ignore')
                if re.search(r'(log|print|format|messageBox)', content, re.IGNORECASE):
                    has_logging = True
                    break
            except:
                continue
        
        return {
            'name': '包含日志记录功能',
            'passed': has_logging,
            'details': '代码中' + ('发现' if has_logging else '未发现') + '日志或输出语句'
        }
    
    def _check_naming_conventions(self, files: List[Path]) -> Dict:
        """检查命名规范"""
        good_naming = True
        
        for pfile in files[:3]:
            try:
                content = pfile.read_text(encoding='utf-8', errors='ignore')
                # 检查是否有单字母变量（除了i, j, k这类循环变量）
                bad_vars = re.findall(r'\b([a-hln-z])\s*=', content, re.IGNORECASE)
                if len(bad_vars) > 5:
                    good_naming = False
                    break
            except:
                continue
        
        return {
            'name': '遵循命名规范',
            'passed': good_naming,
            'details': '变量命名' + ('符合' if good_naming else '需要改进') + '最佳实践'
        }
    
    def _calculate_score(self, checks: List[Dict]) -> float:
        """计算检查项得分"""
        if not checks:
            return 0.0
        passed = sum(1 for c in checks if c['passed'])
        return (passed / len(checks)) * 100
    
    def _calculate_overall_score(self):
        """计算总体得分和评级"""
        scores = []
        weights = {'level1': 0.35, 'level2': 0.30, 'level3': 0.20, 'level4': 0.15}
        
        for level, weight in weights.items():
            score = self.results['levels'][level]['score']
            scores.append(score * weight)
        
        self.results['overall_score'] = sum(scores)
        
        # 确定评级
        score = self.results['overall_score']
        level1_score = self.results['levels']['level1']['score']
        level2_score = self.results['levels']['level2']['score']
        
        if score >= 95 and level1_score == 100 and level2_score >= 90:
            self.results['rating'] = '优秀 (Excellent)'
        elif score >= 85 and level1_score >= 90 and level2_score >= 80:
            self.results['rating'] = '良好 (Good)'
        elif score >= 70 and level1_score >= 80:
            self.results['rating'] = '合格 (Pass)'
        else:
            self.results['rating'] = '不合格 (Fail)'
        
        # 生成建议
        self._generate_recommendations()
    
    def _generate_recommendations(self):
        """生成改进建议"""
        recommendations = []
        
        for level_key, level_data in self.results['levels'].items():
            if level_data['score'] < 80:
                failed_checks = [c['name'] for c in level_data['checks'] if not c['passed']]
                if failed_checks:
                    recommendations.append(f"{level_data['name']}: 需要改进 - {', '.join(failed_checks[:3])}")
        
        if not recommendations:
            recommendations.append("所有检查项表现良好！继续保持。")
        
        self.results['recommendations'] = recommendations
    
    def _print_report(self):
        """打印验证报告"""
        print("\n" + "=" * 60)
        print("📊 验证报告 (Verification Report)")
        print("=" * 60)
        
        if self.results['plugin_name']:
            print(f"插件名称: {self.results['plugin_name']}")
        if self.results['version']:
            print(f"版本: {self.results['version']}")
        
        print(f"\n总体得分: {self.results['overall_score']:.1f}/100")
        print(f"评级: {self.results['rating']}")
        
        print(f"\n各级别得分:")
        for level_key, level_data in self.results['levels'].items():
            print(f"  {level_data['name']}: {level_data['score']:.1f}%")
        
        print(f"\n改进建议:")
        for i, rec in enumerate(self.results['recommendations'], 1):
            print(f"  {i}. {rec}")
        
        print("\n" + "=" * 60)
    
    def save_report(self, output_file: str = 'verification-report.json'):
        """保存验证报告为JSON"""
        output_path = self.plugin_dir / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"\n📄 报告已保存到: {output_path}")


def main():
    """主函数"""
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        print("""
3ds Max插件在线验证工具
3ds Max Plugin Online Verification Tool

使用方法 (Usage):
    python verify_plugin.py <plugin_directory>
    python verify_plugin.py /path/to/your/plugin

示例 (Example):
    python verify_plugin.py ./my-plugin
    python verify_plugin.py C:\\Plugins\\MyAwesomePlugin

选项 (Options):
    --help, -h    显示此帮助信息
        """)
        sys.exit(0)
    
    plugin_dir = sys.argv[1]
    
    verifier = PluginVerifier(plugin_dir)
    results = verifier.verify()
    verifier.save_report()
    
    # 根据评级返回退出码
    if results['rating'] in ['优秀 (Excellent)', '良好 (Good)', '合格 (Pass)']:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
