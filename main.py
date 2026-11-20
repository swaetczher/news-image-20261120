# main.py — Entrypoint kompetisi news-image-20261120 (Make Fun, $250).
#
# Program ini HANYA memakai pustaka standar Python: ia menyalin gambar
# `entry.png` (1024x1024, sudah dirender saat build dan disimpan di repo)
# ke `--output` (default `/output/entry.png`), lalu memverifikasi gambar
# hasil salinan itu: tanda tangan PNG, dimensi dari header IHDR, ukuran
# maksimal 1 MiB, dan sha256 yang sama dengan sumber. Dua kali jalan
# menghasilkan byte yang identik, karena sumbernya satu file yang sama dan
# tidak ada network, waktu, acak, atau subprocess di sini.
#
# File ini sengaja TIDAK mengimpor PIL, render.py, news_data.py, atau
# layout.py — grader menjalankan main.py di python:3.13-slim tanpa Pillow,
# dan program harus tetap jalan (exit 0) meski modul PIL tidak ada.
#
# Catatan isi gambar (cek kilat Produksi 20 Nov 2026 ~07:25 WIB, sebelum
# render final): pendaratan Siklon Akvan belum terkonfirmasi saat render,
# jadi strip cuaca memakai label netral "LANDFALL TODAY"; respons resmi
# Myanmar belum ada, yang dicatat hanya langkah Inggris soal Dewan Keamanan.

import argparse
import hashlib
import os
import struct
import sys

MAX_BYTES = 1048576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def read_png_size(data):
    """Baca lebar dan tinggi dari header IHDR sebuah file PNG."""
    if len(data) < 33 or data[:8] != PNG_SIGNATURE:
        raise ValueError("bukan file PNG yang valid")
    if data[12:16] != b"IHDR":
        raise ValueError("chunk IHDR tidak ditemukan")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Salin entry.png ke /output/entry.png dan verifikasi.")
    parser.add_argument(
        "--output", default="/output/entry.png",
        help="jalur file gambar hasil (default: /output/entry.png)")
    args = parser.parse_args(argv)

    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    with open(source, "rb") as handle:
        data = handle.read()

    width, height = read_png_size(data)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print("GAGAL: ukuran gambar %dx%d, harus 1024x1024"
              % (width, height), file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print("GAGAL: ukuran file %d byte, melebihi 1 MiB" % len(data),
              file=sys.stderr)
        return 1

    digest = hashlib.sha256(data).hexdigest()
    out_dir = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(out_dir, exist_ok=True)
    with open(args.output, "wb") as handle:
        handle.write(data)
    with open(args.output, "rb") as handle:
        written_digest = hashlib.sha256(handle.read()).hexdigest()
    if written_digest != digest:
        print("GAGAL: sha256 hasil salinan tidak cocok dengan sumber",
              file=sys.stderr)
        return 1

    print("entry.png: %dx%d, %d bytes, sha256: %s"
          % (width, height, len(data), digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
