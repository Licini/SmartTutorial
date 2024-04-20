<template>
  <v-sheet class="chatbot">

    <div class="messageBox">
      <div v-for="message in messages" :key="message.id"
        :class="message.from === 'user' ? 'messageFromUser' : 'messageFromChatGpt'">
        <!-- Conditionally render the message as either code or text -->
        <code-block v-if="message.format === 'code'" :code="message.data"></code-block>
        <div v-else v-html="message.data"></div>
      </div>
    </div>

    <v-footer app color="transparent" class="inputBox">
      <v-text-field background-color="grey lighten-1" dense solo v-model="currentMessage"
        @keyup.enter="sendMessage(currentMessage)">
      </v-text-field>
    </v-footer>

  </v-sheet>
</template>

<script>
import axios from 'axios'
import CodeBlock from './CodeBlock.vue';

export default {
  name: "ChatBox",
  components: { CodeBlock },
  data() {
    return {
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

      let response = await axios.post('http://0.0.0.0:3000/', { message: message });
      
      response.data.forEach(msg => {
        this.messages.push({
          id: Date.now() + Math.random(),
          from: msg.from,
          data: msg.data,
          format: msg.format
        });
      });
      
      this.$nextTick(() => {
        this.scrollToBottom();
      });

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
  margin: 0 15% 5% 15% !important;
  background: white !important;
}

.messageBox {
  height: 70vh;
  margin: 150px 15% 0 15%;
  overflow-y: auto;
}

.messageFromUser {
  text-align: left;
  background-color: aliceblue;
  border-radius: 10px;
  padding: 10px;
  margin-top: 15px;
  margin-bottom: 15px;
  width: 30%;
  margin-left: 70%;
}

.messageFromChatGpt {
  text-align: left;
  background-color: antiquewhite;
  border-radius: 10px;
  padding: 10px;
  margin-top: 15px;
  margin-bottom: 15px;
  width: 30%;
  margin-right: 70%;
}
</style>
