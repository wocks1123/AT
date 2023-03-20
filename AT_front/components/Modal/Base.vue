<template>
  <div
      v-if="localShow"
      @click.stop="clickBackground"
      class="
      fixed top-0 left-0 bg-opacity-70
      w-full h-full bg-black z-50
    "
  >
    <div
        class="
        flex
        fixed transform top-1/2 -translate-y-1/2
        left-1/2 -translate-x-1/2
        bg-white
      "
        @click.stop=""
        :class="classVal"
    >
      <slot />
    </div>
  </div>
</template>

<script setup>

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: true
  },
  classVal: {
    type: String,
    default: "",
  }
})
const emit = defineEmits(['update:modelValue', 'open', 'close'])


const localShow = computed({
  get() {
    return props.modelValue
  },
  set(value) {
    emit('update:modelValue', value)
  }
})


watch(
    localShow,
    async(newVal, prevVal) => {
      if (newVal === true) {
        emit('open', true)
      }
      else if (newVal === false) {
        emit('close', false)
      }
    }
)


const clickBackground = () => {
  localShow.value = false
}

</script>
