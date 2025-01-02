<script lang="ts" setup>
import { ref } from "vue";

const should_show_menu = ref(false);

const theme_icons: Record<string, any> = {
  light: "moon",
  dark: "sun",
  system: "computer-desktop",
};

const get_icon = () => {
  return theme_icons[Djing.get_system_theme_key()];
};

const toggle_theme = (theme: string) => {
  localStorage.setItem("theme", theme);

  const chosen_theme = Djing.get_system_theme();

  if (chosen_theme === "dark") {
    document.documentElement.classList.add("dark");
  } else {
    document.documentElement.classList.remove("dark");
  }

  should_show_menu.value = false;
};
</script>

<template>
  <Dropdown
    :should_show_menu="should_show_menu"
    @toggle="should_show_menu = $event"
  >
    <template #button>
      <Icon
        class="cursor-pointer text-center text-primary-500"
        :type="get_icon()"
      />
    </template>

    <template #menu>
      <div class="p-1 items-center">
        <div
          v-for="[theme, icon] in Object.entries(theme_icons)"
          class="flex space-x-2 px-[10px] py-[4px] hover:bg-gray-100 hover:dark:bg-gray-800 rounded cursor-pointer"
          @click.stop="() => toggle_theme(theme)"
        >
          <Icon :type="icon" />

          <Button
            class="w-full text-left cursor-pointer capitalize font-normal"
          >
            {{ theme }}
          </Button>
        </div>
      </div>
    </template>
  </Dropdown>
</template>
