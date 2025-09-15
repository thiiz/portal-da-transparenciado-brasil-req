"""
Sistema de logging para console do PEP Downloader Bot.
"""
from datetime import datetime


class ConsoleLogger:
    """Gerencia logs de console com diferentes níveis."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
    
    def _get_timestamp(self) -> str:
        """Retorna timestamp formatado."""
        return datetime.now().strftime('%H:%M:%S')
    
    def info(self, message: str) -> None:
        """Log de informações."""
        print(f"[{self._get_timestamp()}] INFO: {message}")
    
    def success(self, message: str) -> None:
        """Log de sucesso."""
        print(f"[{self._get_timestamp()}] [OK] SUCESSO: {message}")
    
    def error(self, message: str) -> None:
        """Log de erros."""
        print(f"[{self._get_timestamp()}] [ERROR] ERRO: {message}")
    
    def debug(self, message: str) -> None:
        """Log de debug (apenas em modo verbose)."""
        if self.verbose:
            print(f"[{self._get_timestamp()}] DEBUG: {message}")