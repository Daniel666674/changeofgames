/* Menú del celular: abre y cierra el panel de navegación. */
(function () {
  var boton = document.querySelector('.menu-btn');
  var menu = document.getElementById('menu');
  if (!boton || !menu) return;

  function poner(abierto) {
    boton.setAttribute('aria-expanded', abierto ? 'true' : 'false');
    boton.setAttribute('aria-label', abierto ? 'Cerrar menú' : 'Abrir menú');
    menu.classList.toggle('abierto', abierto);
  }

  boton.addEventListener('click', function () {
    poner(boton.getAttribute('aria-expanded') !== 'true');
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') poner(false);
  });

  menu.addEventListener('click', function (e) {
    if (e.target.closest('a')) poner(false);
  });
})();
