<template>
  <div>
    <p class="error">{{ error }}</p>
    <qrcode-stream @detect="onDetect" @init="onInit"/>
    <qrcode-capture v-if="test" @detect="onDetect"/>
  </div>
</template>

<script>
import {QrcodeCapture, QrcodeStream} from 'vue-qrcode-reader'
import {validateType, validateUUID} from '@/util/qrcode-util'

export default {
  name: 'QrcodeReader',

  components: {QrcodeStream, QrcodeCapture},

  data() {
    return {
      error: ''
    }
  },

  props: {
    test: Boolean
  },

  emits: ['validDecode'],

  methods: {
    onDetect(detectedCodes) {
      detectedCodes.map(code => {
        const value = JSON.parse(code.rawValue)
        if (validateType(value.t) && validateUUID(value.u)) {
          this.$emit('validDecode', value)
        }
      })
    },

    async onInit(promise) {
      try {
        await promise
      } catch (error) {
        if (error.name === 'NotAllowedError') {
          this.error = "ERROR: you need to grant camera access permission"
        } else if (error.name === 'NotFoundError') {
          this.error = "ERROR: no camera on this device"
        } else if (error.name === 'NotSupportedError') {
          this.error = "ERROR: secure context required (HTTPS, localhost)"
        } else if (error.name === 'NotReadableError') {
          this.error = "ERROR: is the camera already in use?"
        } else if (error.name === 'OverconstrainedError') {
          this.error = "ERROR: installed cameras are not suitable"
        } else if (error.name === 'StreamApiNotSupportedError') {
          this.error = "ERROR: Stream API is not supported in this browser"
        } else if (error.name === 'InsecureContextError') {
          this.error = 'ERROR: Camera access is only permitted in secure context. Use HTTPS or localhost rather than HTTP.';
        } else {
          this.error = `ERROR: Camera error (${error.name})`;
        }
      }
    }
  }
}
</script>

<style scoped>
.error {
  font-weight: bold;
  color: red;
}
</style>
