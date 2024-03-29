// Composables
import {createRouter, createWebHistory} from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "home" */ '@/views/Home.vue'),
      },
      {
        path: '/createNewCopy',
        name: 'CreateNewCopy',
        component: () => import('@/views/CreateNewCopy')
      },
      {
        path: '/test/qrcodeReader',
        name: 'TestQrcodeReader',
        component: () => import('@/views/TestQrcodeReader')
      },
      {
        path: '/test/bggAutocomplete',
        name: 'TestBggAutocomplete',
        component: () => import('@/views/TestBggAutocomplete')
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
