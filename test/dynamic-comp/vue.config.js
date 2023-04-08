const { defineConfig } = require('@vue/cli-service')
// vue.config.js文件
module.exports = {
  outputDir: 'dist',
  publicPath: './', // 需注意是相对路径，不然dist打包访问后就会出现空白问题。
  productionSourceMap: false, // 去除Vue打包后js目录下生成的一些.map文件，用于加速生产环境构建。
  filenameHashing: false, // 去除Vue打包后.css和.js文件名称中8位hash值，跟缓存有关；一般为true就行。
  transpileDependencies: true
}