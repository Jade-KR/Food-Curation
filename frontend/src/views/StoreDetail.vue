<template>
  <div>
    <Nav></Nav>
    <div class="header">
      <!-- 가게 사진들  -->
    </div>
    <div class="main">
      <!-- 음식점 정보 -->
      <div class="main_content">
        <StoreInfo
          :storeName="storeName"
          :storeScore="storeScore"
          :reviewCnt="reviewCnt"
          :storeArea="storeArea"
          :storeTel="storeTel"
          :storeAddress="storeAddress"
          :storeCategories="storeCategories"
          :storeMenuList="storeMenuList"
          @add-to-review="updatedReview"
        ></StoreInfo>
        <!-- 리뷰 테이블 -->
        <StoreReview ref="updateReview" @avg="avgScore"></StoreReview>
        <br />
        <br />
      </div>
      <!-- 오른쪽 기능 메뉴 -->
      <div class="aside">
        <StoreLocation :longitude="longitude" :latitude="latitude"></StoreLocation>
      </div>
    </div>
    <footer>.</footer>
  </div>
</template>

<script>
import Nav from "@/components/Nav.vue";
import router from "@/router";
import axios from "axios";
import StoreLocation from "@/components/StoreLocation";
import StoreInfo from "@/components/StoreInfo";
import StoreReview from "@/components/StoreReview";
export default {
  props: ["storeId"],
  components: {
    Nav,
    StoreLocation,
    StoreInfo,
    StoreReview
  },
  mounted(res) {
    axios
      .get(
        `http://i02d106.p.ssafy.io:8765/api/stores/${this.$route.params.storeId}`
      )
      .then(res => {
        console.log(res);
        this.storeName = res.data.store_name;
        this.storeArea = res.data.area;
        this.storeAddress = res.data.address;
        this.storeTel = res.data.tel;
        this.storeCategories = res.data.category_list;
        this.latitude = res.data.latitude;
        this.longitude = res.data.longitude;
        this.reviewCnt = res.data.review_count;
        this.storeMenuList = res.data.menues;
      });
  },
  data() {
    return {
      storeName: "",
      storeScore: 0,
      reviewCnt: "작성된 리뷰가 없습니다",
      storeArea: "",
      storeTel: "",
      storeAddress: "",
      storeCategories: [],
      storeMenuList: [],
      latitude: "",
      longitude: ""
    };
  },
  methods: {
    updatedReview() {
      this.$refs.updateReview.reRoad();
    },
    avgScore(avgScore) {
      this.storeScore = avgScore;
    }
  }
};
</script>

<style scoped>
.header {
  background: url("../../public/images/header.jpg");
  height: 200px;
  filter: brightness(30%);
}
.main {
  display: flex;
  background-color: rgb(15, 15, 15);
}
.aside {
  width: 30%;
  margin-left: 20px;
  background-color: whitesmoke;
  height: fit-content;
}
.main_content {
  width: 60%;
  display: flex;
  flex-flow: column nowrap;
  margin-left: 50px;
  background-color: whitesmoke;
  border-radius: 1%;
}
h2 {
  margin-top: 20px;
}
footer {
  height: 300px;
  width: 100%;
  background-color: rgb(15, 15, 15);
}
</style>