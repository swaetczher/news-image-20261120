# layout.py — Konstanta layout 1024x1024 + helper teks untuk render.py.
#
# Semua angka di sini dipilih agar teks tetap terbaca saat gambar dilihat
# pada lebar sekitar 300 piksel: headline panel minimal 24 px, body minimal
# 18 px, dan tidak ada blok teks yang lebih dari 5 baris. Tidak ada waktu,
# acak, network, atau subprocess di file ini.

WIDTH = 1024
HEIGHT = 1024

# Palet poster koran: navy gelap untuk header, kertas krem untuk latar,
# emas untuk judul, merah bata untuk aksen hero, teal gelap untuk strip cuaca.
NAVY = (14, 42, 71)
NAVY_DARK = (9, 30, 52)
GOLD = (212, 175, 90)
GOLD_LIGHT = (232, 205, 130)
PAPER = (247, 242, 231)
CARD = (255, 255, 255)
INK = (24, 28, 34)
MUTED = (92, 98, 108)
RED = (168, 44, 34)
RED_SOFT = (246, 231, 227)
BLUE_SOFT = (231, 238, 245)
TEAL = (13, 74, 79)
TEAL_DARK = (9, 54, 58)
GREY_LINE = (203, 209, 216)

MARGIN = 24
GAP = 16
HEADER_H = 148

# Geometri panel (x, y, lebar, tinggi), dihitung dari atas ke bawah.
HERO = (MARGIN, HEADER_H + MARGIN, 640, 296)
SUMMIT = (MARGIN + 640 + GAP, HEADER_H + MARGIN, 312, 296)
BERLIN = (MARGIN, HEADER_H + MARGIN + 296 + GAP, 496, 264)
HORMUZ = (MARGIN + 496 + GAP, HEADER_H + MARGIN + 296 + GAP, 460, 264)
AKVAN = (MARGIN, HEADER_H + MARGIN + 296 + GAP + 264 + GAP, 976, 148)
ALSO_Y = HEADER_H + MARGIN + 296 + GAP + 264 + GAP + 148 + 12
FOOTER_Y = ALSO_Y + 34

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = FONT_DIR + "/DejaVuSerif-Bold.ttf"
SANS_BOLD = FONT_DIR + "/DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "/DejaVuSans.ttf"


def load_fonts():
    """Muat font DejaVu ukuran tetap; ukuran sama di setiap run."""
    from PIL import ImageFont

    return {
        "title": ImageFont.truetype(SERIF_BOLD, 52),
        "date": ImageFont.truetype(SANS_BOLD, 28),
        "kicker": ImageFont.truetype(SANS_BOLD, 15),
        "hero_head": ImageFont.truetype(SERIF_BOLD, 33),
        "head": ImageFont.truetype(SERIF_BOLD, 25),
        "strip_head": ImageFont.truetype(SERIF_BOLD, 27),
        "body": ImageFont.truetype(SANS, 19),
        "body_small": ImageFont.truetype(SANS, 18),
        "facts": ImageFont.truetype(SANS_BOLD, 15),
        "also": ImageFont.truetype(SANS_BOLD, 17),
        "footer": ImageFont.truetype(SANS, 14),
    }


def wrap_text(draw, text, font, max_width):
    """Bungkus teks per kata berdasarkan lebar terukur font.

    Mengembalikan daftar baris; kata yang lebih lebar dari max_width
    dibiarkan utuh di barisnya sendiri (tidak ada kata yang dipotong).
    """
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=font) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def text_block(draw, xy, lines, font, fill, leading):
    """Gambar daftar baris dari (x, y); kembalikan y setelah baris terakhir."""
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y
