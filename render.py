# render.py — Mesin gambar build-time (Pillow) untuk news-image-20261120.
#
# Dijalankan sekali saat build oleh Produksi: `python3 render.py`.
# File ini TIDAK diimpor main.py (grader menjalankan main.py tanpa Pillow),
# dan TIDAK memakai network, waktu, acak, atau subprocess — outputnya
# deterministik: piksel yang sama di setiap run menghasilkan byte PNG sama.
#
# Gaya gambar: poster koran satu halaman — header navy + judul emas, satu
# panel hero (ICJ), tiga panel menengah (Shenzhen, Berlin, Hormuz), satu
# strip cuaca (Akvan), lalu baris "also today" dan footer sumber.

import hashlib
import os
import sys

from PIL import Image, ImageDraw

import layout
from layout import (
    AKVAN,
    ALSO_Y,
    BERLIN,
    BLUE_SOFT,
    CARD,
    FOOTER_Y,
    GOLD,
    GOLD_LIGHT,
    GREY_LINE,
    HEADER_H,
    HEIGHT,
    HORMUZ,
    HERO,
    INK,
    MARGIN,
    MUTED,
    NAVY,
    NAVY_DARK,
    PAPER,
    RED,
    RED_SOFT,
    SUMMIT,
    TEAL,
    TEAL_DARK,
    WIDTH,
    load_fonts,
    text_block,
    wrap_text,
)
from news_data import ALSO_LINE, FOOTER, HEADER, STORIES


def card(draw, box, fill=CARD):
    """Kartu putih sudut membulat dengan garis tepi tipis.

    `box` berbentuk (x, y, lebar, tinggi) seperti konstanta di layout.py.
    """
    x, y, w, h = box
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=fill,
                           outline=GREY_LINE, width=2)


def head_block(draw, fonts, box, story, head_font_key, text_x, text_w):
    """Gambar kicker + headline di dalam satu panel; kembalikan y di bawahnya."""
    x, y, _w, _h = box
    y += 16
    draw.text((text_x, y), story["kicker"], font=fonts["kicker"], fill=MUTED)
    y += 24
    head_font = fonts[head_font_key]
    head_lines = wrap_text(draw, story["headline"], head_font, text_w)
    return text_block(draw, (text_x, y), head_lines, head_font, INK, 32)


def body_block(draw, fonts, story, body_font_key, x, y, text_w):
    """Gambar body di (x, y); kembalikan y di bawah blok body."""
    body_font = fonts[body_font_key]
    body_lines = wrap_text(draw, story["body"], body_font, text_w)
    leading = 25 if body_font_key == "body" else 23
    return text_block(draw, (x, y), body_lines, body_font, INK, leading)


def kicker_headline_body(draw, fonts, box, story, body_font_key, head_font_key,
                         text_x, text_w, art_x=None):
    """Gambar kicker + headline + body di dalam satu panel.

    Mengembalikan y di bawah blok body. Ilustrasi digambar terpisah oleh
    pemanggil di zona art_x (tidak pernah menimpa kolom teks).
    """
    y = head_block(draw, fonts, box, story, head_font_key, text_x, text_w)
    return body_block(draw, fonts, story, body_font_key, text_x, y + 8, text_w)


