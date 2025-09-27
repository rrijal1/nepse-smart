import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import App from "./App.vue";
import Dashboard from "./views/Dashboard.vue";
import TradingDashboard from "./views/TradingDashboard.vue";
import PortfolioDashboard from "./views/PortfolioDashboard.vue";
import "./style.css";

const routes = [
  { path: "/", name: "Dashboard", component: Dashboard },
  { path: "/trading", name: "Trading", component: TradingDashboard },
  { path: "/portfolio", name: "Portfolio", component: PortfolioDashboard },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

createApp(App).use(router).mount("#app");
