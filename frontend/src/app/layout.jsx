import "./globals.css";
import { AuthProvider } from "../context/AuthContext";
import Navbar from "../components/Navbar";

export const metadata = {
  title: "CineRec — Movie Recommendation Engine",
  description: "Personalized movie recommendations using Content-Based and Collaborative Filtering",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-950 min-h-screen text-white">
        <AuthProvider>
          <Navbar />
          <main className="max-w-7xl mx-auto px-4 py-8">
            {children}
          </main>
        </AuthProvider>
      </body>
    </html>
  );
}
