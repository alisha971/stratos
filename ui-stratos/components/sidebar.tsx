"use client"

import type React from "react"
import { StratosLogo } from "components/stratos-logo"
import { useState } from "react"
import { Button } from "components/ui/button"
import { ScrollArea } from "components/ui/scroll-area"
import { Plus, Search, Home, Library, Lock, ChevronDown, Trash2 } from "lucide-react"

interface SidebarProps {
  onCollapse: () => void
}

export function Sidebar({ onCollapse }: SidebarProps) {
  const [chatsExpanded, setChatsExpanded] = useState(true)
  const [privateExpanded, setPrivateExpanded] = useState(true)
  const [hoveredChatId, setHoveredChatId] = useState<number | null>(null)

  const [chats, setChats] = useState([
    { id: 1, title: "Pluripotency, Differentiation...", date: "Today" },
    { id: 2, title: "Agentic AI News and Trends", date: "Yesterday" },
    { id: 3, title: "Age reversal research", date: "2 days ago" },
  ])

  const handleDeleteChat = (e: React.MouseEvent, id: number) => {
    e.stopPropagation()
    setChats(chats.filter((chat) => chat.id !== id))
  }

  return (
    <div className="flex flex-col h-full bg-sidebar">
      {/* Header */}
      <div className="p-4 border-b border-sidebar-border flex items-center justify-between">
        <div className="flex items-center gap-2">
          <StratosLogo className="w-5 h-5 text-accent" animated={true} />
          <h2 className="font-semibold text-sidebar-foreground text-sm">Stratos</h2>
        </div>
        <Button
          variant="ghost"
          size="icon"
          onClick={onCollapse}
          className="h-6 w-6 text-sidebar-foreground/60 hover:text-sidebar-foreground transition-colors"
        >
          <ChevronDown className="w-4 h-4" />
        </Button>
      </div>

      {/* New Chat Button */}
      <div className="p-4">
        <Button
          className="w-full bg-sidebar-primary hover:bg-sidebar-primary/90 text-sidebar-primary-foreground justify-start gap-2 transition-colors active:scale-95"
          size="sm"
        >
          <Plus className="w-4 h-4" />
          New Chat
        </Button>
      </div>

      {/* Search */}
      <div className="px-4 pb-4">
        <div className="relative">
          <Search className="absolute left-2.5 top-2.5 w-4 h-4 text-sidebar-foreground/40" />
          <input
            type="text"
            placeholder="Search chats..."
            className="w-full pl-8 pr-3 py-1.5 bg-sidebar-accent/30 border border-sidebar-border rounded text-xs text-sidebar-foreground placeholder:text-sidebar-foreground/40 focus:outline-none focus:border-sidebar-primary focus:bg-sidebar-accent/50 transition-colors"
          />
        </div>
      </div>

      {/* Chat Sections */}
      <ScrollArea className="flex-1">
        <div className="px-4 space-y-4 leading-4">
          {/* Navigation */}
          <div className="space-y-2">
            <Button
              variant="ghost"
              className="w-full justify-start gap-2 h-8 text-sidebar-foreground hover:bg-sidebar-accent/50 transition-colors"
              size="sm"
            >
              <Home className="w-4 h-4" />
              <span className="">Home</span>
            </Button>
            <Button
              variant="ghost"
              className="w-full justify-start gap-2 h-8 text-sidebar-foreground hover:bg-sidebar-accent/50 transition-colors"
              size="sm"
            >
              <Library className="w-4 h-4" />
              <span>Library</span>
            </Button>
            <Button
              variant="ghost"
              className="w-full justify-start gap-2 h-8 text-sidebar-foreground hover:bg-sidebar-accent/50 transition-colors"
              size="sm"
            >
              <Search className="w-4 h-4" />
              <span className="">Search</span>
            </Button>
          </div>

          {/* Chats Section */}
          <div>
            <button
              onClick={() => setChatsExpanded(!chatsExpanded)}
              className="w-full flex items-center gap-2 text-xs font-semibold text-sidebar-foreground/60 hover:text-sidebar-foreground p-2 transition-colors"
            >
              <ChevronDown className={`w-3 h-3 transition-transform ${chatsExpanded ? "rotate-0" : "-rotate-90"}`} />
              Chats
            </button>
            {chatsExpanded && (
              <div className="space-y-1 mt-2">
                {chats.map((chat) => (
                  <div
                    key={chat.id}
                    onMouseEnter={() => setHoveredChatId(chat.id)}
                    onMouseLeave={() => setHoveredChatId(null)}
                    className="group flex items-center gap-1"
                  >
                    <button className="flex-1 text-left px-2 py-2 text-xs rounded hover:bg-sidebar-accent/50 text-sidebar-foreground/70 hover:text-sidebar-foreground transition-colors">
                      <div className="truncate">{chat.title}</div>
                      <div className="text-xs text-sidebar-foreground/40 mt-1">{chat.date}</div>
                    </button>
                    {hoveredChatId === chat.id && (
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6 text-sidebar-foreground/40 hover:text-destructive"
                        onClick={(e) => handleDeleteChat(e, chat.id)}
                      >
                        <Trash2 className="w-3 h-3" />
                      </Button>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Private Section */}
          <div>
            <button
              onClick={() => setPrivateExpanded(!privateExpanded)}
              className="w-full flex items-center gap-2 text-xs font-semibold text-sidebar-foreground/60 hover:text-sidebar-foreground p-2 transition-colors"
            >
              <ChevronDown className={`w-3 h-3 transition-transform ${privateExpanded ? "rotate-0" : "-rotate-90"}`} />
              <Lock className="w-3 h-3" />
              Private
            </button>
            {privateExpanded && (
              <div className="space-y-1 mt-2">
                <button className="w-full text-left px-2 py-2 text-xs rounded hover:bg-sidebar-accent/50 text-sidebar-foreground/70 hover:text-sidebar-foreground transition-colors">
                  My Research Projects
                </button>
              </div>
            )}
          </div>
        </div>
      </ScrollArea>

      {/* Footer - User Account */}
      <div className="p-4 border-t border-sidebar-border">
        <Button
          variant="ghost"
          className="w-full justify-start gap-2 h-8 text-sidebar-foreground/70 hover:bg-sidebar-accent/50 transition-colors"
          size="sm"
        >
          <div className="w-5 h-5 rounded-full bg-gradient-to-br from-sidebar-primary to-sidebar-primary/50" />
          <span className="text-xs">Sign in</span>
        </Button>
      </div>
    </div>
  )
}
