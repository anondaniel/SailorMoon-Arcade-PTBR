# Pretty Soldier Sailor Moon (arcade, Gazelle/Banpresto, 1995) — análise inicial

Conjunto recebido: `sailormnu.zip` (versão USA; copiado dos Downloads para `00_Original/`, extraído em `00_Original/sailormnu/`).
Objetivo do usuário: traduzir para PT-BR. Pergunta secundária: existe versão para 3 jogadores? (Nada encontrado; o jogo é de 1–2 jogadores.)

## Arquivos do conjunto (18)

| arquivo | tamanho | CRC32 | papel provável |
|---|---|---|---|
| bpsm945a.u45 | 512 KB | 898C9515 | programa 68000 (palavras com bytes trocados: SP 00110000, PC 00000400) |
| bpsm945a.u9 | 512 KB | 438DE548 | programa Z80 do som (começa com `C3 12 01` = JP 0112) |
| bpsm.u46 / u48 | 2 MB cada | 32084E80 / 498E4ED1 | ? (dados do programa ou gráficos) |
| bpsm.u47 | 512 KB | 0F2901B9 | ? |
| bpsm.u53 … u77 (12 arquivos) | 2 MB cada | ver zip | gráficos (tiles/sprites) e amostras de som |
| sailormn_usa.nv | 128 B | 3915ABE3 | EEPROM (opções/ranking) |

Os papéis dos arquivos de 2 MB ainda não foram confirmados.

## O que se sabe
- Hardware: placa CAVE 68000 (1ª geração), segundo as fontes públicas.
- O programa 68000 não tem texto ASCII nem Shift-JIS legível: o texto deve estar em gráficos (tiles de fonte) e/ou em tabelas de índices de tile.

## Próximos passos
1. Ver o jogo rodando (MAME ou FBNeo; no PC não há emulador de arcade instalado, no Switch há o core FBNeo do RetroArch).
2. Fotografar todas as telas com texto (título, seleção de personagem, falas entre fases, final, créditos).
3. Descobrir como o texto é desenhado: tabelas no 68000 + fonte nos gráficos.
4. Decidir como caber o PT-BR (a fonte japonesa provavelmente é kana/kanji em tiles de 16×16).

## Atualização (2026-10-11): MAME instalado e primeiras capturas

- MAME 0.289 extraído em `C:\Tools\mame` (a partir do `mame0289b_x64.exe` baixado pelo usuário, extraído com o 7-Zip, sem executar). O conjunto `sailormnu` (clone de `sailormn`, driver `atlus/cave.cpp`) foi verificado: "is good". ROM copiada em `C:\Tools\mameoms\sailormnu.zip`.
- Controles: 1–2 jogadores, 3 botões por jogador (portas `:IN0` e `:IN1`). Não há entrada para um 3º jogador.
- **A versão USA já está em inglês** ("Deposit Coin", "Credit", "Press Start", "Score Ranking", "Character Contest", "ROUND 1 START", aviso "Notice … U.S.A."). Logo, o trabalho é inglês → PT-BR.
- Pouco texto visto em ~5 minutos de jogo (fase 1): HUD (TIME, nomes das guerreiras, Credit/Press Start), ROUND n START, tela de ranking, escolha de personagem (CHARACTER CONTEST), aviso legal, créditos do título. Ainda não vi: continue/game over, entrada de nome, diálogos de chefes, final.
- Scripts de captura em `tools/` (`cap_demo.lua` = modo demonstração; `jogar.lua` = coloca moeda, aperta START na hora certa — a tela "Notice" dura ~1800 quadros — e joga). Uso:
  `mame.exe sailormnu -rompath roms -video none -sound none -nothrottle -seconds_to_run 400 -autoboot_script jogar.lua -snapshot_directory snap`
- Capturas em `04_Graficos/capturas/`.

## Próximo passo
Achar onde o texto inglês está (o programa 68000 `u45` não tem ASCII legível: provavelmente tabelas de índices de tile + fonte nos gráficos) e quais telas realmente têm texto.

## Atualização 2 (2026-10-11): jogo zerado e onde está o texto

- Jogo zerado pelo MAME com um robô de botões (`tools/jogar2.lua`: moedas, START e ataques repetidos; ~480 mil quadros). Há **7 fases + Final Round**, chefes: KASTOL & POLX (R1), TWIN KYULENE (R6), THE BIG FOUR = ZOISAIT & KNZAIT, THE LAST BOSS = QUEEN BERIL. Depois do último chefe vêm: FINAL ROUND CLEAR, entrada de nome (Name Entry), créditos "Video Game Staff" e GAME OVER. **Não há diálogos nem cenas de história com texto**: só UI, nomes e créditos.
- **Todo o texto está em ASCII no programa 68000** `bpsm945a.u45`, mas o arquivo tem os bytes trocados dois a dois (ROM_LOAD16_WORD_SWAP). Versão já destrocada em `01_ROM/u45_bytes_trocados.bin`; lista de 213 cadeias com offset e tamanho em `03_Traducao/strings_u45.txt`.
- Regiões: UI (0x064DC: Credit, Deposit Coin, Press Start, Select Player, Continue?, Game Over, Wait Please..., Name Entry), nomes de golpes (0x22731), menu de teste/operador (0x22CEC–0x2346C), aviso legal "Notice" (0x23855), créditos do título (0x23DD3), SCORE RANKING/CHARACTER CONTEST (0x245EE), créditos da equipe (0x25800–0x25CB8), textos das fases (0x30476–0x34900: ROUND n START/BOSS/CLEAR + nomes dos chefes).
- Há também um relatório de símbolos do compilador (0x38000, "Global Cross Reference Report") com nomes de rotinas e variáveis: útil para engenharia reversa.
- Ainda a verificar: (1) se os textos têm ponteiros (podem ser maiores que o original) ou ocupam espaço fixo; (2) se a fonte do jogo tem acentos (ã, ç, é...) — nas capturas parece só caixa alta/baixa sem acento; (3) o que é gráfico e não texto (logos, "ROUND n START" pode ser desenhado por sprites; "Press Start" rosa).
