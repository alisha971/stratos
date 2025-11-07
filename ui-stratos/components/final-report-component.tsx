"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "components/ui/button"
import { FileText, Share2, ExternalLink, Copy, Check } from "lucide-react"

interface FinalReportComponentProps {
  onOpenCanvas: () => void
}

export function FinalReportComponent({ onOpenCanvas }: FinalReportComponentProps) {
  const [highlightedText, setHighlightedText] = useState<string>("")
  const [showFollowUp, setShowFollowUp] = useState(false)
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null)

  const handleTextSelection = (e: React.MouseEvent) => {
    const selected = window.getSelection()?.toString()
    if (selected) {
      setHighlightedText(selected)
      setShowFollowUp(true)
    }
  }

  const handleCopy = (text: string, index: number) => {
    navigator.clipboard.writeText(text)
    setCopiedIndex(index)
    setTimeout(() => setCopiedIndex(null), 2000)
  }

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: "Research Report",
          text: "Check out this research report",
        })
      } catch (err) {
        // Ignore cancellation
      }
    }
  }

  const reportContent = (
    <div className="prose prose-invert prose-sm max-w-none" onMouseUp={handleTextSelection}>
      <div className="flex items-center gap-2 mb-4">
        <FileText className="w-5 h-5 text-accent" />
        <h3 className="text-lg font-semibold text-accent m-0">Research Report</h3>
      </div>

      <h4 className="text-accent font-semibold mt-4 mb-2">Latest Advancements in Agentic AI</h4>

      <p className="text-foreground/90 mb-3">
        The field of agentic AI has witnessed remarkable progress in 2025, with several breakthrough developments
        transforming how autonomous systems approach complex reasoning and task execution.
      </p>

      <h4 className="text-accent font-semibold mt-4 mb-2">Key Findings</h4>

      <div className="space-y-3 mb-4">
        <div className="p-3 bg-card/50 border-l-2 border-accent rounded hover:bg-card/70 transition-colors cursor-text">
          <p className="text-foreground/90 m-0">
            <strong className="text-accent">Multi-Modal Reasoning:</strong> Recent agents now integrate vision,
            language, and code understanding simultaneously, enabling richer problem decomposition and solution
            synthesis.
          </p>
        </div>

        <div className="p-3 bg-card/50 border-l-2 border-accent rounded hover:bg-card/70 transition-colors cursor-text">
          <p className="text-foreground/90 m-0">
            <strong className="text-accent">Efficient Tool Use:</strong> Improved meta-learning approaches allow agents
            to rapidly adapt to new tools without extensive fine-tuning{" "}
            <span className="text-primary cursor-pointer hover:text-accent transition-colors">[↗ 1]</span>.
          </p>
        </div>

        <div className="p-3 bg-card/50 border-l-2 border-accent rounded hover:bg-card/70 transition-colors cursor-text">
          <p className="text-foreground/90 m-0">
            <strong className="text-accent">Long-Horizon Planning:</strong> Novel architectures enable agents to
            maintain coherent goals across extended task sequences{" "}
            <span className="text-primary cursor-pointer hover:text-accent transition-colors">[↗ 2]</span>.
          </p>
        </div>
      </div>

      <h4 className="text-accent font-semibold mt-4 mb-2">Comparison of Approaches</h4>

      <div className="overflow-x-auto mb-4">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border bg-card/50">
              <th className="text-left p-2 text-accent">Method</th>
              <th className="text-left p-2 text-accent">Reasoning Type</th>
              <th className="text-left p-2 text-accent">Complexity</th>
              <th className="text-left p-2 text-accent">Speed</th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-b border-border/50 hover:bg-card/30 transition-colors">
              <td className="p-2 text-foreground/80">Chain-of-Thought</td>
              <td className="p-2 text-foreground/80">Sequential</td>
              <td className="p-2 text-foreground/80">Low</td>
              <td className="p-2 text-foreground/80">Fast</td>
            </tr>
            <tr className="border-b border-border/50 bg-card/20 hover:bg-card/40 transition-colors">
              <td className="p-2 text-foreground/80">Tree Search</td>
              <td className="p-2 text-foreground/80">Branching</td>
              <td className="p-2 text-foreground/80">Medium</td>
              <td className="p-2 text-foreground/80">Moderate</td>
            </tr>
            <tr className="border-b border-border/50 hover:bg-card/30 transition-colors">
              <td className="p-2 text-foreground/80">Multi-Agent Systems</td>
              <td className="p-2 text-foreground/80">Collaborative</td>
              <td className="p-2 text-foreground/80">High</td>
              <td className="p-2 text-foreground/80">Adaptive</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h4 className="text-accent font-semibold mt-4 mb-2">Resources</h4>
      <ul className="space-y-2 text-sm">
        <li className="text-foreground/80">
          [1]{" "}
          <button onClick={onOpenCanvas} className="text-primary hover:text-accent transition-colors underline">
            "Efficient Agent Adaptation" - Recent arXiv paper
          </button>
        </li>
        <li className="text-foreground/80">
          [2]{" "}
          <button onClick={onOpenCanvas} className="text-primary hover:text-accent transition-colors underline">
            "Long-Horizon Planning in AI Agents" - Conference Proceedings 2025
          </button>
        </li>
      </ul>
    </div>
  )

  return (
    <div className="max-w-2xl w-full">
      <div className="bg-card/40 border border-border rounded-lg p-6 relative hover:border-border/80 transition-colors">
        {reportContent}

        {showFollowUp && highlightedText && (
          <div className="absolute top-2 right-2 flex gap-2 animate-in fade-in slide-in-from-top-1 duration-200">
            <Button
              size="sm"
              variant="outline"
              className="text-xs border-accent/50 text-accent hover:bg-accent/10 bg-transparent"
              onClick={() => {
                setShowFollowUp(false)
                setHighlightedText("")
              }}
            >
              Ask follow-up
            </Button>
          </div>
        )}
      </div>

      <div className="mt-4 flex gap-2">
        <Button
          variant="outline"
          size="sm"
          className="border-border text-muted-foreground hover:text-foreground bg-transparent transition-colors"
          onClick={handleShare}
        >
          <Share2 className="w-4 h-4 mr-2" />
          Share
        </Button>
        <Button
          variant="outline"
          size="sm"
          className="border-border text-muted-foreground hover:text-foreground bg-transparent transition-colors"
          onClick={() => handleCopy(reportContent.props.children, 1)}
        >
          {copiedIndex === 1 ? (
            <>
              <Check className="w-4 h-4 mr-2" />
              Copied
            </>
          ) : (
            <>
              <Copy className="w-4 h-4 mr-2" />
              Copy
            </>
          )}
        </Button>
        <Button
          variant="outline"
          size="sm"
          className="border-border text-muted-foreground hover:text-foreground bg-transparent transition-colors"
        >
          <ExternalLink className="w-4 h-4 mr-2" />
          Export
        </Button>
      </div>
    </div>
  )
}
