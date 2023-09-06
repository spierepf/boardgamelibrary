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

const checkResponseStatus = (response) => {
  if (response.status >= 200 && response.status < 300) {
    return response.json()
  } else {
    let error = new Error(response.statusText)
    error.response = response
    throw error
  }
}

export default {
  data: () => ({
    dialog: false,
    userDetails: {
      username: "",
      password: ""
    },
  }),
  methods: {
    login: function () {
      fetch(`http://localhost:8000/api/token/`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.userDetails)
      }).then(checkResponseStatus).then(response => {
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
