<template>

  <div id="app">

    <!-- <v-app-bar flat height="120" class="title" app> 
      <h4>Smart Docs for Github Repository</h4>
    </v-app-bar> -->

    <ChatBox />

  </div>

</template>

<script>
import ChatBox from './components/ChatBox.vue'

export default {
  name: 'App',
  components: {
    ChatBox
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.title {
  /* background: white !important; */
  padding-left: 15%;
}
</style>
