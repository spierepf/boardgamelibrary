/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Plugins
import { registerPlugins } from '@/plugins'
import mitt from "mitt"

const app = createApp(App)
export const bus = mitt()

registerPlugins(app)

app.mount('#app')
