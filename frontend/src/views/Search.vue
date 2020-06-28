<template>
  <div
    v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loading"
    infinite-scroll-distance="10"
  >
    <v-container fill-height fluid grid-list-xl>
      <v-layout justify-center wrap mt-5>
        <v-flex xs12 md8>
          <card title="맛집 검색">
            <v-form>
              <v-container py-0>
                <v-layout wrap>
                  <v-flex xs12 md12>
                    <v-text-field v-if="location" v-model="storeName" label="음식점 이름" />
                    <v-text-field v-else v-model="storeName" label="음식점 이름" />
                    <v-radio-group v-model="sort_value" row class="radio">
                      <v-radio label="주변검색" value="주변검색" color="black" />
                      <v-radio label="일반검색" value="일반검색" color="black" />
                    </v-radio-group>
                  </v-flex>
                  <v-flex xs12 text-center>
                    <v-btn
                      large
                      class="indigo white--text ma-5"
                      rounded
                      color="blue lighten-1"
                      @click="onSubmit"
                      v-if="location"
                    >GO!</v-btn>
                    <v-btn
                      large
                      class="indigo white--text ma-5"
                      rounded
                      color="blue lighten-1"
                      @click="locationSubmit"
                      v-else
                    >GO!</v-btn>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-form>
          </card>
          <v-divider class="mx-4" />
        </v-flex>

        <v-flex xs12 md8>
          <v-flex v-for="store in stores" :key="store.id" pa-4>
            <router-link
              :to="{ name: 'StoreDetail', params: {
              storeId: store.id,
              storeName: store.name,
              storeAddress: store.address,
              storeTel: store.tel
            }}"
            >
              <store-list-card
                :id="store.id"
                :name="store.name"
                :categories="store.categories"
                :address="store.address"
                :tel="store.tel"
              />
            </router-link>
          </v-flex>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import Card from "@/components/Card";
import router from "@/router";
import StoreListCard from "@/components/StoreListCard";
import { mapState, mapActions } from "vuex";
import axios from "axios";
export default {
  components: {
    Card,
    StoreListCard
  },
  data: () => ({
    storeName: "",
    loading: true,
    lon: 0,
    lat: 0,
    location: 1,
    sort_value: ""
  }),
  watch: {
    sort_value: function() {
      if (this.sort_value == "주변검색") {
        this.getLocation();
        this.loading = false;
      } else {
        this.noLocation();
      }
    }
  },
  computed: {
    ...mapState({
      stores: state => state.data.storeSearchList,
      page: state => state.data.storeSearchPage
    })
  },
  methods: {
    ...mapActions("data", ["getStores"]),
    ...mapActions("data", ["searchByLocation"]),
    onSubmit: async function() {
      const params = {
        name: this.storeName,
        page: 1,
        append: false
      };
      await this.getStores(params);
      this.loading = false;
    },
    loadMore: async function() {
      this.loading = true;
      const params = {
        name: this.storeName,
        page: this.page,
        append: true
      };
      if (this.location) {
        await this.getStores(params);
        setTimeout(() => {
          this.loading = false;
        }, 1000);
      }
    },
    getLocation() {
      const that = this;
      navigator.geolocation.getCurrentPosition(function(pos) {
        console.log(pos.coords.longitude, pos.coords.latitude);
        that.lat = pos.coords.latitude;
        that.lon = pos.coords.longitude;
        that.location = 0;
      });
    },
    noLocation() {
      this.location = 1;
    },
    locationSubmit: async function() {
      const params = {
        latitude: this.lat,
        longitude: this.lon,
        words: this.storeName
      };
      await this.searchByLocation(params);
    }
  }
};
</script>
<style scoped>
</style>