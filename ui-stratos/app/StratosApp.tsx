"use client";

import { useState } from "react";
import { Sidebar } from "components/sidebar";
import { MainWorkspace } from "components/main-workspace";
import { Canvas } from "components/canvas";

export default function StratosApp() {
  // renamed to "sidebarCollapsed" for clarity
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [canvasOpen, setCanvasOpen] = useState(false);

  return (
    <div className="flex h-screen bg-background text-foreground overflow-hidden">
      {/* Sidebar section */}
      <div
        className={`transition-all duration-300 border-r border-border bg-sidebar ${
          sidebarCollapsed ? "w-16" : "w-64"
        } overflow-hidden`}
      >
        <Sidebar
          collapsed={sidebarCollapsed}
          onCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
        />
      </div>

      {/* Main content area */}
      <div className="flex-1 flex overflow-hidden">
        {canvasOpen && (
          <div className="w-1/2 border-r border-border overflow-hidden">
            <Canvas onClose={() => setCanvasOpen(false)} />
          </div>
        )}

        <div
          className={`${
            canvasOpen ? "w-1/2" : "w-full"
          } flex flex-col overflow-hidden`}
        >
          <MainWorkspace onOpenCanvas={() => setCanvasOpen(true)} />
        </div>
      </div>
    </div>
  );
}
