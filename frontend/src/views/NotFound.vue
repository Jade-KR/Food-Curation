<template>
  <div id="notfound_back">
    <div id="notfound_box">
      <div id="notfound_badgate">
        잘못된 접근입니다
      </div>
      <div id="notfound_gohome" @click="goHome()">
        홈으로 돌아가기
      </div>
    </div>
  </div>
</template>

<script>
import router from "../router"
import { mapActions } from "vuex";

export default {
  methods: {
    ...mapActions("data", ["checkRegister"]),
    goHome() {
      router.push("/")
    }
  },
  mounted() {
    // console.log("aaa")
    this.checkRegister()
  },
  destroyed() {
    // console.log("bbb")
    this.checkRegister()
  }
}
</script>

<style scoped>
#notfound_back {
  text-align: center;
  height: 100%;
  background-color: black;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}
#notfound_box {
  border: 5px solid;
  color: white;
  width: 50vw;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 30px;
}
#notfound_badgate {
  font-size: 50px;
  margin-bottom: 10px;
}
#notfound_gohome {
  cursor: pointer;
}
</style>