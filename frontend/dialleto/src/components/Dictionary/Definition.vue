<template>
  
    <article class="media">
      <figure class="media-left">
        
        <ul class="rating">
            <li><a href="#"><span class="fa fa-chevron-up" aria-hidden="true"></span></a></li>
            <li>0</li>
            <li><a href="#"><span class="fa fa-chevron-down" aria-hidden="true"></span></a></li>
        </ul>
        
      </figure>
      <div class="media-content">
        <div class="content">
          
          <p>{{definition.text}}</p>
          
        </div>
        <nav class="level is-mobile">
          <div class="level-left">

            <p class="level-item"><strong>Related:</strong></p>
                

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

</style>
