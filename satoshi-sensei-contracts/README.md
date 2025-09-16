# Satoshi Sensei Smart Contracts

AI-powered DeFi strategy execution and management contracts for the Stacks blockchain.

## Overview

This repository contains the smart contracts that power the Satoshi Sensei DeFi copilot platform. The contracts handle strategy creation, execution, and performance tracking for various DeFi protocols on the Stacks ecosystem.

## Contracts

### 1. Satoshi Sensei Core (`satoshi-sensei-core.clar`)

The main contract that manages DeFi strategy recommendations and execution tracking.

**Key Features:**
- Strategy creation and management
- Performance tracking
- User strategy history
- Protocol fee management
- Contract statistics

**Main Functions:**
- `create-strategy`: Create a new DeFi strategy recommendation
- `execute-strategy`: Execute a strategy with transaction hash
- `update-strategy-performance`: Update strategy performance metrics
- `get-strategy`: Retrieve strategy details
- `get-user-strategies`: Get all strategies for a user
- `get-contract-stats`: Get contract statistics

### 2. DeFi Strategy Executor (`defi-strategy-executor.clar`)

Handles the execution of specific DeFi strategies across different protocols.

**Key Features:**
- Multi-protocol support (ALEX, Arkadiko, Velar)
- Liquidity provision execution
- Yield farming execution
- Protocol configuration management
- Fee calculation and collection

**Supported Protocols:**
- **ALEX**: Decentralized exchange for Stacks
- **Arkadiko**: Lending and borrowing protocol
- **Velar**: Advanced DeFi protocol

**Main Functions:**
- `execute-liquidity-provision`: Execute liquidity provision strategy
- `execute-yield-farming`: Execute yield farming strategy
- `complete-execution`: Mark strategy execution as completed
- `update-protocol-config`: Update protocol configuration

## Strategy Types

1. **Liquidity Provision**: Provide liquidity to DEX pools
2. **Yield Farming**: Stake tokens to earn rewards
3. **Staking**: Stake STX for network rewards
4. **Arbitrage**: Execute arbitrage opportunities

## Getting Started

### Prerequisites

- [Clarinet](https://github.com/hirosystems/clarinet) installed
- Node.js and npm installed

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd satoshi-sensei-contracts
```

2. Install dependencies:
```bash
npm install
```

### Development

1. Start the Clarinet console:
```bash
clarinet console
```

2. Run tests:
```bash
clarinet test
```

3. Check contract syntax:
```bash
clarinet check
```

### Testing

The contracts include comprehensive test suites:

- `satoshi-sensei-core_test.ts`: Tests for the core contract
- `defi-strategy-executor_test.ts`: Tests for the strategy executor

Run tests with:
```bash
clarinet test
```

## Contract Architecture

### Data Structures

**Strategy:**
```clarity
{
  id: uint,
  user: principal,
  strategy-type: (string-utf8 50),
  risk-score: uint,
  expected-apy: uint,
  amount: uint,
  status: (string-utf8 20),
  created-at: uint,
  executed-at: (optional uint),
  transaction-hash: (optional (string-utf8 100))
}
```

**Execution:**
```clarity
{
  id: uint,
  user: principal,
  strategy-type: uint,
  amount: uint,
  protocol: (string-utf8 50),
  status: (string-utf8 20),
  created-at: uint,
  completed-at: (optional uint),
  fees-paid: uint,
  returns: (optional uint)
}
```

### Error Codes

- `u100`: Unauthorized access
- `u101`: Invalid amount or strategy
- `u102`: Insufficient balance
- `u103`: Strategy not found
- `u104`: Strategy already executed

## Deployment

### Testnet Deployment

1. Configure testnet settings in `settings/Testnet.toml`
2. Deploy contracts:
```bash
clarinet deploy --testnet
```

### Mainnet Deployment

1. Configure mainnet settings in `settings/Mainnet.toml`
2. Deploy contracts:
```bash
clarinet deploy --mainnet
```

## Security Considerations

- All contract functions require owner authorization
- Input validation for all parameters
- Safe arithmetic operations
- Proper error handling
- Fee rate limits to prevent excessive fees

## Integration

The contracts are designed to integrate with:

- **Backend API**: FastAPI backend for strategy management
- **Frontend**: Next.js dashboard for user interaction
- **AI Engine**: Groq API for strategy recommendations
- **External APIs**: ALEX, Arkadiko, Velar protocols

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Join our Discord community
- Check the documentation

## Roadmap

- [ ] Cross-chain strategy execution
- [ ] Automated strategy execution
- [ ] Advanced risk management
- [ ] Multi-signature support
- [ ] Governance token integration
