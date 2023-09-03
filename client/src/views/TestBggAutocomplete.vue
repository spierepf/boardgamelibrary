<template>
  <v-container>
    <bgg-autocomplete id='bgg-autocomplete' @itemSelected='selectedItem'/>
    <v-text-field id='selected-item-bgg-id' v-model='selectedItemBggId'/>
    <v-text-field id='selected-item-primary-name' v-model='selectedItemPrimaryName'/>
    <v-text-field id='selected-item-year-published' v-model='selectedItemYearPublished'/>
  </v-container>
</template>

<script>
import BggAutocomplete from '@/components/BggAutocomplete'
import {bggId, primaryName, yearPublished} from '@/util/bgg-util'

export default {
  name: 'TestBggAutocomplete',

  components: {
    BggAutocomplete,
  },

  data() {
    return {
      selectedItemBggId: '',
      selectedItemPrimaryName: '',
      selectedItemYearPublished: ''
    }
  },

  methods: {
    selectedItem(selectedItem) {
      if (selectedItem) {
        this.selectedItemBggId = bggId(selectedItem)
        this.selectedItemPrimaryName = primaryName(selectedItem)
        this.selectedItemYearPublished = yearPublished(selectedItem)
      }
    }
  }
}
</script>
