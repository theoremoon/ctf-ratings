export default {
    components: true,
    head: {
        titleTemplate: 'CTF-Ratings'
    },
    target: 'static',
    ssr: false,
    // generate: {
    //     exclude: [
    //         /^\/team\/.+\//
    //     ]
    // },
    // router: {
    //     base: '/ctf-ratings/'
    // },
    plugins: [
        '@/plugins/vue-virtual-scroll-list.js',
    ],
    css: [
        '@/assets/css/main.css'
    ],
}
