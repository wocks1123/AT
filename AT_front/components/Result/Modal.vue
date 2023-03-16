<template>
  <ModalBase
    v-model="localShow"
  >
    <div class="w-96">

      <video
          class="w-full"
        width="320" height="240" controls autoplay
      >
        <source :src="`${useRuntimeConfig().baseURL}/results/${result.id}/video`" type="video/mp4">
      </video>

      <div class="font-bold text-center">
        {{ result.start_timestamp.slice(0, -7) }} ~
        {{ result.end_timestamp.slice(0, -7) }}
      </div>
    </div>

  </ModalBase>
</template>

<script setup>

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  result: {
    type: Object
  }
})
const emit = defineEmits(['update:modelValue'])

const localShow = computed({
  get() {
    return props.modelValue
  },
  set(value) {
    emit('update:modelValue', value)
  }
})
</script>
