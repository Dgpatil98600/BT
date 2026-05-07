# Assignment 6: Solidity Token Transfer Between Accounts

## 1. Objective
Write a basic token smart contract and transfer tokens from one account to another.

## 2. Theory
### Token Contract
A token contract stores balances in mapping:
- `balanceOf[address] = token_amount`

Transfer logic:
1. Check sender has enough tokens
2. Deduct from sender
3. Add to receiver

### State Transition Equations
For transfer amount `x`:
- `sender_new = sender_old - x`
- `receiver_new = receiver_old + x`

Conservation:
- `sender_old + receiver_old = sender_new + receiver_new`
(ignoring other accounts)

## 3. Practical Files
- `SimpleToken.sol`
- `token_transfer.py`

## 4. Environment Setup
```bash
pip install web3 py-solc-x python-dotenv
```

`.env` example:
```env
RPC_URL=https://your-testnet-rpc
PRIVATE_KEY=deployer_private_key
ACCOUNT_ADDRESS=0xdeployer
RECEIVER_ADDRESS=0xreceiver
```

## 5. Run
```bash
python token_transfer.py
```

## 6. Expected Output
- Token contract deployed address
- Sender/receiver balances before transfer
- Sender/receiver balances after transfer

## 7. Why This Assignment Matters
Token transfer is core to:
- ERC-20 token systems
- Payment DApps
- Reward points / DAO governance tokens

## 8. Extension Ideas
- Add `approve` and `transferFrom`
- Add decimal-friendly amount handling
- Add unit tests with Brownie/Hardhat/Foundry
