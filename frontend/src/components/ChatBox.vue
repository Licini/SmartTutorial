<template>
  <v-sheet class="chatbot">

    <table-of-contents v-show="headers.length > 0" :headers="headers"></table-of-contents>

    <div class="inputBox">

      <v-text-field v-if="!messageSubmitted" background-color="grey lighten-1" solo v-model="currentMessage"
        label="Ask for your customized tutorial here..." @keyup.enter="sendMessage(currentMessage)">
      </v-text-field>

      <h1 v-else @click="toggleInput" class="messageFromUser">{{ currentMessage }}</h1>
      
      <v-progress-circular v-if="isLoading" :width="1"
        color="gray" indeterminate></v-progress-circular>

    </div>

    <div class="messageBox">

      <div v-for="message in messages" :key="message.id"
        :class="message.from === 'user' ? 'messageFromUser' : 'messageFromChatGpt'">
        <markdown-viewer :markdown="message.data" @update:headers="headers = $event"></markdown-viewer>
      </div>

    </div>

  </v-sheet>
</template>

<script>
import axios from 'axios'
import MarkdownViewer from '@/components/MarkdownViewer.vue';
import TableOfContents from '@/components/TableOfContents.vue';

export default {
  name: "ChatBox",

  components: {
    TableOfContents,
    MarkdownViewer
  },

  data() {
    return {
      messages: [],
      currentMessage: '',
      messageSubmitted: false,
      isLoading: false,
      headers: [],
    }
  },

  methods: {
    async sendMessage(message) {

      if (!message.trim()) return;

      this.messageSubmitted = true;
      this.isLoading = true;
      // let response = await axios.post('http://0.0.0.0:3000/', { message: message });
      let response = await axios.post('https://smart-backend.bimriver.com/', { message: message });

      this.isLoading = false;

      response.data.forEach(msg => {
        this.messages.push({
          id: Date.now() + 1,
          from: msg.from,
          data: msg.data.response,
          format: msg.format
        });
      });

      // this.$nextTick(() => {
      //   this.scrollToBottom();
      // });

    },

    // scrollToBottom() {
    //   const container = this.$el.querySelector(".messageBox");
    //   container.scrollTop = container.scrollHeight;
    // },

    // toggle between showing the title or a search bar
    toggleInput() { 
      this.messageSubmitted = !this.messageSubmitted;
      
      if (!this.messageSubmitted) {
        this.currentMessage = '';
      }
    }
  }
};
</script>

<style scoped>
.inputBox {
  margin: 5% 25% 0 28% !important;
  background: white !important;
}

.messageBox {
  height: 80vh;
  margin: 0 25% 0 28%;
  overflow-y: auto;
  ::-webkit-scrollbar { display: none; }
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

.messageFromUser {
  text-align: left;
  background-color: rgb(243, 243, 243);
  border-radius: 1px;
  padding: 1rem;
  margin-top: 1rem;
  margin-bottom: 1rem;
  padding-right: 2rem;
  width: 100%;
}

.messageFromChatGpt {
  text-align: left;
  background-color: rgba(255, 255, 255, 0.32);
  border-radius: 10px;
  padding: 1rem;
  margin-top: 1rem;
  margin-bottom: 1rem;
  padding-right: 2rem;
  width: 100%;
}

h1 {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
  font-size: 30px;
  font-weight: 300;
  margin-bottom: 16.8px;
  color: rgb(69, 157, 185)
}
</style>
