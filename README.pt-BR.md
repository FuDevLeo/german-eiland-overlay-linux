# German Eiland Overlay no Linux — protótipo não oficial

Este pacote reúne os ajustes usados durante uma sessão de diagnóstico no **Fedora KDE, com Wayland/Xwayland e Proton Experimental**. Ele serve para revisão do dono do servidor e para testes de outros usuários Linux.

**Não contém seu login Steam, cookies, personagem, prefixo Wine/Proton, imagens, registros de uso ou executáveis.** Cada usuário precisa obter o overlay oficial por conta própria. O programa cria um ambiente novo e separado, onde o próprio usuário faz o login.

## Ajustes incluídos

- Recorte do fundo preto para mostrar o jogo atrás do overlay; acompanha menus novos.
- Posicionamento da janela sobre o jogo em tela cheia pelo KWin.
- Atalhos de teclado pelo KDE enquanto o The Isle está em foco.
- Bloqueio de cliques para jogar e desbloqueio para mexer no overlay (F7 por padrão).
- Remoção das sombras que viravam margens pretas.
- Lista de espécies da loja dentro da própria página, sem menu nativo atrás do jogo.

## Como começar

Depois de baixar, execute `chmod +x launch.sh` uma vez se o arquivo não estiver marcado como executável.

Leia os requisitos no [README principal](README.md). O pacote depende de bibliotecas Python, X11/Xwayland, D-Bus e KDE. Não instala esses componentes automaticamente.

```bash
./launch.sh --check
./launch.sh --exe "/caminho/para/German Eiland Overlay.exe"
```

É preciso manter a pasta completa do aplicativo oficial, com a pasta `resources`. Para escolher outra instalação do Proton, use `--proton "/caminho/para/Proton - Experimental/proton"`.

Para criar um atalho no menu e guardar os caminhos somente no seu computador:

```bash
./launch.sh --exe "/caminho/para/German Eiland Overlay.exe" --install-shortcut
```

**Não envie para o GitHub** as pastas locais `~/.config/german-eiland-overlay-linux`, `~/.local/share/german-eiland-overlay-linux` ou `~/.local/state/german-eiland-overlay-linux`. Depois do uso elas podem conter sua sessão, caminhos e registros.

## Limitações importantes

O usuário confirmou a exibição do jogo atrás do overlay, menus clicáveis e o F7 no ambiente original. O pacote portátil, com perfil novo, ainda precisa de teste completo em outra instalação. A transmissão de voz e os últimos ajustes da loja e de tela cheia não foram validados integralmente.

O recorte não é transparência real com mistura de cores: pode cortar detalhes escuros e custa processamento. Há uma interface de diagnóstico Chromium na porta local 9340 enquanto o overlay roda; ela pode controlar a sessão do aplicativo. Não exponha nem encaminhe essa porta pela rede. Leia [privacidade e limitações](docs/PRIVACY-AND-LIMITATIONS.md).

Este projeto não altera os arquivos do jogo, não inclui o aplicativo proprietário e não garante aprovação do servidor ou compatibilidade com anticheat. A autorização da equipe do servidor para esse protótipo ainda precisa ser obtida antes de recomendá-lo amplamente.

O [README principal](README.md) também explica os atalhos, os arquivos criados e a remoção. A licença MIT vale somente para os scripts deste repositório.
