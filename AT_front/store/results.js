import { defineStore } from 'pinia'

export const useResultsStore = defineStore('results', {
    state: () => ({
        results: [],
    }),
    actions: {
        init(results) {
            this.results = results
        },
        add(result) {
            this.results.push(result)
        }
    },
})