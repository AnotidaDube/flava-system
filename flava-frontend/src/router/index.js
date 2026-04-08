import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FlavorsView from '../views/FlavorsView.vue'
import JoinView from '../views/JoinView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/flavors',
      name: 'flavors',
      component: FlavorsView
    },
    {
      path: '/join-the-team',
      name: 'join',
      component: JoinView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/rep-dashboard',
      name: 'rep-dashboard',
      component: () => import('../views/RepDashboardView.vue')
    }
  ]
})

export default router