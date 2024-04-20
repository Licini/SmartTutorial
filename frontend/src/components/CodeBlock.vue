<template>
    <pre v-html="formattedCode" class="code-block"></pre>
  </template>
  
  <script>
  export default {
    props: ['code'],
    computed: {
      formattedCode() {
        return this.highlightCode(this.code);
      }
    },
    methods: {
      highlightCode(code) {
        // tbd
        return code;
      }
    }
  }
  </script>
  

  <style>

  .code-block {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  font-family: 'Courier New', Courier, monospace;
  overflow-x: auto;
  white-space: pre-wrap;
}

  </style>