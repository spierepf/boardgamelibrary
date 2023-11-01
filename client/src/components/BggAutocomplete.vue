<template>
  <v-autocomplete
    v-model="selectedItemBggId"
    v-model:items='items'
    v-model:search='search'
    @update:modelValue="$emit('itemSelected', rawItemWithBggId(selectedItemBggId))"
    ref="input"
  />
</template>

<script>
import {bggId, createItemWithPrimaryName, displayName, searchBgg} from '@/util/bgg-util'

function debounce(fn, delay) {
  let timeoutID = null;
  return function () {
    clearTimeout(timeoutID);
    const args = arguments;
    const that = this;
    timeoutID = setTimeout(function () {
      fn.apply(that, args)
    }, delay)
  };
}

export default {
  name: 'BggAutocomplete',

  emits: ['itemSelected'],

  data() {
    return {
      search: '',
      items: [],
      selectedItemBggId: null
    }
  },

  methods: {
    rawItemWithBggId(targetBggId) {
      for (const item of this.items) {
        if (bggId(item.raw) === targetBggId) {
          return item.raw
        }
      }
    }
  },

  watch: {
    search: debounce(async function (localSearch) {
      if (localSearch) {
        if (this.search && this.search !== '') {
          if (!this.selectedItemBggId) {
            const localRawItems = await searchBgg(localSearch).then(rawItems => rawItems.concat([createItemWithPrimaryName(localSearch)]))
            if (this.search === localSearch) {
              this.items = localRawItems.map(rawItem => {
                return {title: displayName(rawItem), value: bggId(rawItem), raw: rawItem};
              })
            }
          }
        } else {
          this.items = []
        }
      }
    }, 500)
  }
}
</script>
