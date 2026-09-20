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

/* Galería: visor de fotos a pantalla completa con navegación anterior/siguiente. */
(function () {
  var galeria = document.getElementById('galeria');
  var visor = document.getElementById('visor');
  if (!galeria || !visor) return;

  var enlaces = Array.prototype.slice.call(galeria.querySelectorAll('a'));
  var visorImg = document.getElementById('visor-img');
  var contador = document.getElementById('visor-contador');
  var indice = 0;
  var disparador = null;

  function mostrar(i) {
    indice = (i + enlaces.length) % enlaces.length;
    var enlace = enlaces[indice];
    var img = enlace.querySelector('img');
    visorImg.src = enlace.getAttribute('href');
    visorImg.alt = img ? img.alt : '';
    contador.textContent = (indice + 1) + ' de ' + enlaces.length;
  }

  function abrir(i, origen) {
    disparador = origen || null;
    mostrar(i);
    visor.hidden = false;
    document.body.style.overflow = 'hidden';
    document.getElementById('visor-cerrar').focus();
  }

  function cerrar() {
    visor.hidden = true;
    document.body.style.overflow = '';
    visorImg.src = '';
    if (disparador) disparador.focus();
  }

  enlaces.forEach(function (enlace, i) {
    enlace.addEventListener('click', function (e) {
      e.preventDefault();
      abrir(i, enlace);
    });
  });

  document.getElementById('visor-cerrar').addEventListener('click', cerrar);
  document.getElementById('visor-prev').addEventListener('click', function () { mostrar(indice - 1); });
  document.getElementById('visor-next').addEventListener('click', function () { mostrar(indice + 1); });

  visor.addEventListener('click', function (e) {
    if (e.target === visor) cerrar();
  });

  document.addEventListener('keydown', function (e) {
    if (visor.hidden) return;
    if (e.key === 'Escape') cerrar();
    if (e.key === 'ArrowLeft') mostrar(indice - 1);
    if (e.key === 'ArrowRight') mostrar(indice + 1);
  });
})();
