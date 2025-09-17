import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ArrowRight, Brain, Shield, Zap, TrendingUp, Users, Award, Play, Star, CheckCircle } from "lucide-react"
import Link from "next/link"
import Image from "next/image"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <Brain className="w-5 h-5 text-primary-foreground" />
            </div>
            <span className="text-xl font-bold text-foreground">Satoshi Sensei</span>
          </div>
          <nav className="hidden md:flex items-center gap-6">
            <Link href="#features" className="text-muted-foreground hover:text-foreground transition-colors">
              Features
            </Link>
            <Link href="#how-it-works" className="text-muted-foreground hover:text-foreground transition-colors">
              How It Works
            </Link>
            <Link href="#security" className="text-muted-foreground hover:text-foreground transition-colors">
              Security
            </Link>
          </nav>
          <Link href="/dashboard">
            <Button className="bg-primary hover:bg-primary/90 text-primary-foreground">
              Launch App
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative py-20 lg:py-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-secondary/5" />
        <div className="container mx-auto px-4 relative">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Column - Text Content */}
            <div className="text-center lg:text-left">
              <Badge variant="secondary" className="mb-6 bg-secondary/20 text-secondary-foreground border-secondary/30">
                <Star className="w-3 h-3 mr-1" />
                AI-Powered DeFi Trading
              </Badge>
              <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-balance mb-6">
                Your AI Copilot for <span className="text-primary">Bitcoin</span> &{" "}
                <span className="text-secondary">Stacks</span> DeFi
              </h1>
              <p className="text-xl text-muted-foreground text-pretty mb-8 max-w-2xl leading-relaxed">
                Satoshi Sensei analyzes your portfolio, identifies opportunities, and guides you through secure DeFi
                trades with AI-powered insights and risk assessment.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                <Link href="/dashboard">
                  <Button size="lg" className="bg-primary hover:bg-primary/90 text-primary-foreground px-8">
                    Connect Wallet & Start Trading
                    <ArrowRight className="w-5 h-5 ml-2" />
                  </Button>
                </Link>
                <Button size="lg" variant="outline" className="border-border hover:bg-card bg-transparent">
                  <Play className="w-4 h-4 mr-2" />
                  Watch Demo
                </Button>
              </div>
              
              {/* Trust Indicators */}
              <div className="mt-12 flex flex-wrap items-center justify-center lg:justify-start gap-6 text-sm text-muted-foreground">
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>Non-Custodial</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>AI-Powered</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>Testnet Live</span>
                </div>
              </div>
            </div>

            {/* Right Column - Hero Image */}
            <div className="relative">
              <div className="relative w-full h-[500px] lg:h-[600px] rounded-2xl overflow-hidden bg-gradient-to-br from-primary/20 to-secondary/20 border border-border/50 shadow-2xl">
                {/* Background with multiple layers */}
                <div className="absolute inset-0 bg-gradient-to-br from-primary/30 via-secondary/20 to-primary/30"></div>
                
                {/* Hero Image */}
                <div className="absolute inset-0 flex items-center justify-center">
                  <img
                    src="/hero-dashboard.svg"
                    alt="Satoshi Sensei AI DeFi Dashboard"
                    className="max-w-full max-h-full object-contain opacity-80"
                  />
                </div>
                
                {/* Fallback Visual Elements */}
                <div className="absolute inset-0 flex items-center justify-center">
                  {/* Dashboard Mockup Elements */}
                  <div className="w-4/5 h-4/5 bg-card/20 backdrop-blur-sm rounded-xl border border-border/30 p-6">
                    {/* Header */}
                    <div className="flex items-center gap-3 mb-6">
                      <div className="w-8 h-8 bg-primary/30 rounded-lg flex items-center justify-center">
                        <Brain className="w-5 h-5 text-primary" />
                      </div>
                      <div>
                        <h3 className="text-lg font-bold text-foreground">AI Dashboard</h3>
                        <p className="text-sm text-muted-foreground">Live Trading Interface</p>
                      </div>
                      <div className="ml-auto flex items-center gap-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                        <span className="text-xs text-green-500">Live</span>
                      </div>
                    </div>
                    
                    {/* Portfolio Cards */}
                    <div className="grid grid-cols-2 gap-4 mb-6">
                      <div className="bg-card/40 rounded-lg p-4 border border-border/20">
                        <div className="flex items-center gap-2 mb-2">
                          <div className="w-6 h-6 bg-orange-500/30 rounded-full flex items-center justify-center">
                            <span className="text-xs font-bold text-orange-500">₿</span>
                          </div>
                          <span className="text-sm font-semibold">Bitcoin</span>
                        </div>
                        <div className="text-lg font-bold text-green-500">+12.5%</div>
                        <div className="text-xs text-muted-foreground">0.025 BTC</div>
                      </div>
                      
                      <div className="bg-card/40 rounded-lg p-4 border border-border/20">
                        <div className="flex items-center gap-2 mb-2">
                          <div className="w-6 h-6 bg-blue-500/30 rounded-full flex items-center justify-center">
                            <span className="text-xs font-bold text-blue-500">S</span>
                          </div>
                          <span className="text-sm font-semibold">Stacks</span>
                        </div>
                        <div className="text-lg font-bold text-green-500">+8.3%</div>
                        <div className="text-xs text-muted-foreground">1,250 STX</div>
                      </div>
                    </div>
                    
                    {/* AI Recommendations */}
                    <div className="space-y-3">
                      <div className="bg-card/40 rounded-lg p-3 border border-green-500/30">
                        <div className="flex items-center gap-2 mb-1">
                          <div className="w-4 h-4 bg-green-500/30 rounded-full flex items-center justify-center">
                            <Brain className="w-2.5 h-2.5 text-green-500" />
                          </div>
                          <span className="text-sm font-semibold">AI Recommendation</span>
                        </div>
                        <div className="text-xs text-muted-foreground">Liquidity Provision - 15.2% APY</div>
                      </div>
                      
                      <div className="bg-card/40 rounded-lg p-3 border border-yellow-500/30">
                        <div className="flex items-center gap-2 mb-1">
                          <div className="w-4 h-4 bg-yellow-500/30 rounded-full flex items-center justify-center">
                            <TrendingUp className="w-2.5 h-2.5 text-yellow-500" />
                          </div>
                          <span className="text-sm font-semibold">Yield Farming</span>
                        </div>
                        <div className="text-xs text-muted-foreground">Arkadiko Protocol - 22.8% APY</div>
                      </div>
                    </div>
                  </div>
                </div>
                
                {/* Overlay gradient */}
                <div className="absolute inset-0 bg-gradient-to-t from-background/90 via-background/10 to-transparent" />
                
                {/* Overlay Information Cards */}
                <div className="absolute top-6 right-6">
                  <div className="bg-card/95 backdrop-blur-sm rounded-lg p-3 border border-border/50 shadow-lg">
                    <div className="flex items-center gap-2 mb-1">
                      <div className="w-6 h-6 bg-primary/20 rounded-full flex items-center justify-center">
                        <Brain className="w-3 h-3 text-primary" />
                      </div>
                      <span className="text-xs font-semibold">AI Active</span>
                    </div>
                    <div className="flex items-center gap-1 text-xs">
                      <div className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse" />
                      <span className="text-muted-foreground">Analyzing markets</span>
                    </div>
                  </div>
                </div>
                
                <div className="absolute bottom-6 left-6 right-6">
                  <div className="bg-card/95 backdrop-blur-sm rounded-lg p-4 border border-border/50 shadow-lg">
                    <div className="flex items-center gap-3 mb-2">
                      <div className="w-8 h-8 bg-primary/20 rounded-lg flex items-center justify-center">
                        <Brain className="w-4 h-4 text-primary" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-sm">AI Strategy Analysis</h3>
                        <p className="text-xs text-muted-foreground">Real-time market insights</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 text-xs">
                      <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                      <span className="text-muted-foreground">Live on Stacks Testnet</span>
                    </div>
                  </div>
                </div>
                
                {/* Additional floating info */}
                <div className="absolute top-1/2 left-6">
                  <div className="bg-card/90 backdrop-blur-sm rounded-lg p-3 border border-border/50 shadow-lg">
                    <div className="flex items-center gap-2">
                      <div className="w-4 h-4 bg-secondary/20 rounded-full flex items-center justify-center">
                        <TrendingUp className="w-2.5 h-2.5 text-secondary" />
                      </div>
                      <span className="text-xs font-medium">Portfolio +12.5%</span>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Enhanced Floating Elements */}
              <div className="absolute -top-4 -right-4 w-20 h-20 bg-primary/20 rounded-full blur-xl animate-pulse" />
              <div className="absolute -bottom-4 -left-4 w-32 h-32 bg-secondary/20 rounded-full blur-xl animate-pulse" />
              <div className="absolute top-1/3 -right-2 w-16 h-16 bg-accent/20 rounded-full blur-lg animate-pulse" />
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-card/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Intelligent DeFi Trading Made Simple</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Advanced AI analysis meets user-friendly design for the ultimate DeFi trading experience
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="bg-card border-border hover:border-primary/50 transition-colors">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center mb-4">
                  <Brain className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-3">AI Strategy Analysis</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Get personalized trading strategies based on your portfolio, market conditions, and risk tolerance
                  with real-time AI analysis.
                </p>
              </CardContent>
            </Card>
            <Card className="bg-card border-border hover:border-secondary/50 transition-colors">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-secondary/20 rounded-lg flex items-center justify-center mb-4">
                  <Shield className="w-6 h-6 text-secondary" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Secure Execution</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Your private keys never leave your wallet. All transactions are prepared, reviewed, and signed locally
                  for maximum security.
                </p>
              </CardContent>
            </Card>
            <Card className="bg-card border-border hover:border-primary/50 transition-colors">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center mb-4">
                  <Zap className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Lightning Fast</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Execute trades in seconds with optimized smart contract interactions and real-time market data
                  integration.
                </p>
              </CardContent>
            </Card>
            <Card className="bg-card border-border hover:border-secondary/50 transition-colors">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-secondary/20 rounded-lg flex items-center justify-center mb-4">
                  <TrendingUp className="w-6 h-6 text-secondary" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Risk Assessment</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Every recommendation comes with detailed risk scoring and impact analysis to help you make informed
                  decisions.
                </p>
              </CardContent>
            </Card>
            <Card className="bg-card border-border hover:border-primary/50 transition-colors">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center mb-4">
                  <Users className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Multi-Wallet Support</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Connect with Hiro Wallet, Xverse, and other popular Bitcoin and Stacks wallets seamlessly.
                </p>
              </CardContent>
            </Card>
            <Card className="bg-card border-border hover:border-secondary/50 transition-colors">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-secondary/20 rounded-lg flex items-center justify-center mb-4">
                  <Award className="w-6 h-6 text-secondary" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Educational Insights</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Learn as you trade with detailed explanations of strategies, market dynamics, and DeFi protocols.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">How Satoshi Sensei Works</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Three simple steps to smarter DeFi trading
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-primary">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-3">Connect Your Wallet</h3>
              <p className="text-muted-foreground">
                Securely connect your Bitcoin or Stacks wallet to analyze your current portfolio and holdings.
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-secondary/20 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-secondary">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-3">Get AI Recommendations</h3>
              <p className="text-muted-foreground">
                Our AI analyzes market conditions and suggests optimal trading strategies tailored to your goals.
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-primary">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-3">Execute Safely</h3>
              <p className="text-muted-foreground">
                Review, approve, and execute trades directly from your wallet with full transparency and control.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Security Section */}
      <section id="security" className="py-20 bg-card/30">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">Security First</h2>
            <p className="text-xl text-muted-foreground mb-12">
              Your funds and data are protected by industry-leading security practices
            </p>
            <div className="grid md:grid-cols-2 gap-8 text-left">
              <div className="flex gap-4">
                <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Shield className="w-6 h-6 text-primary" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold mb-2">Non-Custodial</h3>
                  <p className="text-muted-foreground">
                    Your private keys remain in your wallet. We never have access to your funds or sensitive
                    information.
                  </p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="w-12 h-12 bg-secondary/20 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Brain className="w-6 h-6 text-secondary" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold mb-2">Transparent AI</h3>
                  <p className="text-muted-foreground">
                    All AI recommendations include detailed reasoning and risk assessments for full transparency.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Live Contracts Section */}
      <section className="py-20 bg-card/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Live on Stacks Testnet</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Our smart contracts are deployed and ready for testing
            </p>
          </div>
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <Card className="bg-card border-border hover:border-primary/50 transition-colors">
              <CardContent className="p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-primary/20 rounded-lg flex items-center justify-center">
                    <Brain className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold">Satoshi Sensei Core</h3>
                    <p className="text-sm text-muted-foreground">Strategy Management</p>
                  </div>
                </div>
                <div className="bg-muted/50 rounded-lg p-3 mb-4">
                  <code className="text-xs text-muted-foreground break-all">
                    STWWKZA3X98YT263TP28280FP25TYP2TMHC5F7G2.satoshi-sensei-core
                  </code>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                  <span className="text-muted-foreground">Deployed & Active</span>
                </div>
              </CardContent>
            </Card>
            
            <Card className="bg-card border-border hover:border-secondary/50 transition-colors">
              <CardContent className="p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-secondary/20 rounded-lg flex items-center justify-center">
                    <Zap className="w-5 h-5 text-secondary" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold">DeFi Strategy Executor</h3>
                    <p className="text-sm text-muted-foreground">Trade Execution</p>
                  </div>
                </div>
                <div className="bg-muted/50 rounded-lg p-3 mb-4">
                  <code className="text-xs text-muted-foreground break-all">
                    STWWKZA3X98YT263TP28280FP25TYP2TMHC5F7G2.defi-strategy-executor
                  </code>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                  <span className="text-muted-foreground">Deployed & Active</span>
                </div>
              </CardContent>
            </Card>
          </div>
          
          <div className="text-center mt-8">
            <Link 
              href="https://explorer.stacks.co/?chain=testnet" 
              target="_blank" 
              rel="noopener noreferrer"
            >
              <Button variant="outline" className="border-border hover:bg-card bg-transparent">
                View on Stacks Explorer
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto text-center">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">Ready to Start Trading Smarter?</h2>
            <p className="text-xl text-muted-foreground mb-8">
              Join the future of DeFi trading with AI-powered insights and secure execution.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/dashboard">
                <Button size="lg" className="bg-primary hover:bg-primary/90 text-primary-foreground px-8">
                  Launch Satoshi Sensei
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </Link>
              <Link 
                href="https://explorer.stacks.co/?chain=testnet" 
                target="_blank" 
                rel="noopener noreferrer"
              >
                <Button size="lg" variant="outline" className="border-border hover:bg-card bg-transparent">
                  View Contracts
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border bg-card/50">
        <div className="container mx-auto px-4 py-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-primary rounded flex items-center justify-center">
                <Brain className="w-4 h-4 text-primary-foreground" />
              </div>
              <span className="font-semibold">Satoshi Sensei</span>
            </div>
            <p className="text-sm text-muted-foreground">
              © 2024 Satoshi Sensei. Built for the Bitcoin and Stacks ecosystem.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
