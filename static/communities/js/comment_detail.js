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

// 댓글 좋아요 ajax

const likeForm = document.querySelector('.detail-left-section-form')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

likeForm.addEventListener('submit', (event) => {
  event.preventDefault()

  const commentId = event.target.dataset.commentId
  const likeBtn = event.submitter
  const likeValue = likeBtn.value

  const formData = new FormData(likeForm)
  formData.append('like_value', likeValue)

  axios({
    method: "POST",
    url: `/communities/comments/${commentId}/likes/`,
    headers: {'X-CSRFToken': csrftoken},
    data: formData
  })

    .then((response) => {
      if (response.data.error) {

        const errorMessage = response.data.error

        alert(errorMessage)

      } else {

      const isLiked = response.data.is_liked
      const isUnLiked = response.data.is_unliked
      const likeIcon = likeForm.querySelector('.comment-like-icon')
      const UnLikeIcon = likeForm.querySelector('.comment-unlike-icon')

      const likeCount = likeForm.querySelector('.comment-detail-left-section-count')

      likeCount.textContent = response.data.comment_like

      if (isLiked === true) {
        likeIcon.classList.remove('like_gray')
        likeIcon.classList.add('like_green')
      } else if (isLiked == false) {
        likeIcon.classList.add('like_gray')
        likeIcon.classList.remove('like_green')
      }

      if (isUnLiked === true) {
        UnLikeIcon.classList.remove('like_gray')
        UnLikeIcon.classList.add('like_green')
      } else if (isUnLiked == false) {
        UnLikeIcon.classList.add('like_gray')
        UnLikeIcon.classList.remove('like_green')
      }
      }
    })

    .catch((error) => {
      console.log(error.response)
    })
})

const recommentForms = document.querySelectorAll('.recomment-section-form')

recommentForms.forEach((recommentForm) => {

  recommentForm.addEventListener('submit', (event) => {
    event.preventDefault()
  
    const commentId = event.target.dataset.commentId
    const recommentId = recommentForm.querySelector('.recomment-section-id').value
    const likeBtn = event.submitter
    const likeValue = likeBtn.value
  
    const formData = new FormData(recommentForm)
    formData.append('like_value', likeValue)
  
    axios({
      method: "POST",
      url: `/communities/comments/${commentId}/recomments/${recommentId}/likes/`,
      headers: {'X-CSRFToken': csrftoken},
      data: formData
    })
  
      .then((response) => {
        if (response.data.error) {

          const errorMessage = response.data.error

          alert(errorMessage)

        } else {

          const isLiked = response.data.is_liked
          const isUnLiked = response.data.is_unliked
          const likeIcon = recommentForm.querySelector('.recomment-like-icon')
          const UnLikeIcon = recommentForm.querySelector('.recomment-unlike-icon')
    
          const likeCount = recommentForm.querySelector('.recomment-detail-left-section-count')
    
          likeCount.textContent = response.data.recomment_like
    
          if (isLiked === true) {
            likeIcon.classList.remove('like_gray')
            likeIcon.classList.add('like_green')
          } else if (isLiked == false) {
            likeIcon.classList.add('like_gray')
            likeIcon.classList.remove('like_green')
          }
    
          if (isUnLiked === true) {
            UnLikeIcon.classList.remove('like_gray')
            UnLikeIcon.classList.add('like_green')
          } else if (isUnLiked == false) {
            UnLikeIcon.classList.add('like_gray')
            UnLikeIcon.classList.remove('like_green')
          }
        }

      })
  
      .catch((error) => {
        console.log(error.response)
      })
  })
})

// 대댓글 비동기 생성

document.addEventListener('DOMContentLoaded', () => {
  const recommentForm = document.querySelector('.recomment-section-create-form')
  const recommentContainer = document.querySelector('.recomment-section')

  recommentForm.addEventListener('submit', (event) => {
    event.preventDefault()

    const commentId = recommentForm.dataset.commentId
    const formData = new FormData(recommentForm)

    axios({
      method: 'POST',
      url: `/communities/comments/${commentId}/recomments/create/`,
      headers: { 'X-CSRFToken': csrftoken },
      data: formData
    })
      .then((response) => {
        recommentContainer.innerHTML = response.data.recomment_section_html
        
        const recommentCount = document.querySelector('.recomment-header > span')
        console.log(recommentCount)
        recommentCount.textContent = response.data.recomment_count
      })
      .catch((error) => {
        console.log(error.response)
      })
  })

})
