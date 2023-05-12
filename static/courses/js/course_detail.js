const detailATop = document.querySelector('.section-js-top')
const detailAReviews = document.querySelector('.section-js-reviews')

function handleHashChange() {
  const currentHash = window.location.hash

  detailATop.classList.remove('course-detail-black')
  detailAReviews.classList.remove('course-detail-black')

  if (currentHash === '#top') {
    detailATop.classList.add('course-detail-black')
  } else if (currentHash === '#reviews') {
    detailAReviews.classList.add('course-detail-black')
  }
}

window.addEventListener('hashchange', handleHashChange)

const currentHash = window.location.hash

detailATop.classList.remove('course-detail-black')
detailAReviews.classList.remove('course-detail-black')

if (currentHash === '#top') {
  detailATop.classList.add('course-detail-black')
} else if (currentHash === '#reviews') {
  detailAReviews.classList.add('course-detail-black')
}