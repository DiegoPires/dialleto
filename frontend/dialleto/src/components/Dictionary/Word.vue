<template>

  <div class="container">
    
    <div class="columns">
      <div class="column">
        <p class="level-item">
        <a @click="up"><span class="fa fa-chevron-up"></span></a>
        </p>
      </div>
    </div>

    <div class="columns is-vcentered">

      <div class="column ">
        <div class="media-left">
          <a  @click="previous" :key="1">
            <span class="fa fa-chevron-left"></span>
          </a>
        </div>
      </div>

      <div class="is-four-fifths">  
        
        <h1 class=title>Word</h1>
        <definition v-bind:definition="word.definition"></definition>
      
      </div>

      <div class="column">
        <div class="media-left">
          <a @click="next" >
            <span class="fa fa-chevron-right"></span>
          </a>
        </div>

      </div>

    </div>
      
    <div class="columns">
      <div class="column">
        <p class="level-item">
          <a @click="down"><span class="fa fa-chevron-down"></span></a>
        </p>
      </div>
    </div>

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
      },
      next: function () {
        this.naviguer('next')
      },
      previous: function () {
        this.naviguer('previous')
      },
      up: function () {
        this.naviguer('up')
      },
      down: function () {
        this.naviguer('down')
      },
      naviguer: function (ou) {
        this.$emit(ou)
        this.$router.push({
          name: 'Word',
          params: {
            'word': ou
          }
        })
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
  .columns.is-vcentered {
  -webkit-box-align: center;
     -ms-flex-align: center;
        align-items: center;
}
</style>
