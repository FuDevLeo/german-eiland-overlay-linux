# Instalação no Fedora KDE — passo a passo

[Voltar ao início](../README.pt-BR.md) · [English](INSTALLATION.md)

> **Protótipo não oficial.** Os ajustes funcionaram numa sessão local, mas o procedimento portátil completo, com um perfil novo, ainda não foi validado de ponta a ponta em outra máquina. As instruções abaixo descrevem a separação correta das etapas; não são uma promessa de funcionamento em toda instalação.

## 1. Entenda os três programas

- **Wine:** foi usado para instalar o overlay Windows. Nesta etapa você executa o arquivo de instalação, como `GermanEilandOverlay-Setup-....exe`.
- **Proton Experimental:** foi usado para abrir o aplicativo depois de instalado. O Proton inclui uma versão derivada do Wine; o iniciador chama essa versão, sem depender do comando `wine` para a execução normal.
- **Steam:** continua abrindo o The Isle como você já faz. Não troque a versão do Proton do jogo por causa deste guia.

Instalar e executar são etapas diferentes. Não testamos uma instalação inteira feita somente pelo Proton. Por isso, **Wine também é requisito deste procedimento**.

## 2. Confira o ambiente necessário

Este protótipo é voltado para:

- Fedora com **KDE Plasma/KWin** e sessão D-Bus do próprio usuário.
- **Xwayland/X11** disponível, inclusive numa sessão KDE Wayland.
- Steam instalado no computador e **Proton Experimental** já baixado pela Steam.
- The Isle Evrima funcionando normalmente pela Steam.
- Espaço livre para um perfil de instalação do Wine e outro perfil de execução do Proton.

O iniciador procura o Steam em `~/.local/share/Steam` e `~/.steam/steam`. Para outra biblioteca, há a opção `--proton`. **Steam Flatpak e outros ambientes isolados não foram validados**; não presuma que fornecer um caminho resolve suas permissões e dependências.

Na Steam, procure **Proton Experimental** na Biblioteca, exibindo a categoria de ferramentas se necessário, e instale-o. É a ferramenta utilizada pelo overlay; isso não exige mudar as opções do jogo.

## 3. Instale as dependências

No Fedora, abra o Konsole e use:

```bash
sudo dnf install wine git python3-pillow python3-websockets python3-dbus \
  python3-gobject-base python3-pyside6 xprop libX11 libXext
```

**Leia a lista de pacotes e possíveis remoções antes de confirmar.** Não prossiga com remoções inesperadas. Este projeto não precisa desativar SELinux, ignorar assinaturas de pacotes nem reiniciar o computador.

Os nomes acima correspondem aos pacotes encontrados na máquina usada no diagnóstico; disponibilidade e versões podem variar entre versões do Fedora. Em outra distribuição, instale os equivalentes. `requirements.txt` descreve as bibliotecas Python, mas não substitui automaticamente as dependências do desktop.

Se você usa um ambiente virtual Python, ele precisa enxergar as bibliotecas de integração do sistema (`dbus`, `gi`, Qt/PySide6). O caminho mais simples neste protótipo é usar o `python3` do sistema.

## 4. Baixe e instale o overlay oficial com Wine

