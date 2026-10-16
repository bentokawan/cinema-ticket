import axios from 'axios'

export const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
})

export const formatRupiah = (n: number | string) => 'Rp ' + Number(n).toLocaleString('id-ID')
export const formatJam = (iso: string) => new Date(iso).toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })
export const formatTanggal = (iso: string) => new Date(iso).toLocaleDateString('id-ID', { weekday: 'short', day: 'numeric', month: 'short' })