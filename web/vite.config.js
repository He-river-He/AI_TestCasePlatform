import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// UI 自动化测试通过 VITE_API_TARGET 指向隔离的测试后端
const apiTarget = process.env.VITE_API_TARGET || 'http://localhost:8000';
const configuredBasePath = process.env.VITE_BASE_PATH || '/';
const basePrefix = configuredBasePath === '/'
  ? ''
  : `/${configuredBasePath.replace(/^\/|\/$/g, '')}`;
const apiProxyPath = `${basePrefix}/api`;

export default defineConfig({
  base: configuredBasePath,
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      [apiProxyPath]: {
        target: apiTarget,
        changeOrigin: true,
        rewrite: (path) => (basePrefix ? path.slice(basePrefix.length) || '/' : path),
      },
    },
  },
});
