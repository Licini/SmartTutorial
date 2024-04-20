import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import "vuetify/dist/vuetify.min.css"; // Add this line

Vue.use(Vuetify);

const opts = {
    theme: {
      dark: false
    },
    options: {
      customProperties: true
    },
    icons: {
      iconfont: "mdi"
    }
  };
  
  export default new Vuetify(opts);