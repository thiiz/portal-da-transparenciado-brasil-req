"""
Gerador de datas e nomes de arquivo para o PEP Downloader Bot.
"""
from datetime import datetime
import pytz


class DateGenerator:
    """Responsável por gerar nomes de arquivo baseados na data atual."""
    
    def __init__(self):
        self.brasilia_tz = pytz.timezone('America/Sao_Paulo')
    
    def get_brasilia_datetime(self) -> datetime:
        """Obtém data/hora atual no fuso de Brasília (-03)."""
        utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)
        return utc_now.astimezone(self.brasilia_tz)
    
    def get_current_month_filename(self) -> str:
        """Gera nome do arquivo baseado na data atual (AAAAMM_PEP.zip)."""
        brasilia_time = self.get_brasilia_datetime()
        year_month = brasilia_time.strftime('%Y%m')
        return f"{year_month}_PEP.zip"