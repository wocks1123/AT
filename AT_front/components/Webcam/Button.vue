<template>
  <button
    @click="clickButton"
    class="bg-blue-500 text-white w-24 p-2 rounded-md hover:bg-blue-600 items-center flex-row justify-center"
  >
    <div v-if="on">
      <slot name="on"></slot>
    </div>
    <div v-else>
      <slot name="off"></slot>
    </div>
  </button>
</template>

<script setup>

const emit = defineEmits([
    'on-click', 'off-click'
])

const on = ref(false)

const clickButton = async () => {
  on.value = !on.value
  if (on.value) {
    emit('on-click')
  }
  else {
    emit('off-click')
  }
}



</script>

<style scoped>

</style>