def draw_palace(draw, x0, y0, x1, y1):
    """Peace Palace Den Haag bergaya sederhana + timbangan keadilan."""
    cx = (x0 + x1) // 2
    # Timbangan di atas gedung.
    draw.line([(cx, y0 + 8), (cx, y0 + 52)], fill=NAVY, width=4)
    draw.line([(cx - 34, y0 + 18), (cx + 34, y0 + 18)], fill=NAVY, width=4)
    for sign in (-1, 1):
        px = cx + sign * 34
        draw.line([(px, y0 + 18), (px, y0 + 40)], fill=NAVY, width=3)
        draw.arc([px - 14, y0 + 36, px + 14, y0 + 62], 0, 180, fill=NAVY, width=3)
    # Badan gedung: atap segitiga, kolom, pintu.
    base_y = y1 - 12
    draw.polygon([(x0 + 8, y0 + 96), (x1 - 8, y0 + 96), (cx, y0 + 62)],
                 fill=RED, outline=NAVY)
    draw.rectangle([x0 + 8, y0 + 96, x1 - 8, base_y], fill=(213, 225, 235),
                   outline=NAVY, width=3)
    for i in range(4):
        col_x = x0 + 26 + i * 44
        draw.rectangle([col_x, y0 + 108, col_x + 16, base_y - 26],
                       fill=CARD, outline=NAVY, width=2)
    draw.rectangle([cx - 14, base_y - 40, cx + 14, base_y],
                   fill=NAVY_DARK, outline=NAVY)
    draw.rectangle([x0, base_y, x1, base_y + 12], fill=NAVY)


def draw_summit(draw, x0, y0, w):
    """Tiga bendera kecil di atas meja bundar dengan tiga siluet."""
    flag_w, flag_h = 80, 28
    gap = (w - 3 * flag_w) // 2
    fx = x0
    # Bendera AS: garis merah-putih + kanton biru.
    for i in range(7):
        color = RED if i % 2 == 0 else CARD
        draw.rectangle([fx, y0 + i * 4, fx + flag_w, y0 + i * 4 + 4], fill=color)
    draw.rectangle([fx, y0, fx + 32, y0 + 14], fill=(60, 90, 150))
    for dx, dy in ((8, 4), (20, 4), (14, 10)):
        draw.ellipse([fx + dx, y0 + dy, fx + dx + 4, y0 + dy + 4], fill=CARD)
    draw.rectangle([fx, y0, fx + flag_w, y0 + flag_h], outline=NAVY, width=2)
    # Bendera China: merah + bintang kuning.
    fx += flag_w + gap
    draw.rectangle([fx, y0, fx + flag_w, y0 + flag_h], fill=(222, 41, 16))
    for dx, dy in ((8, 5), (24, 4), (30, 12), (12, 14)):
        draw.ellipse([fx + dx, y0 + dy, fx + dx + 6, y0 + dy + 6], fill=GOLD_LIGHT)
    draw.rectangle([fx, y0, fx + flag_w, y0 + flag_h], outline=NAVY, width=2)
    # Bendera Rusia: tiga pita putih-biru-merah.
    fx += flag_w + gap
    for i, color in enumerate((CARD, (0, 91, 187), RED)):
        draw.rectangle([fx, y0 + i * 9, fx + flag_w, y0 + i * 9 + 10], fill=color)
    draw.rectangle([fx, y0, fx + flag_w, y0 + flag_h], outline=NAVY, width=2)
    # Meja bundar + tiga siluet (kepala + bahu).
    table_y = y0 + flag_h + 26
    cx = x0 + w // 2
    for i, suit in enumerate((NAVY, (90, 90, 96), (122, 30, 30))):
        hx = cx + (i - 1) * 72
        draw.ellipse([hx - 13, table_y - 26, hx + 13, table_y], fill=(232, 190, 150))
        draw.pieslice([hx - 24, table_y - 6, hx + 24, table_y + 30], 180, 360,
                      fill=suit)
    draw.ellipse([cx - 118, table_y - 2, cx + 118, table_y + 26],
                 fill=(176, 141, 87), outline=(120, 90, 50), width=2)


def draw_berlin_flags(draw, x0, y0):
    """Bendera Uni Eropa (lingkaran bintang) + bendera Ukraina."""
    # Uni Eropa.
    draw.rectangle([x0, y0, x0 + 116, y0 + 78], fill=(0, 51, 153),
                   outline=NAVY, width=2)
    import math

    ecx, ecy = x0 + 58, y0 + 39
    for i in range(12):
        angle = 2 * math.pi * i / 12 - math.pi / 2
        sx = ecx + int(26 * math.cos(angle))
        sy = ecy + int(26 * math.sin(angle))
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=GOLD_LIGHT)
    # Ukraina: biru di atas kuning.
    uy = y0 + 94
    draw.rectangle([x0, uy, x0 + 116, uy + 39], fill=(0, 91, 187))
    draw.rectangle([x0, uy + 39, x0 + 116, uy + 78], fill=(255, 213, 0))
    draw.rectangle([x0, uy, x0 + 116, uy + 78], outline=NAVY, width=2)


