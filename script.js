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

/* Fotos de producto: visor a pantalla completa con navegación anterior/siguiente. */
(function () {
  var fotos = document.querySelector('.visor-fotos');
  var visor = document.getElementById('visor');
  if (!fotos || !visor) return;

  var botones = Array.prototype.slice.call(fotos.querySelectorAll('.ver-foto'));
  var visorImg = document.getElementById('visor-img');
  var contador = document.getElementById('visor-contador');
  var prev = document.getElementById('visor-prev');
  var next = document.getElementById('visor-next');
  var indice = 0;
  var disparador = null;

  if (botones.length <= 1) {
    prev.hidden = true;
    next.hidden = true;
  }

  function mostrar(i) {
    indice = (i + botones.length) % botones.length;
    var boton = botones[indice];
    var img = boton.querySelector('img');
    visorImg.src = boton.getAttribute('data-src');
    visorImg.alt = img ? img.alt : '';
    contador.textContent = (indice + 1) + ' de ' + botones.length;
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

  botones.forEach(function (boton, i) {
    boton.addEventListener('click', function () {
      abrir(i, boton);
    });
  });

  document.getElementById('visor-cerrar').addEventListener('click', cerrar);
  prev.addEventListener('click', function () { mostrar(indice - 1); });
  next.addEventListener('click', function () { mostrar(indice + 1); });

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
