<template>
  
    <article class="media">
      
      <div class="media-content">
        <div class="content text">
          
          <p>{{definition.text}}</p>
          
        </div>
        <nav class="level is-mobile">
          <div class="level-left">

            <a class="level-item">
              <span class="fa fa-thumbs-up fa-lg"> </span> &nbsp; 123 
            </a>

            <a class="level-item">
              <span class="fa fa-thumbs-down fa-lg"></span> &nbsp; 123 
            </a>

            <p class="level-item">|&nbsp;<strong>Related:</strong></p>
            
            <router-link :to="{ params : { word : 'whatever' } }" class="level-item" style="border-bottom:2px solid red">
              Calice
            </router-link>
            <router-link to="word" style="border-bottom:2px solid blue">
              fuck
            </router-link>
            
          </div>
        </nav>
      </div>
      <!--div class="media-right">
        <button class="delete"></button>
      </div-->
    </article>
 
</template>

<script>
export default {
  name: 'Definition',
  props: ['definition']
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .text {
    text-align: justify;
  }
</style>
