import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Dev: front em :5173, API em :8000 (proxy evita CORS e simplifica fetch/SSE).
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': { target: 'http://localhost:8000', changeOrigin: true,
                rewrite: (p) => p.replace(/^\/api/, '') },
    },
  },
})
