"""
Tab 1: Crime Scene Visual Evidence Tagger (Epic 2)
Multimodal Object Detection simulating RT-DETR / YOLOv8 for forensic scene intelligence.
"""

import io
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List, Tuple, Any


class VisualEvidenceTagger:
    """RT-DETR & Computer Vision Powered Forensic Visual Tagger."""

    CATEGORY_COLORS = {
        "Firearm": "#ff3366",          # Critical Red
        "Edged Weapon": "#f43f5e",     # Neon Rose
        "Person / Suspect": "#00e5ff", # Forensic Cyan
        "Blood Spatter": "#ef4444",    # Crimson
        "Forced Entry": "#f59e0b",     # Warning Amber
        "Evidence Marker": "#8b5cf6",  # Purple
    }

    @staticmethod
    def calculate_image_metrics(image: Image.Image) -> Dict[str, Any]:
        """Calculates image forensic characteristics (entropy, sharpness, lighting)."""
        np_img = np.array(image.convert("RGB"))
        gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
        sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
        brightness = float(np.mean(gray))
        contrast = float(np.std(gray))

        return {
            "resolution": f"{image.width} x {image.height}",
            "sharpness_score": round(sharpness, 2),
            "lighting_eval": "Low Light / Night Surveillance" if brightness < 80 else ("Optimal Daylight" if brightness < 180 else "Overexposed"),
            "contrast_score": round(contrast, 2),
            "megapixels": round((image.width * image.height) / 1_000_000, 2)
        }

    def detect_objects_rtdetr(
        self,
        image: Image.Image,
        confidence_thresh: float = 0.40,
        preset_type: str = "custom"
    ) -> Dict[str, Any]:
        """
        Simulates state-of-the-art RT-DETR (Real-Time DEtection TRansformer) forensic inference
        detecting persons, firearms, edged weapons, blood patterns, and forced entry points.
        """
        w, h = image.width, image.height

        # Dynamic simulation presets or intelligent contextual mapping
        if preset_type == "bank_vault" or "vault" in preset_type.lower():
            raw_detections = [
                {"label": "Firearm (Semi-Auto 9mm)", "category": "Firearm", "conf": 0.962, "box": [int(h*0.48), int(w*0.52), int(h*0.62), int(w*0.68)], "threat": "CRITICAL"},
                {"label": "Person (Suspect 1 - Masked)", "category": "Person / Suspect", "conf": 0.941, "box": [int(h*0.18), int(w*0.35), int(h*0.88), int(w*0.65)], "threat": "HIGH"},
                {"label": "Forced Entry (Pried Lock Mechanism)", "category": "Forced Entry", "conf": 0.918, "box": [int(h*0.32), int(w*0.08), int(h*0.55), int(w*0.28)], "threat": "HIGH"},
                {"label": "Blood Spatter (Impact Droplets)", "category": "Blood Spatter", "conf": 0.884, "box": [int(h*0.72), int(w*0.42), int(h*0.84), int(w*0.56)], "threat": "HIGH"},
                {"label": "Pry Bar / Burglar Tool", "category": "Evidence Marker", "conf": 0.875, "box": [int(h*0.65), int(w*0.12), int(h*0.78), int(w*0.25)], "threat": "MEDIUM"},
            ]
            classification = "Commercial Burglary & Armed Robbery (Penal Code § 459 / § 211)"
            threat_level = "CRITICAL"
            leads = [
                "Extract ballistic profile and shell casing proximity to 9mm semi-auto at [ymin:0.48, xmin:0.52].",
                "Swab pry mark friction striations on deadbolt casing for metallurgical comparison toolmark matching.",
                "Collect biological contact DNA from blood spatter pool at floor quadrant [ymin:0.72, xmin:0.42].",
                "Cross-reference suspect silhouette and tactical vest geometry against regional heist suspect databases."
            ]
        elif preset_type == "alley_assault" or "assault" in preset_type.lower():
            raw_detections = [
                {"label": "Edged Weapon (Tactical Bowie Knife)", "category": "Edged Weapon", "conf": 0.948, "box": [int(h*0.58), int(w*0.45), int(h*0.72), int(w*0.59)], "threat": "CRITICAL"},
                {"label": "Person (Suspect - Fleeing)", "category": "Person / Suspect", "conf": 0.923, "box": [int(h*0.20), int(w*0.32), int(h*0.82), int(w*0.55)], "threat": "HIGH"},
                {"label": "Blood Spatter (Cast-Off Trajectory)", "category": "Blood Spatter", "conf": 0.935, "box": [int(h*0.40), int(w*0.62), int(h*0.68), int(w*0.85)], "threat": "CRITICAL"},
                {"label": "Discarded Phone / Evidence Item", "category": "Evidence Marker", "conf": 0.842, "box": [int(h*0.75), int(w*0.22), int(h*0.85), int(w*0.34)], "threat": "MEDIUM"},
            ]
            classification = "Aggravated Assault with Deadly Weapon (Penal Code § 245(a)(1))"
            threat_level = "CRITICAL"
            leads = [
                "Recover discarded tactical blade; submit for latent fingerprint lifting and DNA analysis.",
                "Cast-off blood pattern analysis on brick masonry indicates minimum 3 violent downward stroke vectors.",
                "Extract flash memory and IMEI from victim's dropped mobile handset for emergency telemetry.",
            ]
        elif preset_type == "store_holdup" or "holdup" in preset_type.lower():
            raw_detections = [
                {"label": "Firearm (Compact Pistol)", "category": "Firearm", "conf": 0.955, "box": [int(h*0.38), int(w*0.48), int(h*0.52), int(w*0.60)], "threat": "CRITICAL"},
                {"label": "Person (Armed Suspect)", "category": "Person / Suspect", "conf": 0.932, "box": [int(h*0.15), int(w*0.38), int(h*0.85), int(w*0.68)], "threat": "HIGH"},
                {"label": "Person (Store Clerk - Hands Raised)", "category": "Person / Suspect", "conf": 0.910, "box": [int(h*0.25), int(w*0.10), int(h*0.80), int(w*0.32)], "threat": "MEDIUM"},
                {"label": "Breached Cash Register Drawer", "category": "Forced Entry", "conf": 0.865, "box": [int(h*0.55), int(w*0.18), int(h*0.70), int(w*0.35)], "threat": "HIGH"},
            ]
            classification = "Armed Robbery in Progress (Penal Code § 211)"
            threat_level = "CRITICAL"
            leads = [
                "Flag firearm serial database matching compact polymer-frame pistol.",
                "Recover suspect fingerprint residue from cash register handle latch.",
                "Synchronize store security camera feed with dispatch 911 caller tape."
            ]
        else:
            # Default / Custom user image detection (intelligent spatial mapping)
            raw_detections = [
                {"label": "Person (Subject of Interest)", "category": "Person / Suspect", "conf": 0.915, "box": [int(h*0.20), int(w*0.30), int(h*0.85), int(w*0.62)], "threat": "HIGH"},
                {"label": "Potential Concealed Firearm", "category": "Firearm", "conf": 0.824, "box": [int(h*0.48), int(w*0.45), int(h*0.60), int(w*0.58)], "threat": "HIGH"},
                {"label": "Forced Ingress Point (Door Joint)", "category": "Forced Entry", "conf": 0.795, "box": [int(h*0.30), int(w*0.05), int(h*0.65), int(w*0.25)], "threat": "MEDIUM"},
                {"label": "Trace Fluid Staining", "category": "Blood Spatter", "conf": 0.742, "box": [int(h*0.75), int(w*0.60), int(h*0.88), int(w*0.80)], "threat": "MEDIUM"},
            ]
            classification = "Suspicious Intrusion & Potential Weapons Violation"
            threat_level = "HIGH"
            leads = [
                "Execute facial feature analysis against regional booking database.",
                "Conduct presumptive Kastle-Meyer test on detected trace fluid staining.",
                "Review perimeter access logs during estimated intrusion window."
            ]

        # Filter by confidence threshold
        filtered_detections = [d for d in raw_detections if d["conf"] >= confidence_thresh]

        # Calculate final threat level
        if any(d["category"] in ["Firearm", "Edged Weapon"] for d in filtered_detections):
            threat_level = "CRITICAL"
        elif any(d["category"] in ["Forced Entry", "Blood Spatter"] for d in filtered_detections):
            threat_level = "HIGH"
        elif any(d["category"] == "Person / Suspect" for d in filtered_detections):
            threat_level = "MEDIUM"
        else:
            threat_level = "LOW"

        return {
            "threat_level": threat_level,
            "classification": classification,
            "detected_objects": [
                {
                    "id": f"OBJ-{i+1:03d}",
                    "label": d["label"],
                    "category": d["category"],
                    "confidence": d["conf"],
                    "box_coords": d["box"],
                    "threat_weight": d["threat"]
                }
                for i, d in enumerate(filtered_detections)
            ],
            "investigative_leads": leads,
            "image_metrics": self.calculate_image_metrics(image)
        }

    def render_bounding_boxes(
        self,
        image: Image.Image,
        detections: List[Dict[str, Any]],
        selected_categories: Optional[List[str]] = None
    ) -> Image.Image:
        """Renders tactical forensic bounding boxes, glowing badges, and coordinates."""
        annotated = image.copy().convert("RGBA")
        overlay = Image.new("RGBA", annotated.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        for det in detections:
            cat = det.get("category", "Evidence Marker")
            if selected_categories and cat not in selected_categories:
                continue

            ymin, xmin, ymax, xmax = det["box_coords"]
            color_hex = self.CATEGORY_COLORS.get(cat, "#00e5ff")
            r = int(color_hex[1:3], 16)
            g = int(color_hex[3:5], 16)
            b = int(color_hex[5:7], 16)

            # Draw semi-transparent fill
            draw.rectangle([xmin, ymin, xmax, ymax], outline=(r, g, b, 240), width=3, fill=(r, g, b, 35))

            # Corner brackets for tactical look
            corner_len = min(20, (xmax - xmin) // 4, (ymax - ymin) // 4)
            # Top-left
            draw.line([(xmin, ymin), (xmin + corner_len, ymin)], fill=(r, g, b, 255), width=5)
            draw.line([(xmin, ymin), (xmin, ymin + corner_len)], fill=(r, g, b, 255), width=5)
            # Bottom-right
            draw.line([(xmax, ymax), (xmax - corner_len, ymax)], fill=(r, g, b, 255), width=5)
            draw.line([(xmax, ymax), (xmax, ymax - corner_len)], fill=(r, g, b, 255), width=5)

            # Label banner
            conf_str = f"{det['confidence'] * 100:.1f}%"
            label_text = f"[{det['id']}] {det['label']} | {conf_str}"
            banner_h = 24
            banner_w = len(label_text) * 8 + 14
            label_y = max(0, ymin - banner_h - 2)

            draw.rectangle([xmin, label_y, xmin + banner_w, label_y + banner_h], fill=(10, 14, 23, 230), outline=(r, g, b, 200), width=1)
            draw.text((xmin + 6, label_y + 4), label_text, fill=(255, 255, 255, 255))

        annotated = Image.alpha_composite(annotated, overlay)
        return annotated.convert("RGB")
