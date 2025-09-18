import axios from "axios"

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000",
  withCredentials: true,
  timeout: 15000,
})

// Mock API functions for development
export const mockApi = {
  async getNonce(address: string) {
    return { nonce: `nonce_${Date.now()}_${address.slice(-6)}` }
  },

  async verifySignature(address: string, signature: string, nonce: string) {
    // Mock verification - in real app this would validate the signature
    return { success: true, token: `jwt_${address.slice(-6)}` }
  },

  async getPrices() {
    return {
      bitcoin: { usd: 43250.5, change_24h: 2.3 },
      stx: { usd: 2.15, change_24h: -1.2 },
    }
  },

  async getWalletBalances(address: string) {
    return {
      balances: [
        { symbol: "BTC", amount: "0.5432", usdValue: 23456.78 },
        { symbol: "STX", amount: "1250.00", usdValue: 2687.5 },
      ],
    }
  },

  async getRecommendation(address: string) {
    return {
      recommendationId: `rec_${Date.now()}`,
      summary:
        "Consider swapping 10% of your STX holdings to sBTC to diversify your Bitcoin exposure while maintaining Stacks ecosystem participation.",
      riskScore: 3.2,
      confidence: 0.85,
      actions: [
        {
          type: "clarity_call",
          contract: "SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.amm-swap-pool",
          function: "swap-exact-tokens-for-tokens",
          args: ["125", "u1000000", "STX", "sBTC"],
        },
      ],
    }
  },
}
