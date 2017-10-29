<template>

  <div id="languageSelector" class="dropdown  is-right is-hoverable">
    <div class="dropdown-trigger">
      <button class="button is-outlined" aria-haspopup="true" aria-controls="dropdown-menu">
        <span>{{ current_language }}</span>
        <span class="icon is-small">
          <i class="fa fa-angle-down" aria-hidden="true"></i>
        </span>
      </button>
    </div>

    <div class="dropdown-menu" id="dropdown-menu-language" role="menu">
      <div class="dropdown-content">
        <div class="dropdown-item">
            <a href="#" @click="changeLanguage('en-us')">
            en-us
            </a>
        </div>
        <div class="dropdown-item">
            <a href="#" @click="changeLanguage('fr-ca')">
            fr-ca
            </a>
        </div>
      </div>
      
    </div>

  </div>

</template>

<script>
  export default {
    name: 'LanguageSelector',
    data: function () {
      return {
        // ...
      }
    },
    created: function () {
      // this.fetchData()çç
    },
    computed: {
      current_language: function () {
        return this.$i18n.locale
      }
    },
    methods: {
      changeLanguage: function (lang) {
        this.$i18n.locale = lang
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    #languageSelector button
    {
        width: 90px;
    }
    #dropdown-menu-language
    {
        width: 90px;
        min-width: 0px;
    }
</style>