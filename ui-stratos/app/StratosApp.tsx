"use client";

import { useState } from "react"
import { Sidebar } from "components/sidebar"
import { MainWorkspace } from "components/main-workspace"
import { Canvas } from "components/canvas"

export default function StratosApp() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [canvasOpen, setCanvasOpen] = useState(false)

  return (
    <div className="flex h-screen bg-background text-foreground overflow-hidden">
      <div
        className={`transition-all duration-300 ${
          sidebarOpen ? "w-64" : "w-0"
        } border-r border-border bg-sidebar overflow-hidden`}
      >
        <Sidebar onCollapse={() => setSidebarOpen(false)} />
      </div>

      <div className="flex-1 flex overflow-hidden">
        {canvasOpen && (
          <div className="w-1/2 border-r border-border overflow-hidden">
            <Canvas onClose={() => setCanvasOpen(false)} />
          </div>
        )}

        <div className={`${canvasOpen ? "w-1/2" : "w-full"} flex flex-col overflow-hidden`}>
          {/* Header section with logo, Stratos text, and tagline */}
          {/* Removed as per updates */}
          <MainWorkspace onOpenCanvas={() => setCanvasOpen(true)} />
        </div>
      </div>
    </div>
  )
}
