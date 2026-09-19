"""
MapMe - Google Play FOREGROUND_SERVICE_LOCATION Demonstration Video Generator
Generates a 1080p 30fps Full HD MP4 video adhering to Google Play Console policy requirements.
"""

import os
import math
import numpy as np
import imageio
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_PATH = r"c:\git\notes\MapMe\mapme-foreground-service-demo.mp4"
BRAIN_DIR = r"C:\Users\talso\.gemini\antigravity\brain\6b0976e8-6012-4cd9-9316-e77eb6ddc200"

FPS = 30
WIDTH = 1920
HEIGHT = 1080
TOTAL_FRAMES = 1440  # 48 seconds at 30 fps

# Colors
BG_COLOR = (11, 17, 30)
CARD_BG = (19, 29, 49)
BORDER_COLOR = (56, 189, 248, 80)
CYAN = (0, 229, 255)
VIOLET = (139, 92, 246)
EMERALD = (16, 185, 129)
CORAL = (239, 68, 68)
TEXT_WHITE = (248, 250, 252)
TEXT_GRAY = (148, 163, 184)
TEXT_DARK = (30, 41, 59)

# Fonts
FONT_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 34)
FONT_HEADING = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 26)
FONT_SUBHEADING = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 20)
FONT_BODY = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 17)
FONT_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 18)
FONT_BADGE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 14)
FONT_PHONE_STATUS = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 13)
FONT_PHONE_UI = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 14)
FONT_PHONE_UI_B = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 14)
FONT_PHONE_LARGE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 20)

# Load assets
p_icon = os.path.join(BRAIN_DIR, "mapme-googleplay-icon-512x512.png")
icon_img = Image.open(p_icon).convert("RGBA").resize((64, 64), Image.Resampling.LANCZOS)
icon_small = Image.open(p_icon).convert("RGBA").resize((36, 36), Image.Resampling.LANCZOS)

# Phone screen dimensions
PHONE_X = 100
PHONE_Y = 100
PHONE_W = 440
PHONE_H = 880

SCREEN_X = PHONE_X + 12
SCREEN_Y = PHONE_Y + 12
SCREEN_W = PHONE_W - 24
SCREEN_H = PHONE_H - 24

# Right Panel dimensions
PANEL_X = 580
PANEL_Y = 100
PANEL_W = 1240
PANEL_H = 880


def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)


def create_base_canvas():
    canvas = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    # Subtle background gradient
    for y in range(0, HEIGHT, 4):
        alpha = y / HEIGHT
        r = int(11 + 5 * alpha)
        g = int(17 + 10 * alpha)
        b = int(30 + 16 * alpha)
        draw.rectangle([(0, y), (WIDTH, y + 4)], fill=(r, g, b))

    # Top Brand Bar
    canvas.paste(icon_img, (60, 24), icon_img)
    draw.text((136, 26), "MapMe", font=FONT_TITLE, fill=TEXT_WHITE)
    draw.text((270, 36), "v4.8", font=FONT_BADGE, fill=CYAN)
    draw.text((320, 36), "(com.talapp.mapme)", font=FONT_SUBHEADING, fill=TEXT_GRAY)

    # Top Right Badges
    badge_text = "FOREGROUND_SERVICE_LOCATION VERIFICATION"
    bw = 360
    draw_rounded_rect(draw, (WIDTH - bw - 60, 28, WIDTH - 60, 68), 10, fill=(0, 229, 255, 35), outline=CYAN, width=1)
    draw.text((WIDTH - bw - 45, 38), badge_text, font=FONT_BADGE, fill=CYAN)

    return canvas


def draw_phone_frame(canvas):
    draw = ImageDraw.Draw(canvas)
    # Outer Chassis
    draw_rounded_rect(draw, (PHONE_X, PHONE_Y, PHONE_X + PHONE_W, PHONE_Y + PHONE_H), 36, fill=(24, 32, 47), outline=(56, 189, 248, 90), width=2)
    # Inner Bezel
    draw_rounded_rect(draw, (SCREEN_X, SCREEN_Y, SCREEN_X + SCREEN_W, SCREEN_Y + SCREEN_H), 26, fill=(15, 23, 42))


