import { defineStore } from 'pinia'

export const useWebsocketStore = defineStore('websocket', {
    state: () => ({
        socket: null,
        callbacks: {}
    }),
    actions: {
        connect(id) {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
            this.socket = new WebSocket(`${protocol}//0.0.0.0/ws/${id}`)

            this.socket.onopen = () => {

            }

            this.socket.onmessage = ({ data }) => {
                const jsonData = JSON.parse(data)
                if (this.callbacks.hasOwnProperty(jsonData.topic)) {
                    this.callbacks[jsonData.topic](jsonData)
                }
            }

            this.socket.onclose = function () {

            }
        },
        on(topic, callback) {
            this.callbacks[topic] = callback
        },
        send(message) {
            this.socket.send(message)
        }
    },
})