# Assignment 5: Deploy HelloWorld Contract on Ethereum Testnet

## 1. Objective
Deploy a very simple Solidity contract on an Ethereum test network and read its deployed address.

## 2. Theory
### Ethereum
Ethereum is a blockchain that supports programmable smart contracts.
- Smart contracts run on EVM (Ethereum Virtual Machine)
- Users send transactions to deploy or call contract functions

### Test Network
A testnet is used for learning and testing without real money.
Examples: Sepolia, Holesky.

### Deployment Basics
To deploy a contract:
1. Compile Solidity source -> ABI + Bytecode
2. Build deployment transaction
3. Sign with private key
4. Send to network
5. Wait for receipt

## 3. Practical Files
- `HelloWorld.sol` (contract code)
- `deploy_helloworld_testnet.py` (deployment script)

## 4. Setup
```bash
pip install web3 py-solc-x python-dotenv
```

Create `.env`:
```env
RPC_URL=https://your-sepolia-rpc
PRIVATE_KEY=your_test_wallet_private_key
ACCOUNT_ADDRESS=0xyour_wallet_address
```

## 5. Run
```bash
python deploy_helloworld_testnet.py
```

## 6. Expected Output
- Deployment transaction hash
- Contract address
- `helloworld_deployment.json` generated

## 7. Theory + Math Behind Gas
Transaction fee approximation:
- `fee = gasUsed * gasPrice`

Where:
- `gasUsed` = computational steps consumed
- `gasPrice` = price per gas unit in wei

## 8. Why This Is Useful
Deploying contracts is the first practical step for DApp development.
