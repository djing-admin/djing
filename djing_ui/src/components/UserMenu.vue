<script lang="ts" setup>
import { ref } from "vue";
import { minimum } from "@/util/minimum";

defineProps({
  current_user: {
    required: true,
    type: Object as () => { username: string },
  },
});

const should_show_menu = ref(false);

const logout = async () => {
  if (confirm("Are you sure?")) {
    try {
      await minimum(
        Djing.request().post(Djing.url("/logout"), {
          cancelToken: Djing.cancelToken(),
          params: {},
        }),
        300
      );
      Djing.redirectToLogin();
    } catch (error) {
      console.error(error);
    }
  }
};
</script>

<template>
  <Dropdown
    :should_show_menu="should_show_menu"
    @toggle="should_show_menu = $event"
  >
    <!-- Custom button content -->
    <template #button>
      <Gravatar :current_user="current_user" />
      <span>{{ current_user.username }}</span>
      <Icon type="chevron-down" class="w-4" />
    </template>

    <!-- Custom dropdown menu content -->
    <template #menu>
      <div class="p-1 w-36">
        <Button
          @click.stop="logout"
          class="p-2 w-full text-left cursor-pointer inline-block hover:bg-gray-200 dark:hover:bg-gray-800"
        >
          Sign Out
        </Button>
      </div>
    </template>
  </Dropdown>
</template>
