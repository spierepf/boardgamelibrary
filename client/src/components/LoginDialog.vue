<template>
  <v-row justify="center">
    <v-dialog
      id="login_dialog"
      v-model="dialog"
      persistent
      width="512"
    >
      <template v-slot:activator="{ props }">
        <v-btn
          id="open_login_dialog"
          v-bind="props"
        >
          LOGIN
        </v-btn>
      </template>
      <v-alert
        id="login_failed_alert"
        v-if="loginFailed"
        type="error"
        title="Login Failed"
        text="Please check your username and password and try again."
      />
      <v-card>
        <v-card-title>
          <span class="text-h5">Login</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  id="username"
                  label="Username"
                  v-model="userDetails.username"
                  type="email"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  id="password"
                  label="Password"
                  v-model="userDetails.password"
                  type="password"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            id="cancel_login"
            color="blue-darken-1"
            variant="text"
            @click="dialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            id="submit_login"
            color="blue-darken-1"
            variant="text"
            @click="login"
          >
            Submit
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import {bus} from "@/main";
import {fetchFromServer} from "@/util/fetch-util";

export default {
  data: () => ({
    dialog: false,
    loginFailed: false,
    userDetails: {
      username: "",
      password: ""
    },
  }),
  methods: {
    login: function () {
      fetchFromServer(`/api/token/`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.userDetails)
      }).then(response => {
        sessionStorage.auth = JSON.stringify(response)
        bus.emit('loginStateChange', {'loginState': sessionStorage.auth != null})
        this.dialog = false
      }).catch(error => {
        if (error.response.status == 401) {
          this.loginFailed = true
        } else {
          console.error(error)
        }
      });
    }
  }
}
</script>
