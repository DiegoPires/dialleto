<template>

  <div class="container">
    <h1 class="title">
      {{ $t('word.add.title') }}
    </h1>

    <div class="field">
      <div class="control has-icons-left">
        <input type="text" class="input is-large" v-bind:placeholder="$t('word.add.word')">
        <span class="icon is-small is-left">
          <i class="fa fa-book"></i>
        </span>
      </div>
    </div>

    <div class="field">
      <label class="label">{{ $t('word.add.definition') }}</label>
      <div class="control">
        <textarea class="textarea" v-bind:placeholder="$t('word.add.definition')"></textarea>
      </div>
    </div>

    <div class="field">
      <label class="label">{{ $t('word.add.example') }}</label>
      <div class="control">
        <textarea class="textarea" rows=2 v-bind:placeholder="$t('word.add.example')"></textarea>
      </div>
    </div>

    <div class="field">
      <label class="label">{{ $t('word.add.tags') }}</label>
      <div class="control">
        <textarea class="textarea" rows=2 v-bind:placeholder="$t('word.add.tags')"></textarea>
      </div>
    </div>

    <div class="field is-grouped">
      <div class="control">
        <button class="button is-large is-inverted is-link">Submit</button>
      </div>
      <div class="control">
        <button class="button is-large is-text">Cancel</button>
      </div>
    </div>

  </div>
</template>

<script>
  export default {
    name: 'Contact',
    data: function () {
      return {
        // ...
      }
    },
    methods: {
      // nothing yet
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->

<style scoped>
</style>