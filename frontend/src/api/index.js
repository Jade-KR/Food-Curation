// import axios from "axios";
import http from "./http"

const apiUrl = "/api";
const regiUrl = "/rest-auth";

export default {
  getStores(params) {
    return http.get(`${apiUrl}/stores`, {
      params
    });
  },
  getUserReview(params) {
    // console.log("api index ", params.user_id)
    return http.get(`${apiUrl}/user_reviews`, {
      params
    });
  },
  register(params) {
    // console.log(params)
    return http.post(`${regiUrl}/registration/`, params)
  },
  login(params) {
    return http.post(`${apiUrl}/login/`, params)
  },
  reviewDelete(params) {
    return http.delete(`${apiUrl}/user_reviews/${params}`)
  },
  reviewUpdate(params) {
    // console.log(params)
    return http.put(`${apiUrl}/user_reviews/${params["id"]}`, params)
  },
  getStoresByLocation(params) {
    return http.post(`${apiUrl}/search_store`, params)
  }
};