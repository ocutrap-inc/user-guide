import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Allow images from any source in the docs
  images: {
    unoptimized: true,
  },
  // Transpile nothing extra needed
  output: undefined,
};

export default nextConfig;
