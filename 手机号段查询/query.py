#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手机号归属地查询系统
功能：
1. 导入Excel文件到SQLite数据库
2. 根据手机号查询归属地信息
3. 根据城市查询区号和号段信息
4. 菜单驱动界面
"""

import sqlite3
import pandas as pd
import os
import sys
from typing import List, Tuple, Optional


class PhoneLocationSystem:
    def __init__(self, db_path: str = "phone_location.db"):
        """
        初始化手机号归属地查询系统
        
        Args:
            db_path: SQLite数据库文件路径
        """
        self.db_path = db_path
        self.conn = None
        self.init_database()
    
    def init_database(self):
        """初始化数据库连接和表结构"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS phone_location (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone_segment TEXT NOT NULL,
                    area_code TEXT,
                    province TEXT,
                    city TEXT,
                    UNIQUE(phone_segment)
                )
            ''')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_phone_segment ON phone_location(phone_segment)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_city ON phone_location(city)')
            self.conn.commit()
            print(f"数据库初始化成功: {self.db_path}")
        except sqlite3.Error as e:
            print(f"数据库初始化失败: {e}")
            sys.exit(1)
    
    def import_excel_to_db(self, excel_path: str) -> bool:
        """
        导入Excel文件到数据库
        
        Args:
            excel_path: Excel文件路径
            
        Returns:
            bool: 导入是否成功
        """
        if not os.path.exists(excel_path):
            print(f"错误: 文件不存在 - {excel_path}")
            return False
        
        try:
            # 读取Excel文件
            print("正在读取Excel文件...")
            df = pd.read_excel(excel_path)
            print(f"成功读取Excel文件，共 {len(df)} 行数据")
            
            # 显示文件信息
            print(f"Excel文件列名: {list(df.columns)}")
            print(f"前5行数据预览:")
            print(df.head())
            
            # 检查必要的列是否存在
            required_columns = ['手机前缀', '归属地区号', '省', '市']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                print(f"错误: Excel文件缺少必要的列: {missing_columns}")
                print(f"当前列名: {list(df.columns)}")
                print("请检查Excel文件的列名是否正确")
                return False
            
            # 清空现有数据
            self.conn.execute('DELETE FROM phone_location')
            
            # 插入数据
            print("正在导入数据到数据库...")
            insert_count = 0
            error_count = 0
            
            for index, row in df.iterrows():
                try:
                    # 处理手机前缀为整数
                    if pd.notna(row['手机前缀']):
                        phone_segment = str(int(float(row['手机前缀'])))
                    else:
                        phone_segment = ''
                    
                    # 处理归属地区号为整数
                    if pd.notna(row['归属地区号']):
                        area_code = str(int(float(row['归属地区号'])))
                    else:
                        area_code = ''
                    
                    # 处理省市为字符串
                    province = str(row['省']).strip() if pd.notna(row['省']) else ''
                    city = str(row['市']).strip() if pd.notna(row['市']) else ''
                    
                    # 跳过空的手机号段
                    if not phone_segment or phone_segment == 'nan':
                        print(f"跳过第 {index + 1} 行: 手机前缀为空")
                        continue
                    
                    # 显示前几条数据用于调试
                    if insert_count < 5:
                        print(f"插入数据 {insert_count + 1}: 前缀={phone_segment}, 区号={area_code}, 省={province}, 市={city}")
                    
                    self.conn.execute('''
                        INSERT OR REPLACE INTO phone_location 
                        (phone_segment, area_code, province, city) 
                        VALUES (?, ?, ?, ?)
                    ''', (phone_segment, area_code, province, city))
                    
                    insert_count += 1
                    
                    if insert_count % 1000 == 0:
                        print(f"已导入 {insert_count} 条记录...")
                        
                except Exception as e:
                    error_count += 1
                    if error_count <= 5:  # 只显示前5个错误
                        print(f"导入第 {index + 1} 行数据时出错: {e}")
                        print(f"行数据: {dict(row)}")
                    continue
            
            self.conn.commit()
            print(f"导入完成！共导入 {insert_count} 条记录")
            if error_count > 0:
                print(f"跳过 {error_count} 条错误记录")
            return True
            
        except Exception as e:
            print(f"导入Excel文件失败: {e}")
            return False
    
    def query_phone_location(self, phone_number: str) -> Optional[Tuple[str, str, str, str]]:
        """
        根据手机号查询归属地信息
        
        Args:
            phone_number: 手机号码
            
        Returns:
            tuple: (手机号段, 省份, 城市, 区号) 或 None
        """
        if len(phone_number) < 7:
            print("错误: 手机号码长度不足7位")
            return None
        
        # 取前7位作为查询条件
        phone_prefix = phone_number[:7]
        
        try:
            cursor = self.conn.execute('''
                SELECT phone_segment, province, city, area_code 
                FROM phone_location 
                WHERE phone_segment = ?
            ''', (phone_prefix,))
            
            result = cursor.fetchone()
            return result
            
        except sqlite3.Error as e:
            print(f"查询手机号归属地失败: {e}")
            return None
    
    def query_city_info(self, city_name: str, limit: int = 10) -> List[Tuple[str, str, str]]:
        """
        根据城市查询区号和手机号段信息
        
        Args:
            city_name: 城市名称
            limit: 返回的记录数限制
            
        Returns:
            list: [(手机号段, 区号, 省份), ...]
        """
        try:
            cursor = self.conn.execute('''
                SELECT phone_segment, area_code, province 
                FROM phone_location 
                WHERE city LIKE ? 
                LIMIT ?
            ''', (f'%{city_name}%', limit))
            
            results = cursor.fetchall()
            return results
            
        except sqlite3.Error as e:
            print(f"查询城市信息失败: {e}")
            return []
    
    def get_database_stats(self) -> dict:
        """获取数据库统计信息"""
        try:
            cursor = self.conn.execute('SELECT COUNT(*) FROM phone_location')
            total_records = cursor.fetchone()[0]
            
            cursor = self.conn.execute('SELECT COUNT(DISTINCT province) FROM phone_location')
            total_provinces = cursor.fetchone()[0]
            
            cursor = self.conn.execute('SELECT COUNT(DISTINCT city) FROM phone_location')
            total_cities = cursor.fetchone()[0]
            
            return {
                'total_records': total_records,
                'total_provinces': total_provinces,
                'total_cities': total_cities
            }
        except sqlite3.Error as e:
            print(f"获取统计信息失败: {e}")
            return {}
    
    def display_menu(self):
        """显示主菜单"""
        print("\n" + "="*50)
        print("         手机号归属地查询系统")
        print("="*50)
        print("1. 导入Excel文件到数据库")
        print("2. 查询手机号归属地")
        print("3. 查询城市对应的区号和号段")
        print("4. 查看数据库统计信息")
        print("5. 退出系统")
        print("="*50)
    
    def handle_import_excel(self):
        """处理Excel导入功能"""
        print("\n--- 导入Excel文件 ---")
        excel_path = input("请输入Excel文件路径: ").strip()
        
        if not excel_path:
            print("错误: 文件路径不能为空")
            return
        
        # 移除可能的引号
        excel_path = excel_path.strip('"\'')
        
        success = self.import_excel_to_db(excel_path)
        if success:
            stats = self.get_database_stats()
            print(f"导入成功！数据库现有 {stats.get('total_records', 0)} 条记录")
        else:
            print("导入失败，请检查文件路径和格式")
    
    def handle_query_phone(self):
        """处理手机号查询功能"""
        print("\n--- 查询手机号归属地 ---")
        phone_number = input("请输入手机号码: ").strip()
        
        if not phone_number:
            print("错误: 手机号码不能为空")
            return
        
        # 移除可能的非数字字符
        phone_number = ''.join(filter(str.isdigit, phone_number))
        
        if len(phone_number) < 7:
            print("错误: 手机号码格式不正确")
            return
        
        result = self.query_phone_location(phone_number)
        
        if result:
            phone_segment, province, city, area_code = result
            print(f"\n查询结果:")
            print(f"手机号码: {phone_number}")
            print(f"号段: {phone_segment}")
            print(f"省份: {province}")
            print(f"城市: {city}")
            print(f"区号: {area_code}")
        else:
            print(f"未找到手机号 {phone_number} 的归属地信息")
    
    def handle_query_city(self):
        """处理城市查询功能"""
        print("\n--- 查询城市对应的区号和号段 ---")
        city_name = input("请输入城市名称: ").strip()
        
        if not city_name:
            print("错误: 城市名称不能为空")
            return
        
        results = self.query_city_info(city_name, 10)
        
        if results:
            print(f"\n找到 {len(results)} 个相关号段:")
            print(f"{'序号':<4} {'手机号段':<12} {'区号':<8} {'省份':<10}")
            print("-" * 40)
            
            for i, (phone_segment, area_code, province) in enumerate(results, 1):
                print(f"{i:<4} {phone_segment:<12} {area_code:<8} {province:<10}")
        else:
            print(f"未找到城市 '{city_name}' 的相关信息")
    
    def handle_show_stats(self):
        """处理显示统计信息功能"""
        print("\n--- 数据库统计信息 ---")
        stats = self.get_database_stats()
        
        if stats:
            print(f"总记录数: {stats['total_records']}")
            print(f"省份数: {stats['total_provinces']}")
            print(f"城市数: {stats['total_cities']}")
        else:
            print("无法获取统计信息")
    
    def run(self):
        """运行主程序"""
        print("欢迎使用手机号归属地查询系统！")
        
        while True:
            try:
                self.display_menu()
                choice = input("请选择功能 (1-5): ").strip()
                
                if choice == '1':
                    self.handle_import_excel()
                elif choice == '2':
                    self.handle_query_phone()
                elif choice == '3':
                    self.handle_query_city()
                elif choice == '4':
                    self.handle_show_stats()
                elif choice == '5':
                    print("谢谢使用，再见！")
                    break
                else:
                    print("无效选择，请输入 1-5 之间的数字")
                
                input("\n按回车键继续...")
                
            except KeyboardInterrupt:
                print("\n\n程序被用户中断")
                break
            except Exception as e:
                print(f"程序运行出错: {e}")
                input("按回车键继续...")
    
    def __del__(self):
        """析构函数，关闭数据库连接"""
        if self.conn:
            self.conn.close()


def main():
    """主函数"""
    # 检查依赖包
    try:
        import pandas as pd
        import openpyxl  # pandas读取Excel需要这个包
    except ImportError as e:
        print("错误: 缺少必要的Python包")
        print("请运行以下命令安装依赖:")
        print("pip install pandas openpyxl")
        sys.exit(1)
    
    # 创建并运行系统
    system = PhoneLocationSystem()
    system.run()


if __name__ == "__main__":
    main()