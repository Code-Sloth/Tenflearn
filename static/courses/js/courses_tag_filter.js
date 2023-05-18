import { cardHover } from './cardHover.js';
import { toggleBtn } from './course_courses.js';
import { tagBtnActive } from './coursesBtnActive.js';

const coursesContainer = document.querySelector('.courses-content-container');
const tagsContainer = document.querySelector('.skill-tags-container');
const categoryLinks = document.querySelectorAll('.sidebar-item');
const titleH1 = document.querySelector('.title');
const searchInput = document.querySelector('.search-course-input');

let selectedCategory = '';

categoryLinks.forEach((link) => {
  link.addEventListener('click', async (event) => {
    selectedCategory = link.dataset.category;

    try {
      const response = await fetch(`/courses/?category=${selectedCategory}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const html = await response.text();
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const courses = doc.querySelector('.courses-content-container');
      coursesContainer.innerHTML = courses.innerHTML;
      const tagContainer = doc.querySelector('.skill-tags-container');
      tagsContainer.innerHTML = tagContainer.innerHTML;

      const tags = tagsContainer.querySelectorAll('.skill-tags-btn');
      tagBtnActive();
      // 태그 비동기
      tags.forEach((tag) => {
        tag.addEventListener('click', async (event) => {
          const selectedTags = tagsContainer.querySelectorAll(
            '.skill-tags-btn-active'
          );
          // 선택한 태그들 array로 저장
          const tagSlugs = Array.from(selectedTags)
            .map((tag) => tag.dataset.slug)
            .join(',');
          const optionBtnTags = document.querySelectorAll(
            '.courseInfo-btn-active'
          );
          const optionTags = Array.from(optionBtnTags)
            .map((option) => option.dataset.option)
            .join(',');

          try {
            const response = await fetch(
              `/courses/?category=${selectedCategory}&tags=${tagSlugs}&option=${optionTags}`
            );
            console.log(response);
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const courses = doc.querySelector('.courses-content-container');
            coursesContainer.innerHTML = courses.innerHTML;
            cardHover();
            toggleBtn();
          } catch (error) {
            console.error(error);
          }
        });
      });

      titleH1.textContent = selectedCategory;
      const context = link.textContent.trim();
      searchInput.placeholder = context + '  검색';
      cardHover();
      toggleBtn();
    } catch (error) {
      console.error(error);
    }
  });
});

// 태그 비동기
const tags = document.querySelectorAll('.skill-tags-btn');

tags.forEach((tag) => {
  tag.addEventListener('click', async (event) => {
    const selectedTags = document.querySelectorAll('.skill-tags-btn-active');
    // 선택한 태그들 array로 저장
    const tagSlugs = Array.from(selectedTags)
      .map((tag) => tag.dataset.slug)
      .join(',');
    const optionBtnTags = document.querySelectorAll('.courseInfo-btn-active');
    const optionTags = Array.from(optionBtnTags)
      .map((option) => option.dataset.option)
      .join(',');

    try {
      const response = await fetch(
        `/courses/?category=${selectedCategory}&tags=${tagSlugs}&option=${optionTags}`
      );
      console.log(response);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const html = await response.text();
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const courses = doc.querySelector('.courses-content-container');
      coursesContainer.innerHTML = courses.innerHTML;
      cardHover();
      toggleBtn();
    } catch (error) {
      console.error(error);
    }
  });
});

const optionButtons = document.querySelectorAll('.courseInfo-tag');
optionButtons.forEach((optionBtn) => {
  optionBtn.addEventListener('click', async (event) => {
    const selectedTags = document.querySelectorAll('.skill-tags-btn-active');
    const tagSlugs = Array.from(selectedTags)
      .map((tag) => tag.dataset.slug)
      .join(',');
    const sortOption = sortSelect.value;
    const optionBtnTags = document.querySelectorAll('.courseInfo-btn-active');
    const optionTags = Array.from(optionBtnTags)
      .map((option) => option.dataset.option)
      .join(',');

    try {
      const response = await fetch(
        `/courses/?category=${selectedCategory}&tags=${tagSlugs}&option=${optionTags}`
      );
      console.log(response);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const html = await response.text();
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const courses = doc.querySelector('.courses-content-container');
      coursesContainer.innerHTML = courses.innerHTML;
      cardHover();
      toggleBtn();
    } catch (error) {
      console.error(error);
    }
  });
});

const sortSelect = document.querySelector('.form-select');
sortSelect.addEventListener('change', async (event) => {
  const selectedTags = document.querySelectorAll('.skill-tags-btn-active');
  const tagSlugs = Array.from(selectedTags)
    .map((tag) => tag.dataset.slug)
    .join(',');
  const sortOption = event.target.value;
  const optionBtnTags = document.querySelectorAll('.courseInfo-btn-active');
  const optionTags = Array.from(optionBtnTags)
    .map((option) => option.dataset.option)
    .join(',');
  try {
    const response = await fetch(
      `/courses/?category=${selectedCategory}&tags=${tagSlugs}&option=${optionTags}&sort=${sortOption}`
    );
    console.log(response);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const html = await response.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const courses = doc.querySelector('.courses-content-container');
    coursesContainer.innerHTML = courses.innerHTML;
    cardHover();
    toggleBtn();
  } catch (error) {
    console.error(error);
  }
});
