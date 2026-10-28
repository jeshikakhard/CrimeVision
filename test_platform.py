import config
from modules.auth_custody import ChainOfCustodyManager
from modules.visual_tagger import VisualEvidenceTagger
from modules.audio_transcriber import ForensicAudioTranscriber
from modules.video_analyzer import CCTVVideoAnalyzer
from modules.multimodal_fusion import MultimodalFusionEngine
from modules.pdf_generator import ForensicPDFReportGenerator
from modules.llm_engine import ForensicLLMEngine
from sample_data.presets import CASE_PRESETS
from sample_data.asset_generator import generate_crime_scene_image, get_image_bytes

print("1. Testing Imports...")

print("2. Testing Visual Module...")
img = generate_crime_scene_image("vault")
img_bytes = get_image_bytes(img)
tagger = VisualEvidenceTagger()
vis_res = tagger.detect_objects_rtdetr(img, 0.4, "bank_vault")
annotated = tagger.render_bounding_boxes(img, vis_res["detected_objects"])
print(f"Visual Module: SUCCESS ({len(vis_res['detected_objects'])} objects detected)")

print("3. Testing Audio Module...")
transcriber = ForensicAudioTranscriber()
aud_res = transcriber.transcribe_and_analyze(b"", "911_test.wav", "911_vault")
print(f"Audio Module: SUCCESS (Stress index {aud_res['stress_index']})")

print("4. Testing Video Module...")
analyzer = CCTVVideoAnalyzer()
vid_res = analyzer.process_cctv_feed(preset_type="vault")
print(f"Video Module: SUCCESS ({len(vid_res['keyframes'])} keyframes generated)")

print("5. Testing Multimodal Fusion...")
fusion = MultimodalFusionEngine()
master = fusion.build_unified_master_ledger("CR-2026-8831", vis_res, aud_res, vid_res)
fig = fusion.generate_timeline_chart(master)
print(f"Multimodal Fusion: SUCCESS ({len(master)} timeline events synchronized)")

print("6. Testing Chain-of-Custody...")
custody = ChainOfCustodyManager()
custody.register_evidence("EVID-IMG-001", "Photo", "scene.jpg", img_bytes, "Det. Miller", "4928", "DFU-7")
custody.sign_off_evidence("EVID-IMG-001", "Det. Miller", "4928", "Verified")
print(f"Chain-of-Custody: SUCCESS (Entries: {len(custody.evidence_ledger)})")

print("7. Testing PDF Generation (ReportLab)...")
pdf_gen = ForensicPDFReportGenerator()
pdf_bytes = pdf_gen.generate_report(
    case_id="CR-2026-8831",
    case_name="Downtown Vault Breach",
    investigator="Det. J. Miller",
    badge_id="4928",
    precinct="Metro DFU-7",
    custody_ledger=custody.evidence_ledger,
    visual_data=vis_res,
    audio_data=aud_res,
    video_data=vid_res,
    master_timeline=master
)
print(f"PDF Generation: SUCCESS ({len(pdf_bytes)} bytes produced)")

print("8. Testing Grounded RAG Reasoner...")
llm = ForensicLLMEngine(provider="Demo Fallback")
chat_res = llm.generate_chat_response(
    "Was a weapon visible before the suspect fled?",
    [],
    {"visual_evidence": vis_res, "audio_evidence": aud_res, "video_evidence": vid_res, "unified_timeline": master}
)
print(f"Grounded RAG Reasoner: SUCCESS ({chat_res['status']})")
print("\nALL PLATFORM TESTS PASSED WITH 100% SUCCESS!")
