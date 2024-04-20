<template>
  <v-sheet class="chatbot">

    <div class="inputBox">
      <v-text-field background-color="grey lighten-1" solo v-model="currentMessage"
        label="Ask for your customized tutorial here..."
        @keyup.enter="sendMessage(currentMessage)">
      </v-text-field>
    </div>
    
    <div class="messageBox">
      <div v-for="message in messages" :key="message.id"
        :class="message.from === 'user' ? 'messageFromUser' : 'messageFromChatGpt'">
        <!-- Conditionally render the message as either code or text -->
        <code-block v-if="message.format === 'code'" :code="message.data"></code-block>
        <div v-else v-html="message.data"></div>
      </div>
    </div>

  </v-sheet>
</template>

<script>
import axios from 'axios'
import CodeBlock from './CodeBlock.vue';
import MarkdownIt from 'markdown-it';

export default {
  name: "ChatBox",

  components: { CodeBlock },

  data() {
    return {
      md: new MarkdownIt({
        breaks: true,
        html: true,
      }),
      messages: [],
      currentMessage: null,
      sampleCode: `function add(a, b) {\n  return a + b;\n}`
    }
  },

  methods: {
    async sendMessage(message) {

      if (!message.trim()) return; // Prevent sending empty messages

      const timestamp = Date.now();

      this.messages.push({
        id: timestamp,
        from: 'user',
        data: message,
        format: 'text'
      })

      this.currentMessage = '';

      // let response = await axios.post('http://0.0.0.0:3000/', { message: message });
      let response = await axios.post('https://smart-backend.bimriver.com/', { message: message });

      response.data.forEach(msg => {
        this.messages.push({
          id: Date.now() + 1,
          from: msg.from,
          data: this.parseResponse(msg),
          format: msg.format
        });
      });

      this.$nextTick(() => {
        this.scrollToBottom();
      });

    },

    parseResponse(msg) {
      let response = msg.data.response
      response = response.replace(" - ", "\n - ")
      return this.md.render(response)
    },

    scrollToBottom() {
      const container = this.$el.querySelector(".messageBox");
      container.scrollTop = container.scrollHeight;
    }
  }
};
</script>

<style scoped>
.inputBox {
  margin: 5% 15% 0 15% !important;
  background: white !important;
}

.messageBox {
  height: 70vh;
  margin: 0 15% 0 15%;
  overflow-y: auto;
}

.messageFromUser {
  text-align: left;
  background-color: rgb(243, 243, 243);
  border-radius: 10px;
  padding: 1rem;
  margin-top: 1rem;
  margin-bottom: 1rem;
  padding-right: 2rem;
  width: 100%;
}

.messageFromChatGpt {
  text-align: left;
  background-color: rgba(230, 230, 230, 0.32);
  border-radius: 10px;
  padding: 1rem;
  margin-top: 1rem;
  margin-bottom: 1rem;
  padding-right: 2rem;
  width: 100%;
}
</style>
