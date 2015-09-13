/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}


/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ function(module, exports) {

	'use strict';

	var $window = $(window);

	var $navBar = $('nav'),
	    $linksContainer = $('.navigation'),
	    $mainSection = $('.section__main'),
	    $aboutSection = $('.section__about'),
	    $faqSection = $('.section__faq'),
	    $scheduleSection = $('.section__schedule'),
	    $sponsorsSection = $('.section__sponsors'),
	    $beatingHeart = $('.beating-heart');

	var navBarOffset = 66;

	var mainSectionTop = $mainSection.position().top - navBarOffset,
	    aboutSectionTop = $aboutSection.position().top - navBarOffset,
	    faqSectionTop = $faqSection.position().top - navBarOffset,
	    scheduleSectionTop = $scheduleSection.position().top - navBarOffset,
	    sponsorsSectionTop = $sponsorsSection.position().top - navBarOffset;

	// Colors of different sections of the page
	var mainSectionColor = '#223241',
	    aboutSectionColor = '#1A252F',
	    faqSectionColor = '#40626D',
	    scheduleSectionColor = '#224252',
	    sponsorsSectionColor = '#FFFFFF';

	var sections = {
		"main": {
			"domEl": $mainSection,
			"top": mainSectionTop,
			"bg_color": mainSectionColor
		},
		"about": {
			"domEl": $aboutSection,
			"top": aboutSectionTop,
			"bg_color": aboutSectionColor
		},
		"faq": {
			"domEl": $faqSection,
			"top": faqSectionTop,
			"bg_color": faqSectionColor
		},
		"schedule": {
			"domEl": $scheduleSection,
			"top": scheduleSectionTop,
			"bg_color": scheduleSectionColor
		},
		"sponsors": {
			"domEl": $sponsorsSection,
			"top": sponsorsSectionTop,
			"bg_color": sponsorsSectionColor
		}
	};

	// Attaching event listener to the window for listening to scrolling and adjustin the nav bar
	$window.on('scroll', function (event) {
		highlightRelevantLinkBasedOnPosition($window.scrollTop());
	});

	// Attaching event listener to the navigation links
	$linksContainer.children().each(function () {
		$(this).on('click', function () {
			var currentTargetAttr = $(this).attr('data-target');
			var scrollTopPos = sections[currentTargetAttr]["top"];
			$('html, body').animate({
				scrollTop: scrollTopPos
			}, 300, 'easeInOutQuint');
		});
	});

	// For the <3
	// $beatingHeart.on('mouseenter', function() {
	// 	$beatingHeart.addClass('beat-the-heart');
	// });

	//  $beatingHeart.on('webkitAnimationEnd oanimationend msAnimationEnd animationend', function() {
	//         $beatingHeart.removeClass('beat-the-heart');
	// });

	// Utitlity functions
	function highlightRelevantLinkBasedOnPosition(pageScrollPosition) {
		if (pageScrollPosition >= mainSectionTop && pageScrollPosition < aboutSectionTop) {
			selectNavLink("main");
		} else if (pageScrollPosition >= aboutSectionTop && pageScrollPosition < faqSectionTop) {
			selectNavLink("about");
		} else if (pageScrollPosition >= faqSectionTop && pageScrollPosition < scheduleSectionTop) {
			selectNavLink("faq");
		} else if (pageScrollPosition >= scheduleSectionTop && pageScrollPosition < sponsorsSectionTop) {
			selectNavLink("schedule");
		} else if (pageScrollPosition >= sponsorsSectionTop) {
			selectNavLink("sponsors");
		}
	}

	function setNavBarColor(color) {
		if ($navBar.css('background-color') !== color) {
			$navBar.css('background-color', color);
		}
	}

	function selectNavLink(linkDataAttr) {
		$linksContainer.children().each(function () {
			var currentTargetAttr = $(this).attr('data-target');
			if (currentTargetAttr === linkDataAttr) {
				$(this).addClass('active');
			} else {
				$(this).removeClass('active');
			}
		});
	}

/***/ }
/******/ ]);