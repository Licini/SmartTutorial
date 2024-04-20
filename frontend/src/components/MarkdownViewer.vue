<template>
  <div v-html="formattedContent" class="markdown-body"></div>
</template>

<script>
import { marked } from 'marked';
import hljs from 'highlight.js';
import 'highlight.js/styles/vs.css';

export default {
  props: ['markdown'],

  data() {
    return {
      formattedContent: ''
    };
  },

  mounted() {
    this.processContent();
  },

  methods: {
    processContent() {

      let headers = []
      let sub_headers = []
      const regex = /(```[\s\S]+?```)|(^###\s.*$)/gm;
      const segments = this.markdown.split(regex).filter(Boolean);

      this.formattedContent = segments.map((segment, index) => {

        console.log(segment)

        let htmlSegment;

        let spacer = (index < segments.length - 1 ? '<div class="spacer"></div>' : '')
        if (segment.startsWith("```")) { // Code block processing
          const language = segment.match(/```(\w+)/)?.[1] || 'plaintext';
          const code = segment.split('\n').slice(1, -1).join('\n');
          htmlSegment = `<pre class="code-block"><code>${hljs.highlight(code, { language, ignoreIllegals: true }).value}</code></pre>`;
          return htmlSegment + spacer

        } else if (segment.trim().startsWith('###')) { // Heading processing
          const title = segment.trim().substring(4)
          headers.push(title) // add the headers for table of contents
          htmlSegment = `<div class="section-heading" id="${title.replace(/\s+/g, '-').toLowerCase()}">${marked.parse(segment)}</div>`;
          return htmlSegment

        } else if (segment.trim().startsWith('####')) { // Heading processing
          const title = segment.trim().substring(5)
          sub_headers.push(title) // add the headers for table of contents
          htmlSegment = `<div class="section-heading" id="${title.replace(/\s+/g, '-').toLowerCase()}">${marked.parse(segment)}</div>`;
          return htmlSegment

        } else { // Regular Markdown text
          htmlSegment = `<div class="markdown-text">${marked.parse(segment)}</div>`;
          return htmlSegment + spacer
        }

      }).join('');
      if (headers.length == 0) { headers = sub_headers }
      this.$emit('update:headers', headers);
    }
  }
}
</script>

<style>
.spacer {
  height: 0rem;
}

.code-block {
  padding: 1rem;
  border-radius: 10px;
  background: rgb(239, 239, 239);
}

.markdown-text {
  padding: 1.5rem;
}

@media (max-width: 600px) {

  .markdown-text,
  .code-block {
    padding: 0.75rem;
  }
}

.markdown-text,
.code-block {
  transition: all 0.3s ease-in-out;
}
</style>