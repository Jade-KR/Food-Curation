<template>
  <div>
    <v-dialog v-model="dialog" width="50vw">
      <template v-slot:activator="{ on }">
        <div v-on="on"><slot name="load" /></div>
      </template>
      <v-card
        id="check_fav"
        color="raba(0,0,0,0.6)"
        dark
      >
        <div id="check_fav_header">
          <div id="check_fav_title">
            For you, By you, Of you
          </div>
          <div id="check_fav_desc">
            당신의 취향을 알려주세요
          </div>
        </div>
        <v-form>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-autocomplete
                  v-model="foods"
                  :items="categories"
                  filled
                  chips
                  color="white"
                  label="Your Choice"
                  item-text="name"
                  item-value="name"
                  multiple
                  no-data-text="찾으시는 음식이 없습니다"
                >
                  <template v-slot:selection="data">
                    <v-chip
                      v-bind="data.attrs"
                      :input-value="data.selected"
                      close
                      @click="data.select"
                      @click:close="remove(data.item)"
                    >
                      <!-- <v-avatar left>
                        <v-img :src="data.item.avatar" />
                      </v-avatar> -->
                      {{ data.item.name }}
                    </v-chip>
                  </template>
                  <template v-slot:item="data">
                    <template v-if="typeof data.item !== 'object'">
                      <v-list-item-content v-text="data.item" />
                    </template>
                    <template v-else>
                      <!-- <v-list-item-avatar>
                        <img :src="data.item.avatar">
                      </v-list-item-avatar> -->
                      <v-list-item-content row>
                        <v-list-item-title v-text="data.item.name" />
                        <v-list-item-subtitle v-text="data.item.group" />
                      </v-list-item-content>
                    </template>
                  </template>
                </v-autocomplete>
                <div v-if="error_check">
                  asdfasdf
                </div>
              </v-col>
            </v-row>
            <v-btn
              id="check_fav_btn"
              :loading="isUpdating"
              :disabled="vali_check"
              depressed
              @click="isUpdating = true; setCate()"
            >
              <v-icon left>mdi-update</v-icon>
              Tailoring Now
            </v-btn>
          </v-container>
        </v-form>
        <v-divider />
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  export default {
    data () {
      // const srcs = {
      //   1: "http://blogfiles.naver.net/20150628_74/cider99_1435419455892ToOnB_JPEG/003.jpg",
      //   2: 'https://cdn.vuetifyjs.com/images/lists/2.jpg',
      //   3: 'https://cdn.vuetifyjs.com/images/lists/3.jpg',
      //   4: 'https://cdn.vuetifyjs.com/images/lists/4.jpg',
      //   5: 'https://cdn.vuetifyjs.com/images/lists/5.jpg',
      // }

      return {
        dialog: false,
        isUpdating: false,
        foods: ['김치찌개', '탕수육'],
        categories: [
          { header: '한식' },
          { name: '김치찌개', group: '한식'},
          { name: '고추장찌개', group: '한식'},
          { name: '수육', group: '한식'},
          // { name: '족발', group: '한식', avatar: srcs[2] },
          { divider: true },
          { header: '중식' },
          { name: '짜장면', group: '중식' },
          { name: '볶음밥', group: '중식' },
          { name: '짬뽕', group: '중식' },
          { name: '탕수육', group: '중식' },
          { divider: true },
          { header: '양식' },
          { name: "파스타", group: "양식" },
          { name: "피자", group: "양식" },
          { name: "스테이크", group: "양식" },
          { name: "리조또", group: "양식" },
        ],
        error_check: false,
        vali_check: true,
      }
    },
    watch: {
      isUpdating (val) {
        if (val) {
          setTimeout(() => (this.isUpdating = false), 3000)
        }
      },
      foods() {
        // console.log(this.foods.length)
        if (this.foods.length > 10) {
          this.vali_check = true
          this.error_check = true
        } else if (this.foods.length == 0) {
          this.vali_check = true
        } else {
          this.vali_check = false
          this.error_check = false
        }
      }
    },
    methods: {
      remove (item) {
        const index = this.foods.indexOf(item.name)
        if (index >= 0) this.foods.splice(index, 1)
      },
      setCate() {
        console.log(this.foods)
        // this.dialog = false
      }
    },
  }
</script>

<style scoped>
#check_fav {
  padding: 20px;
}
#check_fav_header {
  text-align: center;
}
#check_fav_title {
  font-size: 36px;
  margin-bottom: 10px;
}
#check_fav_desc {
  font-size: 20px;
}
#check_fav_btn {
  width: 100%;
  font-size: 20px;
  height: 50px;
}
</style>