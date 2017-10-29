// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import i18n from './i18n'
import VueProgressBar from 'vue-progressbar'
import store from './store'

Vue.config.productionTip = false

Vue.use(VueProgressBar, {
  color: 'rgb(10, 146, 92)',
  failedColor: 'red',
  thickness: '7px'
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  i18n,
  store,
  template: '<App/>',
  components: { App }
})
