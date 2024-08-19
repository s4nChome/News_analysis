import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/mutil',
    name: 'mutil',
    component: () => import(/* webpackChunkName: "about" */ '../views/MutilScrapeView.vue')
  },
  {
    path: '/history',
    name: 'history',
    component: () => import(/* webpackChunkName: "about" */ '../views/HistoryView.vue')
  },
  {
    path: '/single',
    name: 'single',
    component: () => import(/* webpackChunkName: "about" */ '../views/SingleScrapeView.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
