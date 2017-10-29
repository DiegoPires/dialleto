import Vue from 'vue'
import Router from 'vue-router'
import Word from '@/components/Dictionary/Word'
import WordAdd from '@/components/Dictionary/Add'

Vue.use(Router)

// https://forum-archive.vuejs.org/topic/5277/replace-route-mapping-in-vue-router-2-x/3

export default new Router({
  routes: [
    {
      path: '/word/:word?',
      name: 'Word',
      component: Word
    },
    {
      path: '/add',
      name: 'WordAdd',
      component: WordAdd
    },
    {
      path: '/random',
      name: 'Random',
      redirect: '/word'
    },
    {
      path: '*',
      redirect: '/word/404'
    }
  ]
})
