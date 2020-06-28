<template>
  <div class="card_container" />
</template>

<script>
import axios from "axios";
export default {
  mounted(res) {
    axios.get("http://127.0.0.1:8000/api/stores").then(res => {
      console.log(res.results);
      this.stores = res.results;
    });
  },
  data() {
    return{}
  },
  methods: {}
};
</script>

<style scoped>
.card_container {
  background: white;
  width: 100%;
  height: 400px;
}
</style>