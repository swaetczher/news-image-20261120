# news_data.py — Isi gambar ringkasan berita dunia Jumat 20 November 2026.
#
# Sumber isi: riset.md job news-image-20261120 (5 berita utama, diverifikasi
# dari >=2 sumber) + cek kilat Produksi 20 Nov 2026 ~07:25 WIB via pencarian
# web teks: pendaratan Siklon Akvan BELUM terkonfirmasi (masih prakiraan siang
# ini) sehingga label tetap netral "LANDFALL TODAY"; Myanmar belum memberi
# respons resmi, Inggris mengusir atase pertahanan Myanmar dan meminta sidang
# Dewan Keamanan PBB (Le Monde, 20 Nov); tidak ada serangan Hormuz baru yang
# terverifikasi pada 20 Nov; Putin menolak gencatan senjata energi dan Laut
# Hitam (briefing konflik 20 Nov); operasi tank Gaza selesai 19 Nov.
#
# Aturan akurasi yang dipatuhi di semua label: klaim Iran soal 3 tanker kena
# ranjau ditulis "CLAIMS" (belum terverifikasi); reparasi Myanmar ditulis
# "ordered", bukan dibayar; tidak ada klaim kesepakatan Ukraina atau batas
# nuklir dari KTT Shenzhen (tidak ada); jaminan keamanan Berlin ditulis
# sebagai usulan, bukan sudah berlaku; tidak ada tanggal 19 Nov di gambar.

HEADER = {
    "kicker": "THE WORLD IN ONE DAY",
    "date": "FRIDAY, 20 NOVEMBER 2026",
}

# Setiap cerita: kicker kecil, headline besar, body 1-2 kalimat pendek.
# "art" memilih ilustrasi vektor yang digambar render.py untuk panel itu.
STORIES = [
    {
        "id": "icj",
        "kicker": "THE HAGUE  ·  WORLD COURT",
        "headline": "MYANMAR GUILTY OF GENOCIDE",
        "body": (
            "The world court finds Myanmar responsible for genocide "
            "against the Rohingya - a first for any state. Myanmar has "
            "not replied; the UK seeks a UN Security Council session."
        ),
        "facts": "VOTE 9-6  ·  ABOUT 10,000 KILLED  ·  REPARATIONS ORDERED",
        "art": "palace",
    },
    {
        "id": "shenzhen",
        "kicker": "SHENZHEN  ·  SUMMIT",
        "headline": "TRUMP, XI AND PUTIN MEET",
        "body": (
            "First-ever three-way summit issues a 4-point "
            "'Declaration Towards Peace' - no mention of Ukraine, "
            "no nuclear limits."
        ),
        "facts": "",
        "art": "summit",
    },
    {
        "id": "berlin",
        "kicker": "BERLIN  ·  UKRAINE",
        "headline": "ALLIES BACK KYIV: 70BN EUROS",
        "body": (
            "Coalition of the Willing pledges 70bn euros in military "
            "aid for 2026 and urges a winter energy ceasefire. Putin "
            "rejects energy and Black Sea ceasefires."
        ),
        "facts": "",
        "art": "berlin",
    },
    {
        "id": "hormuz",
        "kicker": "STRAIT OF HORMUZ  ·  TANKER WAR",
        "headline": "TANKER WAR ESCALATES",
        "body": (
            "About 14 attacks in November. ADNOC ship hit: 11 hurt, "
            "1 missing. Iran CLAIMS 3 more tankers mined - unverified. "
            "India condemns the Tara Gas attack: 1 missing, 2 hurt."
        ),
        "facts": "",
        "art": "tanker",
    },
    {
        "id": "akvan",
        "kicker": "BAY OF BENGAL  ·  CYCLONE AKVAN",
        "headline": "CYCLONE AKVAN MAKES LANDFALL TODAY",
        "body": (
            "Red alert on India's east coast. Tens of thousands "
            "evacuated. Winds 90-100 km/h, gusts to 110 km/h. "
            "Landfall expected near Gopalpur, Odisha, around noon."
        ),
        "facts": "",
        "art": "cyclone",
    },
]

ALSO_LINE = (
    "ALSO TODAY: Gaza tank raid ends, main road reopens  ·  "
    "Kerch rail link partly reopens"
)

FOOTER = (
    "Sources: ICJ  ·  White House  ·  German Government  ·  "
    "UKMTO / Bloomberg  ·  IMD  ·  Reuters  —  Illustrated summary, not a photograph."
)
