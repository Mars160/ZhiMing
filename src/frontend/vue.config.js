// webpack.config.js
const AutoImport = require('unplugin-auto-import/webpack')
const Components = require('unplugin-vue-components/webpack')
const {ElementPlusResolver} = require('unplugin-vue-components/resolvers')
const IconsResolver = require('unplugin-icons/resolver')
const Icons = require('unplugin-icons/webpack')
const HtmlWebpackPlugin = require("html-webpack-plugin");

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
            new HtmlWebpackPlugin({
                filename: "index.cdn.html",
                template: "public/index.html",
                cdn: {
                    vue: "https://cdn.jsdelivr.net/npm/vue/dist/vue.min.js",
                    "vue-router":
                        "https://cdn.jsdelivr.net/npm/vue-router/dist/vue-router.min.js",
                    "element-plus":
                        "https://unpkg.com/element-plus/lib/index.full.min.js",
                    "element-plus-icon":
                        "https://unpkg.com/element-plus/lib/theme-chalk/el-icon.css",
                },
            }),
        ],
        output: {
            chunkFilename: 'js/[name].js',
        },
        externals: {
            vue: "Vue",
            "vue-router": "VueRouter",
            "element-plus": "ElementPlus",
            "element-plus-icon": "ElementPlusIcon",
        },
    },
    css : {
        extract: {
            ignoreOrder: true,
            filename: 'css/[name].css',
            chunkFilename: 'css/[name].css',
        }
    },
    pages: {
        index: {
            entry: 'src/main.js',
            title: '知明——轻量级作业管理系统',
        }
    }
}
