$(document).ready(function () {
  const targetScroll = $('#scroll-to-me-js');
  if (targetScroll.length) {
    $('html, body').animate({
      scrollTop: targetScroll.offset().top
    }, 1000);
  }
});
