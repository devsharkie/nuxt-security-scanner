<script>
export default {
  data() {
    return { htmlContent: "<strong>Hello</strong>" };
  }
};
</script>
<template>
  <div v-html="htmlContent"></div>
    <a
      :href="userProvidedUrl"
      :style="userProvidedStyles"
    >
      click me
    </a>
</template>