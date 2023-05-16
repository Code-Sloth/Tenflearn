const detailATop = document.querySelector('.section-js-top')
const detailAReviews = document.querySelector('.section-js-reviews')

function handleHashChange() {
  const currentHash = window.location.hash

  detailATop.classList.remove('course-detail-black')
  detailAReviews.classList.remove('course-detail-black')

  if (currentHash === '#top') {
    detailATop.classList.add('course-detail-black')
  } else if (currentHash === '#reviews') {
    detailAReviews.classList.add('course-detail-black')
  }
}

window.addEventListener('hashchange', handleHashChange)

const currentHash = window.location.hash

detailATop.classList.remove('course-detail-black')
detailAReviews.classList.remove('course-detail-black')

if (currentHash === '#top') {
  detailATop.classList.add('course-detail-black')
} else if (currentHash === '#reviews') {
  detailAReviews.classList.add('course-detail-black')
}

var modal = document.getElementById("myModal");
var div = document.querySelector('.banner-container-left');

div.addEventListener('click', function() {
  modal.style.display = "block";
});

window.addEventListener('click', function(event) {
  if (event.target === modal) {
    modal.style.display = "none";
  }
});


var iframes = document.getElementsByClassName("modal-content-list")[0].getElementsByTagName("iframe");
var firstVideo = iframes[0].cloneNode(true);
var bodyVideo = document.getElementsByClassName("modal-content-video")[0];
bodyVideo.appendChild(firstVideo);

function playVideo(index) {
  bodyVideo.innerHTML = "";
  var targetVideo = iframes[index].cloneNode(true);
  bodyVideo.appendChild(targetVideo);
}

var buttons = document.getElementsByClassName("modal-content-list")[0].getElementsByTagName("button");
for (var i = 0; i < buttons.length; i++) {
  buttons[i].addEventListener("click", function () {
    var index = parseInt(this.getAttribute("data-index"));
    playVideo(index);
  });
}

var closeButton = document.querySelector(".close-btn");
closeButton.addEventListener("click", function () {
  var modal = document.getElementById("myModal");
  modal.style.display = "none";
});
