"use client"

import type React from "react"

import { useAuthStore } from "../app/lib/store"
import { ConnectWalletButton } from "@/components/connect-wallet-button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Wallet, Shield, Zap } from "lucide-react"

interface WalletGuardProps {
  children: React.ReactNode
}

export function WalletGuard({ children }: WalletGuardProps) {
  const { isAuthed } = useAuthStore()

  if (!isAuthed) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center p-6">
        <Card className="w-full max-w-md bg-card border-border">
          <CardHeader className="text-center">
            <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <Wallet className="w-8 h-8 text-primary" />
            </div>
            <CardTitle className="text-2xl">Connect Your Wallet</CardTitle>
            <p className="text-muted-foreground text-pretty">
              Connect your Stacks wallet to access AI-powered DeFi trading features
            </p>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-secondary/20 rounded-lg flex items-center justify-center">
                  <Shield className="w-4 h-4 text-secondary" />
                </div>
                <div>
                  <p className="text-sm font-medium">Secure & Non-Custodial</p>
                  <p className="text-xs text-muted-foreground">Your keys never leave your wallet</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-primary/20 rounded-lg flex items-center justify-center">
                  <Zap className="w-4 h-4 text-primary" />
                </div>
                <div>
                  <p className="text-sm font-medium">Instant Access</p>
                  <p className="text-xs text-muted-foreground">Start trading with AI insights immediately</p>
                </div>
              </div>
            </div>

            <ConnectWalletButton size="lg" className="w-full bg-primary hover:bg-primary/90 text-primary-foreground" />

            <p className="text-xs text-muted-foreground text-center">
              Supports Hiro Wallet, Xverse, and other Stacks-compatible wallets
            </p>
          </CardContent>
        </Card>
      </div>
    )
  }

  return <>{children}</>
}
