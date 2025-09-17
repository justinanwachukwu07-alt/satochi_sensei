"use client"

import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { useWallet } from "@/hooks/use-wallet"
import { useAuthStore } from "lib/store"
import { Wallet, Loader2, AlertCircle } from "lucide-react"

interface ConnectWalletButtonProps {
  variant?: "default" | "outline" | "secondary"
  size?: "default" | "sm" | "lg"
  className?: string
}

export function ConnectWalletButton({ variant = "default", size = "default", className }: ConnectWalletButtonProps) {
  const { isConnecting, connect, error } = useWallet()
  const { isAuthed } = useAuthStore()

  if (isAuthed) {
    return null
  }

  return (
    <div className="space-y-3">
      <Button onClick={connect} disabled={isConnecting} variant={variant} size={size} className={className}>
        {isConnecting ? (
          <>
            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
            Connecting...
          </>
        ) : (
          <>
            <Wallet className="w-4 h-4 mr-2" />
            Connect Wallet
          </>
        )}
      </Button>

      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
    </div>
  )
}
