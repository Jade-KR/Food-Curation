<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="500">
      <template v-slot:activator="{ on }">
        <i class="fas fa-edit" v-on="on"></i>
      </template>

      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title>리뷰 수정</v-card-title>
        <textarea type="text" v-model="eContent" value="hhh">content</textarea>
        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn color="primary" text @click="editDone">수정</v-btn>
          <v-btn color="red" text @click="dialog = false">취소</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from "axios";
export default {
  props: {
    reviewId: Number,
    content: String
  },
  data() {
    return {
      dialog: false,
      eContent: this.content,
      score: 3
    };
  },
  methods: {
    editDone() {
      axios
        .put(
          `http://i02d106.p.ssafy.io:8765/api/store_reviews/${this.reviewId}`,
          {
            score: this.score,
            content: this.eContent
          }
        )
        .then(this.$emit("editReview"))
        .then((this.dialog = false));
    }
  }
};
</script>

<style scoped>
i:hover {
  font-size: 18px;
  cursor: pointer;
}
textarea {
  width: 100%;
  height: 200px;
  padding-left: 20px;
  padding-right: 20px;
}
</style>