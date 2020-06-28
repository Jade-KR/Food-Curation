<template>
  <v-container class="mt-5" fill-height>
    <checkFavorite>
      <div id="checkFav" slot="load" />
    </checkFavorite>
    <v-card-text class="text-center">
      <p class="display-3 pa-2">🍜</p>
      <p class="display-2 pa-5">코딩도 식후경</p>
      <v-btn large color="blue lighten-1 white--text ma-5" rounded to="/search">검색하기</v-btn>
    </v-card-text>
  </v-container>
</template>

<script>
import CheckFavorite from "../components/CheckFavorite"

export default {
  components: {
    CheckFavorite
  },
  data() {
    return {
      dialog: false,
      checkfav_on: {
        display: "block"
      },
      checkfav_off: {
        display: "none"
      }
    }
  },
  mounted() {
    const flag = true
    if (flag == true) {
      this.dialog = true
      window.onload=function(){
        document.getElementById("checkFav").click();
      };
    }
    
  }
};
</script>