<template>
    <div style="height: 100%;">
        <header>
            <div>
                <div><NuxtLink :to="{name: 'index'}">CTF-Ratings</NuxtLink></div>
                <div><NuxtLink :to="{name: 'events'}">events</NuxtLink></div>
            </div>
            <div>
                <div><a href="https://github.com/theoremoon/ctf-ratings">GitHub Repository</a></div>
            </div>
        </header>
        <main>
            <Nuxt />
        </main>
    </div>
</template>

<script>
</script>

<style>
header {
    display: flex;
    justify-content: space-between;
    width: 100%;
    padding: 0.5rem 1rem;
    background-color: #eeeeee;
    border-bottom: 2px solid #333333;
}
header div {
    display: flex;
    margin-right: 1rem;
}
main {
    height: calc(100% - 2rem - 5px);
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
