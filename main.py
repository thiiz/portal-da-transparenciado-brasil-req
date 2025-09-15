#!/usr/bin/env python3
"""
Script principal do PEP Downloader Bot.
Bot para download automático de arquivos PEP do Portal da Transparência do Brasil.
"""
import argparse
import os
import sys
from pep_downloader.bot import PEPDownloaderBot


def parse_arguments():
    """Configura e processa argumentos da linha de comando."""
    parser = argparse.ArgumentParser(
        description="Bot para download de arquivos PEP do Portal da Transparência",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py                          # Download básico
  python main.py --extract                # Download e extração
  python main.py --output-dir dados       # Diretório personalizado
  python main.py --extract --verbose      # Modo detalhado com extração
        """
    )
    
    parser.add_argument(
        '--extract', 
        action='store_true',
        help='Extrair arquivos ZIP automaticamente após download'
    )
    
    parser.add_argument(
        '--output-dir',
        default='downloads',
        help='Diretório onde salvar os arquivos (padrão: downloads)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Exibir logs detalhados durante a execução'
    )
    
    parser.add_argument(
        '--max-retries',
        type=int,
        default=3,
        help='Número máximo de tentativas de download (padrão: 3)'
    )
    
    return parser.parse_args()


def load_environment_config():
    """Carrega configurações de variáveis de ambiente."""
    return {
        'download_dir': os.getenv('PEP_DOWNLOAD_DIR', 'downloads'),
        'extract_files': os.getenv('PEP_EXTRACT_FILES', 'false').lower() == 'true',
        'max_retries': int(os.getenv('PEP_MAX_RETRIES', '3')),
        'verbose': os.getenv('PEP_VERBOSE', 'false').lower() == 'true'
    }


def main():
    """Função principal do script."""
    try:
        # Processar argumentos da linha de comando
        args = parse_arguments()
        
        # Carregar configurações de ambiente
        env_config = load_environment_config()
        
        # Argumentos da linha de comando têm prioridade sobre variáveis de ambiente
        config = {
            'download_dir': args.output_dir or env_config['download_dir'],
            'extract_files': args.extract or env_config['extract_files'],
            'verbose': args.verbose or env_config['verbose'],
            'max_retries': args.max_retries or env_config['max_retries']
        }
        
        # Criar e executar o bot
        bot = PEPDownloaderBot(**config)
        download_result, extraction_result = bot.run()
        
        # Código de saída baseado no resultado
        if download_result.success:
            if config['extract_files'] and extraction_result and not extraction_result.success:
                sys.exit(2)  # Download OK, mas extração falhou
            else:
                sys.exit(0)  # Sucesso completo
        else:
            sys.exit(1)  # Falha no download
            
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")
        sys.exit(130)
    except Exception as e:
        print(f"\nErro inesperado: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()