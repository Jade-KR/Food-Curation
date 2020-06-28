<template>
  <v-app id="app">
    <!-- <toolbar /> -->
    <!-- <drawer /> -->
    <Nav v-if="onRegister == false" style="height: 86px;" />
    <route-view />
    <!-- <go-top /> -->
  </v-app>
</template>

<script>
// import Drawer from "@/components/Drawer";
// import Toolbar from "@/components/Toolbar";
import RouteView from "@/components/RouteView";
import Nav from "@/components/Nav";
// import GoTop from "@/components/GoTop";
import { mapState } from "vuex";

export default {
  components: {
    // Drawer,
    // Toolbar,
    RouteView,
    Nav
    // GoTop
  },
  computed: {
    ...mapState({
      onRegister: state => state.data.onRegisterFlag,
    })
  },
};
</script>


