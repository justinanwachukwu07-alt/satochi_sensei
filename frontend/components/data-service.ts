import { api, mockApi } from './api'

// Configuration for data mode
export const DATA_MODE = {
  MOCK: 'mock',
  REAL_TIME: 'real_time',
  HYBRID: 'hybrid' // Use real-time when available, fallback to mock
} as const

export type DataMode = typeof DATA_MODE[keyof typeof DATA_MODE]

// Global data mode setting (can be changed via environment variable or UI toggle)
export const getDataMode = (): DataMode => {
  // Check environment variable first
  const envMode = process.env.NEXT_PUBLIC_DATA_MODE as DataMode
  if (envMode && Object.values(DATA_MODE).includes(envMode)) {
    return envMode
  }
  
  // Check localStorage for user preference
  if (typeof window !== 'undefined') {
    const savedMode = localStorage.getItem('satoshi-sensei-data-mode') as DataMode
    if (savedMode && Object.values(DATA_MODE).includes(savedMode)) {
      return savedMode
    }
  }
  
  // Default to hybrid mode
  return DATA_MODE.HYBRID
}

// Data service class that handles switching between real-time and mock data
export class DataService {
  private mode: DataMode

  constructor(mode: DataMode = getDataMode()) {
    this.mode = mode
  }

  setMode(mode: DataMode) {
    this.mode = mode
  }

  getMode(): DataMode {
    return this.mode
  }

  // Generic method to try real-time first, then fallback to mock
  private async tryRealTimeThenMock<T>(
    realTimeCall: () => Promise<T>,
    mockCall: () => Promise<T>,
    fallbackToMock: boolean = true
  ): Promise<T> {
    if (this.mode === DATA_MODE.MOCK) {
      return mockCall()
    }

    if (this.mode === DATA_MODE.REAL_TIME) {
      try {
        return await realTimeCall()
      } catch (error) {
        console.warn('Real-time API failed, but real-time mode is enforced:', error)
        throw error
      }
    }

    // HYBRID mode: try real-time first, fallback to mock
    try {
      return await realTimeCall()
    } catch (error) {
      console.warn('Real-time API failed, falling back to mock data:', error)
      if (fallbackToMock) {
        return mockCall()
      }
      throw error
    }
  }

  // Price data
  async getPrices() {
    return this.tryRealTimeThenMock(
      () => api.get('/api/v1/prices').then(res => res.data),
      () => mockApi.getPrices()
    )
  }

  // Wallet balances
  async getWalletBalances(address: string) {
    return this.tryRealTimeThenMock(
      () => api.get(`/api/v1/wallet/${address}/balances`).then(res => res.data),
      () => mockApi.getWalletBalances(address)
    )
  }

  // AI recommendations
  async getRecommendation(address: string) {
    return this.tryRealTimeThenMock(
      () => api.get(`/api/v1/ai/recommendation/${address}`).then(res => res.data),
      () => mockApi.getRecommendation(address)
    )
  }

  // AI insights
  async getInsights(address: string) {
    return this.tryRealTimeThenMock(
      () => api.get(`/api/v1/ai/insights/${address}`).then(res => res.data),
      () => this.generateMockInsights(address)
    )
  }

  // Trade preparation
  async prepareTrade(params: {
    fromToken: string
    toToken: string
    amount: string
    slippage: string
    address: string
  }) {
    return this.tryRealTimeThenMock(
      () => api.post('/api/v1/trade/prepare', params).then(res => res.data),
      () => this.generateMockTradeRecommendation(params)
    )
  }

  // Market data
  async getMarketData() {
    return this.tryRealTimeThenMock(
      () => api.get('/api/v1/market/data').then(res => res.data),
      () => this.generateMockMarketData()
    )
  }

  // Portfolio performance
  async getPortfolioPerformance(address: string) {
    return this.tryRealTimeThenMock(
      () => api.get(`/api/v1/portfolio/${address}/performance`).then(res => res.data),
      () => this.generateMockPortfolioPerformance(address)
    )
  }

