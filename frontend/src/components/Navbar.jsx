"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "../context/AuthContext";

const Navbar = () => {
  const { user, logout } = useAuth();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  return (
    <nav className="bg-gray-900 sticky top-0 z-50 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 flex items-center justify-between h-16">
        <Link href="/" className="text-indigo-400 font-bold text-xl">
          🎬 CineRec
        </Link>
        <div className="flex items-center gap-6">
          <Link href="/" className="text-gray-300 hover:text-white text-sm transition">
            Movies
          </Link>
          {user ? (
            <>
              <Link href="/profile" className="text-gray-300 hover:text-white text-sm transition">
                Profile
              </Link>
              <span className="text-indigo-400 text-sm">Hi, {user.username}</span>
              <button
                onClick={handleLogout}
                className="text-sm border border-gray-600 text-gray-300 px-3 py-1 rounded-md hover:border-indigo-400 hover:text-white transition"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link href="/login" className="text-gray-300 hover:text-white text-sm transition">
                Login
              </Link>
              <Link
                href="/register"
                className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm px-4 py-1.5 rounded-md transition"
              >
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
