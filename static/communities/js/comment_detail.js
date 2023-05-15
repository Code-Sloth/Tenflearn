document.addEventListener('DOMContentLoaded', function() {

  document.getElementById('detail-share-btn').addEventListener('click', function() {
      var currentUrl = window.location.href
      var tempInput = document.createElement('input')

      tempInput.value = currentUrl
      document.body.appendChild(tempInput)

      tempInput.select()

      document.execCommand('copy')
 
      document.body.removeChild(tempInput)

      alert('URL이 복사되었습니다!')
  })
})

const recommentStartBtn = document.querySelector('.recomment-header-btn')
const recommentFormDiv = document.querySelector('.recomment-header-none')
const recommentCancleBtn = document.querySelector('.recomment-cancle')

recommentStartBtn.addEventListener('click', (event) => {
  recommentStartBtn.classList.remove('d-flex')
  recommentStartBtn.classList.add('d-none')

  recommentFormDiv.classList.remove('d-none')
  recommentFormDiv.classList.add('d-block')
})

recommentCancleBtn.addEventListener('click', (event) => {
  recommentStartBtn.classList.remove('d-none')
  recommentStartBtn.classList.add('d-flex')

  recommentFormDiv.classList.remove('d-block')
  recommentFormDiv.classList.add('d-none')
})