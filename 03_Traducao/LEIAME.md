# Pretty Soldier Sailor Moon (arcade) — tradução PT-BR (só texto, ASCII sem acentos)

Base: conjunto MAME `sailormnu` (USA, em inglês). Só o programa 68000 `bpsm945a.u45` muda (70 textos, mesmo lugar e mesmo tamanho).

## Usar
- **MAME:** `01_ROM/ptbr/sailormnu.zip` no lugar do `sailormnu.zip` (ou o patch `sailormnu_ptbr_u45.ips` no `bpsm945a.u45` original, CRC32 898C9515 -> D429F659). O MAME avisa "ROM com checksum diferente" e roda normalmente.
- O teste de memória do boot mostra "Program ROM ... Good" (a soma dos bytes do arquivo foi corrigida: `tools/patch_u45.py fix_checksum`).
- Em FBNeo/RetroArch (Switch) usar o mesmo esquema do Bucky O'Hare (zip completo + zip diff na pasta `patched`) — testado no Switch (RetroArch/FBNeo): jogo zerado, tradução 100% (informado em 23/10/2026).

## Refazer
`python 03_Traducao/traducao_ptbr.py` (lê `00_Original/sailormnu/`, grava `01_ROM/ptbr/`). Para mudar um texto, edite o dicionário `T`; o texto novo não pode passar do tamanho do original (é completado com espaços).

## Regras do jogo descobertas
- Texto = ASCII no `u45` com os bytes trocados dois a dois; cadeias terminadas em NUL e coladas umas nas outras (sem folga).
- **Letras acentuadas não funcionam:** bytes >= 0x80 são lidos como caracteres japoneses e desenham lixo na tela. Por isso não há acentos.
- Soma de todos os bytes do `u45` precisa dar 0 (mod 65536) para o boot dizer "Good".

## Traduzido (70)
Interface (Cred., Insira Ficha, Pulse Start, Selecione, Continua?, Aguarde..., Seu Nome, RECORDES, POPULARIDADE), aviso legal (Aviso ...), fases (FASE n COMECA / CHEFE / ZERADA, FASE FINAL, OS 4 GRANDES, ULTIMO CHEFE) e cargos dos créditos da equipe.
## Não traduzido
Nomes de pessoas, nomes dos chefes e das heroínas, golpes de teste (só aparecem no modo de teste), menus de teste/configuração do operador, logos (gráficos).
