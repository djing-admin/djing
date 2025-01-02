<template>
  <div class="relative" :class="{ 'overflow-hidden': loading }">
    <!-- Default -->
    <template v-if="variant === 'default'">
      <div
        v-if="loading"
        dusk="loading-view"
        class="flex items-center justify-center z-30 p-6"
        style="min-height: 220px"
      >
        <span>loading...</span>
      </div>
      <slot v-else />
    </template>

    <!-- Overlay -->
    <template v-if="variant === 'overlay'">
      <div
        v-if="loading"
        dusk="loading-view"
        class="absolute inset-0 z-20 bg-white/75 dark:bg-gray-800/75 flex items-center justify-center p-6"
      />
      <slot />
    </template>
  </div>
</template>

<script lang="ts" setup>
defineProps({
  loading: { type: Boolean, default: true },
  variant: {
    type: String,
    validator: (v: string) => ["default", "overlay"].includes(v),
    default: "default",
  },
});
</script>
