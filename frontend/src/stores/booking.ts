import { defineStore } from 'pinia'

interface Seat {
    id: number
    row_label: string
    seat_number: number
    status: string
}

export const useBooking = defineStore('booking', {
    state: () => ({
        movie: null as any,
        showtime: null as any,
        selectedSeats: [] as Seat[]
    }),
    getters: {
        totalPrice: (state) => (state.showtime?.price || 0) * state.selectedSeats.length,
    },
    actions: {
        toggleSeat(seat: Seat) {
            const index = this.selectedSeats.findIndex((s) => s.id === seat.id)
            if (index >= 0) this.selectedSeats.splice(index, 1)
            else if (this.selectedSeats.length < 6) this.selectedSeats.push(seat)
        },
        resetBooking() {
            this.movie = null
            this.showtime = null
            this.selectedSeats = []
        }
    }
})