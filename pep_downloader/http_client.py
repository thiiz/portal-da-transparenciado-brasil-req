"""
Cliente HTTP para download de arquivos PEP.
"""
import requests
import time
from typing import Optional
from .console_logger import ConsoleLogger


class HTTPClient:
    """Gerencia requisições HTTP com headers apropriados e retry logic."""
    
    def __init__(self, logger: Optional[ConsoleLogger] = None, max_retries: int = 3):
        self.logger = logger or ConsoleLogger()
        self.max_retries = max_retries
        self.session = requests.Session()
        
        # Headers para simular navegador real
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def download_file(self, url: str, filepath: str) -> bool:
        """
        Baixa arquivo do URL especificado com retry automático.
        
        Args:
            url: URL do arquivo para download
            filepath: Caminho onde salvar o arquivo
            
        Returns:
            bool: True se download foi bem-sucedido, False caso contrário
        """
        for attempt in range(self.max_retries):
            try:
                self.logger.info(f"Iniciando download (tentativa {attempt + 1}/{self.max_retries}): {url}")
                
                # Primeiro fazer uma requisição HEAD para verificar se o arquivo existe
                head_response = self.session.head(url, timeout=10)
                self.logger.debug(f"Status da verificação HEAD: {head_response.status_code}")
                
                if head_response.status_code == 404:
                    self.logger.error(f"Arquivo não encontrado no servidor: {url}")
                    return False
                elif head_response.status_code == 403:
                    self.logger.warning("Acesso negado na verificação HEAD, tentando download direto...")
                
                response = self.session.get(url, stream=True, timeout=30)
                response.raise_for_status()
                
                # Obter tamanho do arquivo se disponível
                total_size = int(response.headers.get('content-length', 0))
                if total_size > 0:
                    self.logger.info(f"Tamanho do arquivo: {total_size / (1024*1024):.2f} MB")
                
                # Download com progresso
                downloaded = 0
                with open(filepath, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            downloaded += len(chunk)
                            
                            # Mostrar progresso a cada 1MB baixado
                            if total_size > 0 and downloaded % (1024*1024) == 0:
                                progress = (downloaded / total_size) * 100
                                self.logger.debug(f"Progresso: {progress:.1f}%")
                
                self.logger.success(f"Download concluído: {filepath}")
                return True
                
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Erro na tentativa {attempt + 1}: {str(e)}")
                
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt  # Backoff exponencial
                    self.logger.info(f"Aguardando {wait_time}s antes da próxima tentativa...")
                    time.sleep(wait_time)
                else:
                    self.logger.error("Todas as tentativas de download falharam")
                    return False
            
            except Exception as e:
                self.logger.error(f"Erro inesperado: {str(e)}")
                return False
        
        return False