def draw_tanker(draw, x0, y0, x1, y1):
    """Tanker di laut dengan api di geladak dan satu ranjau laut."""
    sea_y = y1 - 88
    draw.rectangle([x0, sea_y, x1, y1], fill=(38, 90, 120))
    for wx in range(x0 + 8, x1 - 8, 26):
        draw.arc([wx, sea_y + 12, wx + 22, sea_y + 26], 180, 360,
                 fill=(160, 200, 220), width=2)
    # Lambung kapal + anjungan.
    draw.rectangle([x0 + 6, sea_y - 34, x1 - 6, sea_y + 2], fill=(40, 44, 50))
    draw.polygon([(x1 - 6, sea_y - 34), (x1 + 14, sea_y - 18), (x1 - 6, sea_y + 2)],
                 fill=(40, 44, 50))
    draw.rectangle([x0 + 18, sea_y - 62, x0 + 58, sea_y - 34], fill=CARD,
                   outline=NAVY, width=2)
    # Api oranye di atas anjungan + asap.
    ax = x0 + 38
    draw.polygon([(ax - 16, sea_y - 62), (ax, sea_y - 108), (ax + 16, sea_y - 62)],
                 fill=(240, 120, 20))
    draw.polygon([(ax - 8, sea_y - 62), (ax, sea_y - 88), (ax + 8, sea_y - 62)],
                 fill=(250, 200, 60))
    for dx, dy, r in ((24, -118, 10), (40, -132, 13), (10, -138, 9)):
        draw.ellipse([ax + dx - r, sea_y + dy - r, ax + dx + r, sea_y + dy + r],
                     fill=(120, 124, 128))
    # Ranjau laut: lingkaran hitam berduri di air.
    mx, my = x1 - 34, sea_y + 46
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1)):
        draw.line([(mx, my), (mx + dx * 18, my + dy * 18)], fill=INK, width=3)
    draw.ellipse([mx - 11, my - 11, mx + 11, my + 11], fill=INK)


def draw_spiral(draw, cx, cy):
    """Pusaran siklon: busur-busur konsentris yang berputar."""
    for i, radius in enumerate((14, 24, 34, 44, 54)):
        start = i * 55
        draw.arc([cx - radius, cy - radius, cx + radius, cy + radius],
                 start, start + 230, fill=(255, 255, 255), width=4)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=GOLD)


