"use client"

export function StratosLogo({
  className = "w-8 h-8 text-accent",
  animated = false,
}: { className?: string; animated?: boolean }) {
  return (
    <svg
      viewBox="-8 -8 48 48"
      className={`${className} drop-shadow-lg`}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      style={{ overflow: "visible" }}
    >
      <defs>
        {animated && (
          <>
            <style>{`
              /* Unified animation system with matching 12s duration and smooth keyframes */
              @keyframes rotateOrbits {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
              }
              
              @keyframes particle1Orbit {
                0% { transform: translate(6px, 0px); }
                100% { transform: translate(6px, 0px) rotate(-360deg); }
              }
              
              @keyframes particle2Orbit {
                0% { transform: translate(4.24px, 4.24px); }
                100% { transform: translate(4.24px, 4.24px) rotate(-360deg); }
              }
              
              @keyframes particle3Orbit {
                0% { transform: translate(0px, 6px); }
                100% { transform: translate(0px, 6px) rotate(-360deg); }
              }
              
              @keyframes particle4Orbit {
                0% { transform: translate(-4.24px, 4.24px); }
                100% { transform: translate(-4.24px, 4.24px) rotate(-360deg); }
              }
              
              .orbiting-group { 
                animation: rotateOrbits 12s linear infinite; 
                transform-origin: 16px 16px;
              }
              
              .particle-1 { 
                animation: particle1Orbit 12s linear infinite; 
                transform-origin: 16px 16px;
              }
              .particle-2 { 
                animation: particle2Orbit 12s linear infinite; 
                transform-origin: 16px 16px;
              }
              .particle-3 { 
                animation: particle3Orbit 12s linear infinite; 
                transform-origin: 16px 16px;
              }
              .particle-4 { 
                animation: particle4Orbit 12s linear infinite; 
                transform-origin: 16px 16px;
              }
            `}</style>
          </>
        )}
      </defs>

      {/* Main central orb */}
      <circle cx="16" cy="16" r="3.5" fill="currentColor" opacity="0.95" />

      <g className={animated ? "orbiting-group" : ""}>
        {/* Elliptical orbit path 1 - wide horizontal */}
        <ellipse cx="16" cy="16" rx="7" ry="4" stroke="currentColor" strokeWidth="0.4" opacity="0.2" />

        {/* Elliptical orbit path 2 - tilted */}
        <ellipse
          cx="16"
          cy="16"
          rx="5"
          ry="6"
          stroke="currentColor"
          strokeWidth="0.35"
          opacity="0.15"
          transform="rotate(45 16 16)"
        />

        {/* Elliptical orbit path 3 - tall vertical */}
        <ellipse cx="16" cy="16" rx="4" ry="7" stroke="currentColor" strokeWidth="0.35" opacity="0.15" />

        {/* Outer accent ellipse */}
        <ellipse cx="16" cy="16" rx="8" ry="5" stroke="currentColor" strokeWidth="0.3" opacity="0.1" />
      </g>

      {/* Particle 1 - horizontal right */}
      <g className={animated ? "particle-1" : ""}>
        <circle cx="22" cy="16" r="1.4" fill="currentColor" opacity="0.8" />
      </g>

      {/* Particle 2 - diagonal upper right */}
      <g className={animated ? "particle-2" : ""}>
        <circle cx="22" cy="9" r="1.3" fill="currentColor" opacity="0.75" />
      </g>

      {/* Particle 3 - vertical top */}
      <g className={animated ? "particle-3" : ""}>
        <circle cx="16" cy="26" r="1.4" fill="currentColor" opacity="0.78" />
      </g>

      {/* Particle 4 - diagonal upper left */}
      <g className={animated ? "particle-4" : ""}>
        <circle cx="10" cy="9" r="1.2" fill="currentColor" opacity="0.72" />
      </g>

      {/* Central accent glow */}
      <circle cx="16" cy="16" r="1" fill="currentColor" opacity="0.5" />
    </svg>
  )
}
