
balances = {
    "Alice": 10,
    "Bob": 0,
    "Charlie": 0
}


transaction_history = []


def send(sender, receiver, amount, tx_id):
    
    if tx_id in transaction_history:
        print("Transaction already processed (Double Spending Detected)")
        return


    if balances[sender] < amount:
        print("Not enough balance")
        return

  
    balances[sender] -= amount
    balances[receiver] += amount

    # Record transaction
    transaction_history.append(tx_id)

    print(f"{sender} sent {amount} coins to {receiver}")


send("Alice", "Bob", 10, "tx1")


send("Alice", "Charlie", 10, "tx1")


send("Alice", "Charlie", 10, "tx2")


print("\nFinal Balances:")
for user, balance in balances.items():
    print(user, ":", balance)
