"""
Gerenciador de arquivos e diretórios para o PEP Downloader Bot.
"""
import os
import shutil
from pathlib import Path
from typing import Optional
from .console_logger import ConsoleLogger


class FileManager:
    """Gerencia operações de arquivo e diretório."""
    
    def __init__(self, download_dir: str = "downloads", logger: Optional[ConsoleLogger] = None):
        self.download_dir = download_dir
        self.logger = logger or ConsoleLogger()
    
    def ensure_download_directory(self) -> None:
        """Cria diretório downloads se não existir."""
        try:
            Path(self.download_dir).mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Diretório garantido: {self.download_dir}")
        except Exception as e:
            self.logger.error(f"Erro ao criar diretório {self.download_dir}: {str(e)}")
            raise
    
    def get_download_path(self, filename: str) -> str:
        """Retorna caminho completo para download."""
        return os.path.join(self.download_dir, filename)
    
    def check_disk_space(self, required_mb: int = 100) -> bool:
        """
        Verifica se há espaço suficiente em disco.
        
        Args:
            required_mb: Espaço mínimo necessário em MB
            
        Returns:
            bool: True se há espaço suficiente
        """
        try:
            free_bytes = shutil.disk_usage(self.download_dir).free
            free_mb = free_bytes / (1024 * 1024)
            
            if free_mb < required_mb:
                self.logger.error(f"Espaço insuficiente. Disponível: {free_mb:.1f}MB, Necessário: {required_mb}MB")
                return False
            
            self.logger.debug(f"Espaço disponível: {free_mb:.1f}MB")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao verificar espaço em disco: {str(e)}")
            return False
    
    def file_exists(self, filename: str) -> bool:
        """Verifica se arquivo já existe no diretório de download."""
        filepath = self.get_download_path(filename)
        exists = os.path.exists(filepath)
        
        if exists:
            file_size = os.path.getsize(filepath)
            self.logger.info(f"Arquivo já existe: {filename} ({file_size / (1024*1024):.2f} MB)")
        
        return exists
    
    def get_file_size(self, filename: str) -> int:
        """Retorna tamanho do arquivo em bytes."""
        filepath = self.get_download_path(filename)
        try:
            return os.path.getsize(filepath)
        except OSError:
            return 0