# -*- coding: utf-8 -*-
"""Aplica traducoes (mesmo lugar, mesmo tamanho) no u45 e monta o zip/pasta de teste para o MAME.
uso: python tools/patch_u45.py [arquivo_de_traducao.tsv] [saida_dir]
tsv: offset_hex<TAB>texto   (texto em latin-1; mais curto que o original e completado com espacos)"""
import sys, zipfile, re, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
ORIG = ROOT / "00_Original/sailormnu/bpsm945a.u45"

def unswap(b):
    o = bytearray(len(b)); o[0::2], o[1::2] = b[1::2], b[0::2]; return o

def orig_len(d, off):
    n = 0
    while 0x20 <= d[off + n] < 0x7F: n += 1
    return n

def apply(d, items, report=True):
    for off, txt in items:
        n = orig_len(d, off)
        b = txt.encode("latin-1")
        if len(b) > n:
            raise SystemExit("%05X: '%s' tem %d bytes, o original tem %d" % (off, txt, len(b), n))
        d[off:off + n] = b + b" " * (n - len(b))
    return d

def fix_checksum(d):
    """o teste do boot ("Program ROM ... Good") exige soma de todos os bytes = 0 (mod 65536), como na ROM original.
    Compensa a troca de textos baixando bytes do bloco vazio (todo FF) a partir de 0x60000."""
    k = sum(d) & 0xFFFF
    if k == 0: return 0
    base = 0x60000
    if any(v != 0xFF for v in d[base:base + 0x1000]): raise SystemExit("bloco 0x60000 nao e preenchimento FF")
    left, i = k, base
    while left > 0:
        dec = min(255, left); d[i] = 0xFF - dec; left -= dec; i += 1
    assert sum(d) & 0xFFFF == 0
    return k

def write_set(d, outdir):
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    src = ROOT / "00_Original/sailormnu"
    for f in src.iterdir():
        if f.name != "bpsm945a.u45": shutil.copy2(f, outdir / f.name)
    (outdir / "bpsm945a.u45").write_bytes(bytes(unswap(d)))   # trocar de novo = destrocar

if __name__ == "__main__":
    d = unswap(ORIG.read_bytes())
    items = []
    tsv = sys.argv[1] if len(sys.argv) > 1 else None
    if tsv:
        for line in open(tsv, encoding="utf-8"):
            if line.strip() and not line.startswith("#"):
                o, t = line.rstrip("\n").split("\t", 1); items.append((int(o, 16), t))
    apply(d, items)
    write_set(d, sys.argv[2] if len(sys.argv) > 2 else ROOT / "01_ROM/teste")
    print(len(items), "textos aplicados")
