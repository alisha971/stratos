import type { Metadata } from "next";
import { Analytics } from "@vercel/analytics/next";
import "./globals.css";

// --- THIS IS THE FIX ---

// 1. Import Google Fonts from 'next/font/google'
import {
  Comfortaa as V0_Font_Comfortaa,
  Cormorant_Garamond as V0_Font_Cormorant_Garamond,
} from "next/font/google";

// 2. Import the localFont loader from 'next/font/local'
import localFont from "next/font/local";

// 3. Initialize the Google fonts
const _comfortaa = V0_Font_Comfortaa({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  variable: "--font-v0-comfortaa",
});
const _cormorantGaramond = V0_Font_Cormorant_Garamond({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  variable: "--font-v0-cormorant-garamond",
});

// 4. Initialize the LOCAL Geist_Mono font
// This path is relative to 'layout.tsx' and points to your 'fonts' folder
// We'll use 'GeistVF.woff' as shown in your screenshot
const _geistMono = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-v0-geist-mono",
  weight: "100 900",
});
// --- END OF FIX ---


export const metadata: Metadata = {
  title: "Stratos",
  description: "Agentic AI Research & Knowledge Hub",
  generator: "v0.app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      {/* 5. Apply all font variables to the body */}
      <body
        className={`${_comfortaa.variable} ${_geistMono.variable} ${_cormorantGaramond.variable} font-sans antialiased`}
      >
        {children}
        <Analytics />
      </body>
    </html>
  );
}