from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from dataclasses import dataclass, field
import random
import re

# ------------------------------
# Branding
# ------------------------------

def random_hex_color(min_val=40, max_val=200):
    return "{:02X}{:02X}{:02X}".format(
        random.randint(min_val, max_val),
        random.randint(min_val, max_val),
        random.randint(min_val, max_val),
    )

@dataclass
class Branding:
    logo_path: str | None = None
    brand_text: str | None = None  # REAL lecture title
    primary_color: str = field(default_factory=random_hex_color)
    accent_color: str = field(default_factory=random_hex_color)
    background_color: str = field(default_factory=lambda: random_hex_color(220, 255))

# ------------------------------
# Models
# ------------------------------

@dataclass
class SlideContent:
    title: str
    lines: list[str]

# ------------------------------
# Parser (Faithful)
# ------------------------------

def parse_faithful_notes(text: str) -> list[SlideContent]:
    slides = []
    current_title = None
    buffer = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        if line.lower().startswith("slide"):
            if current_title:
                slides.append(SlideContent(current_title, buffer))
            current_title = line
            buffer = []
        elif not line.lower().startswith("presenter note"):
            buffer.append(line)

    if current_title:
        slides.append(SlideContent(current_title, buffer))

    return slides

# ------------------------------
# Utilities
# ------------------------------

def clean_title(raw_title: str, lecture_title: str) -> str:
    """
    Rules:
    - Slide 1: Title Slide -> lecture title
    - Lecture X: Something -> Something
    - Slide X: Something -> Something
    """
    if re.match(r"slide\s*1\s*:", raw_title, re.IGNORECASE):
        return lecture_title

    return re.sub(
        r"^(slide\s*\d+\s*:|lecture\s*\d+\s*:)\s*",
        "",
        raw_title,
        flags=re.IGNORECASE,
    )

def remove_all_shapes(slide):
    spTree = slide.shapes._spTree
    for shape in list(slide.shapes):
        spTree.remove(shape._element)

def apply_background(slide, hex_color):
    if hex_color.upper() == "000000":
        hex_color = "FFFFFF"
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor.from_string(hex_color)

def should_use_table(lines):
    return len(lines) >= 2 and all(":" in l for l in lines)

# ------------------------------
# Renderers
# ------------------------------

def insert_title(slide, title):
    box = slide.shapes.add_textbox(
        Inches(1),
        Inches(0.5),
        Inches(8),
        Inches(1.2),
    )
    tf = box.text_frame
    tf.clear()

    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 0, 0)

def insert_bullets(slide, lines, start_y=1.9):
    """
    Single-slide bullet renderer.
    Auto-scales font size to avoid overflow.
    """
    bullet_icon = "•"
    box_height = 5.0  # inches
    max_font = 26
    min_font = 16

    line_count = max(len(lines), 1)
    font_size = max(
        min_font,
        min(max_font, int((box_height * 72) / line_count) - 4),
    )

    box = slide.shapes.add_textbox(
        Inches(1.2),
        Inches(start_y),
        Inches(7.6),
        Inches(box_height),
    )

    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True

    for i, l in enumerate(lines):
        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p.text = f"{bullet_icon}  {l}"
        p.font.size = Pt(font_size)
        p.font.color.rgb = RGBColor(0, 0, 0)
        p.level = 0

def insert_table(slide, lines):
    data = []
    for l in lines:
        if ":" in l:
            left, right = l.split(":", 1)
            data.append((left.strip(), right.strip()))

    if not data:
        return

    rows = len(data)
    table = slide.shapes.add_table(
        rows,
        2,
        Inches(1.2),
        Inches(2.2),
        Inches(7.6),
        Inches(4),
    ).table

    for r, (l, v) in enumerate(data):
        table.cell(r, 0).text = l
        table.cell(r, 1).text = v
        for c in (0, 1):
            for p in table.cell(r, c).text_frame.paragraphs:
                p.font.size = Pt(22)
                p.font.color.rgb = RGBColor(0, 0, 0)

# ------------------------------
# Intro Slide
# ------------------------------

def build_intro_slide(prs, branding: Branding):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    remove_all_shapes(slide)
    apply_background(slide, branding.background_color)

    if branding.logo_path:
        slide.shapes.add_picture(
            branding.logo_path,
            Inches(3),
            Inches(2),
            width=Inches(4),
        )

# ------------------------------
# Generator (Faithful, Stable)
# ------------------------------

def generate_pptx_faithful(template, notes, output, branding: Branding):
    prs = Presentation(template)
    slides = parse_faithful_notes(notes)

    lecture_title = branding.brand_text or ""

    # Clear template slides
    while prs.slides:
        rId = prs.slides._sldIdLst[0].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[0]

    # Intro slide (logo only)
    build_intro_slide(prs, branding)

    for slide_data in slides:
        raw_title = slide_data.title.strip()
        title = clean_title(raw_title, lecture_title)

        # Skip Slide 1 (intro already created)
        if re.match(r"slide\s*1\s*:", raw_title, re.IGNORECASE):
            continue

        content_lines = slide_data.lines.copy()

        # Fallback: no title → first content line
        if not title and content_lines:
            title = content_lines.pop(0)

        slide = prs.slides.add_slide(prs.slide_layouts[1])
        remove_all_shapes(slide)
        apply_background(slide, branding.background_color)

        insert_title(slide, title)

        if should_use_table(content_lines):
            insert_table(slide, content_lines)
        else:
            insert_bullets(slide, content_lines)

    prs.save(output)
