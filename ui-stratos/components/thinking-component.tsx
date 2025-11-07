"use client"

import { useState, useEffect } from "react"
import { ChevronDown, ChevronUp, Zap } from "lucide-react"

interface ThinkingComponentProps {
  onOpenCanvas: () => void
}

export function ThinkingComponent({ onOpenCanvas }: ThinkingComponentProps) {
  const [expanded, setExpanded] = useState(true)
  const [showLiveThoughts, setShowLiveThoughts] = useState(true)
  const [completedSteps, setCompletedSteps] = useState(0)

  const planItems = [
    { icon: "🔎", label: "Planning 3 web searches", status: "pending" as const },
    { icon: "📄", label: "2 academic paper searches", status: "pending" as const },
    { icon: "📊", label: "Gathering and synthesizing data", status: "pending" as const },
  ]

  const liveThoughts = [
    "[Tool: tavily_search] Searching for latest agentic AI advances",
    "[Tool: scholar_search] Finding peer-reviewed papers on AI reasoning",
    "[Agent: critic] Reviewing search results... REJECTED (insufficient depth)",
    "[Tool: tavily_search] Running refined search with better parameters",
    "[Agent: synthesizer] Compiling findings into coherent narrative",
    "[Status: COMPLETE] Ready to generate final report",
  ]

  useEffect(() => {
    const interval = setInterval(() => {
      setCompletedSteps((prev) => (prev < planItems.length ? prev + 1 : prev))
    }, 800)
    return () => clearInterval(interval)
  }, [planItems.length])

  return (
    <div className="max-w-2xl w-full">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center gap-3 p-4 bg-gradient-to-r from-accent/20 to-accent/10 border border-accent/30 rounded-lg hover:from-accent/25 hover:to-accent/15 transition-all duration-200 active:scale-98"
      >
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-accent to-primary flex items-center justify-center animate-pulse">
          <Zap className="w-4 h-4 text-accent-foreground" />
        </div>
        <div className="flex-1 text-left">
          <div className="font-semibold text-foreground text-sm">Thinking</div>
          <div className="text-xs text-muted-foreground mt-1">
            {completedSteps < planItems.length
              ? `Completed ${completedSteps}/${planItems.length} steps`
              : "Agent is planning and executing research strategy..."}
          </div>
        </div>
        <div className="flex-shrink-0">
          {expanded ? (
            <ChevronUp className="w-4 h-4 text-muted-foreground" />
          ) : (
            <ChevronDown className="w-4 h-4 text-muted-foreground" />
          )}
        </div>
      </button>

      {expanded && (
        <div className="mt-3 space-y-3 p-4 bg-card/50 border border-border rounded-lg animate-in fade-in slide-in-from-top-1 duration-300">
          {/* Plan Section */}
          <div>
            <h4 className="text-xs font-semibold text-accent mb-2">Plan of Action</h4>
            <div className="space-y-2">
              {planItems.map((item, i) => (
                <div
                  key={i}
                  className={`flex items-center gap-2 text-xs transition-all duration-300 ${
                    i < completedSteps ? "text-accent opacity-100" : "text-muted-foreground opacity-60"
                  }`}
                >
                  <span className="text-lg">{item.icon}</span>
                  <span>{item.label}</span>
                  {i < completedSteps && <span className="text-green-500 ml-auto">✓</span>}
                </div>
              ))}
            </div>
          </div>

          {/* Live Thoughts */}
          <div className="border-t border-border pt-3">
            <button
              onClick={() => setShowLiveThoughts(!showLiveThoughts)}
              className="flex items-center gap-2 text-xs font-semibold text-accent hover:text-primary transition-colors mb-2"
            >
              <span>Live Execution Log</span>
              {showLiveThoughts ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
            </button>

            {showLiveThoughts && (
              <div className="space-y-1 font-mono text-xs text-muted-foreground bg-background/50 p-3 rounded border border-border/50 max-h-40 overflow-y-auto">
                {liveThoughts.map((thought, i) => (
                  <div
                    key={i}
                    className="text-foreground/70 animate-in fade-in slide-in-from-left-1 duration-300"
                    style={{ animationDelay: `${i * 100}ms` }}
                  >
                    {"> "} {thought}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
