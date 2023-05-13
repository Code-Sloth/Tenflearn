const orderA = document.querySelectorAll('.middle-section-order-item')

orderA.forEach((btn) => {

  btn.addEventListener('click', (event) => {
    event.preventDefault()

    btnValue = btn.getAttribute('value')
    Url = window.location.href

    const reUrl = Url.replace(/&order=[\w\d]+/g,'')
    const newUrl = `${reUrl}&order=${btnValue}`

    window.location.href = newUrl

  })
})

const searchForm = document.querySelector('.comment-middle-form')

searchForm.addEventListener('submit', (event) => {

    event.preventDefault()

    const form = event.target
    const searchInput = form.querySelector('.search-q')
    const tagInput = form.querySelector('.tag-q')
    
    const searchValue = searchInput.value
    const tagValue = tagInput.value

    const url = new URL(window.location.href)
    const searchParams = url.searchParams

    searchParams.delete('search-q')
    searchParams.delete('tag-q')

    searchParams.set('search-q', searchValue)
    searchParams.set('tag-q', tagValue)

    window.location.href = url.toString()
})