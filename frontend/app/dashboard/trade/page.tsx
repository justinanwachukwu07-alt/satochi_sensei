"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { WalletGuard } from "@/components/wallet-guard"
import { UnsignedTxModal } from "@/components/unsigned-tx-modal"
import { ArrowUpDown, TrendingUp, AlertTriangle, Zap, RefreshCw } from "lucide-react"
import { useAuthStore } from "/lib/store"

interface TradeRecommendation {
  recommendationId: string
  summary: string
  riskScore: number
  confidence: number
  actions: Array<{
    type: string
    contract: string
    function: string
    args: string[]
  }>
  unsignedTx?: {
    payload: string
    humanSummary: string
    gasEstimate: string
    fee: string
  }
}

function TradeContent() {
  const { address } = useAuthStore()
  const [fromToken, setFromToken] = useState("STX")
  const [toToken, setToToken] = useState("sBTC")
  const [amount, setAmount] = useState("")
  const [slippage, setSlippage] = useState("0.5")
  const [isLoading, setIsLoading] = useState(false)
  const [recommendation, setRecommendation] = useState<TradeRecommendation | null>(null)
  const [showModal, setShowModal] = useState(false)

  const handlePrepareTradeClick = async () => {
    if (!amount || !address) return

    setIsLoading(true)
    try {
      // Simulate API call to prepare trade
      await new Promise((resolve) => setTimeout(resolve, 2000))

      const mockRecommendation: TradeRecommendation = {
        recommendationId: `rec_${Date.now()}`,
        summary: `Swap ${amount} ${fromToken} for ${toToken} with ${slippage}% slippage tolerance`,
        riskScore: 2.8,
        confidence: 0.92,
        actions: [
          {
            type: "clarity_call",
            contract: "SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.amm-swap-pool",
            function: "swap-exact-tokens-for-tokens",
            args: [amount, "u1000000", fromToken, toToken],
          },
        ],
        unsignedTx: {
          payload: `0x${Math.random().toString(16).substring(2, 50)}`,
          humanSummary: `Swap ${amount} ${fromToken} for approximately ${(Number.parseFloat(amount) * 0.98).toFixed(4)} ${toToken}`,
          gasEstimate: "0.002 STX",
          fee: "$0.12",
        },
      }

      setRecommendation(mockRecommendation)
      setShowModal(true)
    } catch (error) {
      console.error("Failed to prepare trade:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const swapTokens = () => {
    const temp = fromToken
    setFromToken(toToken)
    setToToken(temp)
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-balance">Trade</h1>
        <p className="text-muted-foreground text-pretty">
          Execute secure DeFi trades with AI-powered insights and risk assessment
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Trade Form */}
        <div className="lg:col-span-2">
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-primary" />
                Swap Tokens
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* From Token */}
              <div className="space-y-2">
                <Label htmlFor="from-amount">From</Label>
                <div className="flex gap-2">
                  <div className="flex-1">
                    <Input
                      id="from-amount"
                      type="number"
                      placeholder="0.00"
                      value={amount}
                      onChange={(e) => setAmount(e.target.value)}
                      className="text-lg h-12 bg-input border-border"
                    />
                  </div>
                  <Select value={fromToken} onValueChange={setFromToken}>
                    <SelectTrigger className="w-32 h-12 bg-input border-border">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="STX">STX</SelectItem>
                      <SelectItem value="sBTC">sBTC</SelectItem>
                      <SelectItem value="USDA">USDA</SelectItem>
                      <SelectItem value="ALEX">ALEX</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="flex justify-between text-sm text-muted-foreground">
                  <span>Balance: 1,250.00 STX</span>
                  <span>≈ $2,687.50</span>
                </div>
              </div>

              {/* Swap Button */}
              <div className="flex justify-center">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={swapTokens}
                  className="rounded-full w-10 h-10 p-0 border-border hover:bg-card bg-transparent"
                >
                  <ArrowUpDown className="w-4 h-4" />
                </Button>
              </div>

              {/* To Token */}
              <div className="space-y-2">
                <Label htmlFor="to-amount">To</Label>
                <div className="flex gap-2">
                  <div className="flex-1">
                    <Input
                      id="to-amount"
                      type="number"
                      placeholder="0.00"
                      value={amount ? (Number.parseFloat(amount) * 0.98).toFixed(4) : ""}
                      readOnly
                      className="text-lg h-12 bg-muted border-border text-muted-foreground"
                    />
                  </div>
                  <Select value={toToken} onValueChange={setToToken}>
                    <SelectTrigger className="w-32 h-12 bg-input border-border">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="sBTC">sBTC</SelectItem>
                      <SelectItem value="STX">STX</SelectItem>
                      <SelectItem value="USDA">USDA</SelectItem>
                      <SelectItem value="ALEX">ALEX</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="flex justify-between text-sm text-muted-foreground">
                  <span>Estimated output</span>
                  <span>≈ ${amount ? (Number.parseFloat(amount) * 2.15 * 0.98).toFixed(2) : "0.00"}</span>
                </div>
              </div>

              {/* Slippage */}
              <div className="space-y-2">
                <Label htmlFor="slippage">Slippage Tolerance</Label>
                <Select value={slippage} onValueChange={setSlippage}>
                  <SelectTrigger className="bg-input border-border">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="0.1">0.1%</SelectItem>
                    <SelectItem value="0.5">0.5%</SelectItem>
                    <SelectItem value="1.0">1.0%</SelectItem>
                    <SelectItem value="3.0">3.0%</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Prepare Trade Button */}
              <Button
                onClick={handlePrepareTradeClick}
                disabled={!amount || Number.parseFloat(amount) <= 0 || isLoading}
                className="w-full h-12 bg-primary hover:bg-primary/90 text-primary-foreground"
              >
                {isLoading ? (
                  <>
                    <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                    Preparing Trade...
                  </>
                ) : (
                  <>
                    <Zap className="w-4 h-4 mr-2" />
                    Prepare Trade with AI
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Trade Info Sidebar */}
        <div className="space-y-6">
          {/* Market Info */}
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="text-lg">Market Info</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between">
                <span className="text-muted-foreground">STX Price</span>
                <div className="text-right">
                  <div className="font-medium">$2.15</div>
                  <div className="text-xs text-destructive">-1.2%</div>
                </div>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">sBTC Price</span>
                <div className="text-right">
                  <div className="font-medium">$43,250</div>
                  <div className="text-xs text-primary">+2.3%</div>
                </div>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Pool Liquidity</span>
                <div className="text-right">
                  <div className="font-medium">$2.4M</div>
                  <div className="text-xs text-muted-foreground">Deep</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Risk Assessment */}
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-secondary" />
                Risk Assessment
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-muted-foreground">Impermanent Loss</span>
                <Badge variant="secondary" className="bg-primary/20 text-primary border-primary/30">
                  Low
                </Badge>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-muted-foreground">Slippage Risk</span>
                <Badge variant="secondary" className="bg-secondary/20 text-secondary border-secondary/30">
                  Medium
                </Badge>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-muted-foreground">Smart Contract</span>
                <Badge variant="secondary" className="bg-primary/20 text-primary border-primary/30">
                  Audited
                </Badge>
              </div>
              <div className="pt-2 border-t border-border">
                <div className="flex justify-between items-center">
                  <span className="font-medium">Overall Risk</span>
                  <Badge variant="secondary" className="bg-primary/20 text-primary border-primary/30">
                    2.8/5
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Recent Trades */}
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="text-lg">Recent Activity</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex justify-between items-center text-sm">
                <span className="text-muted-foreground">Swap 100 STX → sBTC</span>
                <span className="text-primary">+0.0046 sBTC</span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-muted-foreground">Swap 50 USDA → STX</span>
                <span className="text-primary">+23.2 STX</span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-muted-foreground">Swap 0.001 sBTC → STX</span>
                <span className="text-primary">+20.1 STX</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Unsigned Transaction Modal */}
      {recommendation && (
        <UnsignedTxModal
          open={showModal}
          onOpenChange={setShowModal}
          recommendation={recommendation}
          onSuccess={() => {
            setShowModal(false)
            setRecommendation(null)
            setAmount("")
          }}
        />
      )}
    </div>
  )
}

export default function TradePage() {
  return (
    <WalletGuard>
      <TradeContent />
    </WalletGuard>
  )
}
