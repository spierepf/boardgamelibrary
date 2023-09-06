<template>
  <UserMenu v-if="loginState"/>
  <LoginDialog v-else/>
</template>
<script>
import UserMenu from "@/components/UserMenu.vue";
import LoginDialog from "@/components/LoginDialog.vue";

export default {
  name: "UserMenuLoginDialogToggle",
  components: {LoginDialog, UserMenu},
  data() {
    return {
      loginState: sessionStorage.auth != null
    }
  },
}
</script>
