import streamlit as st
import os
from pptx_engine import (
    generate_pptx_faithful,
    Branding,
    random_hex_color
)

st.set_page_config(
    page_title="Professional Slide Generator",
    layout="wide"
)

st.title("🎯 Professional Slide Generator")

# --------------------------------------------------
# Branding Sidebar
# --------------------------------------------------

st.sidebar.header("Branding")

logo = st.sidebar.file_uploader(
    "Logo (PNG / JPG / JPEG)",
    type=["png", "jpg", "jpeg"]
)

brand_text = st.sidebar.text_input(
    "Brand Text (used if no logo)"
)

primary = st.sidebar.color_picker(
    "Primary Color (optional)",
    value=None
)

accent = st.sidebar.color_picker(
    "Accent Color (optional)",
    value=None
)

background = st.sidebar.color_picker(
    "Background Color (optional)",
    value=None
)

# --------------------------------------------------
# Main Inputs
# --------------------------------------------------

formatting_pptx = st.file_uploader(
    "Formatting PPTX (REQUIRED)",
    type=["pptx"]
)

notes = st.text_area(
    "Paste Slide Notes (Faithful Mode)",
    height=320
)

faithful_mode = st.checkbox(
    "Faithful Mode (generate exactly as written)",
    value=True
)

# --------------------------------------------------
# Generate
# --------------------------------------------------

if st.button("🚀 Generate Slides"):
    if not formatting_pptx:
        st.error("Formatting PPTX is required.")
        st.stop()

    with open("formatting.pptx", "wb") as f:
        f.write(formatting_pptx.read())

    logo_path = None
    if logo:
        logo_path = logo.name
        with open(logo_path, "wb") as f:
            f.write(logo.read())

    branding = Branding(
        logo_path=logo_path,
        brand_text=brand_text,
        primary_color=primary.replace("#", "") if primary else random_hex_color(),
        accent_color=accent.replace("#", "") if accent else random_hex_color(),
        background_color=background.replace("#", "") if background else random_hex_color(220, 255),
    )

    generate_pptx_faithful(
        formatting_pptx="formatting.pptx",
        output_path="output.pptx",
        raw_text=notes,
        branding=branding
    )

    with open("output.pptx", "rb") as f:
        st.success("Slides generated successfully 🎉")
        st.download_button(
            "⬇️ Download PPTX",
            f,
            file_name="slides.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
