import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SeatSelectionView from '../views/SeatSelectionView.vue'
import PaymentView from '../views/PaymentView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/showtimes/:id/seats',
      name: 'seat-selection',
      component: SeatSelectionView,
    },
    {
      path: '/payment',
      name: 'payment',
      component: PaymentView,
    },
  ],
})

export default router
