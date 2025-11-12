"use client";

import type React from "react";
import { useState } from "react";
import { StratosLogo } from "components/stratos-logo";
import { Button } from "components/ui/button";
import { ScrollArea } from "components/ui/scroll-area";
import {
  Plus,
  Search,
  Home,
  Library,
  Lock,
  ChevronLeft,
  ChevronRight,
  Trash2,
} from "lucide-react";

interface SidebarProps {
  collapsed?: boolean;
  onCollapse: () => void;
}

export function Sidebar({ collapsed = false, onCollapse }: SidebarProps) {
  const [chatsExpanded, setChatsExpanded] = useState(true);
  const [privateExpanded, setPrivateExpanded] = useState(true);
  const [hoveredChatId, setHoveredChatId] = useState<number | null>(null);

  const [chats, setChats] = useState([
    { id: 1, title: "Pluripotency, Differentiation...", date: "Today" },
    { id: 2, title: "Agentic AI News and Trends", date: "Yesterday" },
    { id: 3, title: "Age reversal research", date: "2 days ago" },
  ]);

  const handleDeleteChat = (e: React.MouseEvent, id: number) => {
    e.stopPropagation();
    setChats(chats.filter((chat) => chat.id !== id));
  };

  return (
    <div className="flex flex-col h-full bg-sidebar text-sidebar-foreground transition-all duration-300">
      {/* Header */}
      <div
        className={`flex items-center border-b border-sidebar-border transition-all duration-300 ${
          collapsed ? "justify-center py-6" : "px-4 py-4"
        }`}
      >
        {collapsed ? (
          // --- Collapsed Mode: logo acts as open button ---
          <button
            onClick={onCollapse}
            className="relative group cursor-pointer flex items-center justify-center"
          >
            <StratosLogo
              className="w-8 h-8 text-accent transition-transform duration-300 group-hover:scale-110"
              animated={true}
            />
            {/* Tooltip */}
            <div className="absolute left-12 bg-sidebar text-sidebar-foreground text-xs rounded-md px-2 py-1 opacity-0 group-hover:opacity-100 transition-all duration-200 shadow-lg border border-sidebar-border whitespace-nowrap translate-x-1 group-hover:translate-x-0">
              Open sidebar
            </div>
          </button>
        ) : (
          // --- Expanded Mode ---
          <div className="flex items-center justify-between w-full">
            {/* Left: Logo and title */}
            <div className="flex items-center gap-2">
              <StratosLogo
                className="w-5 h-5 text-accent transition-all duration-300"
                animated={true}
              />
              <h2 className="font-semibold text-sidebar-foreground text-sm">
                Stratos
              </h2>
            </div>

            {/* Right: Collapse Button */}
            <button
              onClick={onCollapse}
              className="ml-auto p-2 rounded-md hover:bg-sidebar-accent/40 text-sidebar-foreground/70 hover:text-sidebar-foreground transition-colors"
            >
              {/* Chevron pointing left */}
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
                className="w-4 h-4"
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
              </svg>
            </button>
          </div>
        )}
      </div>



      {/* Mini or full mode */}
      {collapsed ? (
        // --- MINI SIDEBAR ---
        <div className="flex flex-col items-center py-4 gap-4 text-sidebar-foreground/70">
          <Button variant="ghost" size="icon" className="hover:text-accent">
            <Home className="w-5 h-5" />
          </Button>
          <Button variant="ghost" size="icon" className="hover:text-accent">
            <Library className="w-5 h-5" />
          </Button>
          <Button variant="ghost" size="icon" className="hover:text-accent">
            <Search className="w-5 h-5" />
          </Button>
          <div className="flex-1" />
          <Button variant="ghost" size="icon" className="hover:text-accent">
            <Lock className="w-5 h-5" />
          </Button>
        </div>
      ) : (
        // --- FULL SIDEBAR (your existing one) ---
        <>
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
                  <span>Home</span>
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
                  <span>Search</span>
                </Button>
              </div>

              {/* Chats Section */}
              <div>
                <button
                  onClick={() => setChatsExpanded(!chatsExpanded)}
                  className="w-full flex items-center gap-2 text-xs font-semibold text-sidebar-foreground/60 hover:text-sidebar-foreground p-2 transition-colors"
                >
                  <ChevronLeft
                    className={`w-3 h-3 transition-transform ${
                      chatsExpanded ? "rotate-0" : "-rotate-90"
                    }`}
                  />
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
                          <div className="text-xs text-sidebar-foreground/40 mt-1">
                            {chat.date}
                          </div>
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
                  <ChevronLeft
                    className={`w-3 h-3 transition-transform ${
                      privateExpanded ? "rotate-0" : "-rotate-90"
                    }`}
                  />
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

          {/* Footer */}
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
        </>
      )}
    </div>
  );
}
