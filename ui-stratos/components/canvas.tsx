"use client"

import { ScrollArea } from "components/ui/scroll-area"
import { Button } from "components/ui/button"
import { X, Maximize2, Minimize2 } from "lucide-react"
import { useState } from "react"

interface CanvasProps {
  onClose: () => void
}

export function Canvas({ onClose }: CanvasProps) {
  const [fullscreen, setFullscreen] = useState(false)

  return (
    <div className="flex flex-col h-full bg-background border-r border-border">
      {/* Canvas Header */}
      <div className="flex items-center justify-between p-4 border-b border-border bg-card/40">
        <div>
          <h3 className="font-semibold text-foreground text-sm">Source Document</h3>
          <p className="text-xs text-muted-foreground mt-1">Efficient Agent Adaptation.pdf</p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setFullscreen(!fullscreen)}
            className="text-muted-foreground hover:text-foreground h-8 w-8"
          >
            {fullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
            className="text-muted-foreground hover:text-foreground h-8 w-8"
          >
            <X className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Canvas Content */}
      <ScrollArea className="flex-1">
        <div className="p-6 space-y-6 text-sm text-foreground/80">
          <div>
            <h4 className="font-semibold text-accent mb-2">Efficient Agent Adaptation</h4>
            <p>
              Abstract: We propose a novel meta-learning framework that enables autonomous agents to rapidly adapt to
              new tools and environments with minimal fine-tuning. Our approach leverages in-context learning principles
              combined with efficient parameter updates.
            </p>
          </div>

          <div>
            <h4 className="font-semibold text-accent mb-2">1. Introduction</h4>
            <p>
              The ability to quickly adapt to new tasks and tools is fundamental to intelligent agent behavior.
              Traditional approaches require extensive retraining on new tool sets, which limits their practical
              applicability. Our method addresses this limitation by using a combination of instruction tuning and
              gradient-based meta-learning.
            </p>
          </div>

          <div>
            <h4 className="font-semibold text-accent mb-2">2. Methodology</h4>
            <p>
              We present a multi-stage approach to agent adaptation. First, agents learn general reasoning patterns
              through instruction tuning. Second, they acquire tool-specific knowledge through efficient fine-tuning
              with gradient-based methods...
            </p>
          </div>

          <div className="p-4 bg-card/50 border border-border rounded">
            <p className="text-xs text-muted-foreground mb-2">
              💡 Highlight text above to ask follow-up questions or dive deeper into specific sections
            </p>
          </div>
        </div>
      </ScrollArea>
    </div>
  )
}
