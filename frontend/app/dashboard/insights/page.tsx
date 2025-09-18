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
import { useAuthStore } from "@/components/store"
import { dataService } from "@/components/data-service"
import { DataModeToggle } from "@/components/data-mode-toggle"

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
      // Use hybrid data service to get insights
      const response = await dataService.getInsights(address)
      setInsights(response.insights)
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
          <DataModeToggle />
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
      <Tabs defaultValue="all" className="space-y-8">
        <TabsList className="bg-muted w-full justify-start gap-1 p-1">
          <TabsTrigger value="all" className="flex-1 text-center py-3 px-4">All Insights</TabsTrigger>
          <TabsTrigger value="strategy" className="flex-1 text-center py-3 px-4">Strategy</TabsTrigger>
          <TabsTrigger value="risk" className="flex-1 text-center py-3 px-4">Risk</TabsTrigger>
          <TabsTrigger value="market" className="flex-1 text-center py-3 px-4">Market</TabsTrigger>
        </TabsList>

        <TabsContent value="all" className="space-y-6">
          {insights.map((insight) => (
            <Card key={insight.id} className="bg-card border-border">
              <CardHeader className="pb-6">
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-4">
                    <div
                      className={`w-12 h-12 bg-current/20 rounded-lg flex items-center justify-center ${getTypeColor(insight.type)}`}
                    >
                      {getTypeIcon(insight.type)}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <CardTitle className="text-xl">{insight.title}</CardTitle>
                        <Badge variant="secondary" className="capitalize bg-current/20 text-current border-current/30">
                          {insight.type}
                        </Badge>
                      </div>
                      <p className="text-muted-foreground text-pretty leading-relaxed text-lg">{insight.summary}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
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
              <CardContent className="space-y-6">
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
                  <CollapsibleContent className="space-y-6 pt-6">
                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-semibold mb-3 text-lg">AI Reasoning</h4>
                        <p className="text-muted-foreground leading-relaxed">{insight.details.reasoning}</p>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-3 text-lg">Market Conditions</h4>
                        <ul className="text-muted-foreground space-y-2">
                          {insight.details.marketConditions.map((condition, index) => (
                            <li key={index} className="flex items-start gap-3">
                              <span className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                              {condition}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-semibold mb-3 text-lg">Recommendations</h4>
                        <ul className="text-muted-foreground space-y-2">
                          {insight.details.recommendations.map((rec, index) => (
                            <li key={index} className="flex items-start gap-3">
                              <span className="w-2 h-2 bg-secondary rounded-full mt-2 flex-shrink-0" />
                              {rec}
                            </li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-3 text-lg">Risk Factors</h4>
                        <ul className="text-muted-foreground space-y-2">
                          {insight.details.risks.map((risk, index) => (
                            <li key={index} className="flex items-start gap-3">
                              <span className="w-2 h-2 bg-destructive rounded-full mt-2 flex-shrink-0" />
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

        <TabsContent value="strategy" className="space-y-6">
          {insights
            .filter((insight) => insight.type === "strategy")
            .map((insight) => (
              <Card key={insight.id} className="bg-card border-border">
                <CardHeader className="pb-6">
                  <CardTitle className="flex items-center gap-3 text-xl">
                    <Target className="w-6 h-6 text-primary" />
                    {insight.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground text-lg leading-relaxed">{insight.summary}</p>
                </CardContent>
              </Card>
            ))}
        </TabsContent>

        <TabsContent value="risk" className="space-y-6">
          {insights
            .filter((insight) => insight.type === "risk")
            .map((insight) => (
              <Card key={insight.id} className="bg-card border-border">
                <CardHeader className="pb-6">
                  <CardTitle className="flex items-center gap-3 text-xl">
                    <Shield className="w-6 h-6 text-destructive" />
                    {insight.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground text-lg leading-relaxed">{insight.summary}</p>
                </CardContent>
              </Card>
            ))}
        </TabsContent>

        <TabsContent value="market" className="space-y-6">
          {insights
            .filter((insight) => insight.type === "market")
            .map((insight) => (
              <Card key={insight.id} className="bg-card border-border">
                <CardHeader className="pb-6">
                  <CardTitle className="flex items-center gap-3 text-xl">
                    <TrendingUp className="w-6 h-6 text-secondary" />
                    {insight.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground text-lg leading-relaxed">{insight.summary}</p>
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
