
import hashlib

# Function to hash data
def hash_data(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Read transactions from file
with open("transactions.txt", "r") as f:
    transactions = [line.strip() for line in f.readlines()]

# Step 1: Hash all transactions
hashed = [hash_data(tx) for tx in transactions]

# Step 2: Build Merkle Tree
while len(hashed) > 1:
    temp = []

    for i in range(0, len(hashed), 2):
        if i + 1 < len(hashed):
            combined = hashed[i] + hashed[i + 1]
        else:
            # If odd, duplicate last
            combined = hashed[i] + hashed[i]

        temp.append(hash_data(combined))

    hashed = temp

# Final Merkle Root
print("Merkle Root:", hashed[0])

