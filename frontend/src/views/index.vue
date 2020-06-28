<template>
  <div>
    <Nav></Nav>
    <header>
      <div class="header_middle">
        <p>맛집</p>
        <p>검색</p>
      </div>
      <card title="맛집 검색">
        <v-form>
          <v-container py-0>
            <v-layout wrap>
              <v-flex xs12 md12>
                <v-text-field v-model="storeName" label="음식점 이름" />
              </v-flex>
              <v-flex xs12 text-center>
                <v-btn large class="red white--text ma-5" rounded @click="onSubmit">GO!</v-btn>
              </v-flex>
            </v-layout>
          </v-container>
        </v-form>
      </card>
    </header>
    <main>
      <div class="main_top">
        <div class="menu_bar">
          <ul class="menu_bar_left">
            <li>
              <a href="#">메뉴1</a>
            </li>
            <li>
              <a href="#">메뉴2</a>
            </li>
            <li>
              <a href="#">메뉴3</a>
            </li>
            <li>
              <a href="#">메뉴4</a>
            </li>
          </ul>
          <div class="menu_bar_right">
            현재위치 : {{ }}
            <v-btn>위치받기</v-btn>
          </div>
        </div>
      </div>
      <div class="main_content">
        <RecStore />
      </div>
    </main>
    <aside />
    <footer />
  </div>
</template>

<script>
import RecStore from "../components/RecStore.vue";
import Nav from "../components/Nav.vue";

export default {
  components: {
    RecStore,
    Nav
  }
};
</script>

<style scoped>
header {
  display: flex;
  flex-flow: column nowrap;
  background: url("../../public/images/헤더 배경.jpg");
  background-size: cover;
}
.header_top {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  position: sticky;
  background: #666666;
  top: 0px;
  z-index: 100;
}
.header_top_inner_left > a {
  color: white;
  padding-left: 24px;
}
.header_top_inner_right {
  display: flex;
  list-style: none;
  padding-right: 24px;
}
.header_top_inner_right > li {
  padding: 12px 8px;
}
.header_top_inner_right > li > a {
  color: white;
}
.header_middle {
  display: flex;
  flex-flow: column nowrap;
  align-items: center;
  justify-content: center;
  height: 140px;
}
.header_middle > p {
  color: white;
  font-size: 2vw;
  margin: 0;
}
main {
  background: #e1dcd9;
  height: 1000px; /* 나중에 수정해야함. */
  display: flex;
  flex-flow: column nowrap;
  align-items: center;
}
.main_top {
  background: #a5a79a;
  display: flex;
  justify-content: center;
  width: 100%;
}
.menu_bar {
  display: flex;
  justify-content: space-between;
  width: 75%;
}
.menu_bar_left {
  display: flex;
  list-style: none;
  padding: 0;
}
.menu_bar_left > li {
  padding: 12px 25px 12px 0;
}
.menu_bar_left > li > a {
  color: #e1dcd9;
}
.menu_bar_right {
  color: #e1dcd9;
}
.main_content {
  margin: 24px 0;
  width: 75%;
  background: white;
  display: flex;
  justify-content: center;
}
</style>