const starpointInputs = document.querySelectorAll('.star_radio');
const reviewStarInput = document.querySelector('#id_star');

starpointInputs.forEach(input => {
  input.addEventListener('click', () => {
    reviewStarInput.value = input.value;
  });
});
