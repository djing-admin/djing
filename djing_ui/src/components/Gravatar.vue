<script setup lang="ts">
import { computed } from "vue";
import md5 from "md5";

const { current_user } = defineProps({
  current_user: {
    required: true,
    type: Object,
  },
});

const gravatar_url = computed(() => {
  const user_email =
    current_user.email?.trim().toLowerCase() ?? "johndoe@example.com";
  const email_hash = md5(user_email);

  return `https://www.gravatar.com/avatar/${email_hash}?s=30`;
});
</script>

<template>
  <img :src="gravatar_url" class="rounded-full mr-2" />
</template>
