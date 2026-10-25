# Pretty Soldier Sailor Moon (PT-BR) no Switch (RetroArch + FBNeo)

Conjunto `sailormnu` (USA). O FBNeo tem esse conjunto (u45 original CRC 898C9515); o u45 traduzido tem CRC D429F659.
Mesmo esquema do Bucky O'Hare: **dois arquivos**.

## Copiar para o cartão SD (a pasta `SD/` deste pacote espelha o cartão)
| arquivo do pacote | destino no Switch |
|---|---|
| `SD/roms/arcade/sailormnu.zip` (14 MB, conjunto completo com o u45 traduzido) | `/roms/arcade/sailormnu.zip` |
| `SD/retroarch/cores/system/fbneo/patched/sailormnu.zip` (121 KB, só o u45 traduzido) | `/retroarch/cores/system/fbneo/patched/sailormnu.zip` |

O FBNeo ignora o CRC dos arquivos que vêm da pasta `patched` ("Allow patched romsets", ligado por padrão no core).
Não existe `sailormnu.zip` de outro jogo no Switch; não sobrescreve nada. (Se já houver um, faça backup.)
Dica MTP: o CopyHere não sobrescreve; para trocar um arquivo existente, mova o antigo para fora antes.

## Atalho na tela inicial (NSP Auto Installer Maker v2.8)
- Nome: `Sailor Moon (PT-BR)` — Publicador: `Daniel Figueira` — Ícone: `icone_sailormoon_256.jpg`
- Core: `/retroarch/cores/fbneo_libretro_libnx.nro`
- ROM: `/roms/arcade/sailormnu.zip`
- Gerar com um TID novo (o do Bucky é 058F8CC1B65EA000, o do Yu Yu 0585C7AE08516000) e instalar o `.nsp` com o DBI/Tinfoil.
Sem o atalho, dá para abrir pelo RetroArch: Carregar conteúdo > `/roms/arcade/sailormnu.zip` com o core FBNeo.

## Controles
Moeda = Select, Start = Start (padrão do RetroArch/FBNeo); 1–2 jogadores, 3 botões. Não há 3º jogador.

## Observação
Testado no Switch pelo Daniel (23/10/2026): jogo zerado, tradução funcionou 100%. No MAME: boot "Good", aviso, demo, fase 1, chefe.
