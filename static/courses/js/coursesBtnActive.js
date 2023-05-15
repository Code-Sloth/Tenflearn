const targetBtns = document.querySelectorAll('.skill-tags-btn');
const targetInfoBtns = document.querySelectorAll('.courseInfo-tag');

targetBtns.forEach((targetBtn) => {
  targetBtn.addEventListener('click', () => {
    if (targetBtn.classList.contains('skill-tags-btn-active')) {
      targetBtn.classList.remove('bi-check-lg', 'skill-tags-btn-active');
    } else {
      targetBtn.classList.add('bi-check-lg', 'skill-tags-btn-active');
    }
  });
})

targetInfoBtns.forEach((targetBtn) => {
  targetBtn.addEventListener('click', () => {
    if (targetBtn.classList.contains('courseInfo-btn-active')) {
      targetBtn.classList.remove('bi-check-lg', 'courseInfo-btn-active');
    } else {
      targetBtn.classList.add('bi-check-lg', 'courseInfo-btn-active');
    }
  });
})
