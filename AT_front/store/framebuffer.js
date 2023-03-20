import { defineStore } from 'pinia'

import { useWebsocketStore } from "@/store/websocket";
const websocket = useWebsocketStore()

let personShow = 0
let END_CNT = 10
let startTimestamp = ""
let endTimestamp = ""
let SKIP_COUNT = 10
let count = 0

let MAX_SIZE = 3 * 60 // 1 min



export const useFrameBufferStore = defineStore('framebuffer', {
    state: () => ({
        frames: []
    }),
    actions: {
        add(data, predictions) {
            if (this.frames.length === MAX_SIZE) this.frames.shift()

            this.frames.push(data)

            if (predictions && predictions.some(elem => elem.class === "person")) {
                if (startTimestamp === "")
                    personShow++

                if (personShow > 3 && startTimestamp === "") { // 사람이 3프레임 이상 검출되면 시작
                    startTimestamp = data.timestamp
                    count = 0
                }
                endTimestamp = data.timestamp
            }
            else {
                count++
                if (startTimestamp !== "")
                    if (count > SKIP_COUNT) {
                        this.frames.forEach((frame) => {
                            websocket.send(
                                JSON.stringify({
                                    topic: "DETECTED",
                                    data: frame,
                                    start_timestamp: startTimestamp,
                                    end_timestamp: endTimestamp,
                                })
                            )
                        })

                        startTimestamp = ""
                        count = 0
                        personShow = 0
                    }
            }
        },
        clear() {
            this.frames = []
        }
    }
})