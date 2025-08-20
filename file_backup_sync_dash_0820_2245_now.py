# 代码生成时间: 2025-08-20 22:45:05
import os
import shutil
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# 文件备份同步功能类
class FileBackupSync:
    def __init__(self, source_dir, backup_dir):
        """
        文件备份同步构造函数
        :param source_dir: 源目录路径
        :param backup_dir: 备份目录路径
        """
        self.source_dir = source_dir
        self.backup_dir = backup_dir
        self.backup_files = {}
        self.last_backup = None

    def backup_files(self):
        """
        备份文件
        """
        for item in os.listdir(self.source_dir):
            source_file_path = os.path.join(self.source_dir, item)
            backup_file_path = os.path.join(self.backup_dir, item)
            if os.path.isfile(source_file_path):
                try:
                    shutil.copy2(source_file_path, backup_file_path)
                    self.backup_files[item] = {'source': source_file_path, 'backup': backup_file_path}
                except Exception as e:
                    print(f"Error copying file {source_file_path} to {backup_file_path}: {e}")

    def sync_files(self):
        """
        同步文件
        "