def build_image():
    """Rakit poster 1024x1024 dan kembalikan objek gambar Pillow."""
    fonts = load_fonts()
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(img)

    # --- Header navy: judul + tanggal besar. ---
    draw.rectangle([0, 0, WIDTH, HEADER_H], fill=NAVY)
    draw.rectangle([0, HEADER_H - 4, WIDTH, HEADER_H], fill=GOLD)
    title = HEADER["kicker"]
    tw = draw.textlength(title, font=fonts["title"])
    draw.text(((WIDTH - tw) / 2, 22), title, font=fonts["title"], fill=GOLD)
    date = HEADER["date"]
    dw = draw.textlength(date, font=fonts["date"])
    draw.text(((WIDTH - dw) / 2, 92), date, font=fonts["date"], fill=(255, 255, 255))

    by_id = {story["id"]: story for story in STORIES}

    # --- Panel hero: ICJ / Myanmar. ---
    hero = by_id["icj"]
    card(draw, HERO)
    draw.rectangle([HERO[0], HERO[1], HERO[0] + 8, HERO[1] + HERO[3]], fill=RED)
    end_y = kicker_headline_body(draw, fonts, HERO, hero, "body", "hero_head",
                                 HERO[0] + 26, 384)
    facts_lines = wrap_text(draw, hero["facts"], fonts["facts"], 384)
    text_block(draw, (HERO[0] + 26, end_y + 10), facts_lines,
               fonts["facts"], RED, 20)
    draw_palace(draw, HERO[0] + 424, HERO[1] + 22, HERO[0] + HERO[2] - 18,
                HERO[1] + HERO[3] - 18)

    # --- Panel Shenzhen: KTT tiga pihak. Ilustrasi di antara headline dan
    # body supaya tidak menimpa teks (perbaikan setelah cek visual v1). ---
    summit = by_id["shenzhen"]
    card(draw, SUMMIT, fill=BLUE_SOFT)
    head_y = head_block(draw, fonts, SUMMIT, summit, "head",
                        SUMMIT[0] + 24, SUMMIT[2] - 48)
    draw_summit(draw, SUMMIT[0] + 24, head_y + 6, SUMMIT[2] - 48)
    body_block(draw, fonts, summit, "body_small", SUMMIT[0] + 24,
               head_y + 94, SUMMIT[2] - 48)

    # --- Panel Berlin: koalisi pendukung Ukraina. ---
    berlin = by_id["berlin"]
    card(draw, BERLIN)
    kicker_headline_body(draw, fonts, BERLIN, berlin, "body", "head",
                         BERLIN[0] + 24, 300)
    draw_berlin_flags(draw, BERLIN[0] + 348, BERLIN[1] + 34)

    # --- Panel Hormuz: perang tanker. ---
    hormuz = by_id["hormuz"]
    card(draw, HORMUZ)
    kicker_headline_body(draw, fonts, HORMUZ, hormuz, "body_small", "head",
                         HORMUZ[0] + 24, 268)
    draw_tanker(draw, HORMUZ[0] + 312, HORMUZ[1] + 30,
                HORMUZ[0] + HORMUZ[2] - 20, HORMUZ[1] + HORMUZ[3] - 24)

    # --- Strip Akvan: siklon mendarat hari ini. ---
    akvan = by_id["akvan"]
    ax0, ay0, aw, ah = AKVAN
    draw.rounded_rectangle([ax0, ay0, ax0 + aw, ay0 + ah], radius=10, fill=TEAL)
    draw_spiral(draw, AKVAN[0] + 76, AKVAN[1] + AKVAN[3] // 2)
    ax = AKVAN[0] + 168
    ay = AKVAN[1] + 18
    draw.text((ax, ay), akvan["kicker"], font=fonts["kicker"], fill=GOLD_LIGHT)
    head_lines = wrap_text(draw, akvan["headline"], fonts["strip_head"],
                           AKVAN[2] - 192)
    ay = text_block(draw, (ax, ay + 24), head_lines, fonts["strip_head"],
                    (255, 255, 255), 34)
    body_lines = wrap_text(draw, akvan["body"], fonts["body_small"],
                           AKVAN[2] - 192)
    text_block(draw, (ax, ay + 8), body_lines, fonts["body_small"],
               (220, 235, 235), 23)

    # --- Baris "also today" + footer sumber. ---
    draw.text((MARGIN, ALSO_Y), ALSO_LINE, font=fonts["also"], fill=INK)
    draw.text((MARGIN, FOOTER_Y), FOOTER, font=fonts["footer"], fill=MUTED)

    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "entry.png")
    img = build_image()
    img.save(out_path, format="PNG")
    size = os.path.getsize(out_path)
    with open(out_path, "rb") as handle:
        digest = hashlib.sha256(handle.read()).hexdigest()
    print("entry.png: %dx%d, %d bytes, sha256: %s" % (WIDTH, HEIGHT, size, digest))
    if img.size != (WIDTH, HEIGHT):
        print("GAGAL: ukuran bukan 1024x1024", file=sys.stderr)
        return 1
    if size > 1048576:
        print("GAGAL: ukuran melebihi 1 MiB", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
