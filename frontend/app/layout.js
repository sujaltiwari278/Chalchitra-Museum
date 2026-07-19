import { Playfair_Display, Cormorant_Garamond, Cinzel } from "next/font/google";
import "./globals.css";
import Nav from "@/components/Nav";
import Footer from "@/components/Footer";

const playfair = Playfair_Display({
  subsets: ["latin"],
  weight: ["500", "700"],
  variable: "--font-playfair",
});
const cormorant = Cormorant_Garamond({
  subsets: ["latin"],
  weight: ["400", "600"],
  variable: "--font-cormorant",
});
const cinzel = Cinzel({
  subsets: ["latin"],
  weight: ["600"],
  variable: "--font-cinzel",
});

export const metadata = {
  title: "Chalchitra Museum",
  description: "The Heritage of Indian Cinema — a digital museum since 1913.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${playfair.variable} ${cormorant.variable} ${cinzel.variable} font-body`}
      >
        <Nav />
        {children}
        <Footer />
      </body>
    </html>
  );
}