Obtenha o instalador nos canais oficiais do **[German Eiland](https://germaneiland.com/)**. Não use executáveis de terceiros ou arquivos de sessão enviados por outro jogador. Este repositório não distribui o instalador.

No Konsole, escolha um prefixo dedicado para a instalação:

```bash
GE_INSTALL_PREFIX="$HOME/.local/share/german-eiland-overlay-linux/installer-prefix"
mkdir -p "$GE_INSTALL_PREFIX"
```

Agora execute o instalador que você baixou. **Substitua somente o caminho entre aspas pelo caminho real do seu arquivo:**

```bash
WINEPREFIX="$GE_INSTALL_PREFIX" wine "/caminho/real/para/o/instalador-oficial.exe"
```

Na primeira execução, o Wine pode preparar o ambiente e apresentar janelas de configuração. Siga o instalador oficial. Se ele oferecer abrir o overlay ao terminar, desmarque essa opção: a execução normal será pelo iniciador do próximo passo. Se o aplicativo já tiver aberto no Wine e ficar branco, feche apenas o overlay pelo próprio aplicativo ou pela bandeja; não encerre todos os processos Wine, pois outro programa ou o jogo pode estar usando-os.

Mantenha **a pasta completa instalada**, incluindo `resources`, bibliotecas e demais arquivos. Copiar somente o `.exe` não basta.

### Localize o aplicativo instalado

Um caminho típico dentro desse prefixo é:

```text
~/.local/share/german-eiland-overlay-linux/installer-prefix/drive_c/users/SEU_USUARIO/AppData/Local/Programs/German Eiland Overlay/German Eiland Overlay.exe
```

`SEU_USUARIO` é um marcador: substitua pelo nome da pasta que existe no seu computador. Você também pode procurar o arquivo no prefixo:

```bash
find "$GE_INSTALL_PREFIX/drive_c/users" -type f -name 'German Eiland Overlay.exe'
```

Guarde o caminho encontrado. O arquivo correto se chama **`German Eiland Overlay.exe`**. Ele é diferente do arquivo **`...Setup...exe`**, usado somente para instalar.

Você pode reutilizar uma instalação oficial que já tenha no seu próprio computador. Não compartilhe o prefixo que a contém: ele pode guardar dados privados.

## 5. Baixe os scripts deste projeto

```bash
git clone https://github.com/FuDevLeo/german-eiland-overlay-linux.git
cd german-eiland-overlay-linux
chmod +x launch.sh
./launch.sh --check
```

Ou use **Code → Download ZIP** no GitHub, extraia e abra o Konsole na pasta que contém `launch.sh`. Depois execute as duas últimas linhas acima.

O resultado `Dependencies available` confirma os componentes necessários. Essa verificação **não abre o jogo, não instala o overlay e não comprova funcionamento completo**.

## 6. Abra pelo Proton Experimental

Na pasta deste projeto, use o caminho do aplicativo instalado no passo 4:

```bash
./launch.sh --exe "/caminho/completo/para/German Eiland Overlay.exe"
```

Se a ferramenta Proton estiver em outra biblioteca da Steam:

```bash
./launch.sh --exe "/caminho/completo/para/German Eiland Overlay.exe" \
  --proton "/caminho/completo/para/Proton - Experimental/proton"
```

O caminho passado em `--proton` termina no arquivo **`proton`**, não na pasta nem em `wine`.

O iniciador cria **um novo perfil de execução** em `~/.local/share/german-eiland-overlay-linux/compatdata`. Ele não copia o prefixo de instalação do Wine, o prefixo do jogo, cookies ou contas. A pasta do aplicativo continua no local onde você o instalou; não a remova.

Faça o login por conta própria nesse novo perfil. Não envie senha, código ou perfil a outra pessoa. Abra o jogo normalmente pela Steam. A instalação local que motivou este projeto funcionou desse modo; o fluxo portátil novo ainda precisa de teste completo independente.

## 7. Crie o atalho correto

Para guardar os caminhos localmente e adicionar o atalho ao menu de aplicativos:

```bash
./launch.sh --exe "/caminho/completo/para/German Eiland Overlay.exe" --install-shortcut
```

Inclua `--proton` também se você precisou dele no passo anterior. Esse comando só salva a configuração e cria o atalho; não inicia o aplicativo.

Procure **German Eiland Overlay (Linux prototype)** no menu. Use esse atalho para abrir com as correções. Um atalho criado automaticamente pelo instalador do Wine pode abrir a versão sem os ajustes.

**Mantenha a pasta deste projeto no mesmo lugar** depois de criar o atalho. Se movê-la, execute novamente o comando de criação do atalho.

## 8. Mouse e teclas

| Atalho padrão | Ação |
| --- | --- |
| F6 | Esconder/mostrar o overlay |
| F7 | Alternar o bloqueio de cliques: jogar / mexer nos controles do overlay |
| F8 | Falar enquanto segura; a transmissão de voz ainda precisa de validação completa |
| F9 | Silenciar o microfone |
| 5 | Mostrar/esconder a barra de menu |
| Ctrl+S | Travar/destravar o posicionamento dos elementos |

Os atalhos refletem a configuração atual do overlay e são registrados pelo KDE enquanto o The Isle está em foco. Não são instalados como atalhos permanentes para todos os programas. Combinações já ocupadas no KDE não são substituídas. Atalhos com botões do mouse não são implementados por essa ponte.

**Para jogar:** deixe o bloqueio de cliques ligado. **Para mexer no overlay:** libere o cursor no jogo, desligue o bloqueio com F7 e use os menus. Ao terminar, ligue-o novamente. Pressione **Esc** para cancelar uma captura de nova tecla. Evite clicar em várias linhas de redefinição ao mesmo tempo.

## Problemas comuns

| Sintoma | O que conferir |
| --- | --- |
| Tela branca ao usar o ícone do instalador | Use o atalho deste projeto; confirme que ele abre com Proton Experimental. |
| Fundo preto cobrindo o jogo | Confira se o helper está ativo e se `--check` passa. Não considere isso transparência real: o projeto usa um recorte. |
| Menus ou bordas cortados | O recorte acompanha a interface, mas detalhes muito escuros podem ser cortados. Não há garantia de mistura suave das bordas. |
| Overlay não aceita cliques | Verifique F7 e se o cursor do jogo foi liberado. |
| Atalhos só funcionam na janela do overlay | Confira o KDE/KGlobalAccel, conflitos de teclas e se o jogo está em foco. |
| Mensagem de porta ocupada | Feche a instância anterior ou use `--port 9341`; não mate o jogo nem abra a porta na rede. |
| Lista de espécies atrás da janela | O helper tenta substituir o seletor por uma lista dentro da página. Uma atualização do site pode exigir ajuste. |
| Microfone falha | Confira o dispositivo de entrada do Fedora e a permissão do aplicativo. A captura local foi testada; comunicação entre jogadores não foi validada. |
| Barra do KDE ou foco atrapalham o jogo | A janela do overlay usa uma categoria especial para ficar acima da tela cheia. Esse contorno ainda precisa de validação mais ampla. |

Os registros ficam somente no computador, em `~/.local/state/german-eiland-overlay-linux/launch.log`. Eles podem conter caminhos e mensagens de uso: **revise e oculte dados antes de compartilhar qualquer trecho**.

## Privacidade e remoção

As duas etapas criam ambientes diferentes:

| Local | Conteúdo |
| --- | --- |
| `~/.local/share/german-eiland-overlay-linux/installer-prefix` | Instalação do aplicativo pelo Wine |
| `~/.local/share/german-eiland-overlay-linux/compatdata` | Perfil de execução pelo Proton; pode conter login e cookies |
| `~/.config/german-eiland-overlay-linux/config.json` | Caminhos salvos para o atalho |
| `~/.local/state/german-eiland-overlay-linux` | Registros e arquivos de controle locais |

Esses caminhos padrão respeitam os diretórios XDG quando configurados. **Não envie essas pastas ao GitHub.** O projeto publicado contém apenas código e documentação.

O acesso de diagnóstico do Chromium fica limitado a `127.0.0.1` enquanto o overlay está aberto e pode controlar sua sessão no aplicativo. Não exponha nem encaminhe a porta para a rede.

Para remover, feche o overlay/iniciador e remova o atalho `~/.local/share/applications/german-eiland-overlay-linux.desktop`. Depois, remova a pasta baixada deste projeto se desejar. Os perfis e registros são mantidos: só apague esses diretórios manualmente se tiver certeza e não precisar dos dados. Este guia não precisa alterar a configuração da Steam ou os arquivos do The Isle.

## O que ainda precisa de revisão

- Instalação completa em outra máquina e funcionamento com perfis novos.
- Transmissão de voz, rolagem da loja e transições de foco/tela cheia.
- Compatibilidade após atualizações do overlay e do site.
- Revisão e autorização da equipe German Eiland antes de recomendar o protótipo amplamente.

[Leia também os limites técnicos e de privacidade](PRIVACY-AND-LIMITATIONS.md). Não há garantia de aprovação do servidor ou de compatibilidade com anticheat.
