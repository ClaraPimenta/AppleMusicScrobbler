# Apple Music Scrobbler (Windows 11)

Aplicativo desktop que integra o cliente nativo do Apple Music no Windows 11 ao Last.fm.

O aplicativo monitora os controles de transporte de mídia do sistema (GSMTC) para detectar a reprodução atual, processar metadados e realizar o registro (scrobble) das faixas automaticamente.

![Badge License](https://img.shields.io/github/license/ClaraPimenta/AppleMusicScrobbler)
![Badge Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Badge Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-blue)

## Funcionalidades

- **Scrobble Automático:** Registra a música após 50% de reprodução ou após 4 minutos de execução contínua.
- **Status "Ouvindo Agora":** Atualiza o status no Last.fm em tempo real ao detectar mudança de faixa.
- **Tratamento de Metadados:**
  - Remove nomes de álbuns anexados incorretamente ao campo de artista pelo Apple Music.
  - Separa e valida os campos de Título, Artista e Álbum antes do envio.
- **Interface na Bandeja do Sistema:**
  - Execução em segundo plano.
  - Menu de contexto para verificar o status da música e pausar ou retomar o serviço (clique direito).

## Tecnologias Utilizadas

- **Python 3.12**
- **winsdk:** Acesso à API `GlobalSystemMediaTransportControls` do Windows para leitura de mídia.
- **pylast:** Interface para comunicação com a API do Last.fm.
- **pystray:** Criação e gerenciamento do ícone na bandeja do sistema.
- **Asyncio & Threading:** Gerenciamento de concorrência entre a interface de usuário e o loop de verificação de mídia.

## Instalação e Configuração

### Pré-requisitos
1. Python instalado.
2. Conta no Last.fm e credenciais de API (Key e Secret).

### Passos
1. Clone este repositório
   ```bash
   # Clone o repositório
     git clone https://github.com/ClaraPimenta/AppleMusicScrobbler.git

   # Entre na pasta
   cd AppleMusicScrobbler
   ```
2. Instale as dependências listadas no [requirements.txt](https://github.com/ClaraPimenta/AppleMusicScrobbler/blob/main/requirements.txt)
3. Configure as credênciais
   - Insira sua API Key, API Secret, Usuário e Senha do last.fm em [configs.py](https://github.com/ClaraPimenta/AppleMusicScrobbler/blob/main/configs.py)
4. Execute o aplicativo
   ```bash
   python main.py
   ```

### Compilação (Executável)
Para criar um executável standalone (.exe) utilizando o PyInstaller, execute o seguinte comando na raiz do projeto:

```bash
pyinstaller --noconsole --onefile --name="AppleMusicScrobbler" --add-data "app_icon.ico;." --icon="app_icon.ico" --copy-metadata=pylast main
```
O arquivo binário será gerado na pasta dist/

### Estrutura do Projeto
- main.py: Ponto de entrada. Inicializa a thread de interface e o ícone de bandeja.
- scrobbler.py: Lógica principal. Contém o loop de verificação, regras de tempo e controle de estado (pausa/retomada).
- services.py: Camada de integração com APIs externas (Windows SDK e Last.fm).
- utils.py: Funções utilitárias para sanitização de strings e manipulação de recursos gráficos.
- config.py: Arquivo de configuração (não versionado) contendo credenciais sensíveis.

### Licença
Este projeto está licenciado sob a licença GNU. Consulte o arquivo [LICENSE](https://github.com/ClaraPimenta/AppleMusicScrobbler/blob/main/LICENSE) para obter mais detalhes.


