# SLIDES MAKER

**Slides Maker** is a professional slide generation tool that converts structured text into fully styled PowerPoint presentations (`.pptx`).

It supports **strict curriculum-grade slide generation**, **template-driven styling**, and **optional AI assistance**, while guaranteeing **non-corrupt, standards-compliant PPTX output**.

---

## ✨ Key Features

- ✅ Generates **valid, non-corrupt `.pptx` files**
- 🎨 Preserves **designer-defined PowerPoint styles**
- 📚 **Faithful Mode** for exact lecture/curriculum slides
- 🧠 Optional **LLM-assisted generation**
- 🖼️ Logo or text-based branding
- 🎯 Deterministic layout handling
- 🌈 Dynamic branding colors (manual or auto-generated)

---

## 🧩 How Template Usage Works

Slides Maker uses a **single formatting template** as the authoritative source of layout and style.

> ⚠️ Only one PPTX template is required and accepted.

### Formatting Template (Required)

Used for:

- Fonts
- Colors
- Bullet styles
- Spacing
- Placeholder positioning
- Visual hierarchy

**Important behavior:**

- All text inside the template is **cleared**
- Only **styles and layouts** are preserved
- New content is injected safely (no appending)

This guarantees:

- No duplicated text
- No PPTX corruption
- Perfect style preservation

---

## 🎨 Branding Handling (No Branding PPTX)

Branding is handled dynamically

### Branding Options

- **Logo image** (`PNG`, `JPG`, `JPEG`)
- **OR** brand text (centered on intro slide)
- **Three colors**:

  - Primary
  - Accent
  - Background

If colors are not provided, the system generates **readable random HEX colors** automatically.

The **intro slide contains only branding**, nothing else.

---

## 🧠 Faithful Mode (Exact Slide Generation)

### Purpose

Faithful Mode is designed for **strict educational and curriculum content** where accuracy matters.

No summarization.
No paraphrasing.
No creative interpretation.

Perfect for:

- Lectures
- Training material
- Academic content
- Compliance documentation

---

### Behavior

When **Faithful Mode is enabled**:

- Slide titles → **exactly as written**
- Bullet points → **exactly as written**
- Slide order → **preserved**
- Presenter notes → **preserved verbatim**
- LLM → **optional or completely bypassed**

The system **parses the text deterministically** instead of relying on AI to interpret structure.

---

## 🤖 AI Mode (Optional)

When Faithful Mode is disabled:

- The input prompt may be interpreted
- Slides can be summarized or structured
- An LLM (via Ollama) can assist in content generation

> AI is **never required** for Faithful Mode.

---

## 🛠 Requirements

- Python **3.9+**
- PowerPoint-compatible OS (any)
- Optional: Ollama (for AI mode only)

---

## 🔧 Local Build Instructions

### Install Python (Debian / Ubuntu / Mint / PopOS)

```bash
sudo apt update
sudo apt install python3 python3-venv python3-tk
```

### Fedora

```bash
sudo dnf install python3 python3-venv
```

---

## 📦 Clone Repository

```bash
git clone <your-repo-url>
cd slides-maker
```

---

## 🧪 Create Virtual Environment

```bash
python3 -m venv .venv
```

### Activate Environment

```bash
source .venv/bin/activate
```

---

## 📥 Install Dependencies

```bash
pip install streamlit python-pptx requests
```

---

## ▶️ Run Locally

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🤖 Optional: AI Setup (Ollama)

AI generation requires Ollama.

Follow setup instructions here:
👉 [https://github.com/intuvance/ollama-expertsystem](https://github.com/intuvance/ollama-expertsystem)

Ensure the model you want (e.g. `llama3.x`) is pulled and running.

---

## 🐳 Docker Support

### Run with Docker Compose

```bash
docker compose up --build -d
```

---

## 🧑‍🎨 Template Authoring Guidelines (Summary)

Designers should:

- Use **Slide Master layouts**
- Use **placeholders**, not text boxes
- Define bullet styles in the master
- Avoid animations or sample text
- Keep layout indices consistent:

  - Layout 0 → Intro
  - Layout 1 → Title + Content

All text will be replaced at runtime.
