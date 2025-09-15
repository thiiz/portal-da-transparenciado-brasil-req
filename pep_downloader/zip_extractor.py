"""
Extrator de arquivos ZIP para o PEP Downloader Bot.
"""
import zipfile
import os
from pathlib import Path
from typing import List, Optional
from .console_logger import ConsoleLogger


class ZipExtractor:
    """Gerencia extração de arquivos ZIP com segurança."""
    
    def __init__(self, logger: Optional[ConsoleLogger] = None):
        self.logger = logger or ConsoleLogger()
    
    def extract_zip(self, zip_path: str, extract_to: str) -> bool:
        """
        Extrai arquivos .zip com tratamento de erros e proteção contra path traversal.
        
        Args:
            zip_path: Caminho para o arquivo ZIP
            extract_to: Diretório onde extrair os arquivos
            
        Returns:
            bool: True se extração foi bem-sucedida
        """
        try:
            if not os.path.exists(zip_path):
                self.logger.error(f"Arquivo ZIP não encontrado: {zip_path}")
                return False
            
            # Verificar se é um arquivo ZIP válido
            if not zipfile.is_zipfile(zip_path):
                self.logger.error(f"Arquivo não é um ZIP válido: {zip_path}")
                return False
            
            self.logger.info(f"Iniciando extração de: {zip_path}")
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Listar conteúdo do ZIP
                file_list = zip_ref.namelist()
                self.logger.info(f"Arquivos no ZIP: {len(file_list)}")
                
                for file_info in zip_ref.infolist():
                    # Proteção contra path traversal
                    if self._is_safe_path(file_info.filename, extract_to):
                        self.logger.debug(f"Extraindo: {file_info.filename}")
                        zip_ref.extract(file_info, extract_to)
                    else:
                        self.logger.error(f"Caminho inseguro ignorado: {file_info.filename}")
                
                extracted_files = [f for f in file_list if self._is_safe_path(f, extract_to)]
                self.logger.success(f"Extração concluída. {len(extracted_files)} arquivos extraídos em: {extract_to}")
                
                # Listar arquivos extraídos
                for filename in extracted_files:
                    full_path = os.path.join(extract_to, filename)
                    if os.path.exists(full_path):
                        size = os.path.getsize(full_path)
                        self.logger.info(f"  - {filename} ({size / (1024*1024):.2f} MB)")
                
                return True
                
        except zipfile.BadZipFile:
            self.logger.error(f"Arquivo ZIP corrompido: {zip_path}")
            return False
        except Exception as e:
            self.logger.error(f"Erro durante extração: {str(e)}")
            return False
    
    def list_zip_contents(self, zip_path: str) -> List[str]:
        """
        Lista conteúdo do arquivo .zip sem extrair.
        
        Args:
            zip_path: Caminho para o arquivo ZIP
            
        Returns:
            List[str]: Lista de nomes de arquivo no ZIP
        """
        try:
            if not zipfile.is_zipfile(zip_path):
                self.logger.error(f"Arquivo não é um ZIP válido: {zip_path}")
                return []
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                return zip_ref.namelist()
                
        except Exception as e:
            self.logger.error(f"Erro ao listar conteúdo do ZIP: {str(e)}")
            return []
    
    def _is_safe_path(self, filename: str, extract_to: str) -> bool:
        """
        Verifica se o caminho é seguro (proteção contra path traversal).
        
        Args:
            filename: Nome do arquivo no ZIP
            extract_to: Diretório de extração
            
        Returns:
            bool: True se o caminho é seguro
        """
        # Normalizar caminhos
        extract_to = os.path.abspath(extract_to)
        full_path = os.path.abspath(os.path.join(extract_to, filename))
        
        # Verificar se o caminho final está dentro do diretório de extração
        return full_path.startswith(extract_to)