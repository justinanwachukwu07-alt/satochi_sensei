"use client"

import { useState, useCallback } from "react"
import { useAuthStore } from "@/components/store"
import { mockApi } from "/lib/api"

interface WalletConnection {
  address: string
  publicKey: string
  network: "mainnet" | "testnet"
}

interface UseWalletReturn {
  isConnecting: boolean
  connect: () => Promise<void>
  disconnect: () => void
  signMessage: (message: string) => Promise<string>
  signTransaction: (transaction: any) => Promise<string>
  error: string | null
}

export function useWallet(): UseWalletReturn {
  const [isConnecting, setIsConnecting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { setAddress, logout } = useAuthStore()

  const connect = useCallback(async () => {
    setIsConnecting(true)
    setError(null)

    try {
      // Check if Hiro Wallet is available
      if (typeof window !== "undefined" && (window as any).HiroWalletProvider) {
        const wallet = (window as any).HiroWalletProvider

        // Request wallet connection
        const response = await wallet.connect({
          appDetails: {
            name: "Satoshi Sensei",
            icon: "/favicon.ico",
          },
          redirectTo: "/dashboard",
          manifestPath: "/manifest.json",
          network: "testnet", // Use testnet for development
        })

        if (response.addresses?.stacks) {
          const address = response.addresses.stacks

          // Perform nonce-based authentication
          const { nonce } = await mockApi.getNonce(address)
          const signature = await signMessage(nonce)
          const authResult = await mockApi.verifySignature(address, signature, nonce)

          if (authResult.success) {
            setAddress(address)
          } else {
            throw new Error("Authentication failed")
          }
        }
      } else {
        // Mock wallet connection for development/demo
        const mockAddress = "SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7"

        // Simulate nonce authentication flow
        const { nonce } = await mockApi.getNonce(mockAddress)
        const mockSignature = `mock_signature_${Date.now()}`
        const authResult = await mockApi.verifySignature(mockAddress, mockSignature, nonce)

        if (authResult.success) {
          setAddress(mockAddress)
        }
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to connect wallet"
      setError(errorMessage)
      console.error("Wallet connection error:", err)
    } finally {
      setIsConnecting(false)
    }
  }, [setAddress])

  const disconnect = useCallback(() => {
    logout()
    setError(null)
  }, [logout])

  const signMessage = useCallback(async (message: string): Promise<string> => {
    if (typeof window !== "undefined" && (window as any).HiroWalletProvider) {
      const wallet = (window as any).HiroWalletProvider
      const result = await wallet.signMessage({
        message,
        network: "testnet",
      })
      return result.signature
    } else {
      // Mock signature for development
      return `mock_signature_${message}_${Date.now()}`
    }
  }, [])

  const signTransaction = useCallback(async (transaction: any): Promise<string> => {
    if (typeof window !== "undefined" && (window as any).HiroWalletProvider) {
      const wallet = (window as any).HiroWalletProvider
      const result = await wallet.signTransaction({
        txHex: transaction.payload,
        network: "testnet",
      })
      return result.txHex
    } else {
      // Mock signed transaction for development
      return `signed_tx_${Date.now()}`
    }
  }, [])

  return {
    isConnecting,
    connect,
    disconnect,
    signMessage,
    signTransaction,
    error,
  }
}
