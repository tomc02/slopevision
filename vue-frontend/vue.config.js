// vue.config.js
module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://0.0.0.0:8000',
        changeOrigin: true,

      },
      '/media': {
        target: 'http://0.0.0.0:8000',
        changeOrigin: true,
      }
    }
  }
};
