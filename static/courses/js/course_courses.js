
const toggleBtn = document.querySelector('.skill-tags-more');

toggleBtn.addEventListener('click', () => {
  const skillTagsContainer = document.querySelector('.skill-tags-container');
  if (!skillTagsContainer.classList.contains('overflow-hidden')) {
    skillTagsContainer.classList.add('overflow-hidden');
    toggleBtn.classList.replace('bi-chevron-compact-up','bi-chevron-compact-down')
  } else {
    skillTagsContainer.classList.remove('overflow-hidden');
    toggleBtn.classList.replace('bi-chevron-compact-down','bi-chevron-compact-up')
  }
});