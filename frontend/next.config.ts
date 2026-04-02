import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "ci.encar.com",
      },
      {
        protocol: "http",
        hostname: "ci.encar.com",
      },
    ],
  },
};

export default nextConfig;
