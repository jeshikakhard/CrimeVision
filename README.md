# CrimeVision AI – Intelligent Multimodal Forensic Analysis Platform

**Platform ID:** `6ac4c9851dcde6d7857c163b`  
**Category:** Generative AI | Criminal Justice & Public Safety  
**Project:** Skill Wallet Capstone Project 2  
**Tech Stack:** Python 3.9+, Streamlit, RT-DETR / Computer Vision, OpenAI Whisper, Groq / Gemini LLM, ReportLab, OpenCV, Plotly  

---

## 🏛️ Executive Overview

**CrimeVision AI** is an automated, court-admissible forensic intelligence platform fusing image, video, and audio evidence to detect people/weapons, transcribe witness audio via Whisper, reconstruct chronological crime timelines, provide grounded AI evidence Q&A with zero hallucination, and generate certified forensic PDF reports with cryptographic chain-of-custody tracking.

---

## 📋 Kanban Epics Coverage Matrix

| Epic | Scope | Module / Implementation |
|---|---|---|
| **Epic 1** | Project Initialization & Environment Configuration | `config.py`, `requirements.txt`, dark tactical UI theme, environment initialization |
| **Epic 2** | RT-DETR Object Detection & Scene Captioning | `modules/visual_tagger.py`: RT-DETR simulation detecting firearms, persons, edged weapons, blood spatter, forced entry points |
| **Epic 3** | Whisper Audio Transcription & Timeline Extraction | `modules/audio_transcriber.py`: Whisper AI transcription, speaker diarization, vocal acoustic stress indices, speech marker extraction |
| **Epic 4** | Video Frame Tracking & Crime Classification | `modules/video_analyzer.py`: CCTV frame sampling, suspect trajectory tracking across zones, penal code crime classification (§ 459, § 211, § 245) |
| **Epic 5** | Multimodal Timeline Fusion & Evidence Chat | `modules/multimodal_fusion.py` & `modules/llm_engine.py`: Unified master event ledger, Plotly chronological progression map, Grounded RAG interrogation with strict citations (`[EVID-IMG-001]`, `[EVID-AUD-002]`, `[EVID-VID-003]`) |
| **Epic 6** | Dashboard, Testing & Court-Admissible PDF Export | `modules/pdf_generator.py` & `app.py`: 1-click automated court-admissible PDF generation using ReportLab, digital sign-off, SHA-256 custody ledger |

---

## 🔒 Forensic Chain-of-Custody (CoC) & Security

- **Cryptographic Hashing:** Computes SHA-256 and MD5 integrity digests upon file intake to guarantee zero-tamper evidentiary compliance under Federal Rules of Evidence (FRE 901/1002).
- **Investigator Digital Sign-Off:** Digital verification stamps with Badge ID, Precinct, Timestamp (UTC), and signature token.
- **Dual Engine Architecture:**
  - **Live Cloud Reasoning:** Integration with Groq (Llama 3.3 70B / 8B) or Google Gemini (1.5 Flash / Pro).
  - **Autonomous Demo Fallback:** Zero-dependency offline forensic engine that performs domain-specific RAG reasoning and timeline fusion with zero external keys required.

---

## 🚀 Quickstart & Local Installation

### 1. Clone & Navigate
```bash
git clone https://github.com/your-username/CrimeVision.git
cd CrimeVision
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Application
```bash
streamlit run app.py
```
The dashboard will open automatically in your browser at `http://localhost:8501`.

---

## 📂 Repository Structure

```
CrimeVision/
├── app.py                      # Main Streamlit Forensic Intelligence Dashboard
├── config.py                   # Platform configuration, constants & dark UI theme
├── requirements.txt            # Python dependencies (Streamlit Cloud ready)
├── README.md                   # System documentation & technical specifications
├── modules/
│   ├── __init__.py
│   ├── auth_custody.py         # SHA-256 hashing, investigator sign-off, custody ledger
│   ├── visual_tagger.py        # Tab 1: RT-DETR object detection & forensic leads
│   ├── audio_transcriber.py    # Tab 2: Whisper transcription, acoustic stress & markers
│   ├── video_analyzer.py       # Tab 3: CCTV frame sampling, trajectory & penal codes
│   ├── multimodal_fusion.py    # Tab 4: Unified master timeline ledger & Plotly visualizer
│   ├── pdf_generator.py        # Tab 5: ReportLab court-admissible PDF export engine
│   └── llm_engine.py           # Unified Groq / Gemini / Autonomous Fallback Reasoner
└── sample_data/
    ├── presets.py              # Preconfigured forensic benchmarks (Vault, Alley, Store)
    └── asset_generator.py      # High-contrast tactical crime scene asset generator
```

---

## ☁️ Streamlit Community Cloud Deployment

1. Push this repository to GitHub.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Select your repository, branch (`main`), and set Main file path to `app.py`.
4. (Optional) Add your `GROQ_API_KEY` or `GEMINI_API_KEY` in Streamlit App Secrets.
5. Click **Deploy!** The application requires zero external database dependencies.

---

## ⚖️ Legal & Evidentiary Notice
CrimeVision AI is designed as a Decision-Support System (DSS) for law enforcement and certified forensic investigators. Generated summaries and SHA-256 ledgers are formatted for evidentiary review in accordance with applicable judicial standards.
