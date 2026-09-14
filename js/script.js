/* IașiAsigură — meniu mobil + an în footer. Fără tracking, fără cookie-uri. */
(function () {
  'use strict';
  var y = document.getElementById('year');
  if (y) y.textContent = String(new Date().getFullYear());
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.getElementById('nav-menu');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { menu.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); });
    });
  }
})();
