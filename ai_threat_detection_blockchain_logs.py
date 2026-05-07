"""
Assignment 12: AI-Powered Threat Detection using Blockchain Logs
----------------------------------------------------------------
What this program demonstrates:
1. Generate sample security logs (login, transfer, config changes, etc.)
2. Use a simple AI-like scoring model to detect suspicious logs
3. Store each log as a hashed, linked block (tamper-evident chain)
4. Verify chain integrity

This is a beginner-friendly educational implementation.
"""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import List


@dataclass
class SecurityLog:
    """Simple event log structure for threat detection."""

    event_id: int
    user: str
    action: str
    amount: float
    ip: str
    status: str
    timestamp: str


@dataclass
class LogBlock:
    """A blockchain block containing one security log."""

    index: int
    log_data: dict
    log_hash: str
    previous_hash: str
    block_hash: str


class ThreatDetectionBlockchain:
    def __init__(self) -> None:
        self.chain: List[LogBlock] = []

    @staticmethod
    def sha256_hex(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def hash_log(self, log: SecurityLog) -> str:
        # Stable serialization ensures same log gives same hash.
        log_json = json.dumps(asdict(log), sort_keys=True)
        return self.sha256_hex(log_json)

    def mine_block_hash(self, index: int, log_hash: str, previous_hash: str) -> str:
        # Block hash links this block with previous block.
        payload = f"{index}|{log_hash}|{previous_hash}"
        return self.sha256_hex(payload)

    def add_log_as_block(self, log: SecurityLog) -> LogBlock:
        index = len(self.chain)
        previous_hash = self.chain[-1].block_hash if self.chain else "0" * 64
        log_hash = self.hash_log(log)
        block_hash = self.mine_block_hash(index, log_hash, previous_hash)

        block = LogBlock(
            index=index,
            log_data=asdict(log),
            log_hash=log_hash,
            previous_hash=previous_hash,
            block_hash=block_hash,
        )
        self.chain.append(block)
        return block

    def verify_chain_integrity(self) -> bool:
        # Recompute each block and compare with stored values.
        for i, block in enumerate(self.chain):
            expected_log_json = json.dumps(block.log_data, sort_keys=True)
            expected_log_hash = self.sha256_hex(expected_log_json)
            if expected_log_hash != block.log_hash:
                print(f"[ALERT] Log hash mismatch at block {i}")
                return False

            expected_prev_hash = "0" * 64 if i == 0 else self.chain[i - 1].block_hash
            if block.previous_hash != expected_prev_hash:
                print(f"[ALERT] Previous hash mismatch at block {i}")
                return False

            expected_block_hash = self.mine_block_hash(i, block.log_hash, block.previous_hash)
            if expected_block_hash != block.block_hash:
                print(f"[ALERT] Block hash mismatch at block {i}")
                return False

        return True


def generate_sample_logs(total: int = 12) -> List[SecurityLog]:
    """Generate mixed normal and suspicious logs."""

    random.seed(42)

    users = ["alice", "bob", "carol", "dave", "eve"]
    actions = [
        "login",
        "logout",
        "token_transfer",
        "change_password",
        "admin_config_change",
        "failed_login",
    ]
    statuses = ["success", "success", "success", "success", "success", "failed"]

    logs: List[SecurityLog] = []
    for i in range(1, total + 1):
        action = random.choice(actions)
        amount = 0.0

        if action == "token_transfer":
            amount = random.choice([40, 80, 120, 250, 900, 1500])

        log = SecurityLog(
            event_id=i,
            user=random.choice(users),
            action=action,
            amount=amount,
            ip=f"192.168.1.{random.randint(2, 250)}",
            status=random.choice(statuses),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        logs.append(log)

    return logs


def ai_threat_score(log: SecurityLog) -> float:
    """
    Very simple AI-like risk scoring model (rule-based weighted score).

    Score range: 0 to 1 (clipped)
    """

    score = 0.0

    # Feature 1: suspicious action type.
    suspicious_action_weights = {
        "failed_login": 0.55,
        "admin_config_change": 0.45,
        "token_transfer": 0.20,
    }
    score += suspicious_action_weights.get(log.action, 0.05)

    # Feature 2: transfer amount (bigger amount -> higher risk).
    if log.amount > 0:
        score += min(log.amount / 3000.0, 0.35)

    # Feature 3: failed status adds risk.
    if log.status == "failed":
        score += 0.25

    # Clamp score to [0, 1].
    return max(0.0, min(score, 1.0))


def classify_log(score: float, threshold: float = 0.60) -> str:
    return "THREAT" if score >= threshold else "NORMAL"


def print_chain_summary(chain: List[LogBlock]) -> None:
    print("\n=== Blockchain Log Summary ===")
    for block in chain:
        action = block.log_data["action"]
        user = block.log_data["user"]
        print(
            f"Block {block.index:02d} | user={user:<5} | action={action:<19} "
            f"| log_hash={block.log_hash[:12]}... | block_hash={block.block_hash[:12]}..."
        )


def main() -> None:
    detector_chain = ThreatDetectionBlockchain()
    logs = generate_sample_logs(total=12)

    print("Generating logs, running AI threat scoring, and storing in blockchain...\n")

    for log in logs:
        score = ai_threat_score(log)
        label = classify_log(score)

        detector_chain.add_log_as_block(log)

        print(
            f"Event {log.event_id:02d} | user={log.user:<5} | action={log.action:<19} "
            f"| score={score:.2f} | label={label}"
        )

    print_chain_summary(detector_chain.chain)

    print("\n=== Integrity Verification ===")
    is_valid = detector_chain.verify_chain_integrity()
    print("Blockchain integrity valid:", is_valid)

    # Optional tampering demo.
    print("\n=== Tampering Demo ===")
    print("Modifying one stored log amount to simulate attacker tampering...")
    detector_chain.chain[3].log_data["amount"] = 999999

    tamper_check = detector_chain.verify_chain_integrity()
    print("Blockchain integrity after tampering:", tamper_check)


if __name__ == "__main__":
    main()
