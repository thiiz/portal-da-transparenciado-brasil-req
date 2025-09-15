#!/usr/bin/env python3
"""
Script para testar quais arquivos PEP estão disponíveis no servidor.
"""
from pep_downloader.bot import PEPDownloaderBot

def main():
    print("=== Verificando arquivos PEP disponíveis ===")
    
    # Criar bot com logs verbosos
    bot = PEPDownloaderBot(verbose=True)
    
    # Verificar arquivos disponíveis nos últimos 12 meses
    available_files = bot.check_available_files(months_back=12)
    
    print(f"\n=== RESUMO ===")
    print(f"Arquivos disponíveis encontrados: {len(available_files)}")
    for file in available_files:
        print(f"  - {file}")
    
    if available_files:
        print(f"\nArquivo mais recente: {available_files[0]}")
    else:
        print("\nNenhum arquivo encontrado. Pode ser um problema de conectividade ou mudança na API.")

if __name__ == "__main__":
    main()