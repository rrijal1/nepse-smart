import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import App from "./App.vue";
import MarketView from "./views/MarketView.vue";
import AnalyticsView from "./views/AnalyticsView.vue";
import MyCornerView from "./views/MyCornerView.vue";
import AgentView from "./views/AgentView.vue";
import "./style.css";

const routes = [
  { path: "/", redirect: "/market" },
  { path: "/market", name: "Market", component: MarketView },
  {
    path: "/analytics/:section?/:symbol?",
    name: "Analytics",
    component: AnalyticsView,
    props: true,
  },
  { path: "/agent", name: "Agent", component: AgentView },
  { path: "/my-corner", name: "MyCorner", component: MyCornerView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

createApp(App).use(router).mount("#app");
