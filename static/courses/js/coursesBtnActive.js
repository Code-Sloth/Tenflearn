tagBtnActive()
export function tagBtnActive() {

  const targetBtns = document.querySelectorAll('.skill-tags-btn');
  
  targetBtns.forEach((targetBtn) => {
    targetBtn.addEventListener('click', () => {
      if (targetBtn.classList.contains('skill-tags-btn-active')) {
        targetBtn.classList.remove('bi-check-lg', 'skill-tags-btn-active');
      } else {
        targetBtn.classList.add('bi-check-lg', 'skill-tags-btn-active');
      }
    });
  })
  
}

optionBtnActive()
export function optionBtnActive() {
  const targetInfoBtns = document.querySelectorAll('.courseInfo-tag');
    targetInfoBtns.forEach((targetBtn) => {
      targetBtn.addEventListener('click', () => {
      if (targetBtn.classList.contains('courseInfo-btn-active')) {
        targetBtn.classList.remove('bi-check-lg', 'courseInfo-btn-active');
      } else {
        targetBtn.classList.add('bi-check-lg', 'courseInfo-btn-active');
      }
      
      const freeButton = document.querySelector('.courseInfo-tag[data-option="무료"]');
      const isActive = freeButton.classList.contains('courseInfo-btn-active');


      const discountButton = document.querySelector('.courseInfo-tag[data-option="할인중"]');
      if (isActive) {
        discountButton.disabled = true;
      } else{
        discountButton.disabled = false;
      }
    });
  })
}
