"use client"

import { useState } from "react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { useWallet } from "@/hooks/use-wallet"
import { useToast } from "@/hooks/use-toast"
import { AlertTriangle, CheckCircle, ExternalLink, Loader2, Shield, Zap } from "lucide-react"

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

interface UnsignedTxModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  recommendation: TradeRecommendation
  onSuccess: () => void
}

export function UnsignedTxModal({ open, onOpenChange, recommendation, onSuccess }: UnsignedTxModalProps) {
  const [isExecuting, setIsExecuting] = useState(false)
  const [txId, setTxId] = useState<string | null>(null)
  const { signTransaction } = useWallet()
  const { toast } = useToast()

  const handleSignAndExecute = async () => {
    if (!recommendation.unsignedTx) return

    setIsExecuting(true)
    try {
      // Sign the transaction
      const signedTx = await signTransaction(recommendation.unsignedTx)

      // Simulate broadcasting
      await new Promise((resolve) => setTimeout(resolve, 2000))

      const mockTxId = `0x${Math.random().toString(16).substring(2, 66)}`
      setTxId(mockTxId)

      toast({
        title: "Transaction Submitted",
        description: "Your trade has been successfully submitted to the network.",
      })

      // Auto-close after success
      setTimeout(() => {
        onSuccess()
        setTxId(null)
      }, 3000)
    } catch (error) {
      console.error("Transaction failed:", error)
      toast({
        title: "Transaction Failed",
        description: "Failed to execute the trade. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsExecuting(false)
    }
  }

  const getRiskColor = (score: number) => {
    if (score <= 2) return "text-primary"
    if (score <= 3.5) return "text-secondary"
    return "text-destructive"
  }

  const getRiskLabel = (score: number) => {
    if (score <= 2) return "Low Risk"
    if (score <= 3.5) return "Medium Risk"
    return "High Risk"
  }

  if (txId) {
    return (
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent className="sm:max-w-md bg-card border-border">
          <DialogHeader className="text-center">
            <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <CheckCircle className="w-8 h-8 text-primary" />
            </div>
            <DialogTitle className="text-2xl">Transaction Submitted!</DialogTitle>
            <DialogDescription>Your trade has been successfully submitted to the Stacks network.</DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <Card className="bg-muted/50 border-border">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">Transaction ID:</span>
                  <div className="flex items-center gap-2">
                    <code className="text-xs bg-background px-2 py-1 rounded">
                      {txId.slice(0, 8)}...{txId.slice(-8)}
                    </code>
                    <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
                      <ExternalLink className="w-3 h-3" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
            <p className="text-sm text-muted-foreground text-center">
              Your transaction is being processed. You can track its progress on the Stacks Explorer.
            </p>
          </div>
        </DialogContent>
      </Dialog>
    )
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-2xl bg-card border-border">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Shield className="w-5 h-5 text-primary" />
            Review Transaction
          </DialogTitle>
          <DialogDescription>Review the AI-generated trade details before signing with your wallet.</DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {/* AI Analysis */}
          <Card className="bg-gradient-to-br from-primary/5 to-secondary/5 border-primary/20">
            <CardContent className="p-4">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <Zap className="w-4 h-4 text-primary" />
                  <span className="font-semibold">AI Analysis</span>
                </div>
                <div className="flex gap-2">
                  <Badge variant="secondary" className="bg-primary/20 text-primary border-primary/30">
                    {Math.round(recommendation.confidence * 100)}% Confidence
                  </Badge>
                  <Badge
                    variant="secondary"
                    className={`${getRiskColor(recommendation.riskScore)} border-current/30 bg-current/20`}
                  >
                    {getRiskLabel(recommendation.riskScore)}
                  </Badge>
                </div>
              </div>
              <p className="text-sm text-muted-foreground leading-relaxed">{recommendation.summary}</p>
            </CardContent>
          </Card>

          {/* Transaction Details */}
          {recommendation.unsignedTx && (
            <div className="space-y-4">
              <h3 className="font-semibold flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-secondary" />
                Transaction Details
              </h3>
              <Card className="bg-muted/50 border-border">
                <CardContent className="p-4 space-y-3">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Action:</span>
                    <span className="font-medium">{recommendation.unsignedTx.humanSummary}</span>
                  </div>
                  <Separator />
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Estimated Gas:</span>
                    <span className="font-medium">{recommendation.unsignedTx.gasEstimate}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Network Fee:</span>
                    <span className="font-medium">{recommendation.unsignedTx.fee}</span>
                  </div>
                  <Separator />
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Risk Score:</span>
                    <span className={`font-medium ${getRiskColor(recommendation.riskScore)}`}>
                      {recommendation.riskScore}/5
                    </span>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Smart Contract Info */}
          <div className="space-y-2">
            <h3 className="font-semibold text-sm">Smart Contract Interaction</h3>
            <Card className="bg-muted/50 border-border">
              <CardContent className="p-3">
                <div className="text-xs space-y-1">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Contract:</span>
                    <code className="bg-background px-1 rounded text-xs">
                      {recommendation.actions[0]?.contract.slice(0, 20)}...
                    </code>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Function:</span>
                    <code className="bg-background px-1 rounded text-xs">{recommendation.actions[0]?.function}</code>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        <DialogFooter className="flex gap-2">
          <Button variant="outline" onClick={() => onOpenChange(false)} className="border-border hover:bg-card">
            Cancel
          </Button>
          <Button
            onClick={handleSignAndExecute}
            disabled={isExecuting}
            className="bg-primary hover:bg-primary/90 text-primary-foreground"
          >
            {isExecuting ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Signing & Executing...
              </>
            ) : (
              <>
                <Shield className="w-4 h-4 mr-2" />
                Sign with Wallet
              </>
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
