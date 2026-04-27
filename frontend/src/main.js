import { createApp } from 'vue'
import axios from 'axios'
import {createHead} from '@vueuse/head'

import router from './router'
import App from './App.vue'
import store from './store'

import './css/style.css'

const app = createApp(App)

axios.defaults.withCredentials = true;
//axios.defaults.baseURL = '/';  // the FastAPI backend
axios.defaults.baseURL = 'http://localhost:8000/';  // the FastAPI backend


app.use(router)
app.use(store);
app.use(createHead());
app.mount('#app')
