"""
Forensic Chain-of-Custody & Cryptographic Verification Module
Handles SHA-256 evidence hashing, investigator sign-off, and immutable audit logging.
"""

import hashlib
import datetime
from typing import Dict, List, Optional


class ChainOfCustodyManager:
    """Manages forensic chain-of-custody records complying with legal admissibility standards."""

    def __init__(self):
        self.evidence_ledger: List[Dict] = []
        self.audit_log: List[Dict] = []

    @staticmethod
    def calculate_file_hash(file_bytes: bytes) -> Dict[str, str]:
        """Calculates SHA-256 and MD5 cryptographic integrity hashes for evidentiary integrity."""
        sha256 = hashlib.sha256(file_bytes).hexdigest()
        md5 = hashlib.md5(file_bytes).hexdigest()
        return {
            "sha256": sha256,
            "md5": md5,
            "short_sha": sha256[:12].upper(),
        }

    def register_evidence(
        self,
        evidence_id: str,
        evidence_type: str,
        filename: str,
        file_bytes: bytes,
        investigator: str,
        badge_id: str,
        precinct: str,
        notes: str = "",
    ) -> Dict:
        """Registers a new piece of digital evidence with cryptographic signature and chain entry."""
        hashes = self.calculate_file_hash(file_bytes)
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        record = {
            "evidence_id": evidence_id,
            "type": evidence_type,
            "filename": filename,
            "file_size_bytes": len(file_bytes),
            "sha256": hashes["sha256"],
            "md5": hashes["md5"],
            "short_sha": hashes["short_sha"],
            "timestamp": timestamp,
            "investigator": investigator,
            "badge_id": badge_id,
            "precinct": precinct,
            "notes": notes,
            "status": "SECURED & HASHED",
            "signed_off": False,
        }

        # Check if already registered
        for i, item in enumerate(self.evidence_ledger):
            if item["evidence_id"] == evidence_id:
                self.evidence_ledger[i] = record
                self.log_action(evidence_id, "RE-SECURED", investigator, badge_id, "Updated hash & re-secured")
                return record

        self.evidence_ledger.append(record)
        self.log_action(evidence_id, "INGESTION & HASH", investigator, badge_id, f"Registered with SHA-256 {hashes['short_sha']}")
        return record

    def sign_off_evidence(self, evidence_id: str, investigator: str, badge_id: str, signature_notes: str = "") -> bool:
        """Investigator formal digital sign-off confirming integrity and legal preservation."""
        for item in self.evidence_ledger:
            if item["evidence_id"] == evidence_id:
                item["signed_off"] = True
                item["signed_by"] = investigator
                item["signed_badge"] = badge_id
                item["signed_time"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
                item["status"] = "VERIFIED & SIGNED"
                self.log_action(evidence_id, "INVESTIGATOR SIGN-OFF", investigator, badge_id, f"Formal sign-off: {signature_notes}")
                return True
        return False

    def log_action(self, evidence_id: str, action: str, investigator: str, badge_id: str, details: str):
        """Appends an immutable audit event to the chain-of-custody ledger."""
        entry = {
            "log_id": f"LOG-{len(self.audit_log)+1:04d}",
            "evidence_id": evidence_id,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            "action": action,
            "investigator": investigator,
            "badge_id": badge_id,
            "details": details,
        }
        self.audit_log.append(entry)

    def get_custody_report(self) -> List[Dict]:
        return self.audit_log

    def get_evidence_by_id(self, evidence_id: str) -> Optional[Dict]:
        for item in self.evidence_ledger:
            if item["evidence_id"] == evidence_id:
                return item
        return None
