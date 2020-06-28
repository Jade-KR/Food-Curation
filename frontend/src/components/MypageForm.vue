<template>
  <div>
    <div id="my_box">
      <div id="my_body">
        <div id="my_body_head">
          <div id="my_body_head_catesort">카테고리정렬</div>
          <div id="my_body_head_search">검색</div>
        </div>
        <div id="my_body_card">
          <MypageCard />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MypageCard from "./MypageCard"

export default {
  components: {
    MypageCard
  }
}
</script>

<style scoped>
#my_body {
  width: 75%;
  float: right;
  border: 1px solid black;
}
#my_body_head {
  display: block;
  width: 100%;
}
#my_body_head_catesort {
  display: inline-block;
}
#my_body_head_search {
  
  float: right;
}
#my_body_card {
  display: block;
}
</style>