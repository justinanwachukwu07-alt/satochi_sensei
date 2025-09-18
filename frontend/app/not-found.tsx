"use client"

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useRouter } from "next/navigation"
import { useAuthStore } from "@/components/store"
import { Home, ArrowLeft, Brain } from "lucide-react"
import Link from "next/link"

export default function NotFound() {
  const [countdown, setCountdown] = useState(5)
  const router = useRouter()
  const { isAuthed } = useAuthStore()

  useEffect(() => {
    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(timer)
          router.push(isAuthed ? "/dashboard" : "/")
          return 0
        }
        return prev - 1
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [router, isAuthed])

  const redirectPath = isAuthed ? "/dashboard" : "/"
  const redirectLabel = isAuthed ? "Dashboard" : "Home"

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-6">
      <Card className="w-full max-w-md bg-card border-border text-center">
        <CardHeader>
          <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-4">
            <Brain className="w-8 h-8 text-primary" />
          </div>
          <CardTitle className="text-2xl">Page Not Found</CardTitle>
          <p className="text-muted-foreground text-pretty">
            The page you're looking for doesn't exist or has been moved.
          </p>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="p-4 bg-muted/50 rounded-lg">
            <p className="text-sm text-muted-foreground mb-2">Redirecting to {redirectLabel} in:</p>
            <div className="text-3xl font-bold text-primary">{countdown}</div>
          </div>

          <div className="flex flex-col sm:flex-row gap-3">
            <Link href={redirectPath} className="flex-1">
              <Button className="w-full bg-primary hover:bg-primary/90 text-primary-foreground">
                <Home className="w-4 h-4 mr-2" />
                Go to {redirectLabel}
              </Button>
            </Link>
            <Button variant="outline" onClick={() => router.back()} className="border-border hover:bg-card">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Go Back
            </Button>
          </div>

          <p className="text-xs text-muted-foreground">
            If you believe this is an error, please contact our support team.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
