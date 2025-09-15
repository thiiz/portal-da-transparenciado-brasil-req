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
        """Gera nome do arquivo baseado no mês anterior (AAAAMM_PEP.zip)."""
        brasilia_time = self.get_brasilia_datetime()
        
        # Calcular mês anterior (dados têm atraso)
        year = brasilia_time.year
        month = brasilia_time.month - 2  # 2 meses atrás para garantir disponibilidade
        
        if month <= 0:
            month += 12
            year -= 1
        
        year_month = f"{year:04d}{month:02d}"
        return f"{year_month}_PEP.zip"
    
    def get_available_months(self, months_back: int = 6) -> list[str]:
        """
        Gera lista de meses para verificar disponibilidade (do mais recente para o mais antigo).
        
        Args:
            months_back: Quantos meses para trás verificar
            
        Returns:
            list: Lista de strings no formato AAAAMM
        """
        brasilia_time = self.get_brasilia_datetime()
        months = []
        
        for i in range(months_back):
            year = brasilia_time.year
            month = brasilia_time.month - i
            
            if month <= 0:
                month += 12
                year -= 1
            
            months.append(f"{year:04d}{month:02d}")
        
        return months