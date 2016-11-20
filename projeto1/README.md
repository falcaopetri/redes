# Projeto 1 - Servidor de Consultas Linux

## O projeto

## Estrutura do projeto

- `server/`: Contém o webserver.py, responsável por receber a requisição do usuário, enviá-la para o backend.py (também nesse diretório), receber a resposta do backend.py e exibi-lá em formato de página web.
- `slave/`: Contém o daemon.py, programa que executa comandos localmente, processa a saída e é replicado em várias máquinas.
- `scripts/`: Scripts auxiliares para facilitar algumas configurações, e.g. subir a rede Host-only na VM.

## TODO
- Tudo?
