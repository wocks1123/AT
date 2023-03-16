<template>
  <div class="flex h-screen">
    <div
      class="w-full flex flex-col sm:flex-row"
    >
      <Webcam />

      <!-- Result Area -->
      <div class="bg-gray-600 w-full h-80 sm:h-full sm:w-96 border-l-2 border-gray-500">
        <!-- Result Card... -->
        <div
          v-for="(result, i) in store.results"
          :key="i"
          class="
            p-1
            bg-gray-700
            text-white
            font-bold
            hover:bg-gray-800
            cursor-pointer
            justify-center
          "
          @click="clickResultCard(result)"
        >
          {{ result.start_timestamp.slice(0, -7) }} ~
          {{ result.end_timestamp.slice(0, -7) }}
        </div>
      </div>
    </div>
  </div>
  <ResultModal
    v-model="showResultModal"
    :result="currResult"
  />

</template>

<script setup>
import { useResultsStore } from "@/store/results";
import { useWebsocketStore } from "@/store/websocket";
const store = useResultsStore()
const websocket = useWebsocketStore()

const showResultModal = ref(false)
let currResult

onMounted(async () => {
  websocket.connect(Math.floor(Math.random() * 900000) + 100000)

  websocket.on("PREDICT_RESULT", async (data) => {
    store.add(data)
  })
})

const clickResultCard = async (result) => {
  currResult = result
  showResultModal.value = true
}

</script>
