<template>
  <div>
    <div id="my_page_head">
      <div id="my_page_head_search">
        <form @submit.prevent="goSearch">
          <v-select
            id="my_page_head_option"
            v-model="options_value"
            :items="options"
            dense
            item-color="black"
            color="rgba(0, 0, 0, 1)"
            placeholder="검색조건"
            style="display: inline-block; width: 100px; font-size: 15px; transform: translateY(-7.5%); margin-left: 10px;"
            @change="selectOption"
          />
          <input id="my_page_head_search_bar" v-model="word" type="text" placeholder="search">
          <button id="my_page_head_search_btn" type="submit">검색</button>
        </form>
        <button id="my_page_head_reset_btn" @click="reset('all')">초기화</button>
      </div>
      <div id="my_page_head_sort">
        <v-container fluid pb-0>
          <!-- <div @click="sortValue()">asdf</div> -->
          <v-radio-group v-model="sort_value" row>
            <v-radio label="Latest" value="latest" color="black" />
            <v-radio label="Oldest" value="oldest" color="black" />
            <v-radio label="Rating" value="rating" color="black" />
          </v-radio-group>
        </v-container>
        
      </div>
    </div>
    <div id="blackbox" />
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  data() {
    return {
      options: [
				{ text: "리뷰", value: 1 },
				{ text: "상호명", value: 2 }
      ],
      options_value: 1,
      sort_value: "",
      word: ""
    }
  },
  watch: {
    sort_value: function() {
      // console.log(this.sort_value)
      this.$emit("sortvalue", this.sort_value)
    }
  },
  methods: {
    ...mapActions("data", ["resetCategoryList"]),
    ...mapActions("data", ["SHA256"]),
    goSearch() {
      // console.log(this.word)
      this.sort_value = ""
      if (this.word == "" || this.word == " " || this. word == "  ") {
        this.word = ""
        alert("검색어를 입력해주세요")
      } else {
        for (let i = 0; i < document.getElementsByClassName("user_category").length; ++i) {
          document.getElementsByClassName("user_category")[i].style = ""
        }
        this.sort_value = ""
        this.$emit("searchword", this.word, this.options_value);
        this.resetCategoryList()
      }
    },
    selectOption(value) {
      this.options_value = value
    },
    async reset(reset) {
      for (let i = 0; i < document.getElementsByClassName("user_category").length; ++i) {
        document.getElementsByClassName("user_category")[i].style = ""
      }
      this.word = ""
      this.options_value = 0
      this.sort_value = ""
      this.$emit("searchcate", reset);
      this.resetCategoryList()


      let a = ""
      await this.SHA256("test")
      .then(res => {
        // console.log(res)
        a = res
      })
      console.log(a)
    }
  }
}
</script>

<style scoped>
#my_page_head {
  display: flex;
  width: 100%;
  min-height: 70px;
  border: 1px solid black;
  text-align: start;
  background-color: rgba(255, 255, 255, 1);
}
#my_page_head_search {
  display: flex;
  flex: 1;
}
#my_page_head_search_bar {
  display: inline-block;
	border-bottom: 0.25px solid gray;
	width: 100px;
	-webkit-transition: width 0.4s ease-in-out;
	transition: width 0.4s ease-in-out;
}
#my_page_head_search_bar:focus {
	width: 200px;
  /* box-shadow: black; */
}
::placeholder {
	color: black;
	font-size: 18px;
}
#my_page_head_sort > div > div {
  margin: 0px;
}
#my_page_head_search_btn {
  font-size: 16px;
  margin: 10px;
  padding: 5px;
  background-color: black;
  color: white;
  width: 50px;
  transition: all .5s;
}
#my_page_head_reset_btn {
  font-size: 16px;
  margin: 10px;
  padding: 5px;
  background-color: black;
  color: white;
  width: 70px;
  height: 34px;
  transition: all .5s;
  transform: translateY(15%);
}
#blackbox {
  height: 20px;
  background-color: rgb(48, 48, 48);
}
</style>