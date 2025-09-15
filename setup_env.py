#!/usr/bin/env python3
"""
Script para configurar ambiente virtual e instalar dependências.
"""
import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Executa comando e trata erros."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"[OK] {description} concluído com sucesso")
        return result
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro em {description}:")
        print(f"  Comando: {command}")
        print(f"  Código de saída: {e.returncode}")
        print(f"  Erro: {e.stderr}")
        return None


def main():
    """Configura ambiente virtual e instala dependências."""
    print("=== Configuração do Ambiente PEP Downloader Bot ===")
    
    # Verificar se Python está disponível
    try:
        python_version = subprocess.check_output([sys.executable, "--version"], text=True).strip()
        print(f"Python encontrado: {python_version}")
    except Exception as e:
        print(f"Erro ao verificar Python: {e}")
        sys.exit(1)
    
    # Criar ambiente virtual
    venv_path = Path(".venv")
    if not venv_path.exists():
        if not run_command(f"{sys.executable} -m venv .venv", "Criando ambiente virtual"):
            sys.exit(1)
    else:
        print("[OK] Ambiente virtual já existe")
    
    # Determinar comando de ativação baseado no OS
    if os.name == 'nt':  # Windows
        activate_cmd = ".venv\\Scripts\\activate"
        pip_cmd = ".venv\\Scripts\\pip"
        python_cmd = ".venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        activate_cmd = "source .venv/bin/activate"
        pip_cmd = ".venv/bin/pip"
        python_cmd = ".venv/bin/python"
    
    # Atualizar pip
    if not run_command(f"{pip_cmd} install --upgrade pip", "Atualizando pip"):
        sys.exit(1)
    
    # Instalar dependências
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Instalando dependências"):
        sys.exit(1)
    
    # Verificar instalação
    print("\n=== Verificando Instalação ===")
    result = run_command(f"{python_cmd} -c \"import requests, pytz; print('Dependências OK')\"", 
                        "Verificando dependências")
    
    if result:
        print("\n=== Configuração Concluída ===")
        print("Para usar o bot:")
        print(f"1. Ative o ambiente virtual: {activate_cmd}")
        print("2. Execute o bot: python main.py")
        print("3. Para ajuda: python main.py --help")
        print("\nExemplos:")
        print("  python main.py --extract --verbose")
        print("  python main.py --output-dir dados")
    else:
        print("\n✗ Falha na verificação. Verifique os erros acima.")
        sys.exit(1)


if __name__ == "__main__":
    main()