  // Mock data generators
  private async generateMockInsights(address: string) {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    return {
      insights: [
        {
          id: `insight_${Date.now()}_1`,
          type: "strategy",
          title: "Diversification Opportunity Detected",
          summary: "Your portfolio shows high STX concentration. Consider rebalancing 15% into sBTC for better risk distribution.",
          confidence: 0.87,
          riskScore: 2.3,
          timestamp: new Date().toISOString(),
          details: {
            reasoning: "Analysis of your current holdings reveals 78% allocation in STX tokens, creating concentration risk.",
            marketConditions: [
              "STX showing increased volatility (+12% in 7 days)",
              "sBTC maintaining stable peg to Bitcoin",
              "Stacks DeFi TVL growing 23% month-over-month",
            ],
            recommendations: [
              "Swap 125 STX (10% of holdings) to sBTC",
              "Set up DCA strategy for gradual rebalancing",
              "Monitor correlation metrics weekly",
            ],
            risks: ["Temporary impermanent loss during swap", "Gas fees for rebalancing", "Market timing risk"],
          },
          rawResponse: {
            prompt: `Analyze portfolio allocation for address ${address} and provide diversification recommendations`,
            model: "grok-beta",
            response: '{"analysis": "High STX concentration detected", "recommendation": "Diversify into sBTC", "confidence": 0.87}',
            auditId: "audit_67890",
          },
        },
        {
          id: `insight_${Date.now()}_2`,
          type: "market",
          title: "Favorable Swap Conditions",
          summary: "Current market conditions show optimal timing for STX→sBTC swaps with minimal slippage.",
          confidence: 0.92,
          riskScore: 1.8,
          timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
          details: {
            reasoning: "Deep liquidity pools and low volatility create ideal conditions for large swaps.",
            marketConditions: [
              "Pool liquidity at 3-month high ($2.4M)",
              "Slippage under 0.3% for trades up to $10K",
              "Low volatility period (VIX equivalent: 18)",
            ],
            recommendations: [
              "Execute swaps within next 4-6 hours",
              "Consider larger position sizes due to low slippage",
              "Monitor pool depth before execution",
            ],
            risks: ["Market conditions can change rapidly", "Pool liquidity may decrease", "Arbitrage opportunities"],
          },
        },
      ]
    }
  }

  private async generateMockTradeRecommendation(params: any) {
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    return {
      recommendationId: `rec_${Date.now()}`,
      summary: `Swap ${params.amount} ${params.fromToken} for ${params.toToken} with ${params.slippage}% slippage tolerance`,
      riskScore: 2.8,
      confidence: 0.92,
      actions: [
        {
          type: "clarity_call",
          contract: "SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.amm-swap-pool",
          function: "swap-exact-tokens-for-tokens",
          args: [params.amount, "u1000000", params.fromToken, params.toToken],
        },
      ],
      unsignedTx: {
        payload: `0x${Math.random().toString(16).substring(2, 50)}`,
        humanSummary: `Swap ${params.amount} ${params.fromToken} for approximately ${(Number.parseFloat(params.amount) * 0.98).toFixed(4)} ${params.toToken}`,
        gasEstimate: "0.002 STX",
        fee: "$0.12",
      },
    }
  }

  private async generateMockMarketData() {
    return {
      stx: {
        price: 2.15,
        change24h: -1.2,
        volume24h: 1250000,
        marketCap: 3000000000,
      },
      sbtc: {
        price: 43250,
        change24h: 2.3,
        volume24h: 850000,
        marketCap: 850000000,
      },
      poolLiquidity: {
        stxSbtc: 2400000,
        depth: "Deep",
        fees24h: 12500,
      },
      riskMetrics: {
        volatility: 18,
        correlation: 0.65,
        impermanentLoss: "Low",
      },
    }
  }

  private async generateMockPortfolioPerformance(address: string) {
    return {
      totalValue: 26144.28,
      change24h: 2.3,
      change7d: 5.8,
      change30d: 12.4,
      holdings: [
        {
          symbol: "BTC",
          amount: "0.5432",
          usdValue: 23456.78,
          change24h: 2.3,
          allocation: 89.7,
        },
        {
          symbol: "STX",
          amount: "1250.00",
          usdValue: 2687.5,
          change24h: -1.2,
          allocation: 10.3,
        },
      ],
      performance: {
        sharpeRatio: 1.85,
        maxDrawdown: -8.2,
        volatility: 15.3,
        beta: 0.92,
      },
    }
  }
}

// Export singleton instance
export const dataService = new DataService()

// Export individual methods for convenience
export const {
  getPrices,
  getWalletBalances,
  getRecommendation,
  getInsights,
  prepareTrade,
  getMarketData,
  getPortfolioPerformance,
} = dataService
