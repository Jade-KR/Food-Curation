<template>
  <div 
    id="mypage"
    v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loading"
    infinite-scroll-distance="10"
  >
    <div id="mypageform">
      <MypageSidebar
        id="mypage_sidebar"
        :reviews="reviews"
        @searchcate="searchcate"
      />
      <div id="mypage_body">
        <MypageHeader 
          id="mypage_body_header"
          @searchword="searchword"
          @sortvalue="sortvalue"
          @searchcate="searchcate"
        />
        <div v-if="reviews != false">
          <div v-for="review in reviews" :key="review.id">
            <MypageCard
              :id="review.id"
              class="mypage_body_card"
              :store="review.store"
              :store-name="review.store_name"
              :user="review.user"
              :score="review.score"
              :content="review.content"
              :reg-time="review.reg_time"
            />
          </div>
        </div>
        <div v-else>
          <div id="no_content">
            검색 결과가 없습니다.
          </div>
        </div>
      </div>
      
    </div>
  </div>

</template>

<script>
// import router from "../router"
import MypageSidebar from "../components/MypageSidebar"
import MypageHeader from "../components/MypageHeader"
import MypageCard from "../components/MypageCard"
import { mapState, mapActions } from "vuex";


export default {
  components: {
    MypageSidebar,
    MypageHeader,
    MypageCard
  },
  props: {
    userId: {
      type: String,
      defalut: ""
    }
  },
  data() {
    return {
      loading: true,
      flag: true
    }
  },
  computed: {
    ...mapState({
      reviews: state => state.data.userReviewList,
      page: state => state.data.userReviewPage
    })
  },
  methods: {
    ...mapActions("data", ["getUserReview"]),
    ...mapActions("data", ["getReviewByCategory"]),
    ...mapActions("data", ["sortReviewByScore"]),
    ...mapActions("data", ["sortReviewByTime"]),
    async searchword(word, value) {
      // console.log("되나", word, value)
      let params = {}
      if (value == 1) {
        params = {
          user: this.$route.params.userId,
          content: word,
          page_size: 1000
        };
      } else if (value == 2) {
        params = {
          user: this.$route.params.userId,
          store_name: word,
          page_size: 1000
        }
      }
      // console.log("mypage ", params)
      await this.getUserReview(params)
      this.flag = false
    },
    loadMore: async function() {
      if (this.flag == true) {
        this.loading = true;
        const params = {
          user: this.$route.params.userId,
          page: this.page,
          append: true
        };
        await this.getUserReview(params);
        setTimeout(() => {
          this.loading = false;
        }, 1000);
      }
    },
    async searchcate(word) {
      // console.log(word)
      if (word == "all") {
        const params = {
          user: this.$route.params.userId,
          page: 1,
          append: false
        }
        await this.getUserReview(params)
        this.loading = false
        this.flag = true
      } else {
        const dataform = {
          params: {
            user: this.$route.params.userId,
            page_size: 1000
          },
          word: word
        }
        await this.getReviewByCategory(dataform)
        this.flag = false
      }
    },
    sortvalue(value) {
      // console.log(value)
      if (value == "rating") {
        this.sortReviewByScore()
      } else {
        this.sortReviewByTime(value)
      }
      this.flag = false
    }
  },
  async mounted() {
    const params = {
      user: this.$route.params.userId,
      page: 1,
      append: false
    };
    // console.log("mypage ", params)
    await this.getUserReview(params)
    this.loading = false
  }
}
</script>

<style scoped>
#mypage {
  background-color: rgba(0,0,0,0.8);
  height: 100%;
}
#mypageform {
  height: 100%;
  width: 90%;
  margin: 0 auto;
  text-align: center;
  padding: 60px 30px;

  /* position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 2;
  padding: 20px;
  text-align: center; */
}
#mypage_body {
  width: 75%;
  float: right;
  /* border: 1px solid black; */
}
#mypage_sidebar {
  position: sticky;
  top: 80px;
}
#mypage_body_header {
  display: block;
  position: sticky;
  top: 80px;
  z-index: 10;
}
.mypage_body_card {
  display: block;
  width: 100%;
  background-color: whitesmoke;
  margin-top: 10px;
}
#no_content {
  color: black;
  font-size: 30px;
  height: 100px;
  width: 100%;
  background-color: whitesmoke;
  margin-top: 20px;
  padding-top: 25px;
}
</style>