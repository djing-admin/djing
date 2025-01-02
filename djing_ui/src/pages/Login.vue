<script lang="ts" setup>
import { useForm } from "@inertiajs/vue3";
import { Head } from "@inertiajs/vue3";

const djing_config = {
  app_name: "Djing",
  base_url: "/djing-admin",
  auth: { username_field: "username" },
};

const { base_url, auth } = djing_config;

const form = useForm({
  username_field: auth.username_field,
  username: "",
  password: "",
});

const submit = () => {
  form.post(`${base_url}/login`, {
    onSuccess: () => {
      console.log("Logged in successfully");
    },
    onError: (err) => {
      console.log(err);
    },
  });
};
</script>

<script lang="ts">
import AuthLayout from "@/layouts/Auth.vue";

export default {
  name: "Login",

  layout: AuthLayout,
};
</script>

<template>
  <Head title="Sign In" />

  <div class="py-6 px-1 md:px-2 lg:px-6">
    <form
      @submit.prevent="submit"
      class="bg-white dark:bg-gray-800 shadow rounded-lg p-8 max-w-[25rem] mx-auto"
    >
      <h2 class="text-2xl text-center font-normal mb-6">Welcome Back!</h2>

      <div class="w-24 h-[2px] dark:bg-gray-300 bg-gray-400 m-auto mb-6"></div>

      <div class="mb-6">
        <label
          class="block text-gray-700 dark:text-gray-400 mb-2"
          for="username"
        >
          <span v-if="auth.username_field == 'email'">Email</span>
          <span v-if="auth.username_field == 'username'">Username</span>
        </label>

        <input
          id="username"
          v-model="form.username"
          required
          :type="auth.username_field === 'email' ? 'email' : 'text'"
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-blue-400"
          autocomplete="off"
          :placeholder="
            auth.username_field === 'email' ? 'Enter Email' : 'Enter Username'
          "
          :class="{ 'border-red-500': form.errors.username }"
        />

        <p v-if="form.errors.username" class="text-red-500 text-sm mt-1">
          {{ form.errors.username }}
        </p>
      </div>

      <div class="mb-6">
        <label
          class="block text-gray-700 dark:text-gray-400 mb-2"
          for="password"
          >Password</label
        >

        <input
          id="password"
          v-model="form.password"
          type="password"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-blue-400"
          autocomplete="off"
          placeholder="Enter your password"
          :class="{ 'border-red-500': form.errors.password }"
        />
        <p v-if="form.errors.password" class="text-red-500 text-sm mt-1">
          {{ form.errors.password }}
        </p>
      </div>

      <div class="mt-10">
        <Button
          type="submit"
          class="border text-left appearance-none cursor-pointer rounded text-sm font-bold focus:outline-none focus:ring ring-primary-200 dark:ring-gray-600 relative disabled:cursor-not-allowed items-center shadow h-9 px-3 bg-primary-500 border-primary-500 hover:[&:not(:disabled)]:bg-primary-400 hover:[&:not(:disabled)]:border-primary-400 text-white dark:text-gray-900 w-full flex justify-center"
        >
          Sign In
        </Button>
      </div>
    </form>
  </div>
</template>
