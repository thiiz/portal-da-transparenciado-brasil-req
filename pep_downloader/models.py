"""
Modelos de dados para o PEP Downloader Bot.
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DownloadResult:
    """Resultado de uma operação de download."""
    success: bool
    filename: str
    file_path: str
    file_size: int
    download_time: float
    error_message: Optional[str] = None
    
    def __str__(self) -> str:
        if self.success:
            return f"Download bem-sucedido: {self.filename} ({self.file_size / (1024*1024):.2f} MB em {self.download_time:.1f}s)"
        else:
            return f"Download falhou: {self.filename} - {self.error_message}"


@dataclass
class ExtractionResult:
    """Resultado de uma operação de extração."""
    success: bool
    extracted_files: List[str]
    extraction_path: str
    error_message: Optional[str] = None
    
    def __str__(self) -> str:
        if self.success:
            return f"Extração bem-sucedida: {len(self.extracted_files)} arquivos em {self.extraction_path}"
        else:
            return f"Extração falhou: {self.error_message}"