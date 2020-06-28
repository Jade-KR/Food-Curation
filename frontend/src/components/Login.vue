<template>
  <div>
    <v-dialog v-model="dialog" width="35vw">
      <template v-slot:activator="{ on }">
        <div v-on="on">
          <slot name="click" />
        </div>
      </template>
      <v-card id="login_modal">
        <div id="login_title">Food Tailor</div>
        <div id="login_desc">당신의 품격을 높여드립니다</div>
        <hr style="width: 88%; margin: 20px auto; border: 0.5px solid;" />
        <form @keypress.enter="check()">
          <div id="login_inner">
            <v-text-field
              v-model="credential.username"
              label="ID"
              placeholder="  아이디를 입력해주세요"
              color="black"
            />
            <v-text-field
              v-model="credential.password"
              type="password"
              label="Password"
              placeholder="  비밀번호를 입력해주세요"
              color="black"
            />
          </div>
          <div class="login_footer">
            <v-btn dark color="rgba(0, 0, 0, 0.9)" class="login_btn" @click="check()">LOGIN</v-btn>
          </div>
        </form>
        <div id="divideLine">
          <hr style="width:37%; display:inline-block; margin-right:10px; border: 0.5px solid;" />
          <p style="display:inline;">또는</p>
          <hr style="width:37%; display:inline-block; margin-left:10px; border: 0.5px solid;" />
        </div>
        <div style="margin-bottom: 20px;">
          <v-btn color="rgba(255, 255, 0, 1)" class="login_btn" @click="check()">KAKAO</v-btn>
        </div>
        <div>
          계정이 없으신가요?
          <button style="color:blue;" @click="goRegi()">가입하기</button>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import router from "../router";
import { mapActions } from "vuex";

export default {
  data() {
    return {
      credential: {
        username: "",
        password: ""
      },
      dialog: false
    };
  },
  methods: {
    ...mapActions("data", ["login"]),
    ...mapActions("data", ["SHA256"]),
    async check() {
      if (this.credential.username && this.credential.password) {
        let hash_password = "";
        await this.SHA256(String(this.credential.password)).then(res => {
          hash_password = res;
        });
        const params = {
          username: this.credential.username,
          password: hash_password
        };
        // console.log(params)
        const tmp = await this.login(params)
        // console.log(tmp)
        if (tmp == true) {
          this.credential.username = "";
          this.credential.password = "";
          this.dialog = false;
        }
      } else {
        alert("아이디와 비밀번호를 확인해 주세요");
        this.dialog = true;
      }
    },
    goRegi() {
      router.push("/register");
      this.dialog = false;
    }
  }
};
</script>

<style scoped>
#login_modal {
  text-align: center;
  padding: 20px;
  background-color: rgba(221, 221, 221, 0.95);
}
#login_title {
  font-size: 50px;
  font-weight: 700;
}
#login_desc {
  font-size: 20px;
}
#login_inner {
  width: 28vw;
  margin: 0 auto;
}
#login_id {
  display: block;
  margin: 0 auto;
}
#login_pwd {
  display: block;
  margin: 0 auto;
}
.login_btn {
  width: 28vw;
  margin: 0 auto;
}
#divideLine {
  text-align: center;
  margin-top: 15px;
  margin-bottom: 15px;
}
</style>