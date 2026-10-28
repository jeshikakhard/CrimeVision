"""
CrimeVision AI - Intelligent Multimodal Forensic Analysis Platform
Platform ID: 6ac4c9851dcde6d7857c163b
Category: Generative AI | Criminal Justice & Public Safety
Capstone Project 2 (Skill Wallet)
"""

import os
import sys

# Ensure repository root is in sys.path for Streamlit Community Cloud deployment
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import io
import re
import textwrap
import datetime
import streamlit as st
import pandas as pd
from PIL import Image

# Import platform configuration & modules
from config import APP_CONFIG, FORENSIC_THEME_CSS
from modules.auth_custody import ChainOfCustodyManager
from modules.visual_tagger import VisualEvidenceTagger
from modules.audio_transcriber import ForensicAudioTranscriber
from modules.video_analyzer import CCTVVideoAnalyzer
from modules.multimodal_fusion import MultimodalFusionEngine
from modules.pdf_generator import ForensicPDFReportGenerator
from modules.llm_engine import ForensicLLMEngine
from sample_data.presets import CASE_PRESETS
from sample_data.asset_generator import generate_crime_scene_image, get_image_bytes


def format_forensic_citations(text: str) -> str:
    """Format evidence IDs like [EVID-IMG-001] into glowing forensic citation tags."""
    if not text:
        return ""
    pattern = r'\[(EVID-[A-Za-z0-9\-]+)\]'
    return re.sub(pattern, r'<span class="citation-chip">🔒 \1</span>', text)



# Set Streamlit Page Configuration
st.set_page_config(
    page_title=f"{APP_CONFIG['APP_NAME']} | Forensic Analysis Platform",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Forensic Dark Theme CSS
st.markdown(FORENSIC_THEME_CSS, unsafe_allow_html=True)


# Initialize Session State
if "custody_mgr" not in st.session_state:
    st.session_state.custody_mgr = ChainOfCustodyManager()

if "active_case_id" not in st.session_state:
    st.session_state.active_case_id = "CR-2026-8831"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": "CrimeVision AI evidentiary reasoner online. Multimodal evidence context loaded. You may query timestamps, suspect telemetry, weapon detections, and witness statements. Strict Evidence ID citations will be enforced."
        }
    ]

if "investigator_name" not in st.session_state:
    st.session_state.investigator_name = APP_CONFIG["DEFAULT_INVESTIGATOR"]
if "badge_id" not in st.session_state:
    st.session_state.badge_id = "DFU-4928"
if "precinct" not in st.session_state:
    st.session_state.precinct = APP_CONFIG["DEFAULT_PRECINCT"]


# Cached Helper instances
@st.cache_resource
def get_visual_tagger():
    return VisualEvidenceTagger()

@st.cache_resource
def get_video_analyzer():
    return CCTVVideoAnalyzer()

@st.cache_resource
def get_fusion_engine():
    return MultimodalFusionEngine()

@st.cache_resource
def get_pdf_generator():
    return ForensicPDFReportGenerator()


visual_tagger = get_visual_tagger()
video_analyzer = get_video_analyzer()
fusion_engine = get_fusion_engine()
pdf_generator = get_pdf_generator()


