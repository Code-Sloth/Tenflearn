const cartBtns = document.querySelectorAll('.selector')

cartBtns.forEach((btn) => {
  btn.addEventListener('click', (event) => {
    
    const btnPrice = btn.querySelector('.selector-price')
    const btnRate = btn.querySelector('.selector-discount_rate')
    const btnDiscountedPrice = btn.querySelector('.selector-discounted_price')

    const cartPrice = document.querySelector('.cart-price')
    const cartRate = document.querySelector('.cart-discount_rate')
    const cartDiscountedPrice = document.querySelector('.cart-discounted_price')

    const formPrice = document.querySelector('.pay-button')

    cartPrice.textContent = `${parseInt(btnPrice.value).toLocaleString()}원`
    cartRate.textContent = `${btnRate.value}%`
    cartDiscountedPrice.textContent = `${parseInt(btnDiscountedPrice.value).toLocaleString()}원`

    formPrice.value = btnDiscountedPrice.value

    if (btn.classList.contains('cart-gray')) {
      btn.classList.remove('cart-gray')
      cartPrice.textContent = '-'
      cartRate.textContent = '-'
      cartDiscountedPrice.textContent = '-'
    } else {
      btn.classList.add('cart-gray')
    }

    const coursePk = btn.querySelector('.selector-course_pk')
    const cartForm = document.querySelector('.cart-form')

    cartForm.setAttribute('action', `/${coursePk.value}/kakaopay/`)

    const cancelForm = document.querySelector('.cart-body-cancel')
    const cancelBtn = cancelForm.querySelector('button')

    cancelForm.setAttribute('action', `/course/${coursePk.value}/cart/`)
    cancelBtn.value = 1
  })
})