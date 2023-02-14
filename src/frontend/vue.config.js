// webpack.config.js
const AutoImport = require('unplugin-auto-import/webpack')
const Components = require('unplugin-vue-components/webpack')
const { ElementPlusResolver } = require('unplugin-vue-components/resolvers')
const IconsResolver = require('unplugin-icons/resolver')
const Icons = require('unplugin-icons/webpack')

// const { defineConfig } = require('@vue/cli-service')
// module.exports = defineConfig({
//   transpileDependencies: true
// })



module.exports = {
  transpileDependencies: true,
  devServer: {
    port: 9098,
    proxy: "http://127.0.0.1:5000"
  },
  configureWebpack: {
    plugins: [
      AutoImport({
        resolvers: [
            ElementPlusResolver(),
            IconsResolver({
                prefix: 'Icon',
            }),
        ],
      }),
      Components({
        resolvers: [
            ElementPlusResolver(),
            IconsResolver({
              enabledCollections: ['ep'],
            }),
        ],
      }),
        Icons({
            autoInstall: true,
        }),
    ],
  },
  pages: {
    index: {
      entry: 'src/main.js',
      title: '知明——轻量级作业管理系统',
    }
  }
}
