# Projeto 1 - Servidor de Consultas Linux

## O projeto

## Estrutura do projeto

- `server/`: Contém o webserver.py, responsável por receber a requisição do usuário, enviá-la para o backend.py (também nesse diretório), receber a resposta do backend.py e exibi-lá em formato de página web.
- `slave/`: Contém o daemon.py, programa que executa comandos localmente, processa a saída e é replicado em várias máquinas.
- `scripts/`: Scripts auxiliares para facilitar algumas configurações, e.g. subir a rede Host-only na VM.

## Setup

> Todos os comandos devem ser executados dentro da pasta `projeto1`

1. Instalar dependências:
`$ pip3 install -r requirements.txt`

2. Configurar PATH do projeto:
2.1. `$ source ./scripts/export_path.sh`
2.2. Editar `./util.py` com o PATH absoluto do projeto, e.g. `/home/aluno/redes/projeto1`

3. Subir rede:
`$ ./scripts/net_setup.sh`

4. Configurar symlinks:
`$ ./scripts/ln_setup.sh`

5. Iniciar as daemons:
`$ ./scripts/run_daemons.sh`
