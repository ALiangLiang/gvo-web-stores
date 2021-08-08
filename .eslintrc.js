module.exports = {
  env: {
    browser: true,
    commonjs: true,
    node: true
  },
  extends: [
    'plugin:vue/vue3-recommended',
    'plugin:vue/vue3-essential',
    'standard'
  ],
  parserOptions: {
    ecmaVersion: 2021
  },
  rules: {
    'vue/no-v-model-argument': 'off', // In element plus, it's needed
    'import/no-webpack-loader-syntax': 'off' // This project doesn't used webpack
  }
}
