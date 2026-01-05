from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from dataclasses import dataclass, field
from typing import List, Optional
import random
import re


# --------------------------------------------------
# Color Utilities
# --------------------------------------------------

def random_hex_color(min_val=40, max_val=200) -> str:
    """
    Generates a readable random HEX color (no extremes).
    """
    return "{:02X}{:02X}{:02X}".format(
        random.randint(min_val, max_val),
        random.randint(min_val, max_val),
        random.randint(min_val, max_val),
    )


def hex_to_rgb(hex_color: str) -> RGBColor:
    return RGBColor.from_string(hex_color.replace("#", ""))


# --------------------------------------------------
# Data Models
# --------------------------------------------------

@dataclass
class Branding:
    logo_path: Optional[str] = None
    brand_text: Optional[str] = None

    primary_color: str = field(default_factory=random_hex_color)
    accent_color: str = field(default_factory=random_hex_color)
    background_color: str = field(default_factory=lambda: random_hex_color(220, 255))


@dataclass
class SlideContent:
    title: str
    bullets: List[str]


# --------------------------------------------------
# Slide Utilities (SAFE)
# --------------------------------------------------

def clear_shape_text(shape):
    if shape.has_text_frame:
        shape.text_frame.clear()


def clear_slide(slide):
    for shape in slide.shapes:
        clear_shape_text(shape)


def apply_background(slide, hex_color: str):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = hex_to_rgb(hex_color)


# --------------------------------------------------
# Faithful Text Parser
# --------------------------------------------------

def parse_faithful_text(raw_text: str) -> List[SlideContent]:
    slides = []
    current_title = None
    bullets = []

    for line in raw_text.splitlines():
        line = line.strip()

        if re.match(r"^Slide\s+\d+:", line):
            if current_title:
                slides.append(SlideContent(current_title, bullets))
            current_title = line.split(":", 1)[1].strip()
            bullets = []

        elif line and not line.lower().startswith("presenter note"):
            bullets.append(line)

    if current_title:
        slides.append(SlideContent(current_title, bullets))

    return slides


# --------------------------------------------------
# Slide Builders
# --------------------------------------------------

def build_intro_slide(prs: Presentation, branding: Branding):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    clear_slide(slide)
    apply_background(slide, branding.background_color)

    if branding.logo_path:
        slide.shapes.add_picture(
            branding.logo_path,
            left=Inches(3),
            top=Inches(2),
            width=Inches(4)
        )
    else:
        title = slide.shapes.title
        tf = title.text_frame
        tf.clear()

        p = tf.paragraphs[0]
        p.text = branding.brand_text or ""
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(40)
        p.font.bold = True
        p.font.color.rgb = hex_to_rgb(branding.primary_color)


def build_content_slide(
    prs: Presentation,
    slide_data: SlideContent,
    branding: Branding
):
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    clear_slide(slide)
    apply_background(slide, branding.background_color)

    # Title
    title_shape = slide.shapes.title
    tf = title_shape.text_frame
    tf.clear()

    title_p = tf.paragraphs[0]
    title_p.text = slide_data.title
    title_p.font.color.rgb = hex_to_rgb(branding.primary_color)

    # Content
    body = slide.placeholders[1]
    tf = body.text_frame
    tf.clear()

    for i, bullet in enumerate(slide_data.bullets):
        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p.text = bullet
        p.level = 0
        p.font.color.rgb = hex_to_rgb(branding.primary_color)


# --------------------------------------------------
# Main Generators
# --------------------------------------------------

def _clear_all_slides(prs: Presentation):
    while prs.slides:
        rId = prs.slides._sldIdLst[0].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[0]


def generate_pptx_faithful(
    formatting_pptx: str,
    output_path: str,
    raw_text: str,
    branding: Branding
):
    prs = Presentation(formatting_pptx)
    _clear_all_slides(prs)

    slides = parse_faithful_text(raw_text)

    build_intro_slide(prs, branding)

    for slide_data in slides:
        build_content_slide(prs, slide_data, branding)

    prs.save(output_path)


def generate_pptx(
    formatting_pptx: str,
    output_path: str,
    slides: List[SlideContent],
    branding: Branding
):
    prs = Presentation(formatting_pptx)
    _clear_all_slides(prs)

    build_intro_slide(prs, branding)

    for slide in slides:
        build_content_slide(prs, slide, branding)

    prs.save(output_path)
