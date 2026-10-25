# -*- coding: utf-8 -*-
"""Traducao PT-BR (ASCII, sem acentos: o jogo trata bytes >= 0x80 como caracteres japoneses e desenha lixo).
Cada texto troca o original NO MESMO LUGAR e fica do mesmo tamanho (completado com espacos): os textos de UI sao
chamados por LEA relativo ao PC e os das fases ficam dentro dos scripts de fase.

python 03_Traducao/traducao_ptbr.py   ->  01_ROM/ptbr/ (conjunto de ROMs para o MAME) + relatorio
"""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import patch_u45 as P

# (inicio, fim) das regioes onde se procura cada texto (NUL antes e depois)
REG = [(0x06400, 0x06600), (0x23840, 0x23940), (0x245E0, 0x24640), (0x25700, 0x25CE0), (0x30400, 0x34920)]

T = {
    # interface
    "Credit ": "Cred. ", "Credits ": "Creds. ", "Free Play": "Gratis",
    "Deposit Coin": "Insira Ficha", "Press Start": "Pulse Start", "Select Player": "Selecione",
    "Continue? ": "Continua? ", "Wait Please...": "Aguarde...", "Name Entry": "Seu Nome",
    "SCORE RANKING": "RECORDES", "CHARACTER CONTEST": "POPULARIDADE",
    # aviso legal (as linhas seguem a ordem do original)
    "Notice": "Aviso",
    "This game is for use": "Este jogo e para uso",
    "exclusively in ": "unicamente nos ",
    "The sale, export, use or operation": "Venda, exportacao, uso ou operacao",
    "of this outside of ": "disto fora dos ",
    "may be a violation of": "pode violar leis",
    "international copyright, trademark": "internacionais de direito autoral,",
    "or other related laws subjecting": "e marcas ou outras leis afins,",
    "the violator to legal penalties.": "com penas legais ao infrator.",
    # fases
    "THE BIG FOUR": "OS 4 GRANDES", "THE LAST BOSS": "ULTIMO CHEFE",
    "FINAL ROUND START": "FASE FINAL COMECA", "FINAL ROUND CLEAR": "FASE FINAL ZERADA",
    # creditos da equipe (so os cargos; os nomes nao se traduzem)
    "Video Game Staff": "Equipe do Jogo", "Supervisor": "Supervisao", "Also Supervisor": "Co-Supervisao",
    "Executive Producer": "Produtor Executivo", "Producer": "Produtor", "Total Co-ordinator": "Coordenacao Geral",
    "Director": "Diretor", "Art Director": "Dir. de Arte", "Art Co-director": "Co-dir. de Arte",
    "Graphic Designer": "Designer Grafico", "Animation Director": "Direcao Animacao",
    "Animation Art Director": "Dir. Arte Animacao", "Animator": "Animador",
    "Animation Digitizer": "Digitalizador Anim.", "Music Composer": "Compositor",
    "Character Voice": "Elenco de Voz", "Sound Effect": "Efeitos Sons",
    "Hardware Supervisor": "Superv. Hardware", "Hardware Co-ordinator": "Coord. Hardware",
    "Hardware Designer": "Projeto Hardware", "All Program Works by": "Toda Programacao",
    "Special Thanks to": "Agradecimentos", "Game Designer": "Game Design",
    "Developped by Gazelle Co.,Ltd. 1995": "Desenv. por Gazelle Co.,Ltd. 1995",
    "Produced by Banpresto Co.,Ltd. 1995": "Producao Banpresto Co.,Ltd. 1995",
}
for n in range(1, 8):
    T["ROUND %d START" % n] = "FASE %d COMECA" % n
    T["ROUND %d BOSS" % n] = "FASE %d CHEFE" % n
    T["ROUND %d CLEAR" % n] = "FASE %d ZERADA" % n


def collect(d):
    items, missing = [], []
    for en, pt in T.items():
        b = en.encode("ascii")
        if len(pt) > len(en):
            raise SystemExit("'%s' -> '%s' passa do tamanho" % (en, pt))
        found = False
        for a, z in REG:
            for m in re.finditer(re.escape(b) + b"\x00", bytes(d[a:z])):
                off = a + m.start()
                # so no inicio de uma cadeia (byte anterior e NUL ou nao imprimivel)
                if off == 0 or not (0x20 <= d[off - 1] < 0x7F) or d[off - 2:off] == b"Nu":   # 'Nu' = RTS (4E75) colado no texto
                    items.append((off, pt)); found = True
        if not found: missing.append(en)
    return items, missing


if __name__ == "__main__":
    d = P.unswap(P.ORIG.read_bytes())
    items, missing = collect(d)
    P.apply(d, items)
    print("soma corrigida em", P.fix_checksum(d), "bytes")
    out = ROOT / "01_ROM" / "ptbr"
    P.write_set(d, out)
    print("%d trocas aplicadas em %d textos; sem ocorrencia: %s" % (len(items), len(T) - len(missing), missing))
    print("conjunto em", out)
