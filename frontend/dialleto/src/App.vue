<template>
  <div id="app">
    <section class="hero is-success is-fullheight">
      
      <div class="hero-head">
        <nav class="navbar">
          <div class="container">
            <div class="navbar-brand">
              <router-link to="/random" class="navbar-item is-capitalized has-text-weight-bold is-size-3">
                Dialleto
              </router-link>
              <span class="navbar-burger burger" data-target="navbarMenuHeroA">
                <span></span>
                <span></span>
                <span></span>
              </span>
            </div>
            <div id="navbarMenuHeroA" class="navbar-menu">
              <div class="navbar-end">
                
                <router-link to="/add" v-bind:title=" $t('menu.add') " class="navbar-item">
                  <span class="icon">
                    <i class="fa fa-plus fa-lg"></i>
                  </span>
                </router-link>
                <router-link to="/random" class="navbar-item">
                  <span class="icon">
                    <i class="fa fa-random fa-lg"></i>
                  </span>
                </router-link>

                 <span class="navbar-item">
                  <language-selector />
                </span>

              </div>
            </div>
          </div>
        </nav>
      </div>
      
      <div class="hero-body">
        <div class="container">
          
          <transition
            v-on:before-enter="beforeEnter"
            v-on:after-enter="afterEnter"
            v-on:before-leave="beforeLeave"
            v-on:after-leave="afterLeave">
            <router-view 
              :key="key"
              v-on:up="up"
              v-on:down="down"
              v-on:next="next"
              v-on:previous="previous" />
          </transition> 

          <vue-progress-bar></vue-progress-bar>
        </div>
      </div>

      <footer class="footer is-success">
        <div class="container">
          <div class="content has-text-centered">
            <div class="columns">
              <div class="column has-text-left">
                <router-link to="/contact">{{ $t("menu.contact")}}</router-link> | 
                <router-link to="/about">{{ $t("menu.about") }}</router-link> |
                <a href="https://www.facebook.com/dialletoDictionary/" target="_blank"><span class="fa fa-facebook-official fa-lg"></span></a>
              </div>
              <div class="column has-text-right">
                <strong>Dialleto</strong> by <a href="http://www.diegopires.com.br" target=_blank>Diego Silva Pires</a>.
                <span class="love">Made with <i class="fa fa-heart"></i> in Québec</span>
              </div>
            </div>
           
          </div>
        </div>
      </footer>
  </section>

  </div>
</template>

<script>
import LanguageSelector from './components/languageSelector'

export default {
  name: 'app',
  data () {
    return {
      transition: {
        in: 'fadeInLeftBig',
        out: 'fadeOutRightBig'
      }
    }
  },
  computed: {
    key () {
      return this.$route.params.word !== undefined
        ? this.$route.params.word
        : this.$route.name
    }
  },
  mounted () {
    //  [App.vue specific] When App.vue is finish loading finish the progress bar
    this.$Progress.finish()
  },
  created () {
    //  [App.vue specific] When App.vue is first loaded start the progress bar
    this.$Progress.start()
    //  hook the progress bar to start before we move router-view
    this.$router.beforeEach((to, from, next) => {
      //  does the page we want to go to have a meta.progress object
      if (to.meta.progress !== undefined) {
        let meta = to.meta.progress
        // parse meta tags
        this.$Progress.parseMeta(meta)
      }
      //  start the progress bar
      this.$Progress.start()
      //  continue to next page
      next()
    })
    //  hook the progress bar to finish after we've finished moving router-view
    this.$router.afterEach((to, from) => {
      //  finish the progress bar
      this.$Progress.finish()
    })
  },
  methods: {
    beforeEnter: function (el) {
      if (this.$route.params.word !== undefined) {
        el.className = 'animated ' + this.transition.in
      }
    },
    afterEnter: function (el) {
      if (this.$route.params.word !== undefined) {
        el.className = ''
      }
    },
    beforeLeave: function (el) {
      if (this.$route.params.word !== undefined) {
        el.className = 'animated position_abs ' + this.transition.out
      }
    },
    afterLeave: function (el) {
      if (this.$route.params.word !== undefined) {
        el.className = ''
      }
    },
    up: function () {
      this.transition.in = 'fadeInUpBig'
      this.transition.out = 'fadeOutUpBig'
    },
    down: function () {
      this.transition.in = 'fadeInDownBig'
      this.transition.out = 'fadeOutDownBig'
    },
    next: function () {
      this.transition.in = 'fadeInLeftBig'
      this.transition.out = 'fadeOutRightBig'
    },
    previous: function () {
      this.transition.in = 'fadeInRightBig'
      this.transition.out = 'fadeOutLeftBig'
    }
  },
  components: {
    'language-selector': LanguageSelector
  }
}
</script>

<style lang="css">
@import "https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.5.2/animate.min.css";  
</style>
<style lang="scss">
 
  $footer-background-color: hsl(141, 71%, 48%);
  @import 'src/assets/scss/custom.scss';
  .position_abs {
    position: absolute;
  }
  .footer { 
    padding: 1rem 1.5rem 1rem; 
  }
 
</style>
