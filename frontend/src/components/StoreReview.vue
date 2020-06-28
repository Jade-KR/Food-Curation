<template>
  <div class="container">
    <h2 class="review_header">리뷰 ({{reviewCnt}})</h2>
    <div class="review_main" v-for="(review, index) in paginatedData" :key="index">
      <div class="review_container">
        <div class="review_container_left">{{review.user}}</div>
        <div class="review_container_middle">{{review.content}}</div>
        <div class="review_container_right">
          <div v-if="review.user == myId">
            <updateReview :reviewId="review.id" :content="review.content" @editReview="reRoad">
              <i class="fas fa-edit" slot="click"></i>
            </updateReview>
            <i class="fas fa-trash-alt" @click="deleteReview(review.id)"></i>
          </div>
          <div v-else>
            <i class="far fa-thumbs-up"></i>
          </div>
        </div>
      </div>
    </div>
    <div class="btn-cover">
      <button :disabled="pageNum === 0" @click="prevPage" class="page-btn">이전</button>
      <span class="page-count">{{ pageNum + 1 }} / {{ pageCount }} 페이지</span>
      <button :disabled="pageNum >= pageCount - 1" @click="nextPage" class="page-btn">다음</button>
    </div>
  </div>
</template>

<script>
import router from "@/router";
import axios from "axios";
import updateReview from "@/components/updateReview";
export default {
  components: {
    updateReview
  },
  data() {
    return {
      reviews: [],
      pageSize: 10,
      pageNum: 0,
      myId: localStorage.getItem("pk"),
      modal: false,
      avgScore: 0,
      reviewCnt: 0
    };
  },
  mounted(res) {
    axios
      .get(
        `http://i02d106.p.ssafy.io:8765/api/get_store_reviews_by_store_id/${this.$route.params.storeId}`
      )
      .then(res => {
        console.log(res.data);
        if (res.data.length) {
          var value = 0;
          let allScore = 0;
          while (value < res.data.length) {
            allScore = allScore + res.data[value].score;
            value++;
          }
          this.reviewCnt = value;
          this.reviews = res.data.reverse();
          allScore = allScore / value;
          allScore = allScore.toFixed(1);
          this.$emit("avg", allScore);
        } else {
          this.$emit("avg", 0);
        }
      });
  },
  methods: {
    reRoad(res) {
      setTimeout(() => {
        axios
          .get(
            `http://i02d106.p.ssafy.io:8765/api/get_store_reviews_by_store_id/${this.$route.params.storeId}`
          )
          .then(res => {
            this.reviews = res.data.reverse();
          });
      }, 500);
    },
    nextPage() {
      this.pageNum += 1;
    },
    prevPage() {
      this.pageNum -= 1;
    },
    editReview(review_id) {
      this.modal = true;
    },
    deleteReview(review_id) {
      console.log(review_id);
      axios
        .delete(`http://i02d106.p.ssafy.io:8765/api/store_reviews/${review_id}`)
        .then(this.reRoad());
    }
  },
  computed: {
    pageCount() {
      let listLeng = this.reviews.length,
        listSize = this.pageSize,
        page = Math.floor(listLeng / listSize);
      if (listLeng % listSize > 0) page += 1;
      return page;
    },
    paginatedData() {
      const start = this.pageNum * this.pageSize,
        end = start + this.pageSize;
      return this.reviews.slice(start, end);
    }
  }
};
</script>

<style scoped>
.review_header {
  margin-top: 20px;
  font-family: "Do Hyeon", sans-serif;
}
.review_container {
  display: flex;
  flex-flow: row nowrap;
  margin-top: 15px;
  padding-bottom: 15px;
  justify-content: space-between;
  border-bottom: solid #a5a79a 1px;
}
.review_container_left {
  width: 20%;
  color: rgb(172, 171, 171);
}
.review_container_middle {
  width: 60%;
  font-family: "Jua", sans-serif;
}
.review_container_right {
  width: 20%;
  text-align: center;
}
.review_container_right > div > i:hover {
  font-size: 18px;
  cursor: pointer;
}
.review_container_right > div {
  display: flex;
  align-items: baseline;
}
.review_container_right > div > i {
  margin-left: 10px;
}
.btn-cover {
  margin-top: 1.5rem;
  text-align: center;
}
.btn-cover .page-btn {
  width: 5rem;
  height: 2rem;
  letter-spacing: 0.5px;
  font-family: "Yeon Sung", cursive;
  background: rgb(219, 219, 219);
  border-radius: 15%;
}
.page-btn:hover {
  background: rgb(133, 132, 132);
}
.btn-cover .page-count {
  padding: 0 1rem;
  font-family: "Yeon Sung", cursive;
}
</style>