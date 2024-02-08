<template>
  <v-app-bar
    color="primary">
    <template v-slot:append>
      <UserMenuLoginDialogToggle/>
    </template>
  </v-app-bar>
  <v-form id="create_new_copy_form">
    <v-container>
      <v-col>
        <v-select
          id="copy_owner"
          :items="copy_owner_items"
          v-model="selected_copy_owner_id"
          item-title="username"
          item-value="id"
        />
        <bgg-autocomplete id="copy_title" @itemSelected="title_selected" ref="copy_title"/>
        <v-btn id="submit" @click="create_copy">Submit</v-btn>
      </v-col>
    </v-container>
  </v-form>
  <v-snackbar
    id="success_message_snackbar"
    v-model="success_message_visible"
  >
    {{ success_message }}
    <template v-slot:actions>
      <v-btn
        id="success_message_snackbar_close_button"
        @click="success_message_visible=false"
      >
        Close
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
import {jwtDecode} from "jwt-decode";
import {fetchFromServer, urlFor, urlForQuery} from "@/util/fetch-util";
import BggAutocomplete from "@/components/BggAutocomplete.vue";
import {bggId, primaryName, yearPublished} from "@/util/bgg-util";
import UserMenuLoginDialogToggle from "@/components/UserMenuLoginDialogToggle.vue";

function create(datatype, properties) {
  return fetchFromServer(urlFor(datatype), {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + JSON.parse(sessionStorage["auth"]).access,
      "Accept": "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(properties)
  })
}

export default {
  name: "CreateNewCopy",
  components: {UserMenuLoginDialogToggle, BggAutocomplete},

  data() {
    return {
      selected_title_bgg_id: "",
      selected_title_primary_name: "",
      selected_title_year_published: "",
      copy_owner_items: [],
      selected_copy_owner_id: null,
      success_message: "",
      success_message_visible: false
    }
  },

  methods: {
    title_selected(selected_title) {
      if (selected_title) {
        this.selected_title_bgg_id = bggId(selected_title)
        this.selected_title_primary_name = primaryName(selected_title)
        this.selected_title_year_published = yearPublished(selected_title)
      }
    },
    ensure_title_exists: function(title_primary_name, title_bgg_id) {
      return fetchFromServer((title_bgg_id !== "none") ? urlForQuery("titles", "bgg_id", title_bgg_id) : urlForQuery("titles", "name", title_primary_name))
        .then(json => json.find(title =>
          String(title.bgg_id) === String(title_bgg_id) &&
          title.name === title_primary_name
        )
      )
      .then(title => {
        if(title !== undefined) {
          return title
        } else {
          let properties = {"name": title_primary_name}
          if(title_bgg_id !== "none") {
            properties["bgg_id"] = title_bgg_id
          }
          return create("titles", properties)
        }
      })
    },
    create_copy: function() {
      this.ensure_title_exists(this.selected_title_primary_name, this.selected_title_bgg_id)
        .then((response) => {
          return create("copies", {
            "title": urlFor("titles", response["id"]),
            "owner": urlFor("users", this.selected_copy_owner_id)
          })
        })
        .then(() => {
          let owner = "Unknown"
          for(const item of this.copy_owner_items) {
            if(item["id"] === this.selected_copy_owner_id) owner = item["username"]
          }
          this.success_message=`New copy of ${this.selected_title_primary_name} belonging to ${owner} created.`
          this.success_message_visible=true
          this.$refs.copy_title.$refs.input.reset()
          this.selected_title_bgg_id = ""
          this.selected_title_primary_name = ""
          this.selected_title_year_published = ""
        })
    }
  },

  created: function() {
    let logged_in_user = jwtDecode(JSON.parse(sessionStorage["auth"]).access)
    if (logged_in_user["groups"].includes("ADMIN")) {
      fetchFromServer(urlFor("users")).then(json => this.copy_owner_items = json)
    } else {
      this.copy_owner_items = [
        {"username": logged_in_user["username"], "id": logged_in_user["user_id"]}
      ]
    }
    this.selected_copy_owner_id = logged_in_user["user_id"]
  }
}
</script>

