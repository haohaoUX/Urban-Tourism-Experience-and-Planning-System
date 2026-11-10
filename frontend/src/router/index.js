import { createRouter, createWebHashHistory } from "vue-router"
import MapView from "../views/MapView.vue"
import PlanView from "../views/PlanView.vue"

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: "/", name: "map", component: MapView },
    { path: "/plan", name: "plan", component: PlanView },
  ],
})

export default router
