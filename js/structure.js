(function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 54)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 56
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-shrink");
    } else {
      $("#mainNav").removeClass("navbar-shrink");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Hide navbar when modals trigger
  $('.portfolio-modal').on('show.bs.modal', function(e) {
    $(".navbar").addClass("d-none");
  })
  $('.portfolio-modal').on('hidden.bs.modal', function(e) {
    $(".navbar").removeClass("d-none");
  })

})(jQuery); // End of use strict

function Lien() {
	i = document.Choix.Liste.selectedIndex;
	if (i == 0) return;
	url = document.Choix.Liste.options[i].value;
	parent.location.href = url;
}

function showSection(sectionId) {
  // Hide all sections and reset opacity
  const sections = document.getElementsByClassName('tree');
  for (let i = 0; i < sections.length; i++) {
      sections[i].style.display = 'none';
      sections[i].style.opacity = '0';
  }

  // Show the selected section
  const selectedSection = document.getElementById(sectionId);
  selectedSection.style.display = 'block';

  // Change its opacity with a transition
  setTimeout(function() {
      selectedSection.style.opacity = '1';
  }, 10); // Short delay to ensure display block is applied before opacity transition
}
