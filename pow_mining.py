"""
Assignment 8: Simple Proof-of-Work Mining
-----------------------------------------
Goal:
- Find a nonce such that block hash starts with required number of zeros.

Expected output:
- Nonce found
- Hash satisfying difficulty target
- Mining time
"""

import hashlib
import json
import time


def calculate_hash(index, timestamp, data, previous_hash, nonce):
    payload = json.dumps(
        {
            "index": index,
            "timestamp": timestamp,
            "data": data,
            "previous_hash": previous_hash,
            "nonce": nonce,
        },
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def mine_block(index, data, previous_hash, difficulty=4):
    prefix = "0" * difficulty
    nonce = 0
    timestamp = time.time()

    start = time.time()
    while True:
        block_hash = calculate_hash(index, timestamp, data, previous_hash, nonce)
        if block_hash.startswith(prefix):
            end = time.time()
            return {
                "index": index,
                "timestamp": timestamp,
                "data": data,
                "previous_hash": previous_hash,
                "nonce": nonce,
                "hash": block_hash,
                "difficulty": difficulty,
                "time_taken_sec": end - start,
            }
        nonce += 1


if __name__ == "__main__":
    mined = mine_block(
        index=1,
        data={"from": "Miner", "to": "Network", "reward": 50},
        previous_hash="0" * 64,
        difficulty=4,
    )

    print("Block mined successfully")
    for k, v in mined.items():
        print(f"{k}: {v}")
