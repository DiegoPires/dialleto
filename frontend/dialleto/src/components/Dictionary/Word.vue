<template>
  
  <div class="container">
    <h1 class="title">
      Word
    </h1>
  
    <definition v-bind:definition="word.definition"></definition>

    
  </div>
</template>

<script>
import Definition from './Definition'

export default {
  name: 'Word',
  data: function () {
    return {
      word: {}
    }
  },
  created: function () {
    this.fetchData()
  },
  methods: {
    fetchData: function (route) {
      this.word = {
        'definition': {
          'text': 'sad asdasd sadsasad s d asdasd assa dsad dasd as dsa dasdasd as dasd asd asdas das adssad asdsaad asdasd sadsasad s d asdasd assa dsad dasd as dsa dasdasd as dasd asd asdas das adssad asdsa'
        }
      }
    }
  },
  watch: {
    '$route' (to, from) {
      this.fetchData(to)
    }
  },
  components: {
    'definition': Definition
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
