import vue from '@vitejs/plugin-vue'

/**
 * @type {import('vite').UserConfig}
 */
export default {
  plugins: [vue()],
  base: '/gvo-web-stores/',
  server: {
    port: 3300,
  }
}
