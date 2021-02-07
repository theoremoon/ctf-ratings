<template>
    <div>
        <header>
            <div><NuxtLink :to="{name: 'index'}">CTF-Ratings</NuxtLink></div>
            <div><NuxtLink :to="{name: 'events'}">events</NuxtLink></div>
        </header>
        <main>
            <Nuxt />
        </main>
    </div>
</template>

<script>
</script>

<style>
html, body {
    padding: 0;
    margin: 0;
    font-family: arial,sans-serif;
}
header {
    display: flex;
    padding: 0.5rem 1rem;
    background-color: #eeeeee;
    border-bottom: 2px solid #333333;
}
header>div {
    margin-right: 1rem;
}
main {
    margin: 8px;
}
.flex {
    display: flex;
}

th,td {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    padding: 1rem 0.5rem;
    border-bottom: 1px solid #ccc;
}
th {
    background-color: #f0f0f0;
}
td {
    background-color: #f9f9f9;
}
table {
    border-collapse: collapse;
}
tr:hover>td {
    background-color: #ffffff;
    font-weight: bold;
}
</style>
