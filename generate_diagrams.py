from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

out_dir = Path(r"C:\Users\Asus\.gemini\antigravity\scratch\data-analyst-ai-chatbot\screenshots")
out_dir.mkdir(parents=True, exist_ok=True)

# Try to load Arial or Segoe UI
try:
    font_bold = ImageFont.truetype("arialbd.ttf", 22)
    font_reg = ImageFont.truetype("arial.ttf", 18)
    font_sm = ImageFont.truetype("arial.ttf", 15)
    font_title = ImageFont.truetype("arialbd.ttf", 24)
except Exception:
    font_bold = ImageFont.load_default()
    font_reg = ImageFont.load_default()
    font_sm = ImageFont.load_default()
    font_title = ImageFont.load_default()

# ----------------- Diagram 1: Level 0 DFD -----------------
img1 = Image.new("RGB", (1200, 260), "#ffffff")
d1 = ImageDraw.Draw(img1)

def draw_box(draw, xy, text_lines, bg="#e0f2fe", border="#0284c7"):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=bg, outline=border, width=2)
    total_h = len(text_lines) * 22
    start_y = y0 + (y1 - y0 - total_h) / 2
    for i, line in enumerate(text_lines):
        # Center text
        bbox = draw.textbbox((0, 0), line, font=font_reg)
        w = bbox[2] - bbox[0]
        draw.text((x0 + (x1 - x0 - w) / 2, start_y + i * 24), line, fill="#0f172a", font=font_reg)

def draw_arrow(draw, start, end, label=""):
    x0, y0 = start
    x1, y1 = end
    draw.line([(x0, y0), (x1, y1)], fill="#64748b", width=2)
    # Arrow head
    draw.polygon([(x1, y1), (x1 - 8, y1 - 5), (x1 - 8, y1 + 5)], fill="#64748b")
    if label:
        bbox = draw.textbbox((0, 0), label, font=font_sm)
        w = bbox[2] - bbox[0]
        draw.text(((x0 + x1 - w) / 2, y0 - 22), label, fill="#475569", font=font_sm)

# Boxes
draw_box(d1, (40, 70, 220, 170), ["User", "(CSV/Excel + Qs)"], bg="#dbeafe", border="#2563eb")
draw_box(d1, (360, 50, 680, 190), ["Data Analyst AI Chatbot", "Streamlit + Query Router"], bg="#f1f5f9", border="#0284c7")
draw_box(d1, (800, 30, 1020, 110), ["SQLite Database", "(Cleaned Tabular Data)"], bg="#fef3c7", border="#d97706")
draw_box(d1, (800, 130, 1020, 210), ["OpenAI API", "(GPT-4o-mini LLM)"], bg="#ecfdf5", border="#059669")
draw_box(d1, (1060, 70, 1170, 170), ["Answer +", "Visuals +", "SQL Log"], bg="#dcfce7", border="#16a34a")

# Arrows
draw_arrow(d1, (220, 120), (360, 120), "Upload / Query")
draw_arrow(d1, (680, 80), (800, 80), "SQL Execute")
draw_arrow(d1, (680, 160), (800, 160), "NL Prompt")
draw_arrow(d1, (1020, 80), (1060, 105), "")
draw_arrow(d1, (1020, 160), (1060, 135), "")

img1.save(out_dir / "diagram_level0.png")

# ----------------- Diagram 2: System Block Diagram -----------------
img2 = Image.new("RGB", (1200, 480), "#ffffff")
d2 = ImageDraw.Draw(img2)

# Subtitle 1
d2.text((40, 20), "Ingestion & Data Preparation Pipeline", fill="#0369a1", font=font_bold)

# Pipeline 1 boxes
p1_boxes = [
    ("1. Upload", "CSV / Excel"),
    ("2. Extraction", "Pandas Loader"),
    ("3. Auto Clean", "Type & Missing Fix"),
    ("4. Data Profiler", "KPIs & Quality"),
    ("5. SQLite Store", "Embedded DB")
]
w_box = 190
h_box = 80
y_p1 = 60

for i, (t1, t2) in enumerate(p1_boxes):
    x_box = 40 + i * 230
    draw_box(d2, (x_box, y_p1, x_box + w_box, y_p1 + h_box), [t1, t2], bg="#e0f2fe", border="#0284c7")
    if i < len(p1_boxes) - 1:
        draw_arrow(d2, (x_box + w_box, y_p1 + h_box/2), (x_box + 230, y_p1 + h_box/2))

# Subtitle 2
d2.text((40, 180), "Dual-Engine Query & Visual Analytics Pipeline", fill="#0369a1", font=font_bold)

p2_boxes = [
    ("1. User Query", "Natural Language"),
    ("2. Engine Router", "AI vs Fallback"),
    ("3. SQL Generator", "Prompt + Schema"),
    ("4. SQL Validator", "AST Whitelist"),
    ("5. SQLite Exec", "Read-Only Engine")
]
y_p2 = 220
for i, (t1, t2) in enumerate(p2_boxes):
    x_box = 40 + i * 230
    draw_box(d2, (x_box, y_p2, x_box + w_box, y_p2 + h_box), [t1, t2], bg="#fef3c7" if i==2 else "#f1f5f9", border="#d97706" if i==2 else "#475569")
    if i < len(p2_boxes) - 1:
        draw_arrow(d2, (x_box + w_box, y_p2 + h_box/2), (x_box + 230, y_p2 + h_box/2))

# Result Box at bottom
draw_box(d2, (270, 360, 930, 440), ["6. Streamlit User Interface: Interactive Tables + Auto Plotly Visualizations + AI Explanation"], bg="#dcfce7", border="#16a34a")

# Connecting arrows down to UI
draw_arrow(d2, (960, 300), (800, 360), "Query Output")
draw_arrow(d2, (270, 300), (400, 360), "Local Pandas Output")

img2.save(out_dir / "diagram_block.png")
print("Both architecture diagrams created successfully!")
