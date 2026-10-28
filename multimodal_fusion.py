"""
Tab 4: Multimodal Fusion & Grounded Evidence Chat (Epic 5)
Fuses Image, Audio, and Video evidence into a Master Event Ledger and powers Grounded RAG Chat.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any


class MultimodalFusionEngine:
    """Synchronizes multimodal forensic streams and enforces grounded evidence interrogation."""

    def build_unified_master_ledger(
        self,
        case_id: str,
        visual_data: Dict[str, Any],
        audio_data: Dict[str, Any],
        video_data: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Fuses timestamps across visual, audio, and surveillance video into an ordered master ledger."""
        timeline_events = []

        # 1. Video events
        for v_ev in video_data.get("event_log", []):
            timeline_events.append({
                "timestamp": v_ev.get("timestamp", "23:41:52"),
                "evidence_id": "EVID-VID-003",
                "source_modality": "CCTV SURVEILLANCE",
                "event_type": "Visual Movement / Telemetry",
                "description": v_ev.get("event", ""),
                "tracked_entity": v_ev.get("tracked_entity", "Subject"),
                "threat_level": v_ev.get("threat", "MEDIUM"),
                "legal_statute": v_ev.get("penal_code", "N/A"),
            })

        # 2. Audio events
        for a_ev in audio_data.get("chronological_markers", []):
            timeline_events.append({
                "timestamp": a_ev.get("timestamp", "23:42:08"),
                "evidence_id": "EVID-AUD-002",
                "source_modality": "WITNESS / 911 AUDIO",
                "event_type": a_ev.get("significance", "Acoustic Marker"),
                "description": a_ev.get("event", ""),
                "tracked_entity": "Acoustic Signal / Vocal Witness",
                "threat_level": "CRITICAL" if any(k in a_ev.get("event", "").lower() for k in ["gunshot", "weapon", "shot"]) else "HIGH",
                "legal_statute": "Corroborating Testimony",
            })

        # 3. Visual Still Photography events (Physical Scene Artifacts)
        for obj in visual_data.get("detected_objects", []):
            timeline_events.append({
                "timestamp": "23:42:20 (Scene Frozen)",
                "evidence_id": "EVID-IMG-001",
                "source_modality": "FORENSIC STILL PHOTO",
                "event_type": f"Object Tagger: {obj.get('category', 'Physical')}",
                "description": f"Identified {obj.get('label', '')} with {obj.get('confidence', 0)*100:.1f}% confidence at spatial coordinates {obj.get('box_coords', [])}.",
                "tracked_entity": obj.get("label", ""),
                "threat_level": obj.get("threat_weight", "MEDIUM"),
                "legal_statute": "Physical Demonstrative Evidence",
            })

        # Sort timeline chronologically (extracting time string)
        def sort_key(e):
            t = e["timestamp"].split(" ")[0].replace(":", "")
            try:
                return int(t)
            except ValueError:
                return 999999

        timeline_events.sort(key=sort_key)
        return timeline_events

    def generate_timeline_chart(self, master_ledger: List[Dict[str, Any]]) -> go.Figure:
        """Generates an interactive Plotly timeline progression chart."""
        data_rows = []
        for i, ev in enumerate(master_ledger):
            data_rows.append({
                "Index": i,
                "Time": ev["timestamp"],
                "Evidence": ev["evidence_id"],
                "Modality": ev["source_modality"],
                "Event": ev["description"][:50] + "...",
                "Threat": ev["threat_level"],
                "Level": 3 if ev["threat_level"] == "CRITICAL" else (2 if ev["threat_level"] == "HIGH" else 1)
            })

        df = pd.DataFrame(data_rows)
        if df.empty:
            fig = go.Figure()
            fig.update_layout(title="No Timeline Data Available")
            return fig

        color_map = {
            "CRITICAL": "#ff3366",
            "HIGH": "#f59e0b",
            "MEDIUM": "#00e5ff",
            "LOW": "#10b981"
        }

        fig = px.scatter(
            df,
            x="Time",
            y="Modality",
            color="Threat",
            size="Level",
            hover_data=["Evidence", "Event"],
            color_discrete_map=color_map,
            title="Chronological Forensic Event Synchronization Across Modalities"
        )

        fig.update_layout(
            paper_bgcolor="rgba(10, 14, 23, 0.9)",
            plot_bgcolor="rgba(15, 23, 42, 0.8)",
            font=dict(color="#f8fafc", family="Inter, sans-serif"),
            xaxis=dict(gridcolor="rgba(56, 189, 248, 0.15)", title="Chronological Timestamp"),
            yaxis=dict(gridcolor="rgba(56, 189, 248, 0.15)", title="Evidence Modality"),
            height=320,
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=True
        )

        return fig
