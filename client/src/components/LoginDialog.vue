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
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  id="password"
                  label="Password"
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
            @click="dialog = false"
          >
            Submit
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script setup>
  import { ref } from 'vue'

  const dialog = ref(false)
</script>

<script>
  export default {
    data: () => ({
      dialog: false,
    }),
  }
</script>
