let menu = document.querySelector('.hamburger')
let sideBar = document.querySelector('#sidebar')

window.onscroll = () => {
    sideBar.classList.remove('active')
}
menu.addEventListener('click', () => {
    sideBar.classList.toggle('active')
})