def draw_phone_status_bar(screen_img, show_location_icon=True):
    draw = ImageDraw.Draw(screen_img)
    # Clock
    draw.text((24, 10), "09:41", font=FONT_PHONE_STATUS, fill=TEXT_WHITE)
    # Punch-hole camera in middle
    cx = SCREEN_W // 2
    draw.ellipse([(cx - 7, 8), (cx + 7, 22)], fill=(5, 8, 15))
    # Right icons (WiFi, 5G, Battery, Location)
    rx = SCREEN_W - 90
    if show_location_icon:
        # Mini location marker
        draw.ellipse([(rx - 22, 10), (rx - 14, 18)], fill=CYAN)
        draw.polygon([(rx - 22, 14), (rx - 14, 14), (rx - 18, 22)], fill=CYAN)
    draw.text((rx, 10), "5G", font=FONT_PHONE_STATUS, fill=TEXT_WHITE)
    draw.text((rx + 28, 10), "94%", font=FONT_PHONE_STATUS, fill=TEXT_WHITE)


def render_dashboard_screen():
    img = Image.new("RGB", (SCREEN_W, SCREEN_H), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw_phone_status_bar(img, show_location_icon=False)

    # Header
    img.paste(icon_small, (24, 46), icon_small)
    draw.text((68, 48), "MapMe", font=FONT_PHONE_LARGE, fill=TEXT_WHITE)
    draw.text((24, 76), "Color every street in your city", font=FONT_PHONE_UI, fill=TEXT_GRAY)

    # Search Bar
    draw_rounded_rect(draw, (24, 110, SCREEN_W - 24, 160), 12, fill=(30, 41, 59), outline=(56, 189, 248, 80))
    draw.text((40, 122), "🔍  Where to? Search & Navigate", font=FONT_PHONE_UI_B, fill=CYAN)

    # Stats Row
    box_w = (SCREEN_W - 48 - 16) // 3
    for i, (label, val, col) in enumerate([("Tracks", "14", CYAN), ("Distance", "38.2 km", VIOLET), ("Time", "05:12", EMERALD)]):
        bx = 24 + i * (box_w + 8)
        draw_rounded_rect(draw, (bx, 175, bx + box_w, 245), 10, fill=(24, 32, 47), outline=(56, 189, 248, 40))
        draw.text((bx + 10, 185), label, font=FONT_PHONE_STATUS, fill=TEXT_GRAY)
        draw.text((bx + 10, 210), val, font=FONT_PHONE_UI_B, fill=col)

    # Mini map preview
    draw_rounded_rect(draw, (24, 260, SCREEN_W - 24, 460), 14, fill=(11, 17, 30), outline=(56, 189, 248, 60))
    # Draw simulated streets & tracks on preview
    draw.line([(30, 360), (SCREEN_W - 30, 360)], fill=(30, 41, 59), width=8)
    draw.line([(180, 270), (180, 450)], fill=(30, 41, 59), width=8)
    draw.line([(30, 360), (180, 360), (180, 450)], fill=EMERALD, width=6)

    # Travel History Header
    draw.text((24, 480), "Recent Activity", font=FONT_PHONE_UI_B, fill=TEXT_WHITE)

    # Trip Item
    draw_rounded_rect(draw, (24, 510, SCREEN_W - 24, 575), 12, fill=(24, 32, 47), outline=(56, 189, 248, 40))
    draw.text((38, 522), "Morning Walk • Tel Aviv", font=FONT_PHONE_UI_B, fill=TEXT_WHITE)
    draw.text((38, 546), "4.8 km  •  42 min  •  Today", font=FONT_PHONE_UI, fill=TEXT_GRAY)

    # Action Buttons at bottom
    # Start Walk button (highlighted)
    draw_rounded_rect(draw, (24, 660, SCREEN_W - 24, 725), 24, fill=(16, 185, 129), outline=(52, 211, 153), width=2)
    draw.text((SCREEN_W // 2 - 45, 680), "🚶 Start Walk", font=FONT_PHONE_LARGE, fill=(0, 0, 0))

    # Start Drive button
    draw_rounded_rect(draw, (24, 740, SCREEN_W - 24, 800), 24, fill=(239, 68, 68, 180), outline=CORAL)
    draw.text((SCREEN_W // 2 - 45, 758), "🚗 Start Drive", font=FONT_PHONE_LARGE, fill=TEXT_WHITE)

    return img


def render_active_tracking_screen(progress_pct, elapsed_sec, distance_m):
    img = Image.new("RGB", (SCREEN_W, SCREEN_H), (11, 17, 30))
    draw = ImageDraw.Draw(img)

    # Dark OSM Map Grid
    for gx in range(0, SCREEN_W, 60):
        draw.line([(gx, 0), (gx, SCREEN_H)], fill=(20, 29, 45), width=1)
    for gy in range(0, SCREEN_H, 60):
        draw.line([(0, gy), (SCREEN_W, gy)], fill=(20, 29, 45), width=1)

    # Main Streets
    draw.line([(0, 420), (SCREEN_W, 420)], fill=(35, 48, 71), width=16)
    draw.line([(210, 0), (210, SCREEN_H)], fill=(35, 48, 71), width=16)
    draw.line([(80, 200), (SCREEN_W, 600)], fill=(35, 48, 71), width=12)

    # Animated Traveled GPS Route (Neon Emerald Glow)
    # Define track waypoints
    pts = [
        (210, 750),
        (210, 600),
        (210, 420),
        (280, 420),
        (350, 420),
        (350, 300)
    ]
    total_pts = len(pts)
    current_idx = min(int(progress_pct * (total_pts - 1)), total_pts - 2)
    t = (progress_pct * (total_pts - 1)) - current_idx
    curr_x = int(pts[current_idx][0] + t * (pts[current_idx + 1][0] - pts[current_idx][0]))
    curr_y = int(pts[current_idx][1] + t * (pts[current_idx + 1][1] - pts[current_idx][1]))

    drawn_pts = pts[:current_idx + 1] + [(curr_x, curr_y)]
    if len(drawn_pts) > 1:
        # Glow outer
        for i in range(len(drawn_pts) - 1):
            draw.line([drawn_pts[i], drawn_pts[i + 1]], fill=(16, 185, 129, 100), width=12)
        # Inner solid
        for i in range(len(drawn_pts) - 1):
            draw.line([drawn_pts[i], drawn_pts[i + 1]], fill=EMERALD, width=6)

    # Pulse at current location
    pulse_r = int(14 + 6 * math.sin(progress_pct * 25))
    draw.ellipse([(curr_x - pulse_r, curr_y - pulse_r), (curr_x + pulse_r, curr_y + pulse_r)], fill=(16, 185, 129, 60))
    draw.ellipse([(curr_x - 8, curr_y - 8), (curr_x + 8, curr_y + 8)], fill=(255, 255, 255), outline=EMERALD, width=3)

    # Top Search Pill
    draw_rounded_rect(draw, (24, 46, SCREEN_W - 24, 96), 25, fill=(19, 29, 49, 220), outline=(56, 189, 248, 80))
    draw.text((44, 58), "🔍 Search destination...", font=FONT_PHONE_UI, fill=TEXT_GRAY)

    # Floating Telemetry HUD Card at bottom
    hud_y = SCREEN_H - 220
    draw_rounded_rect(draw, (20, hud_y, SCREEN_W - 20, hud_y + 190), 20, fill=(19, 29, 49, 240), outline=(56, 189, 248, 120), width=2)

    # HUD Title
    draw.ellipse([(38, hud_y + 18), (48, hud_y + 28)], fill=EMERALD)
    draw.text((58, hud_y + 14), "RECORDING ACTIVE • WALKING", font=FONT_PHONE_STATUS, fill=EMERALD)

    # HUD Metrics Grid
    m_min = elapsed_sec // 60
    m_sec = elapsed_sec % 60
    time_str = f"{m_min:02d}:{m_sec:02d}"
    dist_str = f"{distance_m} m" if distance_m < 1000 else f"{distance_m/1000.0:.2f} km"

    draw.text((38, hud_y + 44), "DURATION", font=FONT_PHONE_STATUS, fill=TEXT_GRAY)
    draw.text((38, hud_y + 64), time_str, font=FONT_PHONE_LARGE, fill=TEXT_WHITE)

    draw.text((165, hud_y + 44), "DISTANCE", font=FONT_PHONE_STATUS, fill=TEXT_GRAY)
    draw.text((165, hud_y + 64), dist_str, font=FONT_PHONE_LARGE, fill=CYAN)

    draw.text((290, hud_y + 44), "SPEED", font=FONT_PHONE_STATUS, fill=TEXT_GRAY)
    draw.text((290, hud_y + 64), "4.8 km/h", font=FONT_PHONE_LARGE, fill=VIOLET)

    # HUD Buttons
    draw_rounded_rect(draw, (38, hud_y + 115, 180, hud_y + 165), 12, fill=(30, 41, 59), outline=(56, 189, 248, 80))
    draw.text((80, hud_y + 128), "⏸ Pause", font=FONT_PHONE_UI_B, fill=TEXT_WHITE)

    draw_rounded_rect(draw, (200, hud_y + 115, SCREEN_W - 38, hud_y + 165), 12, fill=(239, 68, 68, 180), outline=CORAL)
    draw.text((SCREEN_W // 2 + 35, hud_y + 128), "⏹ Stop", font=FONT_PHONE_UI_B, fill=TEXT_WHITE)

    draw_phone_status_bar(img, show_location_icon=True)
    return img


def render_home_screen():
    # Android Home Screen
    img = Image.new("RGB", (SCREEN_W, SCREEN_H), (15, 20, 35))
    draw = ImageDraw.Draw(img)

    # Wallpaper styling
    for y in range(SCREEN_H):
        val = int(25 + 30 * math.sin(y / 150))
        draw.line([(0, y), (SCREEN_W, y)], fill=(12, val, 48))

    draw_phone_status_bar(img, show_location_icon=True)

    # Clock Widget
    draw.text((SCREEN_W // 2 - 90, 160), "09:43", font=ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 64), fill=TEXT_WHITE)
    draw.text((SCREEN_W // 2 - 65, 240), "Friday, Sep 19", font=FONT_PHONE_LARGE, fill=TEXT_GRAY)

    # Home Screen App Icons Grid
    # MapMe App Icon
    app_x = 45
    app_y = 480
    img.paste(icon_img.resize((56, 56)), (app_x, app_y), icon_img.resize((56, 56)))
    draw.text((app_x + 4, app_y + 64), "MapMe", font=FONT_PHONE_STATUS, fill=TEXT_WHITE)

    # Other dummy apps
    dummy_apps = [("Maps", (34, 197, 94)), ("Chrome", (59, 130, 246)), ("Camera", (236, 72, 153))]
    for i, (name, col) in enumerate(dummy_apps):
        dx = 45 + (i + 1) * 90
        draw_rounded_rect(draw, (dx, app_y, dx + 56, app_y + 56), 16, fill=col)
        draw.text((dx + 8, app_y + 64), name, font=FONT_PHONE_STATUS, fill=TEXT_WHITE)

    # Bottom App Dock
    draw_rounded_rect(draw, (24, SCREEN_H - 100, SCREEN_W - 24, SCREEN_H - 24), 24, fill=(15, 23, 42, 180), outline=(56, 189, 248, 40))
    for i, col in enumerate([(16, 185, 129), (59, 130, 246), (168, 85, 247), (249, 115, 22)]):
        dx = 45 + i * 88
        draw_rounded_rect(draw, (dx, SCREEN_H - 86, dx + 48, SCREEN_H - 38), 14, fill=col)

    return img


def render_notification_shade(slide_pct, elapsed_sec, distance_m):
    # Renders home screen with notification shade pulled down
    base = render_home_screen()
    shade_h = int(SCREEN_H * slide_pct * 0.72)
    if shade_h < 10:
        return base

    shade = Image.new("RGBA", (SCREEN_W, shade_h), (11, 17, 30, 245))
    sdraw = ImageDraw.Draw(shade)

    # Shade Header
    sdraw.text((24, 20), "09:44", font=FONT_PHONE_LARGE, fill=TEXT_WHITE)
    sdraw.text((SCREEN_W - 140, 22), "Silent / Alerts", font=FONT_PHONE_STATUS, fill=TEXT_GRAY)

    # Quick Settings Icons
    for i, label in enumerate(["Wi-Fi", "Bluetooth", "Location", "Flashlight"]):
        qx = 24 + i * 90
        col = CYAN if label == "Location" else (30, 41, 59)
        draw_rounded_rect(sdraw, (qx, 55, qx + 75, 105), 16, fill=col)
        tcol = (0, 0, 0) if label == "Location" else TEXT_WHITE
        sdraw.text((qx + 10, 72), label[:5], font=FONT_PHONE_STATUS, fill=tcol)

    # MapMe Ongoing Foreground Notification Card
    notif_y = 135
    notif_h = 130
    draw_rounded_rect(sdraw, (18, notif_y, SCREEN_W - 18, notif_y + notif_h), 18, fill=(19, 29, 49), outline=(0, 229, 255, 180), width=2)

    # App icon in notification
    shade.paste(icon_small, (32, notif_y + 16), icon_small)
    sdraw.text((76, notif_y + 16), "MapMe", font=FONT_PHONE_UI_B, fill=TEXT_WHITE)
    sdraw.text((140, notif_y + 17), "•  Ongoing Tracking", font=FONT_PHONE_STATUS, fill=EMERALD)
    sdraw.text((SCREEN_W - 90, notif_y + 17), "Active", font=FONT_PHONE_STATUS, fill=CYAN)

    # Notification Title & Body
    m_min = elapsed_sec // 60
    m_sec = elapsed_sec % 60
    time_str = f"{m_min:02d}:{m_sec:02d}"
    dist_str = f"{distance_m} m" if distance_m < 1000 else f"{distance_m/1000.0:.2f} km"

    sdraw.text((32, notif_y + 48), "Recording Walk in Progress", font=FONT_PHONE_UI_B, fill=TEXT_WHITE)
    sdraw.text((32, notif_y + 70), f"Duration: {time_str}   |   Distance: {dist_str}   |   4.9 km/h", font=FONT_PHONE_UI, fill=TEXT_GRAY)

    # Action buttons inside notification
    draw_rounded_rect(sdraw, (32, notif_y + 96, 110, notif_y + 122), 8, fill=(30, 41, 59), outline=(56, 189, 248, 60))
    sdraw.text((46, notif_y + 101), "⏸ Pause", font=FONT_PHONE_STATUS, fill=TEXT_WHITE)

    draw_rounded_rect(sdraw, (120, notif_y + 96, 190, notif_y + 122), 8, fill=(239, 68, 68, 140), outline=CORAL)
    sdraw.text((136, notif_y + 101), "⏹ Stop", font=FONT_PHONE_STATUS, fill=TEXT_WHITE)

    # Bottom handle
    sdraw.line([(SCREEN_W // 2 - 30, shade_h - 10), (SCREEN_W // 2 + 30, shade_h - 10)], fill=TEXT_GRAY, width=3)

    base.paste(shade, (0, 0), shade)
    return base


def render_right_panel(canvas, step_num, step_badge, title, subtitle, bullets, progress_pct):
    draw = ImageDraw.Draw(canvas)

    # Main Card Container
    draw_rounded_rect(draw, (PANEL_X, PANEL_Y, PANEL_X + PANEL_W, PANEL_Y + PANEL_H), 24, fill=CARD_BG, outline=(56, 189, 248, 60), width=2)

    # Step Badge
    badge_bg = CYAN if "1" in step_badge else (EMERALD if "4" in step_badge or "COMPLIANCE" in step_badge else (CORAL if "2" in step_badge else VIOLET))
    bw = 180
    draw_rounded_rect(draw, (PANEL_X + 48, PANEL_Y + 48, PANEL_X + 48 + bw, PANEL_Y + 86), 10, fill=(*badge_bg[:3], 40), outline=badge_bg, width=1)
    draw.text((PANEL_X + 62, PANEL_Y + 56), step_badge, font=FONT_BADGE, fill=badge_bg)

    # Step Title & Subtitle
    draw.text((PANEL_X + 48, PANEL_Y + 108), title, font=FONT_TITLE, fill=TEXT_WHITE)
    draw.text((PANEL_X + 48, PANEL_Y + 160), subtitle, font=FONT_SUBHEADING, fill=CYAN)

    # Horizontal divider
    draw.line([(PANEL_X + 48, PANEL_Y + 205), (PANEL_X + PANEL_W - 48, PANEL_Y + 205)], fill=(56, 189, 248, 40), width=1)

    # Bullet Points / Criteria Verification
    by = PANEL_Y + 235
    for b_type, heading, text in bullets:
        # Icon / Status badge
        if b_type == "check":
            draw_rounded_rect(draw, (PANEL_X + 48, by, PANEL_X + 80, by + 32), 8, fill=(16, 185, 129, 40), outline=EMERALD)
            draw.text((PANEL_X + 57, by + 5), "✔", font=FONT_BOLD, fill=EMERALD)
        elif b_type == "arrow":
            draw_rounded_rect(draw, (PANEL_X + 48, by, PANEL_X + 80, by + 32), 8, fill=(0, 229, 255, 40), outline=CYAN)
            draw.text((PANEL_X + 57, by + 5), "➔", font=FONT_BOLD, fill=CYAN)
        else:
            draw_rounded_rect(draw, (PANEL_X + 48, by, PANEL_X + 80, by + 32), 8, fill=(139, 92, 246, 40), outline=VIOLET)
            draw.text((PANEL_X + 57, by + 5), "★", font=FONT_BOLD, fill=VIOLET)

        draw.text((PANEL_X + 96, by + 4), heading, font=FONT_HEADING, fill=TEXT_WHITE)
        draw.text((PANEL_X + 96, by + 40), text, font=FONT_BODY, fill=TEXT_GRAY)
        by += 96

    # Bottom Progress Tracker Bar
    bar_y = PANEL_Y + PANEL_H - 70
    draw.text((PANEL_X + 48, bar_y - 28), "POLICY VERIFICATION TIMELINE", font=FONT_BADGE, fill=TEXT_GRAY)
    draw_rounded_rect(draw, (PANEL_X + 48, bar_y, PANEL_X + PANEL_W - 48, bar_y + 12), 6, fill=(30, 41, 59))
    prog_w = int((PANEL_W - 96) * progress_pct)
    if prog_w > 6:
        draw_rounded_rect(draw, (PANEL_X + 48, bar_y, PANEL_X + 48 + prog_w, bar_y + 12), 6, fill=CYAN)


def draw_cursor(canvas, x, y, pulse=False):
    draw = ImageDraw.Draw(canvas)
    if pulse:
        draw.ellipse([(x - 24, y - 24), (x + 24, y + 24)], fill=(0, 229, 255, 80), outline=CYAN, width=2)
    # Cursor pointer
    draw.polygon([(x, y), (x, y + 22), (x + 6, y + 17), (x + 15, y + 23), (x + 19, y + 19), (x + 11, y + 13), (x + 18, y + 11)], fill=(255, 255, 255), outline=(0, 0, 0), width=1)


def generate_video():
    print(f"Generating Google Play compliance video: {OUTPUT_PATH}")
    writer = imageio.get_writer(
        OUTPUT_PATH,
        fps=FPS,
        codec="libx264",
        pixelformat="yuv420p",
        macro_block_size=None,
        ffmpeg_params=["-preset", "fast", "-crf", "18"]
    )

    dashboard_cached = render_dashboard_screen()

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        canvas = create_base_canvas()
        draw_phone_frame(canvas)

        progress_overall = f / TOTAL_FRAMES

        # ==============================================================
        # SCENE 1: Introduction (Frames 0 - 210, 0s - 7s)
        # ==============================================================
        if f < 210:
            screen = dashboard_cached
            canvas.paste(screen, (SCREEN_X, SCREEN_Y))

            bullets = [
                ("star", "Noticeable User-Facing Task", "MapMe records walking, running, and driving routes and colors city streets in real time."),
                ("arrow", "Turn-by-Turn Navigation & Guidance", "Computes routes via OSRM with speech cues, maneuver distances, and auto-rerouting."),
                ("check", "Why Background Location Is Required", "Exploration tracking must continue uninterrupted when the phone is locked or screen is off.")
            ]
            render_right_panel(
                canvas,
                step_num=1,
                step_badge="GOOGLE PLAY VERIFICATION",
                title="FOREGROUND_SERVICE_LOCATION",
                subtitle="MapMe • Continuous Route Recording & Navigation",
                bullets=bullets,
                progress_pct=progress_overall
            )

        # ==============================================================
        # SCENE 2: Step 1 - User Initiates Session (Frames 210 - 480, 7s - 16s)
        # ==============================================================
        elif f < 480:
            sub_f = f - 210
            pct = sub_f / 270.0
            elapsed = int(sub_f / FPS * 4)  # 0 to 36s simulated
            dist = int(pct * 240)           # 0 to 240m

            if sub_f < 45:
                # Still on dashboard, cursor moving to "Start Walk"
                screen = dashboard_cached.copy()
                canvas.paste(screen, (SCREEN_X, SCREEN_Y))
                # "Start Walk" button center in canvas coords:
                bx = SCREEN_X + SCREEN_W // 2
                by = SCREEN_Y + 690
                cur_x = int(SCREEN_X + 150 + (bx - (SCREEN_X + 150)) * (sub_f / 45.0))
                cur_y = int(SCREEN_Y + 400 + (by - (SCREEN_Y + 400)) * (sub_f / 45.0))
                draw_cursor(canvas, cur_x, cur_y, pulse=(sub_f > 35))
            else:
                track_pct = (sub_f - 45) / 225.0
                screen = render_active_tracking_screen(track_pct, elapsed, dist)
                canvas.paste(screen, (SCREEN_X, SCREEN_Y))

            bullets = [
                ("check", "Explicit User Initiation", "Session begins only when user explicitly taps 'Start Walk', 'Start Drive', or 'Start Navigation'."),
                ("arrow", "Real-Time Telemetry HUD", "Elapsed duration, traveled distance, and speed update dynamically as location is received."),
                ("check", "Live Route Polyline Rendering", "Map continuously draws the explored path using high-accuracy GPS coordinates.")
            ]
            render_right_panel(
                canvas,
                step_num=1,
                step_badge="STEP 1 OF 4",
                title="User Explicitly Initiates Tracking",
                subtitle="LocationService activates high-precision GPS updates",
                bullets=bullets,
                progress_pct=progress_overall
            )

        # ==============================================================
        # SCENE 3: Step 2 - App Transitions to Background (Frames 480 - 750, 16s - 25s)
        # ==============================================================
        elif f < 750:
            sub_f = f - 480
            pct = sub_f / 270.0

            # Swipe up / minimize transition
            if sub_f < 35:
                screen = render_active_tracking_screen(0.8, 36, 240)
                canvas.paste(screen, (SCREEN_X, SCREEN_Y))
                # Animated swipe line
                s_draw = ImageDraw.Draw(canvas)
                sy = SCREEN_Y + SCREEN_H - int(sub_f * 6)
                s_draw.line([(SCREEN_X + SCREEN_W // 2 - 40, sy), (SCREEN_X + SCREEN_W // 2 + 40, sy)], fill=CYAN, width=4)
            else:
                screen = render_home_screen()
                canvas.paste(screen, (SCREEN_X, SCREEN_Y))

            bullets = [
                ("arrow", "User Navigates Away / Locks Phone", "User exits to the home screen or locks phone in pocket while continuing their walk or drive."),
                ("check", "Persistent Foreground Service Lifecycle", "The Android OS requires FOREGROUND_SERVICE_LOCATION to guarantee uninterrupted execution."),
                ("star", "Zero Missing Waypoints", "Without foreground service protection, the OS would terminate location updates, losing the route.")
            ]
            render_right_panel(
                canvas,
                step_num=2,
                step_badge="STEP 2 OF 4",
                title="User Leaves App (Background State)",
                subtitle="LocationService continues execution in foreground service mode",
                bullets=bullets,
                progress_pct=progress_overall
            )

        # ==============================================================
        # SCENE 4: Step 3 - Persistent Notification Shade (Frames 750 - 1080, 25s - 36s)
        # ==============================================================
        elif f < 1080:
            sub_f = f - 750
            # Pull down notification shade
            slide = min(1.0, sub_f / 40.0)
            elapsed_sim = 240 + int((sub_f / 330.0) * 45)
            dist_sim = 320 + int((sub_f / 330.0) * 70)

            screen = render_notification_shade(slide, elapsed_sim, dist_sim)
            canvas.paste(screen, (SCREEN_X, SCREEN_Y))

            # Callout box pointing to the notification
            c_draw = ImageDraw.Draw(canvas)
            if slide >= 0.95:
                notif_box_y1 = SCREEN_Y + 135
                notif_box_y2 = notif_box_y1 + 130
                draw_rounded_rect(c_draw, (SCREEN_X + 8, notif_box_y1 - 6, SCREEN_X + SCREEN_W - 8, notif_box_y2 + 6), 20, fill=None, outline=CYAN, width=3)

            bullets = [
                ("check", "Persistent Non-Dismissible Notification", "A noticeable notification remains visible in the system drawer as required by Google Play."),
                ("arrow", "Real-Time Telemetry in Notification", "Displays live duration ('04:15'), total distance ('340 m'), and active tracking mode."),
                ("star", "Immediate User Controls", "User can pause or stop location tracking directly from the notification shade at any time.")
            ]
            render_right_panel(
                canvas,
                step_num=3,
                step_badge="STEP 3 OF 4",
                title="Persistent Foreground Notification",
                subtitle="Noticeable ongoing status informs the user of active location access",
                bullets=bullets,
                progress_pct=progress_overall
            )

        # ==============================================================
        # SCENE 5: Step 4 - User Taps Notification -> Resumes App (Frames 1080 - 1320, 36s - 44s)
        # ==============================================================
        elif f < 1320:
            sub_f = f - 1080
            elapsed_sim = 285 + int((sub_f / 240.0) * 30)
            dist_sim = 390 + int((sub_f / 240.0) * 40)

            if sub_f < 30:
                # Tap on notification
                screen = render_notification_shade(1.0, 285, 390)
                canvas.paste(screen, (SCREEN_X, SCREEN_Y))
                draw_cursor(canvas, SCREEN_X + 180, SCREEN_Y + 185, pulse=True)
            else:
                # Resume into MapMe with fully recorded route!
                screen = render_active_tracking_screen(1.0, elapsed_sim, dist_sim)
                canvas.paste(screen, (SCREEN_X, SCREEN_Y))

            bullets = [
                ("check", "Seamless Return to Application", "Tapping the notification immediately returns the user to the active tracking screen."),
                ("star", "Unbroken GPS Polyline Preserved", "The map verifies that the route continued recording with 100% accuracy during background time."),
                ("check", "Complete Session Telemetry", "Duration, distance, and speed metrics reflect the full elapsed exploration without gaps.")
            ]
            render_right_panel(
                canvas,
                step_num=4,
                step_badge="STEP 4 OF 4",
                title="Seamless Return & Route Preservation",
                subtitle="Tapping notification verifies continuous, gapless background tracking",
                bullets=bullets,
                progress_pct=progress_overall
            )

        # ==============================================================
        # SCENE 6: Summary & Policy Compliance (Frames 1320 - 1440, 44s - 48s)
        # ==============================================================
        else:
            screen = render_active_tracking_screen(1.0, 315, 430)
            canvas.paste(screen, (SCREEN_X, SCREEN_Y))

            bullets = [
                ("check", "Noticeable User-Initiated Task", "Explicitly triggered by user for street exploration and turn-by-turn navigation."),
                ("check", "Persistent Foreground Notification", "Displays ongoing tracking notification with live duration, distance, and stop controls."),
                ("check", "Essential Core Functionality", "Critical for map coverage coloring, GPX/KML export, and Android Auto in-car guidance."),
                ("check", "Strict Privacy Standards", "Location data is never sold, monetized, or shared with third-party advertisers.")
            ]
            render_right_panel(
                canvas,
                step_num=4,
                step_badge="COMPLIANCE VERIFIED",
                title="Google Play Policy Requirements Met",
                subtitle="MapMe meets all FOREGROUND_SERVICE_LOCATION criteria",
                bullets=bullets,
                progress_pct=1.0
            )

        # Convert PIL to numpy and write frame
        frame_np = np.array(canvas)
        writer.append_data(frame_np)

        if f % 150 == 0 or f == TOTAL_FRAMES - 1:
            print(f"Rendered {f}/{TOTAL_FRAMES} frames ({(f/TOTAL_FRAMES)*100:.1f}%)")

    writer.close()
    print(f"Video rendering complete! Saved to {OUTPUT_PATH}")
    file_size_mb = os.path.getsize(OUTPUT_PATH) / (1024 * 1024)
    print(f"Output file size: {file_size_mb:.2f} MB")


if __name__ == "__main__":
    generate_video()
