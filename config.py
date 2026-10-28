"""
CrimeVision AI - Intelligent Multimodal Forensic Analysis Platform
Platform ID: 6ac4c9851dcde6d7857c163b
Configuration & UI Theme
"""

APP_CONFIG = {
    "APP_NAME": "CrimeVision AI",
    "SUBTITLE": "Intelligent Multimodal Forensic Analysis Platform",
    "PLATFORM_ID": "6ac4c9851dcde6d7857c163b",
    "CATEGORY": "Generative AI | Criminal Justice & Public Safety",
    "CAPSTONE_PROJECT": "Skill Wallet Capstone Project 2",
    "VERSION": "2.4.0-PROD",
    "DEFAULT_INVESTIGATOR": "Det. J. Miller (Badge #4928)",
    "DEFAULT_PRECINCT": "Metro Digital Forensics Unit (DFU-7)",
    "DEFAULT_CASE_ID": "CR-2026-8831",
    "DEFAULT_CASE_NAME": "Downtown Vault Breach & Armed Intrusion",
}

# Modern Forensic Dark UI Theme CSS
FORENSIC_THEME_CSS = """
<style>
/* Main Background & Typography */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg-primary: #0a0e17;
    --bg-surface: #0f172a;
    --bg-card: rgba(16, 24, 39, 0.85);
    --bg-card-hover: rgba(22, 33, 54, 0.95);
    --border-color: rgba(56, 189, 248, 0.2);
    --border-glow: rgba(0, 229, 255, 0.45);
    --accent-cyan: #00e5ff;
    --accent-blue: #38bdf8;
    --accent-red: #ff3366;
    --accent-amber: #f59e0b;
    --accent-green: #10b981;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-primary);
}

.stApp {
    background-color: #0a0e17 !important;
    color: #f8fafc !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #0a0e17 !important;
    color: #f8fafc !important;
}

[data-testid="stHeader"] {
    background-color: rgba(10, 14, 23, 0.85) !important;
}

code, pre, .mono-text {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Streamlit main container adjustments */
.main .block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    max-width: 100% !important;
}

/* App Header styling */
.forensic-header {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(10, 14, 23, 0.98) 100%);
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 22px 28px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    position: relative;
    overflow: hidden;
}

.forensic-header::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 6px;
    height: 100%;
    background: linear-gradient(180deg, #00e5ff 0%, #3b82f6 50%, #ff3366 100%);
}

.forensic-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
}

.badge-live {
    background: rgba(16, 185, 129, 0.15);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.35);
}

.badge-critical {
    background: rgba(255, 51, 102, 0.18);
    color: #ff3366;
    border: 1px solid rgba(255, 51, 102, 0.45);
    animation: pulseGlow 2s infinite ease-in-out;
}

.badge-high {
    background: rgba(245, 158, 11, 0.18);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.45);
}

.badge-custody {
    background: rgba(0, 229, 255, 0.12);
    color: #00e5ff;
    border: 1px solid rgba(0, 229, 255, 0.35);
}

@keyframes pulseGlow {
    0% { box-shadow: 0 0 4px rgba(255, 51, 102, 0.3); }
    50% { box-shadow: 0 0 16px rgba(255, 51, 102, 0.75); }
    100% { box-shadow: 0 0 4px rgba(255, 51, 102, 0.3); }
}

/* Responsive KPI Metric Grid (Replaces truncated native st.metric) */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin-bottom: 24px;
}

@media (max-width: 1200px) {
    .kpi-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

@media (max-width: 768px) {
    .kpi-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 480px) {
    .kpi-grid {
        grid-template-columns: 1fr;
    }
}

.kpi-card {
    background: linear-gradient(135deg, rgba(16, 24, 39, 0.95) 0%, rgba(15, 23, 42, 0.8) 100%);
    border: 1px solid rgba(56, 189, 248, 0.22);
    border-radius: 12px;
    padding: 14px 18px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}

.kpi-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 3px;
    height: 100%;
    background: #00e5ff;
}

.kpi-card:hover {
    transform: translateY(-2px);
    border-color: rgba(0, 229, 255, 0.55);
    box-shadow: 0 6px 24px rgba(0, 229, 255, 0.18);
}

.kpi-card .kpi-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.kpi-card .kpi-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.15rem;
    font-weight: 700;
    color: #00e5ff;
    line-height: 1.25;
    word-break: break-word;
    overflow-wrap: break-word;
    white-space: normal;
}

.kpi-card .kpi-delta {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.76rem;
    font-weight: 600;
    color: #10b981;
    margin-top: 6px;
}

.kpi-card.kpi-critical::before { background: #ff3366; }
.kpi-card.kpi-critical .kpi-value { color: #ff3366; }
.kpi-card.kpi-critical .kpi-delta { color: #ff3366; }

.kpi-card.kpi-amber::before { background: #f59e0b; }
.kpi-card.kpi-amber .kpi-value { color: #f59e0b; }
.kpi-card.kpi-amber .kpi-delta { color: #f59e0b; }

.kpi-card.kpi-emerald::before { background: #10b981; }
.kpi-card.kpi-emerald .kpi-value { color: #10b981; }

/* Forensic Glass Card */
.forensic-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 16px;
    backdrop-filter: blur(10px);
    transition: all 0.25s ease;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.forensic-card:hover {
    border-color: var(--border-glow);
    background: var(--bg-card-hover);
    box-shadow: 0 6px 24px rgba(0, 229, 255, 0.12);
}

/* Evidence Tag Label */
.evid-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    padding: 3px 8px;
    border-radius: 5px;
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid #334155;
    color: #38bdf8;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

/* Citation Chip for RAG chat responses */
.citation-chip {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.76rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    background: rgba(0, 229, 255, 0.14);
    color: #00e5ff;
    border: 1px solid rgba(0, 229, 255, 0.45);
    box-shadow: 0 0 10px rgba(0, 229, 255, 0.2);
    margin: 0 2px;
    cursor: default;
}

/* Streamlit Tabs Navigation - Flex-wrap to prevent horizontal overflow */
.stTabs [data-baseweb="tab-list"] {
    display: flex !important;
    flex-wrap: nowrap !important;
    gap: 8px !important;
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.85) 0%, rgba(10, 14, 23, 0.95) 100%) !important;
    padding: 6px !important;
    border-radius: 12px !important;
    border: 1px solid rgba(56, 189, 248, 0.25) !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
    width: 100% !important;
    overflow: visible !important;
}

[data-baseweb="tab-scroll-button"] {
    display: none !important;
}

[data-baseweb="tab-border"] {
    display: none !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}

.stTabs [data-baseweb="tab"] {
    height: auto !important;
    min-height: 40px !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    padding: 8px 12px !important;
    background: rgba(30, 41, 59, 0.45) !important;
    border: 1px solid rgba(51, 65, 85, 0.5) !important;
    transition: all 0.2s ease !important;
    white-space: nowrap !important;
    flex: 1 1 0px !important;
    text-align: center !important;
    justify-content: center !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #f8fafc !important;
    background: rgba(0, 229, 255, 0.12) !important;
    border-color: rgba(0, 229, 255, 0.45) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0, 229, 255, 0.22) 0%, rgba(2, 132, 199, 0.35) 100%) !important;
    color: #00e5ff !important;
    border: 1px solid #00e5ff !important;
    box-shadow: 0 0 16px rgba(0, 229, 255, 0.35) !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #0c121e !important;
    border-right: 1px solid rgba(51, 65, 85, 0.45);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
    color: #ffffff;
    font-weight: 600;
    border: 1px solid rgba(56, 189, 248, 0.45);
    border-radius: 8px;
    padding: 8px 18px;
    transition: all 0.2s ease;
    box-shadow: 0 2px 10px rgba(2, 132, 199, 0.25);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #0369a1 0%, #0284c7 100%);
    box-shadow: 0 0 18px rgba(56, 189, 248, 0.6);
    border-color: #00e5ff;
}

/* Acoustic Stress Meter Bar */
.stress-meter-box {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 14px;
}

.stress-track {
    width: 100%;
    height: 12px;
    background: rgba(30, 41, 59, 0.85);
    border-radius: 6px;
    border: 1px solid rgba(51, 65, 85, 0.6);
    overflow: hidden;
    margin-top: 8px;
    position: relative;
}

.stress-fill {
    height: 100%;
    border-radius: 6px;
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Photometric mini-cards */
.photometric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 16px;
}

.photometric-card {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 8px;
    padding: 12px 14px;
    text-align: center;
}

.photometric-card .pm-label {
    font-size: 0.7rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
}

.photometric-card .pm-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.05rem;
    font-weight: 700;
    color: #00e5ff;
    margin-top: 4px;
}

/* Diarized Chat Bubbles */
.diarized-bubble {
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 10px;
    transition: all 0.2s ease;
}

.diarized-dispatcher {
    background: rgba(2, 132, 199, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.35);
}

.diarized-witness {
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.35);
}

.diarized-suspect {
    background: rgba(255, 51, 102, 0.12);
    border: 1px solid rgba(255, 51, 102, 0.35);
}

/* Timeline pill */
.timeline-event-card {
    padding: 12px 16px;
    border-left: 3px solid #00e5ff;
    background: rgba(15, 23, 42, 0.75);
    margin-bottom: 10px;
    border-radius: 0 8px 8px 0;
    border-top: 1px solid rgba(51, 65, 85, 0.3);
    border-right: 1px solid rgba(51, 65, 85, 0.3);
    border-bottom: 1px solid rgba(51, 65, 85, 0.3);
}

.timeline-event-card.threat-critical {
    border-left-color: #ff3366;
    background: rgba(255, 51, 102, 0.09);
}

.timeline-event-card.threat-high {
    border-left-color: #f59e0b;
    background: rgba(245, 158, 11, 0.09);
}

/* Entity chips */
.entity-chip-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 6px;
}

.entity-chip {
    font-size: 0.78rem;
    padding: 4px 10px;
    border-radius: 6px;
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(56, 189, 248, 0.25);
    color: #e2e8f0;
}

/* Legal Attestation Seal Card */
.attestation-card {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(10, 14, 23, 0.9) 100%);
    border: 1px solid rgba(245, 158, 11, 0.35);
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.45);
    position: relative;
}

.attestation-card::before {
    content: "⚖️ FRE 901 CERTIFIED";
    position: absolute;
    top: 14px;
    right: 18px;
    font-size: 0.7rem;
    font-weight: 700;
    color: #f59e0b;
    letter-spacing: 0.08em;
    background: rgba(245, 158, 11, 0.15);
    padding: 3px 8px;
    border-radius: 4px;
    border: 1px solid rgba(245, 158, 11, 0.4);
}
</style>
"""
