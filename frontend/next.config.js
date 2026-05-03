/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  },
  images: {
    domains: ["image.tmdb.org", "via.placeholder.com"],
  },
};

module.exports = nextConfig;
