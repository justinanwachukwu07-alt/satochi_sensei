"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { WalletGuard } from "@/components/wallet-guard"
import {
  Brain,
  TrendingUp,
  AlertTriangle,
  RefreshCw,
  ChevronDown,
  ChevronUp,
  Download,
  Eye,
  Zap,
  Target,
  Shield,
  Clock,
} from "lucide-react"
import { useAuthStore } from "/lib"

interface AIInsight {
  id: string
  type: "strategy" | "risk" | "market" | "portfolio"
  title: string
  summary: string
  confidence: number
  riskScore: number
  timestamp: Date
  details: {
    reasoning: string
    marketConditions: string[]
    recommendations: string[]
    risks: string[]
  }
  rawResponse?: {
    prompt: string
    model: string
    response: string
    auditId: string
  }
}

function InsightsContent() {
  const { address } = useAuthStore()
  const [insights, setInsights] = useState<AIInsight[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [lastRefresh, setLastRefresh] = useState<Date | null>(null)
  const [expandedInsight, setExpandedInsight] = useState<string | null>(null)

  const generateInsights = async () => {
    if (!address) return

    setIsLoading(true)
    try {
      // Simulate AI insight generation
      await new Promise((resolve) => setTimeout(resolve, 3000))

      const mockInsights: AIInsight[] = [
        {
          id: `insight_${Date.now()}_1`,
          type: "strategy",
          title: "Diversification Opportunity Detected",
          summary:
            "Your portfolio shows high STX concentration. Consider rebalancing 15% into sBTC for better risk distribution.",
          confidence: 0.87,
          riskScore: 2.3,
          timestamp: new Date(),
          details: {
            reasoning:
              "Analysis of your current holdings reveals 78% allocation in STX tokens, creating concentration risk. Market correlation data suggests sBTC provides effective diversification while maintaining Stacks ecosystem exposure.",
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
            prompt:
              "Analyze portfolio allocation for address SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7 and provide diversification recommendations",
            model: "grok-beta",
            response:
              '{"analysis": "High STX concentration detected", "recommendation": "Diversify into sBTC", "confidence": 0.87}',
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
          timestamp: new Date(Date.now() - 1000 * 60 * 30), // 30 minutes ago
          details: {
            reasoning:
              "Deep liquidity pools and low volatility create ideal conditions for large swaps. Historical analysis shows similar conditions preceded 3-5 day periods of stable pricing.",
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
        {
          id: `insight_${Date.now()}_3`,
          type: "risk",
          title: "Smart Contract Risk Assessment",
          summary: "Recent audit completed on primary AMM contracts. Security score improved to 9.2/10.",
          confidence: 0.95,
          riskScore: 1.2,
          timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2), // 2 hours ago
          details: {
            reasoning:
              "Third-party security audit by Trail of Bits completed with no critical vulnerabilities found. Minor optimizations implemented, reducing gas costs by 8%.",
            marketConditions: [
              "Audit report published and verified",
              "No exploits detected in 90 days",
              "Bug bounty program active with $100K rewards",
            ],
            recommendations: [
              "Safe to increase position sizes",
              "Consider this for larger trades",
              "Monitor ongoing security metrics",
            ],
            risks: ["New vulnerabilities may be discovered", "Audit scope limitations", "Implementation risks"],
          },
        },
      ]

      setInsights(mockInsights)
      setLastRefresh(new Date())
    } catch (error) {
      console.error("Failed to generate insights:", error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    generateInsights()
  }, [address])

  const getTypeIcon = (type: string) => {
    switch (type) {
      case "strategy":
        return <Target className="w-4 h-4" />
      case "risk":
        return <Shield className="w-4 h-4" />
      case "market":
        return <TrendingUp className="w-4 h-4" />
      case "portfolio":
        return <Brain className="w-4 h-4" />
      default:
        return <Brain className="w-4 h-4" />
    }
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case "strategy":
        return "text-primary"
      case "risk":
        return "text-destructive"
      case "market":
        return "text-secondary"
      case "portfolio":
        return "text-primary"
      default:
        return "text-muted-foreground"
    }
  }

  const getRiskColor = (score: number) => {
    if (score <= 2) return "text-primary"
    if (score <= 3.5) return "text-secondary"
    return "text-destructive"
  }

  const downloadInsight = (insight: AIInsight) => {
    const data = {
      insight: insight,
      exportedAt: new Date().toISOString(),
      walletAddress: address,
    }
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `satoshi-sensei-insight-${insight.id}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-balance">AI Insights</h1>
          <p className="text-muted-foreground text-pretty">
            Get personalized AI analysis of your portfolio and market conditions
          </p>
        </div>
        <div className="flex items-center gap-3">
          {lastRefresh && (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Clock className="w-4 h-4" />
              Last updated: {lastRefresh.toLocaleTimeString()}
            </div>
          )}
          <Button onClick={generateInsights} disabled={isLoading} className="bg-primary hover:bg-primary/90">
            {isLoading ? (
              <>
                <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Brain className="w-4 h-4 mr-2" />
                Refresh Insights
              </>
            )}
          </Button>
        </div>
      </div>

      {/* Insights Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="bg-card border-border">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 bg-primary/20 rounded-lg flex items-center justify-center">
                <Brain className="w-5 h-5 text-primary" />
              </div>
              <div>
                <div className="text-2xl font-bold">{insights.length}</div>
                <div className="text-sm text-muted-foreground">Active Insights</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-card border-border">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 bg-secondary/20 rounded-lg flex items-center justify-center">
                <Zap className="w-5 h-5 text-secondary" />
              </div>
              <div>
                <div className="text-2xl font-bold">
                  {insights.length > 0
                    ? Math.round((insights.reduce((acc, i) => acc + i.confidence, 0) / insights.length) * 100)
                    : 0}
                  %
                </div>
                <div className="text-sm text-muted-foreground">Avg Confidence</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-card border-border">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 bg-primary/20 rounded-lg flex items-center justify-center">
                <AlertTriangle className="w-5 h-5 text-primary" />
              </div>
              <div>
                <div className="text-2xl font-bold">
                  {insights.length > 0
                    ? (insights.reduce((acc, i) => acc + i.riskScore, 0) / insights.length).toFixed(1)
                    : "0.0"}
                </div>
                <div className="text-sm text-muted-foreground">Avg Risk Score</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Insights List */}
      <Tabs defaultValue="all" className="space-y-6">
        <TabsList className="bg-muted">
          <TabsTrigger value="all">All Insights</TabsTrigger>
          <TabsTrigger value="strategy">Strategy</TabsTrigger>
          <TabsTrigger value="risk">Risk</TabsTrigger>
          <TabsTrigger value="market">Market</TabsTrigger>
        </TabsList>

        <TabsContent value="all" className="space-y-4">
          {insights.map((insight) => (
            <Card key={insight.id} className="bg-card border-border">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3">
                    <div
                      className={`w-10 h-10 bg-current/20 rounded-lg flex items-center justify-center ${getTypeColor(insight.type)}`}
                    >
                      {getTypeIcon(insight.type)}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <CardTitle className="text-lg">{insight.title}</CardTitle>
                        <Badge variant="secondary" className="capitalize bg-current/20 text-current border-current/30">
                          {insight.type}
                        </Badge>
                      </div>
                      <p className="text-muted-foreground text-pretty leading-relaxed">{insight.summary}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant="secondary" className="bg-primary/20 text-primary border-primary/30">
                      {Math.round(insight.confidence * 100)}% confidence
                    </Badge>
                    <Badge
                      variant="secondary"
                      className={`${getRiskColor(insight.riskScore)} border-current/30 bg-current/20`}
                    >
                      Risk: {insight.riskScore}/5
                    </Badge>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <Collapsible
                  open={expandedInsight === insight.id}
                  onOpenChange={(open) => setExpandedInsight(open ? insight.id : null)}
                >
                  <div className="flex items-center justify-between">
                    <CollapsibleTrigger asChild>
                      <Button variant="ghost" size="sm" className="flex items-center gap-2">
                        <Eye className="w-4 h-4" />
                        View Details
                        {expandedInsight === insight.id ? (
                          <ChevronUp className="w-4 h-4" />
                        ) : (
                          <ChevronDown className="w-4 h-4" />
                        )}
                      </Button>
                    </CollapsibleTrigger>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => downloadInsight(insight)}
                      className="flex items-center gap-2"
                    >
                      <Download className="w-4 h-4" />
                      Export
                    </Button>
                  </div>
                  <CollapsibleContent className="space-y-4 pt-4">
                    <div className="grid md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="font-semibold mb-2">AI Reasoning</h4>
                        <p className="text-sm text-muted-foreground leading-relaxed">{insight.details.reasoning}</p>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Market Conditions</h4>
                        <ul className="text-sm text-muted-foreground space-y-1">
                          {insight.details.marketConditions.map((condition, index) => (
                            <li key={index} className="flex items-start gap-2">
                              <span className="w-1 h-1 bg-primary rounded-full mt-2 flex-shrink-0" />
                              {condition}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                    <div className="grid md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="font-semibold mb-2">Recommendations</h4>
                        <ul className="text-sm text-muted-foreground space-y-1">
                          {insight.details.recommendations.map((rec, index) => (
                            <li key={index} className="flex items-start gap-2">
                              <span className="w-1 h-1 bg-secondary rounded-full mt-2 flex-shrink-0" />
                              {rec}
                            </li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Risk Factors</h4>
                        <ul className="text-sm text-muted-foreground space-y-1">
                          {insight.details.risks.map((risk, index) => (
                            <li key={index} className="flex items-start gap-2">
                              <span className="w-1 h-1 bg-destructive rounded-full mt-2 flex-shrink-0" />
                              {risk}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                    {insight.rawResponse && (
                      <div className="border-t border-border pt-4">
                        <h4 className="font-semibold mb-2">Raw AI Response</h4>
                        <div className="bg-muted/50 rounded-lg p-3 space-y-2">
                          <div className="text-xs">
                            <span className="text-muted-foreground">Model:</span> {insight.rawResponse.model}
                          </div>
                          <div className="text-xs">
                            <span className="text-muted-foreground">Audit ID:</span> {insight.rawResponse.auditId}
                          </div>
                          <div className="text-xs">
                            <span className="text-muted-foreground">Prompt:</span>
                            <pre className="mt-1 text-xs bg-background p-2 rounded overflow-x-auto">
                              {insight.rawResponse.prompt}
                            </pre>
                          </div>
                          <div className="text-xs">
                            <span className="text-muted-foreground">Response:</span>
                            <pre className="mt-1 text-xs bg-background p-2 rounded overflow-x-auto">
                              {insight.rawResponse.response}
                            </pre>
                          </div>
                        </div>
                      </div>
                    )}
                  </CollapsibleContent>
                </Collapsible>
              </CardContent>
            </Card>
          ))}
        </TabsContent>

        <TabsContent value="strategy" className="space-y-4">
          {insights
            .filter((insight) => insight.type === "strategy")
            .map((insight) => (
              <Card key={insight.id} className="bg-card border-border">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Target className="w-5 h-5 text-primary" />
                    {insight.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">{insight.summary}</p>
                </CardContent>
              </Card>
            ))}
        </TabsContent>

        <TabsContent value="risk" className="space-y-4">
          {insights
            .filter((insight) => insight.type === "risk")
            .map((insight) => (
              <Card key={insight.id} className="bg-card border-border">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Shield className="w-5 h-5 text-destructive" />
                    {insight.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">{insight.summary}</p>
                </CardContent>
              </Card>
            ))}
        </TabsContent>

        <TabsContent value="market" className="space-y-4">
          {insights
            .filter((insight) => insight.type === "market")
            .map((insight) => (
              <Card key={insight.id} className="bg-card border-border">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-secondary" />
                    {insight.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">{insight.summary}</p>
                </CardContent>
              </Card>
            ))}
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default function InsightsPage() {
  return (
    <WalletGuard>
      <InsightsContent />
    </WalletGuard>
  )
}
