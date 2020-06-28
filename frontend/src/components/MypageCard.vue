<template>
  <div id="card">
    <div id="card_store_name">
      {{ storeName }}, {{ reviewInfo.reg_time }}
      <div v-if="flag" id="card_imgs">
        <img class="card_img" src="../../public/images/icons/update.png" alt="update" @click="forEdit()">
        <img class="card_img" src="../../public/images/icons/delete.png" alt="delete" @click="reviewDelete(id)">
      </div>
    </div>
    <div id="card_body">
      <div v-if="flag" id="card_rating">
        {{ reviewInfo.score }}
      </div>
      <div v-else id="rating_input">
        <input v-model="tmp_score" type="number" step="1" min="0" max="5">
      </div>
      <div id="card_content">
        <form>
          <v-textarea v-model="reviewInfo.content" auto-grow rounded :disabled="flag" />
          <v-btn v-if="!flag" id="content_btn" dark @click="reviewEditCancle()">취소</v-btn>
          <v-btn v-if="!flag" id="content_btn" dark @click="reviewEdit()">수정</v-btn>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  props: {
    id: {
      type: Number,
      default: 0
    },
    store: {
      type: Number,
      default: 0
    },
    storeName: {
      type: String,
      default: ""
    },
    user: {
      type: Number,
      default: 0
    },
    score: {
      type: Number,
      default: 0
    },
    content: {
      type: String,
      default: ""
    },
    regTime: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      reviewInfo: {
        id: this.id,
        store: this.store,
        store_name: this.storeName,
        user: this.user,
        score: this.score,
        content: this.content,
        reg_time: this.regTime
      },
      tmp_score: this.score,
      flag: true
    }
  },
  methods: {
    ...mapActions("data", ["reviewEditByUser"]),
    ...mapActions("data", ["reviewDeleteByUser"]),
    forEdit() {
      this.flag = false
    },
    reviewEdit() {
      this.flag = true
      this.reviewInfo.score = Number(this.tmp_score)
      // this.reviewInfo.reg_time = new Date()
      // console.log(this.reviewInfo.reg_time)
      this.reviewEditByUser(this.reviewInfo)
    },
    reviewEditCancle() {
      this.flag = true
      this.tmp_score = this.score
      this.reviewInfo.content = this.content
    },
    reviewDelete(value) {
      this.reviewDeleteByUser(value)
    }
  }
}
</script>

<style scoped>
#card {
  border: 1px solid black;
}
#card_store_name {
  color: silver;
  text-align: start;
  padding-top: 5px;
  margin-left: 10px;
}
#card_body {
  display: flex;
  text-align: start;
}
#card_rating {
  display: inline-block;
  text-align: center;
  padding: 6px;
  font-size: 32px;
  border-radius: 15%;
  background-color: black;
  color: white;
  margin: 10px;
  min-width: 60px;
  height: 60px;
  transform:  translateX(20%);
}
#rating_input {
  padding: 6px;
  font-size: 32px;
  border-radius: 15%;
  background-color: silver;
  color: white;
  margin-top: 10px;
  margin-left: 20px;
  width: 60px;
  height: 60px;
}
#card_content {
  display: inline-block;
  font-size: 20px;
  margin-right: 20px;
  width: 100%;
  /* height: auto; */
}
#card_content > form > div {
  padding-top: 0;
}
#content_edit {
  width: 55vw;
  overflow: auto;
  border: 1px solid;
}
#content_btn {
  padding: 5px;
  float: right;
  right: 20px;
  bottom: 20px;
  margin-left: 10px;
}
/* .line-clamp {
	overflow: hidden;
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
} */
#card_imgs {
  display: inline-block;
  /* float: right; */
  text-align: inherit;
  min-width: 40px;
  transform:  translateY(10%);
}
.card_img {
  width: 20px;
  height: 20px;
  margin-left: 5px;
  cursor: pointer;
}
</style>