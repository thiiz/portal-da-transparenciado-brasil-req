# Requirements Document

## Introduction

Este documento define os requisitos para um bot em Python que realiza download automático de arquivos de dados PEP (Pessoas Expostas Politicamente) do Portal da Transparência do Brasil. O bot deve funcionar de forma headless, utilizando apenas requisições HTTP diretas para baixar arquivos .zip com dados atualizados mensalmente.

## Requirements

### Requirement 1

**User Story:** Como um usuário do sistema, eu quero que o bot baixe automaticamente os arquivos PEP do Portal da Transparência, para que eu possa obter os dados mais recentes sem intervenção manual.

#### Acceptance Criteria

1. WHEN o bot é executado THEN o sistema SHALL gerar automaticamente o nome do arquivo baseado na data atual no formato AAAAMM_PEP.zip
2. WHEN o bot faz a requisição THEN o sistema SHALL utilizar apenas a biblioteca requests para requisições HTTP diretas
3. WHEN o download é iniciado THEN o sistema SHALL baixar o arquivo do URL https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/pep/AAAAMM_PEP.zip
4. WHEN o arquivo é baixado THEN o sistema SHALL salvar o arquivo na pasta downloads/ dentro do diretório do script

### Requirement 2

**User Story:** Como um desenvolvedor, eu quero que o bot funcione em um ambiente virtual Python isolado, para que as dependências sejam gerenciadas adequadamente e não conflitem com outros projetos.

#### Acceptance Criteria

1. WHEN o ambiente é configurado THEN o sistema SHALL utilizar um ambiente virtual Python (.venv)
2. WHEN as dependências são instaladas THEN o sistema SHALL utilizar pip para instalar as bibliotecas necessárias
3. WHEN o script é executado THEN o sistema SHALL funcionar consistentemente independente de configurações de monitores
4. WHEN o bot roda THEN o sistema SHALL operar em modo console/headless sem interface gráfica

### Requirement 3

**User Story:** Como um usuário, eu quero que o bot simule um navegador real nas requisições HTTP, para que não seja bloqueado por medidas anti-bot básicas.

#### Acceptance Criteria

1. WHEN uma requisição HTTP é feita THEN o sistema SHALL incluir headers HTTP com User-Agent simulando um navegador
2. WHEN ocorre uma falha de rede THEN o sistema SHALL utilizar raise_for_status() para tratamento de erros
3. WHEN a requisição é processada THEN o sistema SHALL exibir mensagens de progresso no console
4. WHEN o download é concluído THEN o sistema SHALL informar o status de sucesso ou falha

### Requirement 4

**User Story:** Como um analista de dados, eu quero ter a opção de descompactar automaticamente os arquivos baixados, para que possa acessar diretamente os arquivos CSV internos.

#### Acceptance Criteria

1. WHEN a opção de descompactação é ativada THEN o sistema SHALL utilizar a biblioteca zipfile para extrair arquivos
2. WHEN a descompactação falha THEN o sistema SHALL tratar erros e continuar a execução
3. WHEN arquivos são extraídos THEN o sistema SHALL salvar os arquivos CSV na mesma pasta downloads/
4. IF a descompactação é bem-sucedida THEN o sistema SHALL exibir mensagem de confirmação no console

### Requirement 5

**User Story:** Como um usuário, eu quero que o bot gere nomes de arquivo baseados na data atual, para que eu sempre obtenha os dados do período correto.

#### Acceptance Criteria

1. WHEN o bot é executado em setembro de 2025 THEN o sistema SHALL gerar o nome 202509_PEP.zip
2. WHEN a data atual é processada THEN o sistema SHALL considerar o fuso horário de Brasília (-03)
3. WHEN o nome do arquivo é gerado THEN o sistema SHALL seguir o padrão AAAAMM_PEP.zip
4. WHEN o mês muda THEN o sistema SHALL automaticamente ajustar o nome do arquivo para o novo período

### Requirement 6

**User Story:** Como um desenvolvedor, eu quero instruções claras de configuração e execução, para que possa implementar e usar o bot facilmente.

#### Acceptance Criteria

1. WHEN a documentação é fornecida THEN o sistema SHALL incluir instruções para criar ambiente virtual
2. WHEN as instruções são seguidas THEN o sistema SHALL incluir comandos para ativar o ambiente virtual
3. WHEN as dependências são listadas THEN o sistema SHALL especificar como instalar via pip
4. WHEN o código é fornecido THEN o sistema SHALL incluir comentários explicativos em português