<template>
  <v-app-bar
    color="primary">
    <template v-slot:append>
      <UserMenuLoginDialogToggle/>
    </template>
  </v-app-bar>
  <HelloWorld/>
</template>

<script setup>
import HelloWorld from '@/components/HelloWorld.vue'
import UserMenuLoginDialogToggle from "@/components/UserMenuLoginDialogToggle.vue";
</script>
