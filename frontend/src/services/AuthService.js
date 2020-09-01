import axios from 'axios';

const url = 'https://scrmtl.ddns.net/';

export default {
  login(credentials) {
    return axios
      .request({
        url: "o/token/",
        method: "post",
        baseURL: "https://scrmtl.ddns.net/",
        auth: {
          username: "ttLwLjOKoJWtm5NDRRfGbgfioDhS7hwGZ0iaAzzD",
          password: "SPWysYuxLcr4ju0ITzqKASIQObiWaaUQbKb4ofYgJTv2QmkFSqfgroR3GIOg1QH41okgg0UHPh3gbTUiXuKKuj85Qy241hyBrn851v6eTVOpRujVWzZZP3npTki1Znnc"
        },
        data:
          "grant_type=password&username=" +
          credentials.username +
          "&password=" +
          credentials.password +
          "&scope=write"
      })
      .then(response => response.data);
  },
  signUp(credentials) {
    return axios
      .post(url + 'sign-up/', credentials)
      .then(response => response.data);
  },
  getSecretContent() {
    return axios.get(url + 'secret-route/').then(response => response.data);
  }
};