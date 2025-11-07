"use client"

import { useState } from "react"
import { Button } from "components/ui/button"
import { ScrollArea } from "components/ui/scroll-area"
import { Input } from "components/ui/input"
import { Send, Loader2 } from "lucide-react"
import { StratosLogo } from "components/stratos-logo"

interface MainWorkspaceProps {
  onOpenCanvas: () => void
}

export function MainWorkspace({ onOpenCanvas }: MainWorkspaceProps) {
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSend = () => {
    if (!input.trim()) return
    setLoading(true)
    setInput("")

    // Simulate response
    setTimeout(() => setLoading(false), 2000)
  }

  return (
    <div className="flex flex-col h-full bg-background">
      {/* Main Content Area */}
      <ScrollArea className="flex-1">
        <div className="flex flex-col items-center justify-center h-full px-6 py-12">
          <div className="max-w-2xl w-full space-y-8">
            <div className="flex justify-center flex-row gap-0 mb-0 leading-7">
              <div className="w-32 h-32 flex items-center justify-center">
                <StratosLogo animated={true} className="w-32 h-32 text-accent" />
              </div>
            </div>

            {/* Header Section */}
            <div className="text-center space-y-3">
              <h2 className="font-semibold text-foreground tracking-tight text-balance leading-tight text-4xl">
                Understand, research and write about anything
              </h2>
              <p className="text-muted-foreground leading-relaxed text-sm">
                Use AI-powered tools to explore topics, analyze documents, and generate insights
              </p>
            </div>

            {/* Input Section */}
            <div className="space-y-6">
              <div className="flex gap-2">
                <Input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault()
                      handleSend()
                    }
                  }}
                  placeholder="Ask me anything..."
                  className="bg-card/50 border border-border/60 text-foreground placeholder:text-muted-foreground input-focus text-base px-4 rounded-lg transition-all mx-2 py-3"
                  disabled={loading}
                />
                <Button
                  onClick={handleSend}
                  disabled={loading || !input.trim()}
                  className="bg-primary hover:bg-primary/90 text-primary-foreground px-4 rounded-lg transition-colors"
                >
                  {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                </Button>
              </div>
            </div>
          </div>
        </div>
      </ScrollArea>
    </div>
  )
}
