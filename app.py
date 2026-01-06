import streamlit as st
import os

from pptx_engine import (
    generate_pptx_faithful,
    Branding,
    random_hex_color,
)

# --------------------------------------------------
# App Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Slides Maker",
    layout="wide"
)

st.title("🎯 Slides Maker")

st.markdown(
    """
Generate **professional, non-corrupt PowerPoint slides** from structured text.

• Use **Faithful Mode** for curriculum / lecture material  
• Upload **one formatting PPTX** to control all styles  
"""
)

# --------------------------------------------------
# Sidebar: Branding
# --------------------------------------------------

st.sidebar.header("🎨 Branding")

logo = st.sidebar.file_uploader(
    "Logo (PNG / JPG / JPEG)",
    type=["png", "jpg", "jpeg"],
    help="Optional. If not provided, brand text will be used."
)

brand_text = st.sidebar.text_input(
    "Brand Text (used if no logo)",
    placeholder="e.g. Introduction to Computing"
)

primary_color = st.sidebar.color_picker(
    "Primary Color (optional)",
    value=None
)

accent_color = st.sidebar.color_picker(
    "Accent Color (optional)",
    value=None
)

background_color = st.sidebar.color_picker(
    "Background Color (optional)",
    value=None
)

# --------------------------------------------------
# Main Inputs
# --------------------------------------------------

st.subheader("📄 Formatting Template")

formatting_pptx = st.file_uploader(
    "Upload Formatting PPTX (required)",
    type=["pptx"],
    help="This PPTX defines fonts, spacing, bullet styles, and layouts."
)

st.subheader("⚙️ Generation Mode")

faithful_mode = st.checkbox(
    "Faithful Mode (generate slides exactly as written)",
    value=True,
    help="Recommended for lectures and curriculum content."
)

notes = ""

if faithful_mode:
    st.subheader("📝 Slide Notes (Faithful Mode)")
    notes = st.text_area(
        "Paste slide notes",
        height=320,
        help="Slides will be generated exactly as written. No summarization."
    )
else:
    st.subheader("🤖 AI Prompt")
    notes = st.text_area(
        "Enter a prompt for AI slide generation",
        height=320,
        help="AI mode may summarize or restructure content (not yet implemented)."
    )

# --------------------------------------------------
# Generate Button
# --------------------------------------------------

if st.button("🚀 Generate Slides", type="primary"):
    if not formatting_pptx:
        st.error("Formatting PPTX is required.")
        st.stop()

    if faithful_mode and not notes.strip():
        st.error("Please paste slide notes for Faithful Mode.")
        st.stop()

    # Save formatting template
    with open("formatting.pptx", "wb") as f:
        f.write(formatting_pptx.read())

    # Save logo if provided
    logo_path = None
    if logo:
        logo_path = logo.name
        with open(logo_path, "wb") as f:
            f.write(logo.read())

    # Build branding (random colors if not provided)
    branding = Branding(
        logo_path=logo_path,
        brand_text=brand_text,
        primary_color=primary_color.replace("#", "") if primary_color else random_hex_color(),
        accent_color=accent_color.replace("#", "") if accent_color else random_hex_color(),
        background_color=background_color.replace("#", "") if background_color else random_hex_color(220, 255),
    )

    # --------------------------------------------------
    # Generation
    # --------------------------------------------------

    if faithful_mode:
        generate_pptx_faithful(
            "formatting.pptx",
            notes,
            "output.pptx",
            branding
        )
    else:
        st.warning("AI mode is not implemented yet.")
        st.stop()

    # --------------------------------------------------
    # Download
    # --------------------------------------------------

    with open("output.pptx", "rb") as f:
        st.success("✅ Slides generated successfully")
        st.download_button(
            "⬇️ Download PPTX",
            f,
            file_name="slides.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