# ==========================================
# SIDEBAR: CASE, INVESTIGATOR & LLM SECURITY
# ==========================================
with st.sidebar:
    st.markdown("### 🛡️ CASE CONTROL & SECURITY")
    st.markdown(f"<span class='evid-tag'>PLATFORM ID: {APP_CONFIG['PLATFORM_ID']}</span>", unsafe_allow_html=True)
    st.markdown(f"<span class='forensic-badge badge-live'>SYSTEM: OPERATIONAL</span>", unsafe_allow_html=True)
    st.markdown("---")

    # Case Selection
    selected_case_id = st.selectbox(
        "Select Active Forensic Case",
        options=list(CASE_PRESETS.keys()) + ["CUSTOM_CASE"],
        index=0,
        help="Select a benchmark case scenario or initialize custom evidence intake."
    )
    st.session_state.active_case_id = selected_case_id

    if selected_case_id != "CUSTOM_CASE":
        case_info = CASE_PRESETS[selected_case_id]
        st.markdown(f"**Case Title:** {case_info['title']}")
        st.markdown(f"**Location:** `{case_info['location']}`")
        st.markdown(f"<span class='forensic-badge badge-critical'>{case_info['threat_rating']}</span>", unsafe_allow_html=True)
    else:
        case_info = {
            "case_id": "CR-CUSTOM-001",
            "title": "Ad-Hoc Digital Evidence Ingestion",
            "location": "Unspecified Jurisdiction",
            "classification": "General Criminal Investigation",
            "threat_rating": "HIGH",
            "visual_preset": "custom",
            "audio_preset": "custom",
            "video_preset": "custom",
            "primary_suspect": "Subject Under Investigation",
            "incident_timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "evidence_files": {"image": "custom_image.jpg", "audio": "custom_audio.wav", "video": "custom_video.mp4"}
        }

    st.markdown("---")

    # Lead Investigator Profile
    st.markdown("#### 👤 Investigator Sign-off")
    st.session_state.investigator_name = st.text_input("Investigator Name", value=st.session_state.investigator_name)
    st.session_state.badge_id = st.text_input("Badge / Token ID", value=st.session_state.badge_id)
    st.session_state.precinct = st.text_input("Agency / Unit", value=st.session_state.precinct)

    # Sign-off button
    if st.button("✍️ Certify & Sign-off Evidence"):
        st.session_state.custody_mgr.sign_off_evidence(
            "EVID-IMG-001",
            st.session_state.investigator_name,
            st.session_state.badge_id,
            "Court-admissible verification certified."
        )
        st.session_state.custody_mgr.sign_off_evidence(
            "EVID-AUD-002",
            st.session_state.investigator_name,
            st.session_state.badge_id,
            "Audio transcript acoustic integrity verified."
        )
        st.session_state.custody_mgr.sign_off_evidence(
            "EVID-VID-003",
            st.session_state.investigator_name,
            st.session_state.badge_id,
            "CCTV keyframes and penal progression verified."
        )
        st.success("✅ Chain-of-Custody digitally sealed!")

    st.markdown("---")

    # LLM Provider Configuration
    st.markdown("#### ⚡ AI Reasoning Engine")
    llm_provider = st.selectbox(
        "LLM Reasoner Provider",
        options=["Autonomous Reasoner (Demo Mode)", "Groq API", "Google Gemini API"],
        index=0,
        help="Select demo fallback for zero-dependency instant execution, or input Groq/Gemini key for live cloud models."
    )

    api_key = ""
    model_choice = None

    if llm_provider == "Groq API":
        api_key = st.text_input("Groq API Key (gsk_...)", type="password", help="Enter your Groq API key")
        model_choice = st.selectbox("Groq Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"])
        if api_key:
            st.caption("🟢 Groq API Key Registered")
        else:
            st.caption("⚠️ No key provided: will gracefully fallback to Autonomous Reasoner")
    elif llm_provider == "Google Gemini API":
        api_key = st.text_input("Gemini API Key (AIza...)", type="password", help="Enter your Google Gemini API key")
        model_choice = st.selectbox("Gemini Model", ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"])
        if api_key:
            st.caption("🟢 Gemini API Key Registered")
        else:
            st.caption("⚠️ No key provided: will gracefully fallback to Autonomous Reasoner")
    else:
        st.caption("🛡️ Autonomous Forensic Reasoner active (Offline Zero-Hallucination Mode)")

    st.markdown("---")
    st.markdown("#### ⛓️ Chain-of-Custody Ledger")
    custody_entries = st.session_state.custody_mgr.evidence_ledger
    if custody_entries:
        for ent in custody_entries:
            st.markdown(f"**{ent['evidence_id']}** • `{ent['short_sha']}` • <span class='badge-live'>{ent['status']}</span>", unsafe_allow_html=True)
    else:
        st.caption("Evidence registered dynamically upon analysis.")


# Initialize LLM Reasoner
provider_label = "Groq" if "Groq" in llm_provider else ("Gemini" if "Gemini" in llm_provider else "Demo Fallback")
llm_engine = ForensicLLMEngine(provider=provider_label, api_key=api_key, model_name=model_choice)
audio_transcriber = ForensicAudioTranscriber(api_key=api_key, provider=provider_label)


# ==========================================
# HEADER: TOP BANNER & METRIC DASHBOARD
# ==========================================
st.markdown(f"""
<div class="forensic-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1 style="margin: 0; font-size: 2.0rem; font-weight: 800; letter-spacing: -0.02em; color: #f8fafc;">
                ⚖️ CrimeVision <span style="color: #00e5ff;">AI</span>
            </h1>
            <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 0.95rem;">
                {APP_CONFIG['SUBTITLE']} • <span class="evid-tag">{APP_CONFIG['CAPSTONE_PROJECT']}</span>
            </p>
        </div>
        <div style="display: flex; gap: 8px; align-items: center; margin-top: 8px;">
            <span class="forensic-badge badge-custody">CASE: {case_info['case_id']}</span>
            <span class="forensic-badge badge-critical">THREAT: {case_info['threat_rating']}</span>
            <span class="forensic-badge badge-live">REASONER: {provider_label}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# Responsive Forensic KPI Status Grid (Replaces clipped st.metric columns)
threat_rating = case_info.get("threat_rating", "HIGH")
kpi_threat_class = "kpi-critical" if threat_rating in ["CRITICAL", "MAXIMUM"] else "kpi-amber"
full_class = case_info.get("classification", "Aggravated Felony")
short_class = "Armed Burglary" if "Burglary" in full_class else ("Homicide Investigation" if "Homicide" in full_class else full_class.split("(")[0].strip()[:24])
statute_delta = "Penal Code § 459 / § 211" if "Burglary" in full_class else "Priority 1 Felony"

st.markdown(textwrap.dedent(f"""
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-label"><span>📁</span> Primary Case ID</div>
        <div class="kpi-value">{case_info['case_id']}</div>
        <div class="kpi-delta"><span>●</span> Active Investigation</div>
    </div>
    <div class="kpi-card kpi-emerald">
        <div class="kpi-label"><span>🔒</span> Custody Integrity</div>
        <div class="kpi-value">100% SHA-256</div>
        <div class="kpi-delta" style="color: #10b981;"><span>✓</span> Zero Tamper Sealed</div>
    </div>
    <div class="kpi-card {kpi_threat_class}">
        <div class="kpi-label"><span>🚨</span> Scene Classification</div>
        <div class="kpi-value">{short_class}</div>
        <div class="kpi-delta"><span>▲</span> {statute_delta}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label"><span>📡</span> Evidence Streams</div>
        <div class="kpi-value">3 Modalities</div>
        <div class="kpi-delta" style="color: #38bdf8;"><span>⚡</span> Img + Aud + Vid</div>
    </div>
    <div class="kpi-card kpi-amber">
        <div class="kpi-label"><span>⚖️</span> Judicial Standard</div>
        <div class="kpi-value">FRE 901 Seal</div>
        <div class="kpi-delta" style="color: #f59e0b;"><span>★</span> Court Admissible</div>
    </div>
</div>
"""), unsafe_allow_html=True)


# Pre-generate Evidence for the Active Case
active_visual_preset = case_info.get("visual_preset", "vault")
active_audio_preset = case_info.get("audio_preset", "vault")
active_video_preset = case_info.get("video_preset", "vault")

preset_image = generate_crime_scene_image(active_visual_preset)
preset_image_bytes = get_image_bytes(preset_image)

# Register evidence in chain of custody
st.session_state.custody_mgr.register_evidence(
    "EVID-IMG-001",
    "Digital Photography",
    case_info["evidence_files"]["image"],
    preset_image_bytes,
    st.session_state.investigator_name,
    st.session_state.badge_id,
    st.session_state.precinct,
    notes=f"Visual evidence for case {case_info['case_id']}"
)

st.session_state.custody_mgr.register_evidence(
    "EVID-AUD-002",
    "Emergency Audio Tape",
    case_info["evidence_files"]["audio"],
    b"WAVE_FORENSIC_AUDIO_MOCK_STREAM_HEADER_CHECK",
    st.session_state.investigator_name,
    st.session_state.badge_id,
    st.session_state.precinct,
    notes=f"Dispatch audio for case {case_info['case_id']}"
)

st.session_state.custody_mgr.register_evidence(
    "EVID-VID-003",
    "CCTV Surveillance Video",
    case_info["evidence_files"]["video"],
    b"MP4_FORENSIC_CCTV_STREAM_HEADER_CHECK",
    st.session_state.investigator_name,
    st.session_state.badge_id,
    st.session_state.precinct,
    notes=f"CCTV surveillance for case {case_info['case_id']}"
)


# Process Data across modalities for global state
visual_analysis = visual_tagger.detect_objects_rtdetr(preset_image, confidence_thresh=0.40, preset_type=active_visual_preset)
audio_analysis = audio_transcriber.transcribe_and_analyze(b"", case_info["evidence_files"]["audio"], preset_type=active_audio_preset)
video_analysis = video_analyzer.process_cctv_feed(preset_type=active_video_preset)
master_timeline = fusion_engine.build_unified_master_ledger(case_info["case_id"], visual_analysis, audio_analysis, video_analysis)


# ==========================================
# MAIN TABBED WORKSPACE (EPICS 2 - 6)
# ==========================================
tabs = st.tabs([
    "📸 Scene Vision",
    "🎙️ Audio & Whisper",
    "🎥 CCTV & Penal",
    "🧠 Fusion & RAG",
    "📄 Legal PDF Export"
])


# ---------------------------------------------------------------------------------
# TAB 1: CRIME SCENE VISUAL EVIDENCE TAGGER (EPIC 2)
# ---------------------------------------------------------------------------------
with tabs[0]:
    st.markdown("### 📸 Crime Scene Visual Evidence Tagger (Epic 2)")
    st.markdown("Multimodal object detection simulating **RT-DETR (Real-Time DEtection TRansformer)** identifying weapons, persons, blood spatter, and forced entry points.")

    col_t1_left, col_t1_right = st.columns([1.1, 0.9])

    with col_t1_left:
        st.markdown("#### 📥 Visual Evidence Input")
        uploaded_img = st.file_uploader(
            "Upload Crime Scene Photography (JPG/PNG)",
            type=["jpg", "jpeg", "png"],
            key="img_uploader",
            help="Upload custom high-resolution scene photography or use active case preset."
        )

        if uploaded_img is not None:
            active_img = Image.open(uploaded_img)
            active_img_bytes = uploaded_img.getvalue()
            current_preset = "custom"
            st.session_state.custody_mgr.register_evidence(
                "EVID-IMG-001",
                "Uploaded Photography",
                uploaded_img.name,
                active_img_bytes,
                st.session_state.investigator_name,
                st.session_state.badge_id,
                st.session_state.precinct,
                notes="Custom user-uploaded crime scene photograph"
            )
        else:
            active_img = preset_image
            current_preset = active_visual_preset

        # Detection Controls
        c_ctrl1, c_ctrl2 = st.columns(2)
        with c_ctrl1:
            conf_thresh = st.slider("RT-DETR Confidence Threshold", 0.20, 0.95, 0.40, 0.05)
        with c_ctrl2:
            all_cats = list(VisualEvidenceTagger.CATEGORY_COLORS.keys())
            selected_cats = st.multiselect("Filter Object Classes", all_cats, default=all_cats)

        # Run Detection
        detection_result = visual_tagger.detect_objects_rtdetr(
            active_img,
            confidence_thresh=conf_thresh,
            preset_type=current_preset
        )
        annotated_image = visual_tagger.render_bounding_boxes(
            active_img,
            detection_result["detected_objects"],
            selected_categories=selected_cats
        )

        st.image(
            annotated_image,
            caption=f"RT-DETR Annotated Crime Scene Evidence [EVID-IMG-001] • {len(detection_result['detected_objects'])} Objects Flagged",
            use_container_width=True
        )

        # Evidence Hash Stamp
        evid_rec = st.session_state.custody_mgr.get_evidence_by_id("EVID-IMG-001")
        if evid_rec:
            st.caption(f"🔒 SHA-256: `{evid_rec['sha256']}` | Status: **{evid_rec['status']}**")

    with col_t1_right:
        st.markdown("#### 🔬 Structured Forensic Analysis")

        # Threat & Classification Banner
        threat_badge_class = "badge-critical" if detection_result["threat_level"] == "CRITICAL" else "badge-high"
        st.markdown(textwrap.dedent(f"""
        <div class="forensic-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.85rem; color: #94a3b8;">OVERALL SCENE THREAT:</span>
                <span class="forensic-badge {threat_badge_class}">{detection_result['threat_level']}</span>
            </div>
            <h4 style="margin: 8px 0 0 0; color: #00e5ff;">{detection_result['classification']}</h4>
        </div>
        """), unsafe_allow_html=True)

        # Detected Objects Table
        st.markdown("##### 🎯 Detected Forensic Entities")
        det_rows = []
        for det in detection_result["detected_objects"]:
            det_rows.append({
                "ID": det["id"],
                "Item": det["label"],
                "Category": det["category"],
                "Confidence": f"{det['confidence']*100:.1f}%",
                "Spatial BBox": str(det["box_coords"]),
                "Threat": det["threat_weight"]
            })

        if det_rows:
            st.dataframe(pd.DataFrame(det_rows), use_container_width=True, hide_index=True)
        else:
            st.info("No objects detected above selected confidence threshold.")

        # Computer Vision Metrics
        st.markdown("##### 📐 Forensic Image Quality & Photometry")
        metrics = detection_result["image_metrics"]
        st.markdown(textwrap.dedent(f"""
        <div class="photometric-grid">
            <div class="photometric-card">
                <div class="pm-label">Resolution</div>
                <div class="pm-val">{metrics['resolution']}</div>
            </div>
            <div class="photometric-card">
                <div class="pm-label">Laplacian Sharpness</div>
                <div class="pm-val">{metrics['sharpness_score']}</div>
            </div>
            <div class="photometric-card">
                <div class="pm-label">Lighting Assessment</div>
                <div class="pm-val">{metrics['lighting_eval']}</div>
            </div>
        </div>
        """), unsafe_allow_html=True)

        # Prioritized Leads
        st.markdown("##### 🚨 Prioritized Investigative Leads")
        for i, lead in enumerate(detection_result["investigative_leads"], 1):
            st.markdown(textwrap.dedent(f"""
            <div style="padding: 10px 14px; margin-bottom: 8px; background: rgba(15, 23, 42, 0.85); border-left: 3px solid #00e5ff; border-radius: 0 8px 8px 0; font-size: 0.88rem; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);">
                <span class="forensic-badge badge-custody" style="margin-right: 6px; padding: 2px 8px;">LEAD #{i}</span>
                <span style="color: #f8fafc;">{lead}</span>
            </div>
            """), unsafe_allow_html=True)


# ---------------------------------------------------------------------------------
# TAB 2: WITNESS AUDIO TRANSCRIPTION & TIMELINE (EPIC 3)
# ---------------------------------------------------------------------------------
with tabs[1]:
    st.markdown("### 🎙️ Witness Audio Transcription & Timeline Extraction (Epic 3)")
    st.markdown("Ingest 911 dispatch audio or witness depositions with **OpenAI Whisper AI**, acoustic stress telemetry, and chronological speech marker extraction.")

    col_t2_left, col_t2_right = st.columns([1.0, 1.0])

    with col_t2_left:
        st.markdown("#### 🎧 Audio Evidence Ingest")
        uploaded_audio = st.file_uploader(
            "Upload Witness Audio or 911 Call (WAV/MP3/M4A)",
            type=["wav", "mp3", "m4a", "ogg"],
            key="audio_uploader"
        )

        if uploaded_audio is not None:
            audio_bytes = uploaded_audio.getvalue()
            audio_analysis = audio_transcriber.transcribe_and_analyze(
                audio_bytes,
                uploaded_audio.name,
                preset_type="custom"
            )
            st.audio(audio_bytes)
            st.session_state.custody_mgr.register_evidence(
                "EVID-AUD-002",
                "Uploaded Witness Audio",
                uploaded_audio.name,
                audio_bytes,
                st.session_state.investigator_name,
                st.session_state.badge_id,
                st.session_state.precinct,
                notes="Custom witness audio recording uploaded"
            )
        else:
            st.info(f"🔊 Playing preset dispatch audio: `{audio_analysis['audio_filename']}`")
            # Synthesized visual audio representation
            st.caption(f"Audio Length: {audio_analysis['duration_seconds']}s | Sample Rate: 44.1 kHz 16-bit PCM")

        # Acoustic Stress & Biometrics
        st.markdown("#### 📊 Acoustic Stress & Vocal Biometrics")
        stress_val = audio_analysis["stress_index"]
        stress_color = "#10b981" if stress_val < 45 else ("#f59e0b" if stress_val < 75 else "#ff3366")
        stress_badge = "badge-live" if stress_val < 45 else ("badge-high" if stress_val < 75 else "badge-critical")

        st.markdown(textwrap.dedent(f"""
        <div class="stress-meter-box">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.82rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">
                    Vocal Stress Telemetry
                </span>
                <span class="forensic-badge {stress_badge}">{audio_analysis['urgency_level']} ({stress_val}/100)</span>
            </div>
            <div class="stress-track">
                <div class="stress-fill" style="width: {stress_val}%; background: linear-gradient(90deg, #10b981 0%, #f59e0b 50%, #ff3366 100%);"></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #64748b; margin-top: 4px;">
                <span>Baseline (0)</span>
                <span>Elevated (50)</span>
                <span>Critical Panic (100)</span>
            </div>
        </div>
        """), unsafe_allow_html=True)

        # Ballistic & Acoustic Signatures
        st.markdown("##### 🔊 Detected Acoustic Signatures")
        sig_df = pd.DataFrame(audio_analysis["acoustic_signatures"])
        st.dataframe(sig_df, use_container_width=True, hide_index=True)

        # Extracted Entities Card
        st.markdown("##### 🏷️ Extracted Forensic Entities")
        entities = audio_analysis["extracted_entities"]
        weapons_chips = "".join([f"<span class='entity-chip' style='border-color: rgba(255, 51, 102, 0.4); color: #fda4af;'>🔫 {w}</span>" for w in entities['weapons']])
        suspect_chips = "".join([f"<span class='entity-chip'>👤 {s}</span>" for s in entities['suspect_descriptors']])

        st.markdown(textwrap.dedent(f"""
        <div class="forensic-card" style="font-size: 0.88rem;">
            <div style="margin-bottom: 8px;">
                <b style="color: #ff3366; font-size: 0.78rem; text-transform: uppercase;">Weapons Flagged:</b>
                <div class="entity-chip-container">{weapons_chips if weapons_chips else '<span class="entity-chip">None detected</span>'}</div>
            </div>
            <div style="margin-bottom: 8px;">
                <b style="color: #38bdf8; font-size: 0.78rem; text-transform: uppercase;">Suspect Descriptors:</b>
                <div class="entity-chip-container">{suspect_chips}</div>
            </div>
            <div style="display: flex; gap: 12px; margin-top: 10px; flex-wrap: wrap;">
                <div style="background: rgba(30, 41, 59, 0.5); padding: 6px 12px; border-radius: 6px; border: 1px solid rgba(56, 189, 248, 0.2);">
                    <span style="font-size: 0.72rem; color: #94a3b8;">VEHICLE:</span> <b style="color: #00e5ff; font-size: 0.82rem;">{entities['vehicle']}</b>
                </div>
                <div style="background: rgba(30, 41, 59, 0.5); padding: 6px 12px; border-radius: 6px; border: 1px solid rgba(56, 189, 248, 0.2);">
                    <span style="font-size: 0.72rem; color: #94a3b8;">ESCAPE VECTOR:</span> <b style="color: #f59e0b; font-size: 0.82rem;">{entities['escape_vector']}</b>
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)

    with col_t2_right:
        st.markdown("#### 📜 Whisper Diarized Transcription")
        for line in audio_analysis["diarized_transcript"]:
            is_disp = "Dispatcher" in line["speaker"]
            is_susp = "Suspect" in line["speaker"]
            bubble_class = "diarized-dispatcher" if is_disp else ("diarized-suspect" if is_susp else "diarized-witness")
            spk_color = "#00e5ff" if is_disp else ("#ff3366" if is_susp else "#f59e0b")
            icon = "📡" if is_disp else ("⚠️" if is_susp else "👤")
            st.markdown(textwrap.dedent(f"""
            <div class="diarized-bubble {bubble_class}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-weight: 700; color: {spk_color}; font-size: 0.84rem; display: flex; align-items: center; gap: 6px;">
                        <span>{icon}</span> {line['speaker']}
                    </span>
                    <span class="mono-text" style="color: #94a3b8; font-size: 0.75rem; background: rgba(15, 23, 42, 0.6); padding: 2px 6px; border-radius: 4px;">[{line['time']}]</span>
                </div>
                <div style="color: #f1f5f9; font-size: 0.9rem; line-height: 1.45;">
                    "{line['text']}"
                </div>
            </div>
            """), unsafe_allow_html=True)

        st.markdown("#### ⏱️ Extracted Chronological Speech Markers")
        for marker in audio_analysis["chronological_markers"]:
            st.markdown(textwrap.dedent(f"""
            <div class="timeline-event-card threat-high">
                <span class="mono-text" style="color: #00e5ff; font-weight: bold;">[{marker['timestamp']}]</span>
                <span style="color: #94a3b8; font-size: 0.8rem; margin-left: 8px;">{marker['significance']}</span>
                <p style="margin: 4px 0 0 0; color: #f8fafc; font-size: 0.88rem;">{marker['event']}</p>
            </div>
            """), unsafe_allow_html=True)


# ---------------------------------------------------------------------------------
# TAB 3: CCTV VIDEO ANALYSIS & EVENT PROGRESSION (EPIC 4)
# ---------------------------------------------------------------------------------
with tabs[2]:
    st.markdown("### 🎥 CCTV Video Analysis & Event Progression (Epic 4)")
    st.markdown("Sample frame-by-frame surveillance feeds, track suspect trajectories across zones, and classify legal penal crime categories.")

    col_t3_left, col_t3_right = st.columns([1.1, 0.9])

    with col_t3_left:
        st.markdown("#### 📹 CCTV Surveillance Progression")
        uploaded_vid = st.file_uploader(
            "Upload CCTV Surveillance Video (MP4/AVI/MOV)",
            type=["mp4", "avi", "mov"],
            key="vid_uploader"
        )

        st.markdown(textwrap.dedent(f"""
        <div style="display: flex; gap: 8px; align-items: center; margin: 10px 0 16px 0; flex-wrap: wrap;">
            <span class="evid-tag">📡 STREAM: {video_analysis['camera_id']}</span>
            <span class="evid-tag">📐 SPEC: {video_analysis['resolution']}</span>
            <span class="forensic-badge badge-live">FPS: 30 FIXED</span>
            <span class="forensic-badge badge-custody">TRACKING: DEEPSORT/RT-DETR</span>
        </div>
        """), unsafe_allow_html=True)

        # Frame keyframe gallery
        st.markdown("##### 🎞️ Critical Keyframe Extraction & Target Tracking")
        kf_tabs = st.tabs([f"Frame {kf['frame_id']}" for kf in video_analysis["keyframes"]])
        for i, kf_tab in enumerate(kf_tabs):
            with kf_tab:
                kf = video_analysis["keyframes"][i]
                kf_threat_class = "badge-critical" if kf['threat'] == "CRITICAL" else "badge-high"
                st.image(kf["image"], caption=f"Keyframe {kf['frame_id']} @ {kf['timestamp']}", use_container_width=True)
                st.markdown(textwrap.dedent(f"""
                <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 8px; padding: 10px 14px; margin-top: 6px; box-shadow: 0 4px 14px rgba(0,0,0,0.3);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span class="forensic-badge {kf_threat_class}">THREAT: {kf['threat']}</span>
                        <span class="evid-tag">STATUTE: {kf['penal_code']}</span>
                    </div>
                    <div style="font-size: 0.9rem; color: #f8fafc;"><b>Observed Action:</b> {kf['event']}</div>
                </div>
                """), unsafe_allow_html=True)

        # Trajectory telemetry chart
        st.markdown("##### 📍 Suspect Spatial Trajectory & Velocity Vector")
        traj_df = pd.DataFrame(video_analysis["trajectories"])
        st.dataframe(traj_df, use_container_width=True, hide_index=True)

    with col_t3_right:
        st.markdown("#### ⚖️ Penal Code Crime Classification")
        for pc in video_analysis["summary_penal"]:
            st.markdown(textwrap.dedent(f"""
            <div class="forensic-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; color: #ff3366; font-size: 0.95rem;">{pc['code']}</span>
                    <span class="forensic-badge badge-critical">{pc['severity']}</span>
                </div>
                <h5 style="margin: 6px 0 0 0; color: #f8fafc;">{pc['title']}</h5>
            </div>
            """), unsafe_allow_html=True)

        st.markdown("#### ⏱️ Chronological CCTV Incident Log")
        for ev in video_analysis["event_log"]:
            badge_class = "threat-critical" if ev["threat"] == "CRITICAL" else "threat-high"
            st.markdown(textwrap.dedent(f"""
            <div class="timeline-event-card {badge_class}">
                <div style="display: flex; justify-content: space-between;">
                    <span class="mono-text" style="color: #00e5ff; font-weight: bold;">{ev['timestamp']} ({ev['frame_id']})</span>
                    <span class="evid-tag">{ev['penal_code']}</span>
                </div>
                <div style="margin-top: 4px; font-weight: 600; color: #f8fafc; font-size: 0.88rem;">{ev['event']}</div>
                <div style="color: #94a3b8; font-size: 0.8rem; margin-top: 2px;">Tracked: {ev['tracked_entity']}</div>
            </div>
            """), unsafe_allow_html=True)


# ---------------------------------------------------------------------------------
# TAB 4: MULTIMODAL FUSION & GROUNDED EVIDENCE CHAT (EPIC 5)
# ---------------------------------------------------------------------------------
with tabs[3]:
    st.markdown("### 🧠 Multimodal Fusion & Grounded Evidence Chat (Epic 5)")
    st.markdown("Unified master event ledger combining image, audio, and video timestamps with zero-hallucination grounded RAG interrogation.")

    # 1. Master Ledger Timeline Visualization
    st.markdown("#### 🌐 Unified Chronological Forensic Master Ledger")
    timeline_fig = fusion_engine.generate_timeline_chart(master_timeline)
    st.plotly_chart(timeline_fig, use_container_width=True)

    # Master Table
    with st.expander("🔍 View Complete Synchronized Evidence Ledger Table", expanded=False):
        ledger_df = pd.DataFrame(master_timeline)
        st.dataframe(ledger_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # 2. Grounded RAG Chat Interface
    st.markdown("#### 💬 Grounded AI Evidence Interrogation (Zero Hallucination)")
    st.caption("Interrogate case evidence in natural language. Answers strictly cite Evidence IDs ([EVID-IMG-001], [EVID-AUD-002], [EVID-VID-003]).")

    # Suggested Prompts
    st.markdown("**Quick Investigative Inquiries:**")
    prompt_cols = st.columns(3)
    quick_query = None
    with prompt_cols[0]:
        if st.button("🔫 Was a weapon visible before suspect fled?"):
            quick_query = "Was a weapon visible before the suspect fled?"
    with prompt_cols[1]:
        if st.button("⏱️ Does the witness audio match CCTV entry?"):
            quick_query = "Does the witness audio timeline match the CCTV entry time?"
    with prompt_cols[2]:
        if st.button("🚗 What is the getaway vehicle & escape route?"):
            quick_query = "What is the primary escape route and vehicle seen?"

    # Chat history display with citation chip highlighting
    for msg in st.session_state.chat_history:
        role = msg["role"]
        if role == "user":
            st.markdown(textwrap.dedent(f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 12px;">
                <div style="background: rgba(2, 132, 199, 0.25); border: 1px solid rgba(56, 189, 248, 0.45); border-radius: 14px 14px 2px 14px; padding: 12px 18px; max-width: 80%; color: #f8fafc; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);">
                    <div style="font-size: 0.72rem; color: #38bdf8; font-weight: 700; margin-bottom: 4px; letter-spacing: 0.05em;">👤 LEAD INVESTIGATOR</div>
                    <div style="font-size: 0.92rem; line-height: 1.45;">{msg['content']}</div>
                </div>
            </div>
            """), unsafe_allow_html=True)
        else:
            styled_content = format_forensic_citations(msg['content'])
            st.markdown(textwrap.dedent(f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 14px;">
                <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(0, 229, 255, 0.35); border-radius: 14px 14px 14px 2px; padding: 16px 20px; max-width: 85%; color: #f8fafc; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);">
                    <div style="font-size: 0.75rem; color: #00e5ff; font-weight: 700; margin-bottom: 6px; letter-spacing: 0.06em; display: flex; align-items: center; gap: 6px;">
                        <span>⚖️</span> CRIMEVISION AI FORENSIC REASONER
                    </div>
                    <div style="font-size: 0.92rem; line-height: 1.55; color: #f1f5f9;">
                        {styled_content}
                    </div>
                </div>
            </div>
            """), unsafe_allow_html=True)

    # Input form
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Enter your forensic inquiry...", placeholder="e.g. Explain how the firearm detection connects with the 911 dispatch audio...", value=quick_query or "")
        submit_btn = st.form_submit_button("Interrogate Evidence 🔍")

    active_query = quick_query or (user_input if submit_btn else None)

    if active_query:
        # Add to history
        st.session_state.chat_history.append({"role": "user", "content": active_query})

        # Build comprehensive evidence context
        evidence_context = {
            "case_id": case_info["case_id"],
            "case_title": case_info["title"],
            "visual_evidence": {
                "evidence_id": "EVID-IMG-001",
                "threat_level": visual_analysis["threat_level"],
                "classification": visual_analysis["classification"],
                "detected_objects": visual_analysis["detected_objects"],
                "leads": visual_analysis["investigative_leads"]
            },
            "audio_evidence": {
                "evidence_id": "EVID-AUD-002",
                "urgency_level": audio_analysis["urgency_level"],
                "stress_index": audio_analysis["stress_index"],
                "key_events": audio_analysis["chronological_markers"],
                "entities": audio_analysis["extracted_entities"]
            },
            "video_evidence": {
                "evidence_id": "EVID-VID-003",
                "camera_id": video_analysis["camera_id"],
                "event_log": video_analysis["event_log"],
                "penal_codes": [p["code"] for p in video_analysis["summary_penal"]]
            },
            "unified_timeline": master_timeline
        }

        with st.spinner("Executing Grounded RAG Evidence Reasoning..."):
            ai_response = llm_engine.generate_chat_response(
                active_query,
                st.session_state.chat_history,
                evidence_context
            )
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response["answer"]})
            st.rerun()


