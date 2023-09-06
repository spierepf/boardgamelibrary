<template>
  <div class="text-center">
    <v-menu>
      <template v-slot:activator="{ props }">
        <v-btn
          id="open_user_menu"
          v-bind="props"
        >
          USER
        </v-btn>
      </template>
      <v-list id="user_menu">
        <v-list-item id="logout">
          <v-list-item-title @click.stop="logout">Logout</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>
<script>
export default {
  methods: {
    logout: function() {
      sessionStorage.removeItem("auth")
    }
  }
}
</script>
