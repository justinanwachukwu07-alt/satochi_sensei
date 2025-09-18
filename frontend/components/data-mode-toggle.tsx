"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuTrigger,
  DropdownMenuSeparator,
  DropdownMenuLabel
} from "@/components/ui/dropdown-menu"
import { 
  Database, 
  Zap, 
  Settings, 
  Check,
  AlertTriangle,
  Wifi,
  WifiOff
} from "lucide-react"
import { DataService, DATA_MODE, type DataMode } from "./data-service"

interface DataModeToggleProps {
  onModeChange?: (mode: DataMode) => void
  className?: string
}

export function DataModeToggle({ onModeChange, className }: DataModeToggleProps) {
  const [currentMode, setCurrentMode] = useState<DataMode>(DATA_MODE.HYBRID)
  const [isOnline, setIsOnline] = useState(true)

  useEffect(() => {
    // Check online status
    const handleOnline = () => setIsOnline(true)
    const handleOffline = () => setIsOnline(false)
    
    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)
    
    // Initial check
    setIsOnline(navigator.onLine)
    
    return () => {
      window.removeEventListener('online', handleOnline)
      window.removeEventListener('offline', handleOffline)
    }
  }, [])

  const handleModeChange = (mode: DataMode) => {
    setCurrentMode(mode)
    dataService.setMode(mode)
    onModeChange?.(mode)
    
    // Store preference in localStorage
    localStorage.setItem('satoshi-sensei-data-mode', mode)
  }

  useEffect(() => {
    // Load saved preference
    const savedMode = localStorage.getItem('satoshi-sensei-data-mode') as DataMode
    if (savedMode && Object.values(DATA_MODE).includes(savedMode)) {
      setCurrentMode(savedMode)
      dataService.setMode(savedMode)
    }
  }, [])

  const getModeIcon = (mode: DataMode) => {
    switch (mode) {
      case DATA_MODE.MOCK:
        return <Database className="w-4 h-4" />
      case DATA_MODE.REAL_TIME:
        return <Zap className="w-4 h-4" />
      case DATA_MODE.HYBRID:
        return <Settings className="w-4 h-4" />
      default:
        return <Settings className="w-4 h-4" />
    }
  }

  const getModeLabel = (mode: DataMode) => {
    switch (mode) {
      case DATA_MODE.MOCK:
        return "Mock Data"
      case DATA_MODE.REAL_TIME:
        return "Real-time"
      case DATA_MODE.HYBRID:
        return "Hybrid"
      default:
        return "Unknown"
    }
  }

  const getModeDescription = (mode: DataMode) => {
    switch (mode) {
      case DATA_MODE.MOCK:
        return "Uses simulated data for development and testing"
      case DATA_MODE.REAL_TIME:
        return "Fetches live data from blockchain and APIs"
      case DATA_MODE.HYBRID:
        return "Uses real-time data with mock fallback"
      default:
        return ""
    }
  }

  const getModeBadgeVariant = (mode: DataMode) => {
    switch (mode) {
      case DATA_MODE.MOCK:
        return "secondary" as const
      case DATA_MODE.REAL_TIME:
        return "default" as const
      case DATA_MODE.HYBRID:
        return "outline" as const
      default:
        return "secondary" as const
    }
  }

  const getModeBadgeColor = (mode: DataMode) => {
    switch (mode) {
      case DATA_MODE.MOCK:
        return "bg-secondary/20 text-secondary border-secondary/30"
      case DATA_MODE.REAL_TIME:
        return "bg-primary/20 text-primary border-primary/30"
      case DATA_MODE.HYBRID:
        return "bg-blue-500/20 text-blue-500 border-blue-500/30"
      default:
        return "bg-secondary/20 text-secondary border-secondary/30"
    }
  }

  return (
    <div className={className}>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button 
            variant="outline" 
            size="sm" 
            className="flex items-center gap-2 border-border hover:bg-card bg-transparent"
          >
            {getModeIcon(currentMode)}
            <span className="hidden sm:inline">{getModeLabel(currentMode)}</span>
            <Badge 
              variant={getModeBadgeVariant(currentMode)}
              className={`ml-1 ${getModeBadgeColor(currentMode)}`}
            >
              {isOnline ? (
                <Wifi className="w-3 h-3" />
              ) : (
                <WifiOff className="w-3 h-3" />
              )}
            </Badge>
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" className="w-64">
          <DropdownMenuLabel className="flex items-center gap-2">
            <Settings className="w-4 h-4" />
            Data Source Mode
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
          
          {Object.values(DATA_MODE).map((mode) => (
            <DropdownMenuItem
              key={mode}
              onClick={() => handleModeChange(mode)}
              className="flex items-center justify-between p-3 cursor-pointer"
            >
              <div className="flex items-center gap-3">
                {getModeIcon(mode)}
                <div>
                  <div className="font-medium">{getModeLabel(mode)}</div>
                  <div className="text-xs text-muted-foreground">
                    {getModeDescription(mode)}
                  </div>
                </div>
              </div>
              {currentMode === mode && (
                <Check className="w-4 h-4 text-primary" />
              )}
            </DropdownMenuItem>
          ))}
          
          <DropdownMenuSeparator />
          
          <div className="px-3 py-2">
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              {isOnline ? (
                <>
                  <Wifi className="w-3 h-3 text-primary" />
                  <span>Connected to network</span>
                </>
              ) : (
                <>
                  <WifiOff className="w-3 h-3 text-destructive" />
                  <span>Offline - using cached data</span>
                </>
              )}
            </div>
            {!isOnline && currentMode === DATA_MODE.REAL_TIME && (
              <div className="flex items-center gap-2 text-xs text-destructive mt-1">
                <AlertTriangle className="w-3 h-3" />
                <span>Real-time mode unavailable offline</span>
              </div>
            )}
          </div>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  )
}
