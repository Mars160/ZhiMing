import {defineAsyncComponent} from "vue";
import axios from "axios";

const templates = {}
const plugins_json = sessionStorage.getItem("plugins")
const plugins = plugins_json === undefined || plugins_json === null ? {} : JSON.parse(plugins_json)

function pluginCompsInit() {
    for (const element in plugins) {
        const webpath = plugins[element]
        axios.get(webpath).then((res) => {
            templates[element] = res.data
        })
    }
}

function loadComponent(originPath) {
    //去除originPath起始的@
    // originPath = originPath.replace(/^@/, '.')
    // return defineAsyncComponent(() => import(originPath) )
    if(originPath === undefined || originPath === null) {
        pluginCompsInit()
        return null
    }
    const fileName = originPath.split('/').pop().split('.')[0]
    const webpath = plugins[fileName]
    //暂停1秒
    return defineAsyncComponent( () => {
        return new Promise((resolve, reject) => {
            if(templates[fileName] === undefined) {
                axios.get(webpath).then((res) => {
                    templates[fileName] = res.data
                    resolve({
                        template: templates[fileName]
                    })
                }).catch((err) => {
                    reject(err)
                })
            } else {
                resolve({
                    template: templates[fileName],
                })
            }})})
    // } else {
    //     return defineAsyncComponent(() => {
    //         return import(originPath)
    //     })
    // }
}

export default loadComponent
