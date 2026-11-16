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

## Precisa de Wine ou de Proton?

**No procedimento usado aqui, precisa dos dois, em etapas diferentes:**

| Etapa | Programa | Para que serve |
| --- | --- | --- |
| Instalar o overlay oficial | **Wine** | Abre o instalador Windows e cria a pasta completa do aplicativo. |
| Abrir o overlay com os ajustes Linux | **Proton Experimental** | Executa o aplicativo instalado com os scripts deste projeto. |
| Jogar The Isle | **Steam** | Abre seu jogo normalmente, com a configuração que você já usa. |

O Proton já contém uma versão derivada do Wine, mas **não validamos instalar tudo usando somente Proton**. A instalação original foi feita com Wine separado. O iniciador não executa o instalador: ele precisa do `German Eiland Overlay.exe` já instalado, junto com a pasta `resources`.

## Instalação passo a passo

➡️ **[Abrir o guia completo em português](docs/INSTALACAO.pt-BR.md)**

O guia explica:

1. Os requisitos de KDE, Steam, Wine, Proton e bibliotecas Python.
2. Como instalar as dependências no Fedora, revisando a transação antes de confirmar.
3. Como obter o instalador oficial e executá-lo em um prefixo separado.
4. Como localizar o executável instalado, sem confundi-lo com o instalador.
5. Como baixar este projeto, verificar dependências e abrir o overlay.
6. Como criar o atalho, usar F6/F7 e resolver problemas comuns.
7. O que é privado e como remover os ajustes.

[Guia em inglês](docs/INSTALLATION.md) · [Descrição técnica](README.md) · [Privacidade e limitações](docs/PRIVACY-AND-LIMITATIONS.md)

## Limitações importantes

O usuário confirmou a exibição do jogo atrás do overlay, menus clicáveis, o F7, o microfone e a comunicação por voz funcionando na instalação original Fedora KDE. Também informou que o problema da borda da área de trabalho foi resolvido usando tela cheia. O pacote portátil, com perfil novo, ainda precisa de teste completo em outra instalação. A correção mais recente de rolagem da lista da loja não foi confirmada separadamente.

O recorte não é transparência real com mistura de cores: pode cortar detalhes escuros e custa processamento. Há uma interface de diagnóstico Chromium na porta local 9340 enquanto o overlay roda; ela pode controlar a sessão do aplicativo. Não exponha nem encaminhe essa porta pela rede. Leia [privacidade e limitações](docs/PRIVACY-AND-LIMITATIONS.md).

Este projeto não altera os arquivos do jogo, não inclui o aplicativo proprietário e não garante aprovação do servidor ou compatibilidade com anticheat. A autorização da equipe do servidor para esse protótipo ainda precisa ser obtida antes de recomendá-lo amplamente.

O [README principal](README.md) também explica os atalhos, os arquivos criados e a remoção. A licença MIT vale somente para os scripts deste repositório.
