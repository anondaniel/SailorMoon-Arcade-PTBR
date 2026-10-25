# -*- coding: utf-8 -*-
"""Gera o patch BPS (u45 original -> u45 traduzido) e confere: aplica o BPS e o IPS e compara com o arquivo traduzido.
uso: python tools/gerar_bps.py   (le 00_Original/sailormnu/bpsm945a.u45 e 01_ROM/ptbr/bpsm945a.u45, grava em 07_Publicacao/patch/)"""
import zlib
from pathlib import Path

R = Path(__file__).resolve().parents[1]
ORIG = R / '00_Original/sailormnu/bpsm945a.u45'
NOVO = R / '01_ROM/ptbr/bpsm945a.u45'
IPS = R / '01_ROM/ptbr/sailormnu_ptbr_u45.ips'
SAIDA = R / '07_Publicacao/patch'


def varint(x):
    out = bytearray()
    while True:
        b = x & 0x7F; x >>= 7
        if x == 0:
            out.append(0x80 | b); return bytes(out)
        out.append(b); x -= 1


def le_varint(d, p):
    x = 0; shift = 1
    while True:
        b = d[p]; p += 1
        x += (b & 0x7F) * shift
        if b & 0x80: return x, p
        shift <<= 7; x += shift


def crc(b): return zlib.crc32(b) & 0xFFFFFFFF


def cria(o, n):
    assert len(o) == len(n)
    out = bytearray(b'BPS1') + varint(len(o)) + varint(len(n)) + varint(0)
    i = 0
    while i < len(n):
        j = i
        if o[i] == n[i]:
            while j < len(n) and o[j] == n[j]: j += 1
            out += varint(((j - i - 1) << 2) | 0)                 # SourceRead
        else:
            while j < len(n) and o[j] != n[j]: j += 1
            out += varint(((j - i - 1) << 2) | 1) + n[i:j]        # TargetRead
        i = j
    out += crc(o).to_bytes(4, 'little') + crc(n).to_bytes(4, 'little')
    out += crc(bytes(out)).to_bytes(4, 'little')
    return bytes(out)


def aplica_bps(p, o):
    assert p[:4] == b'BPS1'
    assert crc(p[:-4]) == int.from_bytes(p[-4:], 'little'), 'CRC do patch'
    ss, q = le_varint(p, 4); ts, q = le_varint(p, q); ms, q = le_varint(p, q); q += ms
    assert ss == len(o) and crc(o) == int.from_bytes(p[-12:-8], 'little'), 'origem diferente do esperado'
    out = bytearray(); fim = len(p) - 12
    while q < fim:
        v, q = le_varint(p, q); modo = v & 3; n = (v >> 2) + 1
        if modo == 0: out += o[len(out):len(out) + n]
        elif modo == 1: out += p[q:q + n]; q += n
        else: raise ValueError('acao nao usada por este gerador')
    assert len(out) == ts and crc(bytes(out)) == int.from_bytes(p[-8:-4], 'little'), 'resultado nao confere'
    return bytes(out)


def aplica_ips(ips, o):
    b = bytearray(o); assert ips[:5] == b'PATCH'; p = 5
    while ips[p:p + 3] != b'EOF':
        off = int.from_bytes(ips[p:p + 3], 'big'); sz = int.from_bytes(ips[p + 3:p + 5], 'big'); p += 5
        if sz == 0:
            rl = int.from_bytes(ips[p:p + 2], 'big'); b[off:off + rl] = bytes([ips[p + 2]]) * rl; p += 3
        else:
            b[off:off + sz] = ips[p:p + sz]; p += sz
    return bytes(b)


if __name__ == '__main__':
    o = ORIG.read_bytes(); n = NOVO.read_bytes()
    SAIDA.mkdir(parents=True, exist_ok=True)
    bps = cria(o, n)
    assert aplica_bps(bps, o) == n
    ips = IPS.read_bytes(); assert aplica_ips(ips, o) == n
    (SAIDA / 'SailorMoon_Arcade_PTBR_u45.bps').write_bytes(bps)
    (SAIDA / 'SailorMoon_Arcade_PTBR_u45.ips').write_bytes(ips)
    print('BPS %d bytes, IPS %d bytes; ambos reproduzem o u45 traduzido (CRC32 %08X) a partir do original (CRC32 %08X)' % (len(bps), len(ips), crc(n), crc(o)))
