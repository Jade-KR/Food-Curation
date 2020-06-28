<template>
  <div>
    <div id="regi_box">
      <div id="regi_title">Food Tailor</div>
      <div id="regi_desc">오직 당신 한 사람을 위한,</div>
      <div id="regi_back" @click="goHome()">혹시 이미 회원이신가요?</div>
      <hr style="width: 80%; margin: 20px auto; border: 0.5px solid black;" />
      <div id="regi_body">
        <ValidationObserver ref="obs" v-slot="{ invalid, validated }">
          <ValidationProvider name="id" rules="required|alpha_num|max:15">
            <div slot-scope="{ errors }">
              <v-text-field
                v-model="userInfo.username"
                label="ID"
                :error-messages="errors[0] ? errors[0] : []"
                color="black"
              />
            </div>
          </ValidationProvider>

          <ValidationProvider name="email" rules="required|email|max:50">
            <div slot-scope="{ errors }">
              <v-text-field
                v-model="userInfo.email"
                label="Email"
                :error-messages="errors[0] ? errors[0] : []"
                color="black"
              />
            </div>
          </ValidationProvider>

          <ValidationProvider
            name="password"
            vid="pwd_confirmation"
            rules="required|password|min:8|max:100"
          >
            <div slot-scope="{ errors }">
              <v-text-field
                v-model="userInfo.password1"
                label="Password"
                :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                :error-messages="errors[0] ? errors[0] : []"
                :type="show1 ? 'text' : 'password'"
                color="black"
                @click:append="show1 = !show1"
              />
            </div>
          </ValidationProvider>

          <ValidationProvider name="password_check" rules="required|confirmed:pwd_confirmation">
            <div slot-scope="{ errors }">
              <v-text-field
                v-model="userInfo.password2"
                label="Password_check"
                :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                :error-messages="errors[0] ? errors[0] : []"
                :type="show2 ? 'text' : 'password'"
                color="black"
                @click:append="show2 = !show2"
              />
            </div>
          </ValidationProvider>

          <v-menu
            ref="calender"
            v-model="calender"
            :close-on-content-click="false"
            transition="scale-transition"
            offset-y
            max-width="290px"
            min-width="290px"
          >
            <template v-slot:activator="{ on }">
              <ValidationProvider name="birth" rules="required|date">
                <div slot-scope="{ errors }">
                  <v-text-field
                    v-model="dateFormatted"
                    label="Birth"
                    :error-messages="errors[0] ? errors[0] : []"
                    color="black"
                    @blur="date = parseDate(dateFormatted)"
                    v-on="on"
                  />
                </div>
              </ValidationProvider>
            </template>
            <v-date-picker v-model="date" no-title @input="calender = false" />
          </v-menu>

          <ValidationProvider name="gender" rules="required">
            <div slot-scope="{ errors }">
              <v-container fluid>
                <v-radio-group
                  v-model="userInfo.gender"
                  row
                  :error-messages="errors[0] ? errors[0] : []"
                >
                  <v-radio label="Male" value="남" color="black" />
                  <v-radio label="Female" value="여" color="black" />
                </v-radio-group>
              </v-container>
            </div>
          </ValidationProvider>

          <v-btn
            dark
            color="black"
            :disabled="invalid || !validated"
            :loading="isloading"
            style="width: 100%;"
            @click="onSubmit()"
          >submit</v-btn>
        </ValidationObserver>
      </div>
    </div>
  </div>
</template>

<script>
import { ValidationProvider, ValidationObserver } from "vee-validate";
import { mapState, mapActions } from "vuex";
import router from "../router";

export default {
  components: {
    ValidationProvider,
    ValidationObserver
  },
  data() {
    vm => ({
      dateFormatted: vm.formatDate(new Date().toISOString().substr(0, 10)),
      date: new Date().toISOString().substr(0, 10)
    });
    return {
      userInfo: {
        username: "",
        email: "",
        password1: "",
        password2: "",
        age: "",
        gender: ""
      },
      // password_check: "",
      show1: false,
      show2: false,
      calender: false,
      date: "",
      dateFormatted: "",
      isloading: false
    };
  },
  computed: {
    computedDateFormatted() {
      return this.formatDate(this.date);
    }
  },
  watch: {
    date(val) {
      this.dateFormatted = this.formatDate(this.date);
    }
  },
  methods: {
    ...mapActions("data", ["register"]),
    ...mapActions("data", ["SHA256"]),
    async onSubmit() {
      this.isloading = true;
      let age = 2021 - this.date.slice(0, 4);
      // console.log(this.userInfo)
      let hash_password = "";
      await this.SHA256(String(this.userInfo.password1)).then(res => {
        hash_password = res;
      });
      const params = {
        username: this.userInfo.username,
        email: this.userInfo.email,
        password1: hash_password,
        password2: hash_password,
        age: age,
        gender: this.userInfo.gender
      };
      // console.log(params)
      await this.register(params);
      this.isloading = false;
    },
    formatDate(date) {
      if (!date) return null;
      const [year, month, day] = date.split("-");
      return `${year}/${month}/${day}`;
    },
    parseDate(date) {
      if (!date) return null;
      const [year, month, day] = date.split("/");
      return `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`;
    },
    goHome() {
      router.push("/");
    }
  }
};
</script>

<style scoped>
#regi_box {
  width: 600px;
  margin: 0 auto;
  text-align: center;
  padding: 20px;
}
#regi_title {
  font-size: 60px;
  color: black;
}
#regi_desc {
  font-size: 24px;
  color: black;
}
#regi_back {
  color: black;
  margin: 10px auto 0 auto;
  cursor: pointer;
  width: 200px;
}
#regi_body {
  width: 80%;
  margin: 0 auto;
}
#regi_body
  > span
  > span:nth-child(1)
  > div
  > div
  > div
  > div.v-input__slot
  > div
  > label {
  color: white;
}
#regi_body > span > span:nth-child(5) > div > div {
  padding: 0;
}
#regi_body > span > span:nth-child(7) > div > div > div {
  justify-content: center;
}
</style>