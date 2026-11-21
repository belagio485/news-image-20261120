# news-image-20261120 -- "The World in One Day"
# A newspaper front page summing up Friday 20 November 2026.
# Drawn from scratch with the Python standard library only: no network,
# no files read, no clock, no randomness. Two runs write identical bytes.
# Output: /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png locally).
import os
import struct
import zlib

W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (185, 28, 28)
DARK = (22, 35, 63)
GREY = (120, 120, 116)
LIGHT = (226, 220, 205)
GOLD = (212, 160, 32)
BLUE = (36, 84, 160)
SKY = (140, 175, 215)
ORANGE = (232, 120, 32)
YELLOW = (245, 200, 60)
GREEN = (34, 120, 60)

# 5x7 bitmap font, one glyph per character. '#' is on, ' ' is off.
FONT = {
    'A': (" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    'B': ("#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "),
    'C': (" ####", "#    ", "#    ", "#    ", "#    ", "#    ", " ####"),
    'D': ("#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "),
    'E': ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"),
    'F': ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "),
    'G': (" ####", "#    ", "#    ", "# ###", "#   #", "#   #", " ### "),
    'H': ("#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    'I': ("#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "#####"),
    'J': ("  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "),
    'K': ("#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"),
    'L': ("#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"),
    'M': ("#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"),
    'N': ("#   #", "##  #", "##  #", "# # #", "#  ##", "#  ##", "#   #"),
    'O': (" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    'P': ("#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "),
    'Q': (" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"),
    'R': ("#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"),
    'S': (" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "),
    'T': ("#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "),
    'U': ("#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    'V': ("#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "),
    'W': ("#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"),
    'X': ("#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"),
    'Y': ("#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "),
    'Z': ("#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"),
    '0': (" ### ", "#  ##", "# # #", "##  #", "#   #", "#   #", " ### "),
    '1': ("  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    '2': (" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"),
    '3': ("#### ", "    #", "    #", " ### ", "    #", "    #", "#### "),
    '4': ("   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "),
    '5': ("#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "),
    '6': (" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "),
    '7': ("#####", "    #", "   # ", "   # ", "  #  ", "  #  ", "  #  "),
    '8': (" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "),
    '9': (" ### ", "#   #", "#   #", " ####", "    #", "    #", " ### "),
    ' ': ("     ", "     ", "     ", "     ", "     ", "     ", "     "),
    '.': ("     ", "     ", "     ", "     ", "     ", " ##  ", " ##  "),
    ',': ("     ", "     ", "     ", "     ", " ##  ", " ##  ", " #   "),
    ':': ("     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", "     "),
    ';': ("     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", " #   "),
    '!': ("  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "),
    '?': (" ### ", "#   #", "    #", "   # ", "  #  ", "     ", "  #  "),
    "'": ("  #  ", "  #  ", " #   ", "     ", "     ", "     ", "     "),
    '-': ("     ", "     ", "     ", "#####", "     ", "     ", "     "),
    '/': ("    #", "    #", "   # ", "  #  ", " #   ", "#    ", "#    "),
    '%': ("##  #", "## # ", "   # ", "  #  ", " #   ", "# ## ", "#  ##"),
    '(': ("   # ", "  #  ", " #   ", " #   ", " #   ", "  #  ", "   # "),
    ')': (" #   ", "  #  ", "   # ", "   # ", "   # ", "  #  ", " #   "),
    '&': (" ##  ", "#  # ", "#  # ", " #   ", "# # #", "#  # ", " ## #"),
    '+': ("     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "),
    '=': ("     ", "     ", "#####", "     ", "#####", "     ", "     "),
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg[0] for _ in range(w * h * 3))
        for i in range(w * h):
            self.px[i * 3:i * 3 + 3] = bytes(bg)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, c)

    def frame(self, x, y, w, h, c, t=2):
        self.rect(x, y, w, t, c)
        self.rect(x, y + h - t, w, t, c)
        self.rect(x, y, t, h, c)
        self.rect(x + w - t, y, t, h, c)

    def line(self, x0, y0, x1, y1, c):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, c)

    def tri(self, x0, y0, x1, y1, x2, y2, c):
        # filled triangle by scanline interpolation
        pts = sorted([(x0, y0), (x1, y1), (x2, y2)], key=lambda p: p[1])
        (ax, ay), (bx, by), (cx, cy) = pts
        for y in range(ay, cy + 1):
            if y <= by:
                t1 = (y - ay) / max(1, by - ay)
                xa = ax + (bx - ax) * t1
            else:
                xa = bx
            t2 = (y - ay) / max(1, cy - ay)
            xb = ax + (cx - ax) * t2
            lo, hi = int(min(xa, xb)), int(max(xa, xb))
            for x in range(lo, hi + 1):
                self.set(x, y, c)

    def text(self, x, y, s, scale, c, bold=False):
        cx = x
        for ch in s:
            g = FONT.get(ch, FONT[' '])
            for r in range(7):
                for col in range(5):
                    if g[r][col] == '#':
                        self.rect(cx + col * scale, y + r * scale,
                                  scale, scale, c)
                        if bold:
                            self.rect(cx + col * scale + 1, y + r * scale,
                                      scale, scale, c)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale

    def text_center(self, y, s, scale, c, bold=False):
        x = (self.w - self.text_w(s, scale)) // 2
        self.text(x, y, s, scale, c, bold)

    def wrap(self, s, scale, max_w):
        lines, cur = [], ""
        for word in s.split(" "):
            trial = (cur + " " + word).strip()
            if self.text_w(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines


def write_png(path, cv):
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 6)

    def chunk(typ, data):
        out = struct.pack(">I", len(data)) + typ + data
        out += struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


# ---- pictograms (flat, drawn shapes only) ----

def draw_kyiv(cv, x, y, w, h):
    cv.rect(x, y, w, h, DARK)
    for i in range(46):  # fixed stars, no randomness
        sx = x + (i * 97) % w
        sy = y + (i * 53) % (h // 2)
        cv.set(sx, sy, (200, 200, 220))
    cv.circle(x + w - 90, y + 42, 20, (235, 230, 200))  # moon
    base = y + h - 30
    # skyline silhouettes, fixed heights
    heights = [120, 80, 150, 95, 170, 70, 130, 105, 160, 85, 140, 100]
    bw = w // len(heights)
    for i, bh in enumerate(heights):
        bx = x + i * bw
        cv.rect(bx + 2, base - bh, bw - 4, bh, (10, 12, 20))
        for wy in range(base - bh + 12, base - 8, 22):
            for wx in range(bx + 8, bx + bw - 8, 16):
                if (wx + wy) % 3 == 0:
                    cv.rect(wx, wy, 4, 6, YELLOW)
    # explosion bursts
    for ex, ey in ((x + 300, y + 78), (x + 690, y + 60)):
        cv.circle(ex, ey, 30, ORANGE)
        cv.circle(ex, ey, 16, YELLOW)
        for a in range(8):
            import math
            dx = int(44 * math.cos(a * 0.785))
            dy = int(44 * math.sin(a * 0.785))
            cv.line(ex, ey, ex + dx, ey + dy, ORANGE)
    # smoke columns
    for sx, sy, r in ((x + 300, y + 40, 14), (x + 690, y + 26, 12),
                      (x + 520, y + 30, 10)):
        cv.circle(sx, sy, r, GREY)
    # river and bridge
    cv.rect(x, base, w, 30, (28, 60, 110))
    cv.line(x + 120, base, x + 120, base - 46, INK)
    cv.line(x + w - 140, base, x + w - 140, base - 46, INK)
    cv.line(x + 120, base - 8, x + w - 140, base - 8, (230, 230, 230))


def draw_court(cv, x, y, w, h):
    cv.rect(x, y, w, h, LIGHT)
    cx = x + w // 2
    cv.tri(cx - 70, y + 16, cx + 70, y + 16, cx, y + 2, INK)
    for i in range(3):
        px = cx - 52 + i * 52
        cv.rect(px, y + 18, 10, 26, INK)
    cv.rect(cx - 70, y + 44, 140, 6, INK)
    cv.line(x + 10, y + 50, x + w - 10, y + 50, RED)


def draw_chart(cv, x, y, w, h):
    cv.rect(x, y, w, h, (255, 255, 255))
    cv.line(x + 8, y + h - 8, x + w - 8, y + h - 8, INK)
    cv.line(x + 8, y + 6, x + 8, y + h - 8, INK)
    pts = [(x + 20, y + 10), (x + 120, y + 16), (x + 220, y + 14),
           (x + 320, y + 30), (x + 420, y + 46)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        cv.line(ax, ay, bx, by, RED)
        cv.line(ax, ay + 1, bx, by + 1, RED)
    ex, ey = pts[-1]
    cv.tri(ex, ey, ex - 14, ey - 4, ex - 14, ey + 6, RED)
    cv.text(x + w - 110, y + 4, "-5.3%", 3, RED, bold=True)


def draw_flags(cv, x, y, w, h):
    cv.rect(x, y, w, h, LIGHT)
    fw, fh = 130, 40
    fx, fy = x + 60, y + 7
    cv.rect(fx, fy, fw, fh, BLUE)  # union jack, simplified
    cv.line(fx, fy, fx + fw, fy + fh, (255, 255, 255))
    cv.line(fx + fw, fy, fx, fy + fh, (255, 255, 255))
    cv.rect(fx + fw // 2 - 5, fy, 10, fh, (255, 255, 255))
    cv.rect(fx, fy + fh // 2 - 5, fw, 10, (255, 255, 255))
    cv.rect(fx + fw // 2 - 3, fy, 6, fh, RED)
    cv.rect(fx, fy + fh // 2 - 3, fw, 6, RED)
    ex = x + w - 60 - fw
    cv.rect(ex, fy, fw, fh, BLUE)  # eu flag
    import math
    for k in range(8):
        dx = int(14 * math.cos(k * 0.785))
        dy = int(12 * math.sin(k * 0.785))
        cv.circle(ex + fw // 2 + dx, fy + fh // 2 + dy, 3, GOLD)


def draw_gaza(cv, x, y, w, h):
    cv.rect(x, y, w, h, (232, 214, 170))
    cv.circle(x + w - 50, y + 14, 10, YELLOW)
    for i, tx in enumerate((x + 60, x + 180, x + 300)):
        cv.tri(tx, y + h - 8, tx + 70, y + h - 8, tx + 35, y + 14, INK)
        cv.rect(tx + 30, y + h - 22, 10, 14, (255, 255, 255))
    for sx, sy, r in ((x + 400, y + 12, 9), (x + 415, y + 22, 7)):
        cv.circle(sx, sy, r, GREY)


def draw_riyadh(cv, x, y, w, h):
    cv.rect(x, y, w, h, (210, 225, 240))
    tx = x + 90
    cv.rect(tx, y + 8, 46, h - 8, INK)
    cv.tri(tx, y + 8, tx + 46, y + 8, tx + 23, y - 2, INK)
    for wy in range(y + 16, y + h - 6, 10):
        cv.rect(tx + 8, wy, 30, 3, (160, 190, 220))
    cv.line(x + 260, y + 44, x + 420, y + 8, ORANGE)
    cv.line(x + 260, y + 45, x + 420, y + 9, ORANGE)
    cv.circle(x + 420, y + 8, 7, ORANGE)
    cv.circle(x + 420, y + 8, 3, YELLOW)
    cv.text(x + 180, y + 30, "5 STOPPED", 2, RED, bold=True)


def draw_bars(cv, x, y, w, h):
    cv.rect(x, y, w, h, (255, 255, 255))
    vals = [(0.95, RED), (0.8, BLUE), (0.55, GOLD), (0.35, GREEN)]
    for i, (f, c) in enumerate(vals):
        bx = x + 20 + i * 110
        bh = int((h - 16) * f)
        cv.rect(bx, y + h - 8 - bh, 60, bh, c)


# ---- layout ----

STORIES = [
    ("MYANMAR CALLS GENOCIDE RULING UNFAIR",
     "WORLD COURT RULED 9-6 ON THURSDAY - FIRST SUCH GENOCIDE FINDING",
     draw_court),
    ("STOCKS PLUNGE INTO CORRECTION",
     "S&P 500 -3.7%, NASDAQ -5.3% - NVIDIA -14% ON SEC PROBE",
     draw_chart),
    ("UK AND EU AGREE RESET DEAL",
     "FOOD TRADE, YOUTH MOBILITY, CARBON LINK - BRUSSELS SUMMIT, FRIDAY",
     draw_flags),
    ("GAZA STRIKES KILL SIX",
     "ISRAELI STRIKES HIT CENTRAL GAZA ON FRIDAY - AFP",
     draw_gaza),
    ("SAUDI DEFENCES STOP MISSILES",
     "FIVE MISSILES INTERCEPTED AFTER PIF TOWER HIT ON THURSDAY",
     draw_riyadh),
]

STATS = ["110+ MISSILES AT KYIV", "400 DRONES OVERNIGHT",
         "9-6 ICJ VOTE"]


def draw_cell(cv, x, y, w, h, headline, body, picto):
    cv.frame(x, y, w, h, GREY, 1)
    picto(cv, x + 6, y + 6, w - 12, 50)
    hy = y + 60
    for ln in cv.wrap(headline, 3, w - 16)[:2]:
        cv.text(x + 8, hy, ln, 3, INK, bold=True)
        hy += 24
    by = hy + 2
    for ln in cv.wrap(body, 2, w - 16)[:2]:
        cv.text(x + 8, by, ln, 2, INK)
        by += 15


def main():
    cv = Canvas(W, H, PAPER)
    cv.frame(8, 8, W - 16, H - 16, INK, 3)
    cv.text_center(24, "THE WORLD", 7, INK, bold=True)
    cv.rect(24, 84, W - 48, 36, RED)
    cv.text_center(92, "FRIDAY 20 NOVEMBER 2026", 3, (255, 255, 255),
                   bold=True)
    cv.text_center(128, "ONE DAY IN PICTURES", 2, INK)

    # lead story: Kyiv
    lx, ly, lw = 24, 156, W - 48
    draw_kyiv(cv, lx, ly, lw, 224)
    cv.text(lx, 392, "KYIV HIT HOURS AFTER PEACE TALK", 4, INK, bold=True)
    cv.text(lx, 430, "RUSSIA FIRES 110+ MISSILES AND 400 DRONES - 8 KILLED",
            2, INK)
    cv.text(lx, 452, "3 BRIDGES STRUCK, POWER CUT - ATTACK FOLLOWS SHENZHEN SUMMIT",
            2, INK)
    cv.line(24, 512, W - 24, 512, INK)

    # grid: 2 columns x 3 rows, 5 stories + numbers cell
    gx, gy = 24, 524
    cw, chh = 480, 144
    gap = 12
    cells = list(STORIES)
    for idx in range(6):
        col, row = idx % 2, idx // 2
        cx = gx + col * (cw + gap)
        cy = gy + row * (chh + gap)
        if idx < 5:
            headline, body, picto = cells[idx]
            draw_cell(cv, cx, cy, cw, chh, headline, body, picto)
        else:
            cv.frame(cx, cy, cw, chh, GREY, 1)
            draw_bars(cv, cx + 6, cy + 6, cw - 12, 50)
            cv.text(cx + 8, cy + 60, "THE DAY IN NUMBERS", 3, INK, bold=True)
            sy = cy + 88
            for st in STATS:
                cv.text(cx + 8, sy, st, 2, INK)
                sy += 14
    cv.text_center(988, "SOURCES: REUTERS, AFP, AP - ALL EVENTS FRIDAY 20 NOV 2026",
                   2, GREY)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    size = write_png(path, cv)
    print("wrote", path, size, "bytes")


if __name__ == "__main__":
    main()
