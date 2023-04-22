const ERROR_BG = "#ff0000"
const SUCCESS_BG = "#00c1b2"

function hideMyToast() {
    const activeToast = document.querySelectorAll('.toastify.on')
    activeToast.forEach(function(item) {
        item.className = item.className.replace(" on", "")
    })
}

function myToast(msg, bgColor, destination='') {
    hideMyToast()
    const activeToast = document.querySelectorAll('.toastify.on')
    activeToast.forEach(function(item) {
        item.className = item.className.replace(" on", "")
    })
    const toastObj = {
        text: msg,
        duration: 3000,
        backgroundColor: bgColor,
        position: "center",
        offset: {x: 0, y: 450},
        className: "border-radius-5px",
        close: true,
    }
    if(destination) {
        toastObj['destination'] = destination
    }
    Toastify(toastObj).showToast()
}