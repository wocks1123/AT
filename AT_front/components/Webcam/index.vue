<template>
  <div
    ref="wrapperDiv"
    class="relative flex-1 bg-black items-center flex"
    @mouseover="onMouseOver"
    @mouseleave="onMouseLeave"
  >
    <div
      v-if="!isStreaming"
      class="
        bg-gray-900 bg-opacity-75 absolute w-full h-full
      "
    >
      <div
        class="
          absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2
        "
      >
        <div
          class="text-white font-bold text-lg"
        >
          실행중인 카메라가 없습니다.
        </div>
<!--        <div class="flex justify-center mt-2">-->
<!--          <button-->
<!--            @click="startStreaming"-->
<!--            class="bg-blue-500 text-white w-24 p-2 rounded-md hover:bg-blue-600 items-center flex justify-center"-->
<!--          >-->
<!--            <Icon name="material-symbols:videocam" class="w-6 h-6" />-->
<!--            <div class="ml-2 font-bold">-->
<!--              Start-->
<!--            </div>-->
<!--          </button>-->
<!--        </div>-->
      </div>

    </div>

    <div
      class="w-full bg-yellow-100 w-[640px] flex items-center justify-center shadow-md"
    >
      <canvas
        class="shadow-md w-full h-full"
        ref="received_canvas"
      />
      <canvas
        class="hidden"
        ref="canvas"
      />
      <video
        class="hidden"
        ref="video"
        playsinline
      />
    </div>

    <div
      v-if="isHovered"
      class="absolute bottom-2 left-2 flex"
    >
      <WebcamButton
        class="mr-2"
        @on-click="startStreaming"
        @off-click="stopStreaming"
      >
        <template v-slot:on>
          <Icon name="material-symbols:videocam-off" class="w-6 h-6" />
          <div class="ml-2 font-bold">
            Stop
          </div>
        </template>
        <template v-slot:off>
          <Icon name="material-symbols:videocam" class="w-6 h-6" />
          <div class="ml-2 font-bold">
            Start
          </div>
        </template>
      </WebcamButton>

      <WebcamButton
        @on-click="startDetection"
        @off-click="stopDetection"
      >
        <template v-slot:on>
          <Icon name="material-symbols:frame-person-off" class="w-6 h-6" />
          <div class="ml-2 font-bold">
            Stop
          </div>
        </template>
        <template v-slot:off>
          <Icon name="material-symbols:frame-person" class="w-6 h-6" />
          <div class="ml-2 font-bold">
            Start
          </div>
        </template>
      </WebcamButton>
    </div>

  </div>

</template>

<script setup>

const { $loadModel, $tf } = useNuxtApp()

import { useWebsocketStore } from "@/store/websocket";
import { useFrameBufferStore } from "@/store/framebuffer";

const websocket = useWebsocketStore()
const frames = useFrameBufferStore()

const canvas = ref(null)
const ctx = ref(null)
const video = ref(null)

const received_canvas = ref(null)
const received_ctx = ref(null)

const isHovered = ref(false)
const isStreaming = ref(false)
const isDetecting = ref(false)

let socket
let stream
let animationId
let intervalId

let detector

const videoConfig = {
  'audio': false,
  'video': {
    width: 640,
    height: 480
  },
}

onMounted(async () => {
  received_ctx.value = received_canvas.value.getContext("2d");
  received_canvas.value.width = 640
  received_canvas.value.height = 480

  received_ctx.lineWidth = 2;
  received_ctx.font = "16px Arial";
  received_ctx.fillStyle = "white";

  websocket.on("STREAMING_START", async (data) => {
    console.log("STREAMING_START")
    isStreaming.value = true
  })

  websocket.on("STREAMING_END", async (data) => {
    console.log("STREAMING_END")
    isStreaming.value = false
  })

  websocket.on("IMAGE_INPUT", async (data) => {
    // console.log("IMAGE_INPUT", getDateString(), data.timestamp)

    isStreaming.value = true

    const image = new Image();
    image.onload = async () => {
      // received_ctx.value.drawImage(image, 0, 0, 640, 480)
      received_ctx.value.drawImage(image, 0, 0,  received_canvas.value.width, received_canvas.value.height)

      received_ctx.value.fillText(data.timestamp, 10, 10)
      if (isDetecting.value) {
        let predictions = await detector.detect(image);

        frames.add(data, predictions)

        // draw bounding box
        predictions.forEach((prediction) => {

          /////////////////////////////////////////////////////////
          // 바운딩 박스 좌표 추출
          let [x, y, w, h] = prediction.bbox;
          x = received_canvas.value.width / image.width * x
          y = received_canvas.value.height / image.height * y
          w = received_canvas.value.width / image.width * w
          h = received_canvas.value.height / image.height * h

          // 바운딩 박스 그리기
          received_ctx.value.strokeStyle = "green";
          received_ctx.value.beginPath();
          received_ctx.value.rect(x, y, w, h);
          received_ctx.value.stroke();

          // 클래스 및 스코어 그리기
          const text = `${prediction.class} ${prediction.score.toFixed(2)}`;
          received_ctx.value.fillText(text, x, y - 5);
          ///////////////////////////////////////////////////////
        });
      }
    };
    image.src = data.data;
  })
})

const onMouseOver = () => {
  isHovered.value = true
}

const onMouseLeave = () => {
  isHovered.value = false
}


const startStreaming = async () => {
  stream = await window.navigator.mediaDevices.getUserMedia(videoConfig);

  ctx.value = canvas.value.getContext("2d");

  video.value.srcObject = stream;
  video.value.play();

  await websocket.send(
      JSON.stringify({
        topic: "STREAMING_START",
        timestamp: getDateString(),
      })
  )

  animationId = requestAnimationFrame(draw);
  intervalId = setInterval(() => { sendImages() }, 330)
}


const stopStreaming = async () => {
  stream.getTracks().forEach(track => track.stop());
  video.value.srcObject = null;
  cancelAnimationFrame(animationId);
  clearInterval(intervalId)
  await websocket.send(
      JSON.stringify({
        topic: "STREAMING_END",
        timestamp: getDateString(),
      })
  )
}


const startDetection = async () => {
  if (!detector) {
    detector = await $loadModel()
  }
  isDetecting.value = true
}

const stopDetection = async () => {
  isDetecting.value = false
}

const draw = async () => {
  canvas.value.width = video.value.videoWidth;
  canvas.value.height = video.value.videoHeight;
  ctx.value.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height);
  animationId = requestAnimationFrame(draw);
};


const sendImages = async () => {
  const imageData = canvas.value.toDataURL()
  await websocket.send(
      JSON.stringify({
        topic: "IMAGE_INPUT",
        timestamp: getDateString(),
        data: imageData
      })
  )
}


const getDateString = () => {
  let date = new Date();
  let year = date.getFullYear();
  let month = String(date.getMonth() + 1).padStart(2, "0");
  let day = String(date.getDate()).padStart(2, "0");
  let hour = String(date.getHours()).padStart(2, "0");
  let minute = String(date.getMinutes()).padStart(2, "0");
  let second = String(date.getSeconds()).padStart(2, "0");
  let millisecond = String(date.getMilliseconds()).padStart(6, "0");

  return`${year}-${month}-${day} ${hour}:${minute}:${second}.${millisecond}`
}


</script>
