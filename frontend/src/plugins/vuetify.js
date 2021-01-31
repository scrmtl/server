import Vue from "vue";
import Vuetify from "vuetify/lib";

Vue.use(Vuetify);

const vuetify = new Vuetify({
  theme: {
    themes: {
      light: {
        primary: "#6441A4",
        secondary: "#424242",
        accent: "#82B1FF",
        error: "#FF5252",
        info: "#2196F3",
        success: "#4CAF50",
        warning: "#FFC107",
        appbar: "#2E4057",
        navbar: "#6441A4",
        tabbody: "#2E4057",
        border: "#00BFA5",
        lanbody: "#FFFFfF",
        card_head: "#6441A4",
        highlight: "#C3F73A",
        link: "#31AA96",
        task: "#999C96",
        frontend: "#6441A4",
        backend: "#2E4057",
        ui_ux: "#31AA96",
        bug: "#FF5252",
      },
    },
  },
});

export default vuetify;
