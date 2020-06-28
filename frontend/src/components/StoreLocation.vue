<template>
  <div>
    <div id="map" style="width:100%;height:350px;"></div>
  </div>
</template>

<script>
export default {
  props: {
    longitude: Number,
    latitude: Number
  },
  data() {
    return {};
  },
  mounted() {
    setTimeout(() => {
      var mapContainer = document.getElementById("map"),
        mapOption = {
          center: new kakao.maps.LatLng(this.latitude, this.longitude),
          level: 3
        };
      var map = new kakao.maps.Map(mapContainer, mapOption);
      var markerPosition = new kakao.maps.LatLng(this.latitude, this.longitude);
      var marker = new kakao.maps.Marker({
        position: markerPosition
      });
      marker.setMap(map);
    }, 500);
  }
};
</script>

<style scoped>
</style>