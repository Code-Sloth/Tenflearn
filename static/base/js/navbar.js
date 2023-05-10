const offCourseA = document.querySelector('.off-course-a')
const offCommunityA = document.querySelector('.off-community-a');
const offCourseItems = document.querySelectorAll('.off-course')
const offCommunityItems = document.querySelectorAll('.off-community');

offCommunityA.addEventListener('mouseover', () => {
  offCommunityItems.forEach(item => {
    item.classList.remove('d-none')
    item.classList.add('d-block')
  })
})

offCourseA.addEventListener('mouseover', () => {
  offCourseItems.forEach(item => {
    item.classList.remove('d-none')
    item.classList.add('d-block')
  })
})

document.addEventListener('mouseover', (event) => {
  const target = event.target

  if (!target.classList.contains('off-community-a') && !target.classList.contains('off-community')) {
    offCommunityItems.forEach(item => {
      item.classList.remove('d-block')
      item.classList.add('d-none')
    })  
  }  

  if (!target.classList.contains('off-course-a') && !target.classList.contains('off-course')) {
    offCourseItems.forEach(item => {
      item.classList.remove('d-block')
      item.classList.add('d-none')
    })  
  } 
})  

