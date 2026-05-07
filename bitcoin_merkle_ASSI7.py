"""
Assignment 7: Bitcoin Block Structure + Merkle Root Computation
----------------------------------------------------------------
This script explains a simplified Bitcoin block and computes Merkle root
for sample transaction IDs.

Expected output:
- Printed block header fields
- Computed Merkle root from sample txids
"""

import hashlib


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def merkle_root(txids):
    # Build upper levels until one hash remains.
    level = txids[:]
    while len(level) > 1:
        if len(level) % 2 == 1:
            # If odd count, duplicate last hash (Bitcoin style).
            level.append(level[-1])

        next_level = []
        for i in range(0, len(level), 2):
            combined = level[i] + level[i + 1]
            next_level.append(sha256_hex(sha256_hex(combined)))
        level = next_level

    return level[0]


if __name__ == "__main__":
    sample_txids = [
        sha256_hex("tx1: Alice->Bob 2 BTC"),
        sha256_hex("tx2: Bob->Charlie 1 BTC"),
        sha256_hex("tx3: Dave->Eve 0.5 BTC"),
        sha256_hex("tx4: Eve->Frank 0.1 BTC"),
    ]

    root = merkle_root(sample_txids)

    bitcoin_block_header = {
        "version": 2,
        "previous_block_hash": "00ab...ff22",
        "merkle_root": root,
        "timestamp": 1710000000,
        "bits": "1d00ffff",  # compact target format
        "nonce": 123456,
    }

    print("Bitcoin Block Header (Simplified)")
    for k, v in bitcoin_block_header.items():
        print(f"{k}: {v}")

    print("\nSample TXIDs:")
    for tx in sample_txids:
        print(tx)

    print("\nComputed Merkle Root:")
    print(root)
