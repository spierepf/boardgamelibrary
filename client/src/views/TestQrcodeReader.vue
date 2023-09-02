<template>
  <v-container>
    <qrcode-reader id='qrcode-reader' test @validDecode='validDecode'/>
    <v-text-field id='decode-type' v-model='decodeType'/>
    <v-text-field id='decode-uuid' v-model='decodeUUID'/>
  </v-container>
</template>

<script>
import QrcodeReader from '../components/QrcodeReader'

export default {
  name: 'TestQRCodeReader',

  components: {
    QrcodeReader,
  },

  data() {
    return {
      decodeType: '',
      decodeUUID: ''
    }
  },

  methods: {
    validDecode(validDecode) {
      this.decodeType = validDecode.t
      this.decodeUUID = validDecode.u
    }
  }
}
</script>
