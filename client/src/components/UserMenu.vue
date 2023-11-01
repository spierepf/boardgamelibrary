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
        <v-list-item v-if="is_admin_or_committee" id="open_create_new_copy_form" href="/createNewCopy">
          <v-list-item-title>Create Library Items</v-list-item-title>
        </v-list-item>
        <v-list-item id="logout">
          <v-list-item-title @click.stop="logout">Logout</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>
<script>
import {bus} from "@/main";
import {jwtDecode} from "jwt-decode";

export default {
  methods: {
    logout: function () {
      sessionStorage.removeItem("auth")
      bus.emit('loginStateChange', {'loginState': sessionStorage.auth != null})
    }
  },
  computed: {
    is_admin_or_committee: function() {
      const groups = jwtDecode(JSON.parse(sessionStorage['auth']).access)['groups']
      return groups.includes('ADMIN') || groups.includes('COMMITTEE')
    }
  }
}
</script>