# ---------------------------------------------------------------------------------
# TAB 5: AUTOMATED FORENSIC PDF EXPORT (EPIC 6)
# ---------------------------------------------------------------------------------
with tabs[4]:
    st.markdown("### 📄 Automated Court-Admissible Forensic PDF Export (Epic 6)")
    st.markdown("Generate 1-click official, court-admissible forensic summary PDF reports using **ReportLab** with cryptographic chain-of-custody hashes.")

    col_t5_left, col_t5_right = st.columns([1.0, 1.0])

    with col_t5_left:
        st.markdown("#### 📋 Report Configuration & Attestation")

        st.markdown(textwrap.dedent(f"""
        <div class="attestation-card">
            <h4 style="margin: 0 0 12px 0; color: #00e5ff; font-size: 1.1rem; display: flex; align-items: center; gap: 8px;">
                <span>📜</span> Official Forensic Attestation Seal
            </h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 12px; font-size: 0.86rem;">
                <div><span style="color: #94a3b8;">Case Number:</span><br/><b style="color: #f8fafc; font-family: 'JetBrains Mono';">{case_info['case_id']}</b></div>
                <div><span style="color: #94a3b8;">Incident Title:</span><br/><b style="color: #f8fafc;">{case_info['title']}</b></div>
                <div><span style="color: #94a3b8;">Lead Examiner:</span><br/><b style="color: #38bdf8;">{st.session_state.investigator_name}</b></div>
                <div><span style="color: #94a3b8;">Token / Badge:</span><br/><b style="color: #38bdf8; font-family: 'JetBrains Mono';">{st.session_state.badge_id}</b></div>
            </div>
            <div style="border-top: 1px solid rgba(56, 189, 248, 0.2); padding-top: 10px; font-size: 0.82rem; color: #94a3b8;">
                <p style="margin: 2px 0;"><b>Division:</b> {st.session_state.precinct}</p>
                <p style="margin: 2px 0;"><b>Evidentiary Standard:</b> Federal Rules of Evidence (FRE 901/1002)</p>
                <p style="margin: 2px 0;"><b>Cryptographic Integrity:</b> SHA-256 Tamper-Evident Ledger Verified</p>
            </div>
        </div>
        """), unsafe_allow_html=True)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # PDF Generation Button
        if st.button("🚀 Compile Court-Admissible Forensic PDF Report", type="primary", use_container_width=True):
            with st.spinner("Synthesizing ReportLab Forensic Document..."):
                pdf_bytes = pdf_generator.generate_report(
                    case_id=case_info["case_id"],
                    case_name=case_info["title"],
                    investigator=st.session_state.investigator_name,
                    badge_id=st.session_state.badge_id,
                    precinct=st.session_state.precinct,
                    custody_ledger=st.session_state.custody_mgr.evidence_ledger,
                    visual_data=visual_analysis,
                    audio_data=audio_analysis,
                    video_data=video_analysis,
                    master_timeline=master_timeline
                )

                st.session_state.last_pdf = pdf_bytes
                st.success("✅ Forensic PDF Compiled & Cryptographically Sealed!")

        if "last_pdf" in st.session_state:
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            st.download_button(
                label=f"⬇️ Download {case_info['case_id']}_Forensic_Report.pdf",
                data=st.session_state.last_pdf,
                file_name=f"CrimeVision_Forensic_Report_{case_info['case_id']}.pdf",
                mime="application/pdf",
                key="download_pdf_btn",
                use_container_width=True
            )

    with col_t5_right:
        st.markdown("#### 📑 Report Structure & Judicial Components")
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 8px; padding: 16px; font-size: 0.88rem; line-height: 1.6;">
            <p><b style="color: #00e5ff;">Header:</b> CrimeVision AI Digital Forensic Division Letterhead & Official Seals</p>
            <p><b style="color: #00e5ff;">Section 1:</b> Cryptographic Chain of Custody & SHA-256 Integrity Verification</p>
            <p><b style="color: #00e5ff;">Section 2:</b> RT-DETR Visual Object Detection Breakdown with Spatial Coordinates</p>
            <p><b style="color: #00e5ff;">Section 3:</b> Whisper AI Witness Statement Transcript & Acoustic Biometrics</p>
            <p><b style="color: #00e5ff;">Section 4:</b> CCTV Surveillance Progression & Penal Code Classification Log</p>
            <p><b style="color: #00e5ff;">Section 5:</b> Unified Multimodal Chronological Master Timeline Table</p>
            <p><b style="color: #00e5ff;">Section 6:</b> Investigator Legal Attestation, Digital Signature Hash & Seal</p>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #64748b; font-size: 0.8rem; padding: 12px 0;">
    <b>{APP_CONFIG['APP_NAME']}</b> v{APP_CONFIG['VERSION']} • {APP_CONFIG['CATEGORY']} • Platform ID: <code>{APP_CONFIG['PLATFORM_ID']}</code><br/>
    Built for Skill Wallet Capstone Project 2 • Zero Database Dependencies • Streamlit Community Cloud Ready
</div>
""", unsafe_allow_html=True)
