<template>
  <div v-html="htmlContent"></div>
</template>

<script>
export default {
  data() {
    return {
      htmlContent: "<strong>Hello</strong>"
    };
  }
};
</script>
