import { createRouter, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue'
import SearchResult from './pages/SearchResult.vue'
import About from './pages/About.vue'

const routerHistory = createWebHistory()

const router = createRouter({
  scrollBehavior(to) {
    if (to.hash) {
      window.scroll({ top: 0 })
    } else {
      document.querySelector('html').style.scrollBehavior = 'auto'
      window.scroll({ top: 0 })
      document.querySelector('html').style.scrollBehavior = ''
    }
  },  
  history: routerHistory,
  routes: [
    {
      path: '/',
      component: Home
    },
    {
      path: '/search',
      component: SearchResult
    },
    {
      path: '/about',
      component: About
    }
  ]
})

export default router
