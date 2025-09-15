# PEP Downloader Bot

Bot em Python para download automático de arquivos PEP (Pessoas Expostas Politicamente) do Portal da Transparência do Brasil.

## Características

- ✅ Download automático baseado na data atual (formato AAAAMM_PEP.zip)
- ✅ Funcionamento headless (apenas requisições HTTP)
- ✅ Headers de navegador para evitar bloqueios
- ✅ Sistema de retry com backoff exponencial
- ✅ Extração automática opcional de arquivos ZIP
- ✅ Logs detalhados com timestamps
- ✅ Verificação de espaço em disco
- ✅ Proteção contra path traversal
- ✅ Configuração via argumentos ou variáveis de ambiente

## Instalação Rápida

### Opção 1: Script Automático
```bash
python setup_env.py
```

### Opção 2: Manual
```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

## Uso

### Uso Básico
```bash
# Download simples
python main.py

# Download com extração automática
python main.py --extract

# Download com logs detalhados
python main.py --verbose

# Diretório personalizado
python main.py --output-dir dados
```

### Exemplos Avançados
```bash
# Download completo com todas as opções
python main.py --extract --verbose --output-dir dados --max-retries 5

# Usando variáveis de ambiente
export PEP_DOWNLOAD_DIR="dados"
export PEP_EXTRACT_FILES="true"
export PEP_VERBOSE="true"
python main.py
```

## Configuração

### Argumentos da Linha de Comando
- `--extract`: Extrair arquivos ZIP automaticamente
- `--output-dir DIR`: Diretório de saída (padrão: downloads)
- `--verbose`: Logs detalhados
- `--max-retries N`: Número máximo de tentativas (padrão: 3)

### Variáveis de Ambiente
- `PEP_DOWNLOAD_DIR`: Diretório de download
- `PEP_EXTRACT_FILES`: "true" para extrair automaticamente
- `PEP_VERBOSE`: "true" para logs detalhados
- `PEP_MAX_RETRIES`: Número de tentativas

## Estrutura do Projeto

```
pep-downloader-bot/
├── pep_downloader/           # Pacote principal
│   ├── __init__.py
│   ├── bot.py               # Bot principal
│   ├── date_generator.py    # Geração de datas
│   ├── http_client.py       # Cliente HTTP
│   ├── file_manager.py      # Gerenciamento de arquivos
│   ├── zip_extractor.py     # Extração de ZIP
│   ├── console_logger.py    # Sistema de logs
│   └── models.py           # Modelos de dados
├── main.py                 # Script principal
├── setup_env.py           # Configuração automática
├── requirements.txt       # Dependências
└── README.md             # Documentação
```

## Como Funciona

1. **Geração do Nome**: O bot gera automaticamente o nome do arquivo baseado na data atual no fuso de Brasília (AAAAMM_PEP.zip)

2. **Download**: Utiliza requisições HTTP diretas com headers de navegador para baixar de:
   ```
   https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/pep/AAAAMM_PEP.zip
   ```

3. **Retry Logic**: Em caso de falha, tenta novamente com backoff exponencial (até 3 tentativas por padrão)

4. **Extração Opcional**: Se solicitado, extrai automaticamente os arquivos CSV do ZIP baixado

## Exemplo de Saída

```
[14:30:15] INFO: === PEP Downloader Bot - Portal da Transparência ===
[14:30:15] INFO: Arquivo alvo: 202509_PEP.zip
[14:30:15] INFO: Iniciando download (tentativa 1/3): https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/pep/202509_PEP.zip
[14:30:16] INFO: Tamanho do arquivo: 45.23 MB
[14:30:45] ✓ SUCESSO: Download concluído: downloads/202509_PEP.zip
[14:30:45] INFO: Iniciando extração do arquivo ZIP...
[14:30:46] ✓ SUCESSO: Extração concluída. 1 arquivos extraídos em: downloads
[14:30:46] INFO: === RESUMO DA OPERAÇÃO ===
[14:30:46] ✓ SUCESSO: Download: 202509_PEP.zip (45.23 MB)
[14:30:46] ✓ SUCESSO: Extração: 1 arquivos extraídos
[14:30:46] INFO: === FIM DA OPERAÇÃO ===
```

## Dependências

- `requests>=2.31.0`: Para requisições HTTP
- `pytz>=2023.3`: Para manipulação de fuso horário

## Códigos de Saída

- `0`: Sucesso completo
- `1`: Falha no download
- `2`: Download OK, mas falha na extração
- `130`: Cancelado pelo usuário (Ctrl+C)

## Troubleshooting

### Erro de Conexão
- Verifique sua conexão com a internet
- O Portal da Transparência pode estar temporariamente indisponível

### Arquivo Não Encontrado (404)
- O arquivo do mês atual pode ainda não estar disponível
- Arquivos são atualizados mensalmente pelo governo

### Espaço Insuficiente
- Libere espaço em disco (arquivos PEP podem ter 40-50 MB)
- Use `--output-dir` para especificar outro diretório

### Problemas de Permissão
- Execute com permissões adequadas para criar diretórios
- No Windows, execute como administrador se necessário

## Contribuição

Este projeto segue as especificações definidas nos documentos de requirements, design e tasks. Para contribuir:

1. Mantenha a compatibilidade com Python 3.7+
2. Siga as convenções de código existentes
3. Adicione testes para novas funcionalidades
4. Mantenha a documentação atualizada

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT.