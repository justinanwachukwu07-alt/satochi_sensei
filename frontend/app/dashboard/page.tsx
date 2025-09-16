"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { WalletGuard } from "@/components/wallet-guard"
import { TrendingUp, TrendingDown, Brain, Zap, ArrowRight, Bitcoin, Coins } from "lucide-react"
import Link from "next/link"

function DashboardContent() {
  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-balance">Welcome to Satoshi Sensei</h1>
          <p className="text-muted-foreground text-pretty">
            Your AI-powered DeFi copilot for Bitcoin and Stacks trading
          </p>
        </div>
        <Link href="/dashboard/trade">
          <Button className="bg-primary hover:bg-primary/90 text-primary-foreground">
            Start Trading
            <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        </Link>
      </div>

      {/* Portfolio Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="bg-card border-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Portfolio</CardTitle>
            <Coins className="h-4 w-4 text-muted-foreground" />
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
            <CardTitle className="text-sm font-medium">Bitcoin Holdings</CardTitle>
            <Bitcoin className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0.5432 BTC</div>
            <div className="flex items-center gap-1 text-xs text-primary">
              <TrendingUp className="w-3 h-3" />
              $23,456.78
            </div>
          </CardContent>
        </Card>

        <Card className="bg-card border-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">STX Holdings</CardTitle>
            <div className="w-4 h-4 bg-secondary rounded-full" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">1,250 STX</div>
            <div className="flex items-center gap-1 text-xs text-destructive">
              <TrendingDown className="w-3 h-3" />
              $2,687.50
            </div>
          </CardContent>
        </Card>

        <Card className="bg-card border-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">AI Confidence</CardTitle>
            <Brain className="h-4 w-4 text-secondary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">85%</div>
            <div className="text-xs text-muted-foreground">High confidence</div>
          </CardContent>
        </Card>
      </div>

      {/* AI Recommendation Card */}
      <Card className="bg-gradient-to-br from-primary/5 to-secondary/5 border-primary/20">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Brain className="w-5 h-5 text-primary" />
              <CardTitle>AI Trade Recommendation</CardTitle>
            </div>
            <Badge variant="secondary" className="bg-primary/20 text-primary border-primary/30">
              <Zap className="w-3 h-3 mr-1" />
              Live Analysis
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <h3 className="font-semibold mb-2">Diversification Opportunity</h3>
            <p className="text-muted-foreground text-pretty leading-relaxed">
              Consider swapping 10% of your STX holdings to sBTC to diversify your Bitcoin exposure while maintaining
              Stacks ecosystem participation. Current market conditions favor this rebalancing strategy.
            </p>
          </div>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="text-sm">
                <span className="text-muted-foreground">Risk Score:</span>
                <span className="ml-2 font-semibold text-primary">3.2/5</span>
              </div>
              <div className="text-sm">
                <span className="text-muted-foreground">Confidence:</span>
                <span className="ml-2 font-semibold text-secondary">85%</span>
              </div>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" size="sm" className="border-border hover:bg-card bg-transparent">
                View Details
              </Button>
              <Link href="/dashboard/trade">
                <Button size="sm" className="bg-primary hover:bg-primary/90 text-primary-foreground">
                  Execute Trade
                </Button>
              </Link>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card className="bg-card border-border hover:border-primary/50 transition-colors cursor-pointer">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 bg-primary/20 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-primary" />
              </div>
              <h3 className="font-semibold">Execute Trade</h3>
            </div>
            <p className="text-sm text-muted-foreground mb-4">
              Prepare and execute DeFi trades with AI guidance and risk assessment.
            </p>
            <Link href="/dashboard/trade">
              <Button variant="outline" size="sm" className="w-full border-border hover:bg-card bg-transparent">
                Start Trading
              </Button>
            </Link>
          </CardContent>
        </Card>

        <Card className="bg-card border-border hover:border-secondary/50 transition-colors cursor-pointer">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 bg-secondary/20 rounded-lg flex items-center justify-center">
                <Brain className="w-5 h-5 text-secondary" />
              </div>
              <h3 className="font-semibold">AI Insights</h3>
            </div>
            <p className="text-sm text-muted-foreground mb-4">
              Get detailed AI analysis of market conditions and portfolio optimization.
            </p>
            <Link href="/dashboard/insights">
              <Button variant="outline" size="sm" className="w-full border-border hover:bg-card bg-transparent">
                View Insights
              </Button>
            </Link>
          </CardContent>
        </Card>

        <Card className="bg-card border-border hover:border-primary/50 transition-colors cursor-pointer">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 bg-primary/20 rounded-lg flex items-center justify-center">
                <Coins className="w-5 h-5 text-primary" />
              </div>
              <h3 className="font-semibold">Portfolio</h3>
            </div>
            <p className="text-sm text-muted-foreground mb-4">
              Track your holdings, performance, and transaction history across wallets.
            </p>
            <Link href="/dashboard/portfolio">
              <Button variant="outline" size="sm" className="w-full border-border hover:bg-card bg-transparent">
                View Portfolio
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default function DashboardHome() {
  return (
    <WalletGuard>
      <DashboardContent />
    </WalletGuard>
  )
}
