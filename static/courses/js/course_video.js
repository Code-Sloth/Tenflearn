// 강의 설명 버튼
const descBtn = document.querySelector('.descriptions-btn');
const courseDescriptionContent = document.querySelector('.course-descriptions-content');
descBtn.addEventListener('click', function() {
  coursetextareaContent.classList.remove('show');
  courseDescriptionContent.classList.toggle('show2');
  if (descBtn.textContent === '강의 설명 보기') {
    descBtn.textContent = '강의 설명 닫기';
  } else {
    descBtn.textContent = '강의 설명 보기';
  }
});

// 메모 버튼
const textareaBtn = document.querySelector('.textarea-btn');
const coursetextareaContent = document.querySelector('.course-descriptions-file');
textareaBtn.addEventListener('click', function() {
  courseDescriptionContent.classList.remove('show2');
  coursetextareaContent.classList.toggle('show');
  if (textareaBtn.textContent === '메모 작성') {
    textareaBtn.textContent = '메모 닫기';
  } else {
    textareaBtn.textContent = '메모 작성';
  }
});

// 메모 저장
function Download(){
  let memo = document.querySelector("#memo");
  let file_name = document.querySelector('.course-descriptions h3').textContent;
  const blob = new Blob([memo.value], {type:'text/plain'});
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.style.display = 'none';
  a.href = url;
  a.download = file_name;
  document.body.appendChild(a);
  
  a.click();

  setTimeout(() => {
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
  }, 100);
}

// video
var iframes = document.getElementsByClassName("course-video-list")[0].getElementsByTagName("iframe");
var firstVideo = iframes[0].cloneNode(true);
var bodyVideo = document.getElementsByClassName("course-video")[0];
bodyVideo.appendChild(firstVideo);

function playVideo(index) {
  bodyVideo.innerHTML = "";
  var targetVideo = iframes[index].cloneNode(true);
  bodyVideo.appendChild(targetVideo);
}
var selectElement = document.getElementById("video-select");
selectElement.addEventListener("change", function () {
  var selectedIndex = parseInt(this.value);
  playVideo(selectedIndex);
});
