const searchForm = document.querySelector('search-course');

searchForm.addEventListener('submit', (e) => {
  e.preventDefault();

  const form = e.target;
  const searchInput = form.querySelector('search-course-input')

  const searchValue = searchInput.value

  const url = new URL(window.location.href``)
  const searchParams = url.searchParams

  searchParams.delete('search-q')
  searchParams.set('search-q', searchValue)

  window.location.href = url.toString()

});
