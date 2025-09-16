"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { WalletGuard } from "@/components/wallet-guard"
import { TrendingUp, TrendingDown, Wallet, ExternalLink, RefreshCw, Bitcoin, Coins } from "lucide-react"

function PortfolioContent() {
  const holdings = [
    {
      symbol: "BTC",
      name: "Bitcoin",
      amount: "0.5432",
      usdValue: 23456.78,
      change24h: 2.3,
      allocation: 89.7,
      icon: <Bitcoin className="w-6 h-6 text-primary" />,
    },
    {
      symbol: "STX",
      name: "Stacks",
      amount: "1,250.00",
      usdValue: 2687.5,
      change24h: -1.2,
      allocation: 10.3,
      icon: <div className="w-6 h-6 bg-secondary rounded-full" />,
    },
  ]

  const transactions = [
    {
      id: "tx_1",
      type: "swap",
      description: "Swap 100 STX → 0.0046 sBTC",
      amount: "+0.0046 sBTC",
      timestamp: "2 hours ago",
      status: "confirmed",
      txHash: "0x1234...5678",
    },
    {
      id: "tx_2",
      type: "swap",
      description: "Swap 50 USDA → 23.2 STX",
      amount: "+23.2 STX",
      timestamp: "1 day ago",
      status: "confirmed",
      txHash: "0x2345...6789",
    },
    {
      id: "tx_3",
      type: "swap",
      description: "Swap 0.001 sBTC → 20.1 STX",
      amount: "+20.1 STX",
      timestamp: "3 days ago",
      status: "confirmed",
      txHash: "0x3456...7890",
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-balance">Portfolio</h1>
          <p className="text-muted-foreground text-pretty">Track your holdings and transaction history</p>
        </div>
        <Button className="bg-primary hover:bg-primary/90 text-primary-foreground">
          <RefreshCw className="w-4 h-4 mr-2" />
          Refresh Data
        </Button>
      </div>

      {/* Portfolio Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="bg-card border-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Value</CardTitle>
            <Wallet className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$26,144.28</div>
            <div className="flex items-center gap-1 text-xs text-primary">
              <TrendingUp className="w-3 h-3" />
              +2.3% (24h)
            </div>
          </CardContent>
        </Card>

        <Card className="bg-card border-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">24h Change</CardTitle>
            <TrendingUp className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-primary">+$587.23</div>
            <div className="text-xs text-muted-foreground">+2.3% increase</div>
          </CardContent>
        </Card>

        <Card className="bg-card border-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Assets</CardTitle>
            <Coins className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{holdings.length}</div>
            <div className="text-xs text-muted-foreground">Different tokens</div>
          </CardContent>
        </Card>
      </div>

      {/* Portfolio Details */}
      <Tabs defaultValue="holdings" className="space-y-6">
        <TabsList className="bg-muted">
          <TabsTrigger value="holdings">Holdings</TabsTrigger>
          <TabsTrigger value="transactions">Transactions</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
        </TabsList>

        <TabsContent value="holdings" className="space-y-4">
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle>Current Holdings</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {holdings.map((holding) => (
                  <div key={holding.symbol} className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
                    <div className="flex items-center gap-3">
                      {holding.icon}
                      <div>
                        <div className="font-semibold">{holding.name}</div>
                        <div className="text-sm text-muted-foreground">{holding.symbol}</div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-semibold">
                        {holding.amount} {holding.symbol}
                      </div>
                      <div className="text-sm text-muted-foreground">${holding.usdValue.toLocaleString()}</div>
                    </div>
                    <div className="text-right">
                      <div
                        className={`flex items-center gap-1 ${holding.change24h >= 0 ? "text-primary" : "text-destructive"}`}
                      >
                        {holding.change24h >= 0 ? (
                          <TrendingUp className="w-3 h-3" />
                        ) : (
                          <TrendingDown className="w-3 h-3" />
                        )}
                        {Math.abs(holding.change24h)}%
                      </div>
                      <div className="text-sm text-muted-foreground">{holding.allocation}% allocation</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="transactions" className="space-y-4">
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle>Recent Transactions</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {transactions.map((tx) => (
                  <div key={tx.id} className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-primary/20 rounded-lg flex items-center justify-center">
                        <TrendingUp className="w-5 h-5 text-primary" />
                      </div>
                      <div>
                        <div className="font-semibold">{tx.description}</div>
                        <div className="text-sm text-muted-foreground">{tx.timestamp}</div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-semibold text-primary">{tx.amount}</div>
                      <div className="flex items-center gap-2">
                        <Badge variant="secondary" className="bg-primary/20 text-primary border-primary/30">
                          {tx.status}
                        </Badge>
                        <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
                          <ExternalLink className="w-3 h-3" />
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="performance" className="space-y-4">
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle>Performance Metrics</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Total Return</span>
                    <span className="font-semibold text-primary">+12.4%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Best Performing Asset</span>
                    <span className="font-semibold">BTC (+15.2%)</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Worst Performing Asset</span>
                    <span className="font-semibold text-destructive">STX (-2.1%)</span>
                  </div>
                </div>
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Total Trades</span>
                    <span className="font-semibold">23</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Successful Trades</span>
                    <span className="font-semibold text-primary">21 (91.3%)</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Avg Trade Size</span>
                    <span className="font-semibold">$1,247</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default function PortfolioPage() {
  return (
    <WalletGuard>
      <PortfolioContent />
    </WalletGuard>
  )
}
