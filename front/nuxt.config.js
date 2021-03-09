export default {
    components: true,
    head: {
        titleTemplate: 'CTF-Ratings'
    },
    target: 'static',
    ssr: true,
    generate: {
        exclude: [
            /^\/team\/.+\//
        ]
    },
    router: {
        base: '/ctf-ratings/'
    }
}
