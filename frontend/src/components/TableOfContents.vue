<template>
  <div class="toc-container">
    <ul>
      <li v-for="header in headers" :key="header" :class="{ 'active': activeHeader === header }"
        class="toc-header">
        <a @click.prevent="scrollTo(header)">{{ header }}</a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: ['headers'],

  data() {
    return {
      activeHeader: null,
    };
  },

  methods: {
    scrollTo(header) {
        const headerId = header.replace(/\s+/g, '-').toLowerCase();
        const element = document.getElementById(headerId);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
            this.activeHeader = header;
        }
    }
  }
}
</script>

<style>
.toc-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: fixed;
  top: 25%;
  left: 10%;
  width: 15%;
  height: 25vh;
  overflow: auto;
  border-right: 1px solid #e2e2e2
}

.toc-header {
  padding: 0.35rem;
  padding-right: 1rem;
  text-align: right;
  font-size: 14px;
  font-weight: lighter;
}

.toc-header.active {
  font-weight: bold;
}
</style>
