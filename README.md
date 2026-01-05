# SLIDES MAKER

This application takes text, a brnad template and an potional layout template and it generates slides Using LLMs.

1. How Template Combination Works

Template 1 – Branding

Used for:

Theme

Logo

Footer

Colors

Fonts

Template 2 – Layout

Used for:

Placeholder positions

Title/body layout

Visual balance

Result:

Brand identity + structured layout + AI-generated content in one slide

2. “Faithful Mode”

Purpose:

Generate slides exactly as written in the input notes. No summarization, rephrasing, or LLM interpretation. Perfect for curriculum content, lectures, or strict teaching material.

Behavior:

Slide titles = exactly from notes

Bullet points = exactly as written

Presenter notes = preserved verbatim

Slide order = preserved

LLM = optional (used only for minor validation or ignored completely)

## Requirements and local build instruction

Install python3

## For Debian/Ubuntu-based systems

```
sudo apt update
sudo apt install python3 python3-venv
```

## Ubuntu / Debian / PopOS / Mint

```
sudo apt update
sudo apt install python3-tk
```

## For Fedora-based systems

```
sudo dnf install python3 python3-venv
```

## Clone this repository

Create a virtual environment using the venv module. This command creates a new directory (commonly named .venv or env) that contains an isolated Python installation:

```
cd slides-maker

python3 -m venv .venv
```

## Activate the virtual environment.

```
source .venv/bin/activate
```

## Install packages using pip.

The packages will be installed into your isolated environment, not the system's Python:

```
pip install streamlit python-pptx requests
```

## Run Application

To run this application locally, you need to setup [Ollama](https://github.com/intuvance/ollama-expertsystem)

# Run locally

```
streamlit run app.py
```

echo "paradygm-storage db-storage certs certbot" | xargs -n 1 docker volume create

# Using docker compose

```
docker compose up --build -d
```
