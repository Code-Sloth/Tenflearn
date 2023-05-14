import { cardHover } from "./cardHover.js";

const tags = document.querySelectorAll('.skill-tags-btn');
const coursesContainer = document.querySelector('.courses-content-container');

tags.forEach(tag => {
  tag.addEventListener('click', async (event) => {
    const selectedTags = document.querySelectorAll('.skill-tags-btn-active');
    // 선택한 태그들 array로 저장
    const tagSlugs = Array.from(selectedTags).map(tag => tag.dataset.slug).join(',');
    
    try {
      const response = await fetch(`/courses/?tags=${tagSlugs}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const html = await response.text();
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html') 
      const courses = doc.querySelector('.courses-content-container')
      coursesContainer.innerHTML = courses.innerHTML;
      cardHover();
    } catch (error) {
      console.error(error);
    }
  });
});