"use client"

import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ConnectWalletButton } from "@/components/connect-wallet-button"
import { useAuthStore, useUIStore } from "@/lib/store"
import { Wallet, Home, Menu, ArrowLeft } from "lucide-react"
import Link from "next/link"
import { usePathname } from "next/navigation"

export function DashboardHeader() {
  const { address, isAuthed, logout } = useAuthStore()
  const { toggleSidebar } = useUIStore()
  const pathname = usePathname()

  const getBreadcrumb = () => {
    if (pathname === "/dashboard") return "Home"
    if (pathname === "/dashboard/trade") return "Trade"
    if (pathname === "/dashboard/insights") return "AI Insights"
    if (pathname === "/dashboard/portfolio") return "Portfolio"
    if (pathname === "/dashboard/settings") return "Settings"
    return "Dashboard"
  }

  return (
    <header className="border-b border-border bg-card/50 backdrop-blur-sm">
      <div className="flex items-center justify-between px-4 py-3">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" onClick={toggleSidebar} className="md:hidden">
            <Menu className="w-4 h-4" />
          </Button>
          <div className="flex items-center gap-2">
            <Link
              href="/"
              className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              <span className="text-sm">Back to Home</span>
            </Link>
            <span className="text-muted-foreground">/</span>
            <Link
              href="/dashboard"
              className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors"
            >
              <Home className="w-4 h-4" />
              <span className="text-sm">Dashboard</span>
            </Link>
            {pathname !== "/dashboard" && (
              <>
                <span className="text-muted-foreground">/</span>
                <span className="text-sm font-medium">{getBreadcrumb()}</span>
              </>
            )}
          </div>
        </div>

        <div className="flex items-center gap-3">
          {isAuthed ? (
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="bg-primary/20 text-primary border-primary/30">
                <Wallet className="w-3 h-3 mr-1" />
                {address ? `${address.slice(0, 6)}...${address.slice(-4)}` : "Connected"}
              </Badge>
              <Button
                variant="outline"
                size="sm"
                onClick={logout}
                className="border-border hover:bg-card bg-transparent"
              >
                Disconnect
              </Button>
            </div>
          ) : (
            <ConnectWalletButton size="sm" className="bg-primary hover:bg-primary/90 text-primary-foreground" />
          )}
        </div>
      </div>
    </header>
  )
}
