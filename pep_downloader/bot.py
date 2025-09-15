"""
Bot principal para download de arquivos PEP do Portal da Transparência.
"""
import os
import time
from typing import Optional
from .date_generator import DateGenerator
from .http_client import HTTPClient
from .file_manager import FileManager
from .zip_extractor import ZipExtractor
from .console_logger import ConsoleLogger
from .models import DownloadResult, ExtractionResult


class PEPDownloaderBot:
    """Bot principal que orquestra o download e extração de arquivos PEP."""
    
    BASE_URL = "https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/pep"
    
    def __init__(self, 
                 download_dir: str = "downloads",
                 extract_files: bool = False,
                 verbose: bool = False,
                 max_retries: int = 3):
        """
        Inicializa o bot com configurações.
        
        Args:
            download_dir: Diretório para salvar arquivos
            extract_files: Se deve extrair arquivos ZIP automaticamente
            verbose: Se deve exibir logs detalhados
            max_retries: Número máximo de tentativas de download
        """
        self.download_dir = download_dir
        self.extract_files = extract_files
        self.max_retries = max_retries
        
        # Inicializar componentes
        self.logger = ConsoleLogger(verbose=verbose)
        self.date_generator = DateGenerator()
        self.file_manager = FileManager(download_dir, self.logger)
        self.http_client = HTTPClient(self.logger, max_retries)
        self.zip_extractor = ZipExtractor(self.logger)
    
    def run(self) -> tuple[DownloadResult, Optional[ExtractionResult]]:
        """
        Executa o processo completo de download e extração opcional.
        
        Returns:
            tuple: (DownloadResult, ExtractionResult opcional)
        """
        self.logger.info("=== PEP Downloader Bot - Portal da Transparência ===")
        
        # Gerar nome do arquivo baseado na data atual
        filename = self.date_generator.get_current_month_filename()
        self.logger.info(f"Arquivo alvo: {filename}")
        
        # Preparar ambiente
        self.file_manager.ensure_download_directory()
        
        # Verificar espaço em disco
        if not self.file_manager.check_disk_space(100):
            error_msg = "Espaço insuficiente em disco"
            return DownloadResult(
                success=False,
                filename=filename,
                file_path="",
                file_size=0,
                download_time=0,
                error_message=error_msg
            ), None
        
        # Verificar se arquivo já existe
        if self.file_manager.file_exists(filename):
            self.logger.info("Arquivo já existe. Prosseguindo com extração se solicitada...")
            file_path = self.file_manager.get_download_path(filename)
            file_size = self.file_manager.get_file_size(filename)
            
            download_result = DownloadResult(
                success=True,
                filename=filename,
                file_path=file_path,
                file_size=file_size,
                download_time=0
            )
        else:
            # Realizar download
            download_result = self._download_file(filename)
        
        # Extração opcional
        extraction_result = None
        if download_result.success and self.extract_files:
            extraction_result = self._extract_file(download_result.file_path)
        
        # Resumo final
        self._print_summary(download_result, extraction_result)
        
        return download_result, extraction_result
    
    def _download_file(self, filename: str) -> DownloadResult:
        """Realiza o download do arquivo PEP."""
        url = f"{self.BASE_URL}/{filename}"
        file_path = self.file_manager.get_download_path(filename)
        
        self.logger.info(f"URL de download: {url}")
        
        start_time = time.time()
        success = self.http_client.download_file(url, file_path)
        download_time = time.time() - start_time
        
        if success:
            file_size = self.file_manager.get_file_size(filename)
            return DownloadResult(
                success=True,
                filename=filename,
                file_path=file_path,
                file_size=file_size,
                download_time=download_time
            )
        else:
            return DownloadResult(
                success=False,
                filename=filename,
                file_path=file_path,
                file_size=0,
                download_time=download_time,
                error_message="Falha no download após todas as tentativas"
            )
    
    def _extract_file(self, zip_path: str) -> ExtractionResult:
        """Extrai o arquivo ZIP baixado."""
        self.logger.info("Iniciando extração do arquivo ZIP...")
        
        # Listar conteúdo antes da extração
        contents = self.zip_extractor.list_zip_contents(zip_path)
        self.logger.info(f"Arquivos no ZIP: {contents}")
        
        # Extrair para o mesmo diretório do arquivo ZIP
        extract_to = os.path.dirname(zip_path)
        success = self.zip_extractor.extract_zip(zip_path, extract_to)
        
        if success:
            return ExtractionResult(
                success=True,
                extracted_files=contents,
                extraction_path=extract_to
            )
        else:
            return ExtractionResult(
                success=False,
                extracted_files=[],
                extraction_path=extract_to,
                error_message="Falha na extração do arquivo ZIP"
            )
    
    def _print_summary(self, download_result: DownloadResult, extraction_result: Optional[ExtractionResult]):
        """Imprime resumo final da operação."""
        self.logger.info("=== RESUMO DA OPERAÇÃO ===")
        
        if download_result.success:
            self.logger.success(f"Download: {download_result.filename} ({download_result.file_size / (1024*1024):.2f} MB)")
        else:
            self.logger.error(f"Download falhou: {download_result.error_message}")
        
        if extraction_result:
            if extraction_result.success:
                self.logger.success(f"Extração: {len(extraction_result.extracted_files)} arquivos extraídos")
            else:
                self.logger.error(f"Extração falhou: {extraction_result.error_message}")
        
        self.logger.info("=== FIM DA OPERAÇÃO ===")
    
    def check_available_files(self, months_back: int = 6) -> list[str]:
        """
        Verifica quais arquivos PEP estão disponíveis nos últimos meses.
        
        Args:
            months_back: Quantos meses para trás verificar
            
        Returns:
            list: Lista de arquivos disponíveis
        """
        available_files = []
        current_date = self.date_generator.get_brasilia_datetime()
        
        for i in range(months_back):
            # Calcular data do mês
            year = current_date.year
            month = current_date.month - i
            
            if month <= 0:
                month += 12
                year -= 1
            
            filename = f"{year:04d}{month:02d}_PEP.zip"
            url = f"{self.BASE_URL}/{filename}"
            
            # Verificar se arquivo existe
            try:
                response = self.http_client.session.head(url, timeout=10)
                if response.status_code == 200:
                    available_files.append(filename)
                    self.logger.info(f"✓ Disponível: {filename}")
                else:
                    self.logger.debug(f"✗ Não disponível: {filename} (Status: {response.status_code})")
            except Exception as e:
                self.logger.debug(f"✗ Erro ao verificar {filename}: {str(e)}")
        
        return available_files