const titleLinks = document.querySelectorAll('.sidebar-item')
const titleH1 = document.querySelector('.title')
const searchInput = document.querySelector(".search-course-input");

titleLinks.forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault(); // 기본 동작 방지
    const linkText = event.currentTarget.textContent;
    titleH1.textContent = linkText;

    const context = link.textContent.trim();
    searchInput.placeholder = context + " 강의 검색";
  });
});

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