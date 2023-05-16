import { cardHover } from "./cardHover.js";
import { tagBtnActive } from "./coursesBtnActive.js";



const coursesContainer = document.querySelector('.courses-content-container');
const tagsContainer = document.querySelector('.skill-tags-container');
const categoryLinks = document.querySelectorAll('.sidebar-item');
const titleH1 = document.querySelector('.title')
const searchInput = document.querySelector(".search-course-input");

let selectedCategory = ""

categoryLinks.forEach(link => {
  link.addEventListener('click', async (event) => {
    
    selectedCategory = link.dataset.category;

    try {
      const response = await fetch(`/courses/?category=${selectedCategory}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const html = await response.text();
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html') 
      const courses = doc.querySelector('.courses-content-container')
      coursesContainer.innerHTML = courses.innerHTML;
      const tagContainer = doc.querySelector('.skill-tags-container'); 
      tagsContainer.innerHTML = tagContainer.innerHTML;

      const tags = tagsContainer.querySelectorAll('.skill-tags-btn');
      tagBtnActive()
  
      tags.forEach(tag => {
        tag.addEventListener('click', async (event) => {
          const selectedTags = tagsContainer.querySelectorAll('.skill-tags-btn-active');
          // 선택한 태그들 array로 저장
          const tagSlugs = Array.from(selectedTags).map(tag => tag.dataset.slug).join(',');
          console.log(tagSlugs)
          
          try {
            const response = await fetch(`/courses/?category=${selectedCategory}&tags=${tagSlugs}`);
            console.log(response)
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


      titleH1.textContent = selectedCategory
      const context = link.textContent.trim();
      searchInput.placeholder = context + "  검색";
      cardHover();
    } catch (error) {
      console.error(error);
    }
  });
});


  const tags = document.querySelectorAll('.skill-tags-btn');
  
  tags.forEach(tag => {
    tag.addEventListener('click', async (event) => {
      const selectedTags = document.querySelectorAll('.skill-tags-btn-active');
      // 선택한 태그들 array로 저장
      const tagSlugs = Array.from(selectedTags).map(tag => tag.dataset.slug).join(',');
      
      try {
        const response = await fetch(`/courses/?category=${selectedCategory}&tags=${tagSlugs}`);
        console.log(response)
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

  
const sortSelect = document.querySelector('.form-select')
sortSelect.addEventListener('change', async (event) => {
  const selectedTags = document.querySelectorAll('.skill-tags-btn-active');
  const tagSlugs = Array.from(selectedTags).map(tag => tag.dataset.slug).join(',');
  const sortOption = event.target.value;
  try {
    const response = await fetch(`/courses/?category=${selectedCategory}&tags=${tagSlugs}&sort=${sortOption}`);
    console.log(response)
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