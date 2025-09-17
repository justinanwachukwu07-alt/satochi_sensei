<div align="center">
  <!-- Updated logo reference to use SVG -->
  <img src="./public/logo.jpg" alt="Satoshi Sensei Logo" width="120" height="120" />
  
  # 🧠 Satoshi Sensei
  
  **AI-Powered DeFi Copilot for Bitcoin & Stacks**
  
  *Your intelligent trading companion for the Bitcoin ecosystem*
  
  [![Next.js](https://img.shields.io/badge/Next.js-14.2-black?style=flat-square&logo=next.js)](https://nextjs.org/)
  [![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
  [![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC?style=flat-square&logo=tailwind-css)](https://tailwindcss.com/)
  [![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
</div>

---

## 🌟 Overview

**Satoshi Sensei** is a cutting-edge AI-powered DeFi trading platform designed specifically for the Bitcoin and Stacks ecosystems. Built with security, performance, and user experience at its core, it provides intelligent trading recommendations while maintaining complete user control over their assets.

### ✨ Key Features

- 🤖 **AI-Powered Analysis** - Advanced market analysis and trading recommendations
- 🔐 **Secure Wallet Integration** - Non-custodial with nonce-based authentication
- 📊 **Real-Time Portfolio Tracking** - Comprehensive asset monitoring and analytics
- 🎯 **Smart Trade Execution** - Prepare → Sign → Broadcast workflow for maximum security
- 🌙 **Neon Bitcoin Noir Theme** - Beautiful dark interface with Bitcoin orange accents
- 📱 **Responsive Design** - Seamless experience across all devices
- ⚡ **Lightning Fast** - Optimized performance with modern React patterns

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- pnpm (recommended), npm, or yarn
- A Stacks-compatible wallet (Hiro Wallet recommended)

### Installation

1. **Clone the repository**
   \`\`\`bash
   git clone https://github.com/your-username/satoshi-sensei.git
   cd satoshi-sensei
   \`\`\`

2. **Install dependencies**
   \`\`\`bash
   pnpm install
   # or
   npm install
   # or
   yarn install
   \`\`\`

3. **Set up environment variables**
   \`\`\`bash
   cp env.example .env.local
   \`\`\`
   
   Configure the following variables:
   \`\`\`env
   NEXT_PUBLIC_API_BASE_URL=https://your-api-endpoint.com
   NEXT_PUBLIC_STACKS_NETWORK=testnet # or mainnet
   NEXT_PUBLIC_DEV_SUPABASE_REDIRECT_URL=http://localhost:3000
   
   # Contract Addresses (Deployed on Testnet)
   NEXT_PUBLIC_SATOSHI_SENSEI_CORE_CONTRACT=STWWKZA3X98YT263TP28280FP25TYP2TMHC5F7G2.satoshi-sensei-core
   NEXT_PUBLIC_DEFI_STRATEGY_EXECUTOR_CONTRACT=STWWKZA3X98YT263TP28280FP25TYP2TMHC5F7G2.defi-strategy-executor
   \`\`\`

4. **Run the development server**
   \`\`\`bash
   pnpm dev
   # or
   npm run dev
   # or
   yarn dev
   \`\`\`

5. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

---

## 🏗️ Architecture

### Tech Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| **Framework** | Next.js 14.2 | React framework with App Router |
| **Language** | TypeScript | Type-safe development |
| **Styling** | Tailwind CSS | Utility-first CSS framework |
| **UI Components** | Radix UI + shadcn/ui | Accessible component library |
| **State Management** | Zustand | Lightweight state management |
| **Animations** | Framer Motion | Smooth animations and transitions |
| **Forms** | React Hook Form + Zod | Form handling and validation |
| **Charts** | Recharts | Data visualization |
| **HTTP Client** | Axios | API communication |

### Project Structure

\`\`\`
satoshi-sensei/
├── app/                    # Next.js App Router
│   ├── dashboard/         # Protected dashboard routes
│   │   ├── insights/      # AI analysis page
│   │   ├── portfolio/     # Portfolio tracking
│   │   ├── settings/      # User settings
│   │   └── trade/         # Trading interface
│   ├── globals.css        # Global styles and theme
│   ├── layout.tsx         # Root layout
│   └── page.tsx          # Landing page
├── components/            # Reusable components
│   ├── ui/               # shadcn/ui components
│   ├── dashboard-*.tsx   # Dashboard-specific components
│   ├── connect-wallet-button.tsx
│   └── wallet-guard.tsx
├── hooks/                # Custom React hooks
│   ├── use-wallet.ts     # Wallet integration
│   └── use-mobile.tsx    # Responsive utilities
├── lib/                  # Utilities and configuration
│   ├── api.ts           # API client
│   ├── store.ts         # Zustand stores
│   └── utils.ts         # Helper functions
└── public/              # Static assets
    └── logo.svg         # Application logo
\`\`\`

---

## 🔐 Security Features

### Wallet Security
- **Non-custodial**: Your keys, your coins - we never store private keys
- **Nonce-based authentication**: Secure challenge-response authentication
- **Transaction review**: Every transaction is reviewed before signing
- **Secure communication**: All API calls use HTTPS with proper headers

### Best Practices
- **TypeScript strict mode** for compile-time safety
- **Input validation** with Zod schemas
- **Rate limiting** on AI API calls
- **CORS protection** and secure headers
- **Environment variable validation**

---

## 🎨 Design System

### Color Palette
- **Primary**: Bitcoin Orange (`#F7931A`)
- **Secondary**: Stacks Purple (`#5546FF`)
- **Background**: Rich Dark (`#0A0A0B`)
- **Surface**: Elevated Dark (`#1A1A1B`)
- **Accent**: Electric Blue (`#00D4FF`)

### Typography
- **Headings**: Inter (Clean, modern sans-serif)
- **Body**: Inter (Optimized for readability)
- **Code**: JetBrains Mono (Monospace for technical content)

### Components
All components follow the **Neon Bitcoin Noir** aesthetic with:
- Subtle gradients and glows
- Smooth animations and micro-interactions
- High contrast for accessibility
- Consistent spacing and typography scales

---

## 📋 Deployed Contracts

The Satoshi Sensei contracts are deployed on Stacks Testnet:

### Contract Addresses
- **Satoshi Sensei Core**: `STWWKZA3X98YT263TP28280FP25TYP2TMHC5F7G2.satoshi-sensei-core`
- **DeFi Strategy Executor**: `STWWKZA3X98YT263TP28280FP25TYP2TMHC5F7G2.defi-strategy-executor`

### Contract Functions
- **Core Contract**: Strategy creation, execution, and management
- **Executor Contract**: DeFi strategy execution (liquidity provision, yield farming)

### View on Explorer
- [Stacks Explorer - Testnet](https://explorer.stacks.co/?chain=testnet)

---

## 🔌 API Integration

### Wallet Connection
\`\`\`typescript
// Connect to Stacks wallet
const { connectWallet, isConnected, address } = useWallet();

await connectWallet();
\`\`\`

### AI Recommendations
\`\`\`typescript
// Get AI trading insights
const insights = await api.getAIInsights({
  portfolio: userPortfolio,
  riskTolerance: 'moderate',
  timeframe: '1d'
});
\`\`\`

### Trade Execution
\`\`\`typescript
// Prepare and execute trade
const unsignedTx = await api.prepareTrade({
  fromToken: 'STX',
  toToken: 'BTC',
  amount: 100
});

const signedTx = await signTransaction(unsignedTx);
const result = await api.broadcastTransaction(signedTx);
\`\`\`

---

## 🧪 Development

### Available Scripts

\`\`\`bash
# Development
pnpm dev             # Start development server
pnpm build           # Build for production
pnpm start           # Start production server
pnpm lint            # Run ESLint
pnpm type-check      # Run TypeScript compiler

# Testing
pnpm test            # Run test suite
pnpm test:watch      # Run tests in watch mode
pnpm test:coverage   # Generate coverage report
\`\`\`

### Environment Setup

Create a `.env.local` file with:

\`\`\`env
# API Configuration
NEXT_PUBLIC_API_BASE_URL=https://api.satoshisensei.com
NEXT_PUBLIC_STACKS_NETWORK=mainnet

# Development URLs
NEXT_PUBLIC_DEV_SUPABASE_REDIRECT_URL=http://localhost:3000

# Feature Flags
NEXT_PUBLIC_ENABLE_MOCK_WALLET=true
NEXT_PUBLIC_ENABLE_AI_INSIGHTS=true
\`\`\`

---

## 🚀 Deployment

### Vercel (Recommended)

1. **Connect your repository** to Vercel
2. **Configure environment variables** in the Vercel dashboard:
   - `NEXT_PUBLIC_STACKS_NETWORK=testnet`
   - `NEXT_PUBLIC_SATOSHI_SENSEI_CORE_CONTRACT=STWWKZA3X98YT263TP28280FP25TYP2TMHC5F7G2.satoshi-sensei-core`
   - `NEXT_PUBLIC_DEFI_STRATEGY_EXECUTOR_CONTRACT=STWWKZA3X98YT263TP28280FP25TYP2TMHC5F7G2.defi-strategy-executor`
   - `NEXT_PUBLIC_API_BASE_URL=https://api.satoshisensei.com`
3. **Deploy** - Vercel will automatically build and deploy your app using the included `vercel.json` configuration

### Render.com

1. **Connect your repository** to Render
2. **Create a new Web Service** and select your repository
3. **Configure the service**:
   - Build Command: `pnpm install && pnpm build`
   - Start Command: `pnpm start`
   - Environment: `Node`
4. **Deploy** - Render will use the included `render.yaml` configuration

### Manual Deployment

\`\`\`bash
# Build the application
pnpm build

# Start the production server
pnpm start
\`\`\`

### Environment Variables for Production

Make sure to set these environment variables in your deployment platform:

\`\`\`env
NEXT_PUBLIC_STACKS_NETWORK=testnet
NEXT_PUBLIC_SATOSHI_SENSEI_CORE_CONTRACT=STWWKZA3X98YT263TP28280FP25TYP2TMHC5F7G2.satoshi-sensei-core
NEXT_PUBLIC_DEFI_STRATEGY_EXECUTOR_CONTRACT=STWWKZA3X98YT263TP28280FP25TYP2TMHC5F7G2.defi-strategy-executor
NEXT_PUBLIC_API_BASE_URL=https://api.satoshisensei.com
NEXT_PUBLIC_ENABLE_MOCK_WALLET=false
NEXT_PUBLIC_ENABLE_AI_INSIGHTS=true
\`\`\`

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Code Standards

- **TypeScript** for all new code
- **ESLint** and **Prettier** for code formatting
- **Conventional Commits** for commit messages
- **Component documentation** with JSDoc
- **Test coverage** for new features

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Stacks Foundation** for the amazing blockchain infrastructure
- **Bitcoin Community** for the inspiration and vision
- **shadcn/ui** for the beautiful component library
- **Vercel** for the incredible deployment platform

---

## 📞 Support

- **Documentation**: [docs.satoshisensei.com](https://docs.satoshisensei.com)
- **Discord**: [Join our community](https://discord.gg/satoshisensei)
- **Twitter**: [@SatoshiSensei](https://twitter.com/satoshisensei)
- **Email**: support@satoshisensei.com

---

<div align="center">
  <p>Built with ❤️ for the Bitcoin ecosystem</p>
  <p>
    <a href="https://satoshisensei.com">Website</a> •
    <a href="https://docs.satoshisensei.com">Documentation</a> •
    <a href="https://discord.gg/satoshisensei">Community</a>
  </p>
</div>
