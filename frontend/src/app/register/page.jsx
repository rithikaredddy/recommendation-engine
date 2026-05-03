"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "../../context/AuthContext";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Register() {
  const { login } = useAuth();
  const router = useRouter();
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Registration failed");
      login(data);
      router.push("/");
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  return (
    <div className="flex items-center justify-center min-h-[70vh]">
      <div className="bg-gray-800 border border-gray-700 rounded-2xl p-8 w-full max-w-md">
        <h2 className="text-white text-2xl font-bold mb-6 text-center">Create Account</h2>
        {error && (
          <div className="bg-red-900/40 border border-red-700 text-red-300 rounded-lg px-4 py-3 mb-4 text-sm">
            {error}
          </div>
        )}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="text" placeholder="Username"
            value={form.username}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
            required
            className="bg-gray-900 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-500 text-sm outline-none focus:border-indigo-500 transition"
          />
          <input
            type="email" placeholder="Email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            required
            className="bg-gray-900 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-500 text-sm outline-none focus:border-indigo-500 transition"
          />
          <input
            type="password" placeholder="Password (min 6 chars)"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            required minLength={6}
            className="bg-gray-900 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-500 text-sm outline-none focus:border-indigo-500 transition"
          />
          <button
            type="submit" disabled={loading}
            className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-600 text-white rounded-lg py-3 font-semibold text-sm transition mt-2"
          >
            {loading ? "Creating account..." : "Create Account"}
          </button>
        </form>
        <p className="text-gray-500 text-sm text-center mt-5">
          Already have an account?{" "}
          <Link href="/login" className="text-indigo-400 hover:text-indigo-300">Login</Link>
        </p>
      </div>
    </div>
  );
}
