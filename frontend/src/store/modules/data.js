import api from "../../api";
import router from "../../router"

// initial state
const state = {
  storeSearchList: [],
  storeSearchPage: "1",
  userReviewPage: "1",

  store: {
    id: "",
    name: "",
    branch: "",
    area: "",
    tel: "",
    address: "",
    lat: 0.0,
    lng: 0.0,
    categories: []
  },

  userReviewList: [],
  reviewListForCate: [],
  isloggined: false,
  onRegisterFlag: false,
  categoryList: []
};

// actions
const actions = {
  // 암호화함수
  SHA256({
    commit
  }, s) {
    var chrsz = 8;
    var hexcase = 0;

    function safe_add(x, y) {
      var lsw = (x & 0xFFFF) + (y & 0xFFFF);
      var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
      return (msw << 16) | (lsw & 0xFFFF);
    }

    function S(X, n) {
      return (X >>> n) | (X << (32 - n));
    }

    function R(X, n) {
      return (X >>> n);
    }

    function Ch(x, y, z) {
      return ((x & y) ^ ((~x) & z));
    }

    function Maj(x, y, z) {
      return ((x & y) ^ (x & z) ^ (y & z));
    }

    function Sigma0256(x) {
      return (S(x, 2) ^ S(x, 13) ^ S(x, 22));
    }

    function Sigma1256(x) {
      return (S(x, 6) ^ S(x, 11) ^ S(x, 25));
    }

    function Gamma0256(x) {
      return (S(x, 7) ^ S(x, 18) ^ R(x, 3));
    }

    function Gamma1256(x) {
      return (S(x, 17) ^ S(x, 19) ^ R(x, 10));
    }

    function core_sha256(m, l) {

      var K = new Array(0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1,
        0x923F82A4, 0xAB1C5ED5, 0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3,
        0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174, 0xE49B69C1, 0xEFBE4786,
        0xFC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
        0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147,
        0x6CA6351, 0x14292967, 0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13,
        0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85, 0xA2BFE8A1, 0xA81A664B,
        0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
        0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A,
        0x5B9CCA4F, 0x682E6FF3, 0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208,
        0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2);

      var HASH = new Array(0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F,
        0x9B05688C, 0x1F83D9AB, 0x5BE0CD19);

      var W = new Array(64);
      var a, b, c, d, e, f, g, h;
      var T1, T2;

      m[l >> 5] |= 0x80 << (24 - l % 32);
      m[((l + 64 >> 9) << 4) + 15] = l;

      for (let i = 0; i < m.length; i += 16) {
        a = HASH[0];
        b = HASH[1];
        c = HASH[2];
        d = HASH[3];
        e = HASH[4];
        f = HASH[5];
        g = HASH[6];
        h = HASH[7];

        for (let j = 0; j < 64; j++) {
          if (j < 16) W[j] = m[j + i];
          else W[j] = safe_add(safe_add(safe_add(Gamma1256(W[j - 2]), W[j - 7]), Gamma0256(W[j - 15])), W[j - 16]);

          T1 = safe_add(safe_add(safe_add(safe_add(h, Sigma1256(e)), Ch(e, f, g)), K[j]), W[j]);
          T2 = safe_add(Sigma0256(a), Maj(a, b, c));

          h = g;
          g = f;
          f = e;
          e = safe_add(d, T1);
          d = c;
          c = b;
          b = a;
          a = safe_add(T1, T2);
        }

        HASH[0] = safe_add(a, HASH[0]);
        HASH[1] = safe_add(b, HASH[1]);
        HASH[2] = safe_add(c, HASH[2]);
        HASH[3] = safe_add(d, HASH[3]);
        HASH[4] = safe_add(e, HASH[4]);
        HASH[5] = safe_add(f, HASH[5]);
        HASH[6] = safe_add(g, HASH[6]);
        HASH[7] = safe_add(h, HASH[7]);
      }
      return HASH;
    }

    function str2binb(str) {
      var bin = Array();
      var mask = (1 << chrsz) - 1;
      for (let i = 0; i < str.length * chrsz; i += chrsz) {
        bin[i >> 5] |= (str.charCodeAt(i / chrsz) & mask) << (24 - i % 32);
      }
      return bin;
    }

    function Utf8Encode(string) {
      string = string.replace(/\r\n/g, "\n");
      var utftext = "";

      for (var n = 0; n < string.length; n++) {

        var c = string.charCodeAt(n);

        if (c < 128) {
          utftext += String.fromCharCode(c);
        } else if ((c > 127) && (c < 2048)) {
          utftext += String.fromCharCode((c >> 6) | 192);
          utftext += String.fromCharCode((c & 63) | 128);
        } else {
          utftext += String.fromCharCode((c >> 12) | 224);
          utftext += String.fromCharCode(((c >> 6) & 63) | 128);
          utftext += String.fromCharCode((c & 63) | 128);
        }

      }

      return utftext;
    }

    function binb2hex(binarray) {
      var hex_tab = hexcase ? "0123456789ABCDEF" : "0123456789abcdef";
      var str = "";
      for (let i = 0; i < binarray.length * 4; i++) {
        str += hex_tab.charAt((binarray[i >> 2] >> ((3 - i % 4) * 8 + 4)) & 0xF) +
          hex_tab.charAt((binarray[i >> 2] >> ((3 - i % 4) * 8)) & 0xF);
      }
      return str;
    }

    s = Utf8Encode(s);
    return binb2hex(core_sha256(str2binb(s), s.length * chrsz));

  },

  async getStores({
    commit
  }, params) {
    const append = params.append;
    const resp = await api.getStores(params);
    // console.log(resp)
    const stores = resp.data.results.map(d => ({
      id: d.id,
      name: d.store_name,
      branch: d.branch,
      area: d.area,
      tel: d.tel,
      address: d.address,
      lat: d.latitude,
      lng: d.longitude,
      categories: d.category_list
    }));

    if (append) {
      commit("addStoreSearchList", stores);
    } else {
      commit("setStoreSearchList", stores);
    }
    commit("setStoreSearchPage", resp.data.next);
  },

  async getUserReview({
    commit
  }, params) {
    // console.log(params["page"])
    if (params["page"] == false) {
      return
    }
    const append = params.append;
    // console.log(append)
    // console.log("data upper ", params)
    const resp = await api.getUserReview(params);
    // console.log(resp.data)
    var reviews = []
    if (resp.data.results == false) {
      commit("setUserReviewList", reviews)
      return
    }

    var sysdate = new Date(resp.data.results[0].reg_time)
    // console.log(sysdate)
    function date_to_str(format) {
      var year = format.getFullYear();
      var month = format.getMonth() + 1;
      if (month < 10) month = '0' + month;
      var date = format.getDate();
      if (date < 10) date = '0' + date;
      var hour = format.getHours();
      if (hour < 10) hour = '0' + hour;
      var min = format.getMinutes();
      if (min < 10) min = '0' + min;
      var sec = format.getSeconds();
      if (sec < 10) sec = '0' + sec;
      return year + "-" + month + "-" + date + " " + hour + ":" + min + ":" + sec;
    }
    sysdate = date_to_str(sysdate)

    reviews = resp.data.results.map(d => ({
      id: d.id,
      store: d.store,
      store_name: d.store_name,
      user: d.user,
      score: d.score,
      content: d.content,
      reg_time: sysdate,
      categories: d.category_list
    }));

    if (append) {
      commit("addUserReviewList", reviews);
    } else {
      commit("setUserReviewList", reviews);
    }
    commit("setUserReviewPage", resp.data.next);
  },

  async getReviewsForCate({
    commit
  }, params) {
    // console.log(params)
    const resp = await api.getUserReview(params);
    // console.log(resp)
    var reviews = []
    if (resp.data.results == false) {
      commit("setReviewListForCate", reviews)
      return
    }
    reviews = resp.data.results.map(d => ({
      categories: d.category_list
    }));
    // console.log("asdasd", reviews)
    commit("setReviewListForCate", reviews)
  },

  resetCategoryList({
    commit
  }) {
    state.categoryList = []
  },

  async getReviewByCategory({
    commit
  }, params) {
    const resp = await api.getUserReview(params["params"]);
    const tmp = []
    const catelist = state.categoryList
    // console.log(catelist)
    const word = params["word"]
    let idx = catelist.indexOf(word)
    let flag = true

    if (idx == -1) {
      catelist.push(word)
    } else {
      catelist.splice(idx, 1)
      flag = false
    }
    if (flag == true) {
      if (catelist.length == 1) {
        let cnt = 0
        for (let i = 0; i < resp.data.results.length; ++i) {
          for (let j = 0; j < resp.data.results[i].category_list.length; ++j) {
            if (resp.data.results[i].category_list[j] == word) {
              let a = resp.data.results[i]
              a["idx"] = cnt
              cnt += 1
              // console.log(a)
              tmp.push(resp.data.results[i])
            }
          }
        }
        commit("setUserReviewList", tmp)
      } else {
        let a = state.userReviewList.length - 1
        let cnt = state.userReviewList[a].idx + 1
        // console.log(cnt)
        for (let i = 0; i < resp.data.results.length; ++i) {
          for (let j = 0; j < resp.data.results[i].category_list.length; ++j) {
            if (resp.data.results[i].category_list[j] == params["word"]) {
              resp.data.results[i]["idx"] = cnt
              cnt += 1
              tmp.push(resp.data.results[i])
              for (let k = 0; k < state.userReviewList.length; ++k) {
                if (resp.data.results[i].id == state.userReviewList[k].id) {
                  tmp.splice(tmp.length - 1, 1)
                }
              }
            }
          }
        }
        commit("addUserReviewList", tmp)
      }
    } else {
      // console.log(state.userReviewList[0].category_list)
      let idxlst = []
      for (let i = 0; i < state.userReviewList.length; ++i) {
        for (let j = 0; j < state.userReviewList[i].category_list.length; ++j) {
          if (state.userReviewList[i].category_list[j] == word) {
            // state.userReviewList.splice(i, 1)
            idxlst.push(i)
          }
        }
      }
      // console.log(idxlst)

      for (let i = 0; i < idxlst.length; ++i) {
        for (let j = 0; j < state.userReviewList.length; ++j) {
          if (state.userReviewList[j].idx == idxlst[i]) {
            state.userReviewList.splice(j, 1)
          }
        }
      }

      let cnt = 0
      for (let i = 0; i < state.userReviewList.length; ++i) {
        state.userReviewList[i].idx = cnt
        cnt += 1
      }
    }
    // console.log(state.userReviewList)
  },

  sortReviewByScore({
    commit
  }) {
    const tmp = state.userReviewList
    let cnt = 0
    tmp.sort(function (first, second) {
      return second["score"] - first["score"];
    })
    for (let i = 0; i < state.userReviewList.length; ++i) {
      state.userReviewList[i].idx = cnt
      cnt += 1
    }
  },

  sortReviewByTime({
    commit
  }, value) {
    const tmp = state.userReviewList
    let cnt = 0
    // console.log(tmp)
    // console.log(value)
    function date_latest(a, b) {
      var dateA = new Date(a["reg_time"]).getTime()
      var dateB = new Date(b["reg_time"]).getTime()
      return dateA < dateB ? 1 : -1
    }

    function date_oldest(a, b) {
      var dateA = new Date(a["reg_time"]).getTime()
      var dateB = new Date(b["reg_time"]).getTime()
      return dateA > dateB ? 1 : -1
    }
    if (value == "latest") {
      tmp.sort(date_latest)
    } else {
      tmp.sort(date_oldest)
    }
    for (let i = 0; i < state.userReviewList.length; ++i) {
      state.userReviewList[i].idx = cnt
      cnt += 1
    }
  },

  async register({
    commit
  }, params) {
    // console.log(params)
    let check = false
    await api.register(params)
      .then(res => {
        if (res.status == 201) {
          alert("인증 이메일을 발송하였습니다. 확인해주세요.")
          // console.log(res)
          check = true
          // localStorage.setItem("token", res.data.token)
          // localStorage.setItem("pk", res.data.user.pk)
          // localStorage.setItem("username", res.data.user.username)
          // localStorage.setItem("email", res.data.user.email)
          // localStorage.setItem("gender", res.data.user.gender)
          // localStorage.setItem("age", res.data.user.age)
          // localStorage.setItem("review_count", res.data.user.review_count)
          router.push("/")
        }
      })
      .catch(err => {
        // alert("문제가 생겼당")
        // console.log(err)
        if (err.response.data.username && err.response.data.email) {
          alert("아이디와 이메일이 중복되었습니다.")
        } else if (err.response.data.username) {
          alert("아이디가 중복되었습니다.")
        } else if (err.response.data.email) {
          alert("이메일이 중복되었습니다.")
        }
        console.log(err.response)
      })
    // commit("setIsLoggined", check)
  },

  async login({
    commit
  }, params) {
    // console.log(params)
    let flag = false
    let check = false
    await api.login(params)
      .then(res => {
        if (res.status == 200) {
          // console.log(res)
          flag = true
          check = true
          localStorage.setItem("token", res.data.token)
          localStorage.setItem("pk", res.data.user.pk)
          localStorage.setItem("username", res.data.user.username)
          localStorage.setItem("email", res.data.user.email)
          localStorage.setItem("gender", res.data.user.gender)
          localStorage.setItem("age", res.data.user.age)
          localStorage.setItem("review_count", res.data.user.review_count)
          router.push("/search")
        }
      })
      .catch(err => {
        if (err.response.data.non_field_errors[0] == "이메일 주소가 확인되지 않았습니다.") {
          alert("이메일 인증을 해주세요")
        } else {
          alert("아이디와 비밀번호를 확인해 주세요")
        }
        // console.log(err)
        // console.log(err.response.data.non_field_errors[0] == "이메일 주소가 확인되지 않았습니다.")
      })
    commit("setIsLoggined", check)
    return flag
  },

  logout({
    commit
  }) {
    let check = false
    localStorage.clear()
    router.push("/")
    commit("setIsLoggined", check)
  },

  checkRegister({
    commit
  }) {
    // console.log(state.onRegisterFlag)
    let check = true
    if (state.onRegisterFlag == false) {
      // console.log(check)
      // console.log(state.onRegisterFlag)
      commit("setOnRegisterFlag", check)
    } else {
      check = false
      // console.log(check)
      // console.log(state.onRegisterFlag)
      commit("setOnRegisterFlag", check)
    }
  },

  checkLogin({
    commit
  }) {
    let check = false
    if (localStorage.getItem("pk")) {
      check = true
      commit("setIsLoggined", check)
    }
  },

  async reviewEditByUser({
    commit
  }, params) {
    // console.log(params["id"])
    // console.log(params)
    await api.reviewUpdate(params)
      .then(res => {
        // console.log(res)
      })
      .catch(err => {
        console.log(err)
      })
  },

  async reviewDeleteByUser({
    commit
  }, params) {
    await api.reviewDelete(params)
      .then(res => {
        // console.log(res)
        for (let i = 0; i < state.userReviewList.length; ++i) {
          if (state.userReviewList[i].id == params) {
            state.userReviewList.splice(i, 1)
            return
          }
        }
      })
      .catch(err => {
        console.log(err)
      })
  },
  async searchByLocation({
    commit
  }, params) {
    const resp = await api.getStoresByLocation(params);
    const stores = resp.data.map(d => ({
      id: d.id,
      name: d.store_name,
      branch: d.branch,
      area: d.area,
      tel: d.tel,
      address: d.address,
      lat: d.latitude,
      lng: d.longitude,
      categories: d.category_list
    }));
    commit("setStoreSearchList", stores)
  },
};

// mutations
const mutations = {
  setStoreSearchList(state, stores) {
    state.storeSearchList = stores.map(s => s);
  },
  addStoreSearchList(state, stores) {
    state.storeSearchList = state.storeSearchList.concat(stores);
  },
  setStoreSearchPage(state, url) {
    state.storeSearchPage = new URL(url).searchParams.get("page");
  },
  setUserReviewList(state, reviews) {
    state.userReviewList = reviews.map(s => s);
  },
  addUserReviewList(state, reviews) {
    state.userReviewList = state.userReviewList.concat(reviews);
  },
  setUserReviewPage(state, url) {
    // console.log(url)
    // console.log(new URL(url).searchParams.get("page"))
    // state.userReviewPage = new URL(url).searchParams.get("page");
    if (url != null) {
      state.userReviewPage = new URL(url).searchParams.get("page");
    } else {
      state.userReviewPage = false
    }
  },
  setReviewListForCate(state, reviews) {
    state.reviewListForCate = reviews.map(s => s)
  },
  setIsLoggined(state, check) {
    state.isloggined = check
  },
  setOnRegisterFlag(state, check) {
    state.onRegisterFlag = check
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};