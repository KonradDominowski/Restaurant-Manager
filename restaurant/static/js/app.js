const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

const toastElList = [].slice.call(document.querySelectorAll('.toast'))
const toastList = toastElList.map(function (toastEl) {
    return new bootstrap.Toast(toastEl, option)
})