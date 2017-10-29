import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const i18n = new VueI18n({
  locale: 'en-us',
  messages: {
    'en-us': require('./en-us.json'),
    'pt-br': require('./pt-br.json'),
    'fr-ca': require('./fr-ca.json')
  }
})

if (module.hot) {
  module.hot.accept(['./en-us.json', './pt-br.json', './fr-ca.json'], () => {
    i18n.setLocaleMessage('en-us', require('./en-us.json'))
    i18n.setLocaleMessage('pt-br', require('./pt-br.json'))
    i18n.setLocaleMessage('fr-ca', require('./fr-ca.json'))
    console.log('hot reload', this, arguments)
  })
}

export default i18n
