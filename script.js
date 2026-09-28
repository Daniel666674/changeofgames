/* Change of Games — interacciones del sitio. Sin librerías. */

var MOVIMIENTO_REDUCIDO = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* Encabezado: fondo con desenfoque al hacer scroll. */
(function () {
  var cab = document.querySelector('[data-cab]');
  if (!cab) return;
  function revisar() { cab.classList.toggle('scrolled', window.scrollY > 8); }
  revisar();
  window.addEventListener('scroll', revisar, { passive: true });
})();

/* Menú del celular: abre y cierra el panel de navegación. */
(function () {
  var boton = document.querySelector('.menu-btn');
  var menu = document.getElementById('menu');
  if (!boton || !menu) return;

  function poner(abierto) {
    boton.setAttribute('aria-expanded', abierto ? 'true' : 'false');
    boton.setAttribute('aria-label', abierto ? 'Cerrar menú' : 'Abrir menú');
    menu.classList.toggle('abierto', abierto);
    document.body.classList.toggle('menu-abierto', abierto);
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
  window.addEventListener('resize', function () {
    if (window.innerWidth > 960) poner(false);
  });
})();

/* Abierto / cerrado según la hora de Bogotá. Festivos no se detectan. */
(function () {
  var HORAS = { 0: [9, 12], 1: [8, 18], 2: [8, 18], 3: [8, 18], 4: [8, 18], 5: [8, 18], 6: [9, 16] };
  var DIAS = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };

  function hora12(h) {
    if (h === 12) return '12 m.';
    return h < 12 ? h + ' a. m.' : (h - 12) + ' p. m.';
  }

  var dia, minutos;
  try {
    var partes = new Intl.DateTimeFormat('en-US', {
      timeZone: 'America/Bogota', weekday: 'short', hour: 'numeric', minute: 'numeric', hourCycle: 'h23'
    }).formatToParts(new Date());
    var v = {};
    partes.forEach(function (p) { v[p.type] = p.value; });
    dia = DIAS[v.weekday];
    minutos = (parseInt(v.hour, 10) % 24) * 60 + parseInt(v.minute, 10);
  } catch (e) {
    return;
  }
  if (dia === undefined || isNaN(minutos)) return;

  var hoy = HORAS[dia];
  var abierto = minutos >= hoy[0] * 60 && minutos < hoy[1] * 60;
  var texto;
  if (abierto) {
    texto = 'Abierto ahora · hasta las ' + hora12(hoy[1]);
  } else if (minutos < hoy[0] * 60) {
    texto = 'Cerrado · abre hoy a las ' + hora12(hoy[0]);
  } else {
    texto = 'Cerrado · abre mañana a las ' + hora12(HORAS[(dia + 1) % 7][0]);
  }

  document.querySelectorAll('[data-estado]').forEach(function (el) {
    el.classList.add(abierto ? 'abierto' : 'cerrado');
    var span = el.querySelector('span');
    if (span) span.textContent = texto;
  });
  document.querySelectorAll('[data-estado-punto]').forEach(function (el) {
    el.classList.add(abierto ? 'abierto' : 'cerrado');
  });
  document.querySelectorAll('[data-horario] li').forEach(function (li) {
    var dias = li.getAttribute('data-dias').split(',');
    if (dias.indexOf(String(dia)) !== -1) li.classList.add('hoy');
  });
})();

/* Aparición suave de bloques al entrar en pantalla. */
(function () {
  var items = document.querySelectorAll('[data-r]');
  if (!('IntersectionObserver' in window) || MOVIMIENTO_REDUCIDO) {
    items.forEach(function (el) { el.classList.add('visto'); });
    return;
  }
  var obs = new IntersectionObserver(function (entradas) {
    entradas.forEach(function (en) {
      if (en.isIntersecting) {
        en.target.classList.add('visto');
        obs.unobserve(en.target);
      }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  items.forEach(function (el) { obs.observe(el); });
})();

/* Luz que sigue el cursor en las tarjetas. */
(function () {
  if (MOVIMIENTO_REDUCIDO) return;
  document.querySelectorAll('.feat, .serv').forEach(function (el) {
    el.addEventListener('pointermove', function (e) {
      var r = el.getBoundingClientRect();
      el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      el.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });
})();

/* Riel de productos destacados: flechas anterior / siguiente. */
(function () {
  var pista = document.querySelector('[data-riel-pista]');
  if (!pista) return;
  var botones = document.querySelectorAll('[data-riel]');

  function actualizar() {
    var max = pista.scrollWidth - pista.clientWidth - 4;
    botones.forEach(function (b) {
      var dir = parseInt(b.getAttribute('data-riel'), 10);
      b.disabled = dir < 0 ? pista.scrollLeft <= 4 : pista.scrollLeft >= max;
    });
  }
  botones.forEach(function (b) {
    b.addEventListener('click', function () {
      var tarjeta = pista.firstElementChild;
      var paso = tarjeta ? tarjeta.getBoundingClientRect().width + 16 : 300;
      pista.scrollBy({ left: paso * parseInt(b.getAttribute('data-riel'), 10), behavior: MOVIMIENTO_REDUCIDO ? 'auto' : 'smooth' });
    });
  });
  pista.addEventListener('scroll', actualizar, { passive: true });
  window.addEventListener('resize', actualizar);
  actualizar();
})();

/* Tienda: categoría, plataforma, búsqueda y orden. */
(function () {
  var tienda = document.getElementById('tienda');
  var filtros = document.getElementById('filtros');
  if (!tienda || !filtros) return;

  var chipsCat = Array.prototype.slice.call(filtros.querySelectorAll('.chip'));
  var chipsPlat = Array.prototype.slice.call(document.querySelectorAll('#plataformas .chip'));
  var buscar = document.getElementById('buscar');
  var orden = document.getElementById('orden');
  var conteo = document.getElementById('conteo');
  var vacio = document.getElementById('sin-resultados');
  var productos = Array.prototype.slice.call(tienda.querySelectorAll('.card-p'));
  productos.forEach(function (p, i) { p.setAttribute('data-orden', i); });

  var estado = { cat: 'todos', plat: 'todas', q: '' };

  function sinTildes(s) {
    return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  }

  function aplicar() {
    var q = sinTildes(estado.q.trim());
    var visibles = 0;
    productos.forEach(function (p) {
      var ok = (estado.cat === 'todos' || p.getAttribute('data-cat') === estado.cat) &&
        (estado.plat === 'todas' || p.getAttribute('data-plat') === estado.plat) &&
        (!q || sinTildes(p.getAttribute('data-nombre') + ' ' + p.getAttribute('data-plat') + ' ' + p.getAttribute('data-cat')).indexOf(q) !== -1);
      p.hidden = !ok;
      if (ok) visibles++;
    });
    conteo.textContent = visibles === 1 ? '1 producto' : visibles + ' productos';
    vacio.hidden = visibles !== 0;
    chipsCat.forEach(function (c) { c.setAttribute('aria-pressed', c.getAttribute('data-filtro') === estado.cat ? 'true' : 'false'); });
    chipsPlat.forEach(function (c) { c.setAttribute('aria-pressed', c.getAttribute('data-plat') === estado.plat ? 'true' : 'false'); });
  }

  function ordenar() {
    var modo = orden.value;
    var lista = productos.slice().sort(function (a, b) {
      if (modo === 'menor') return a.getAttribute('data-precio') - b.getAttribute('data-precio');
      if (modo === 'mayor') return b.getAttribute('data-precio') - a.getAttribute('data-precio');
      return a.getAttribute('data-orden') - b.getAttribute('data-orden');
    });
    lista.forEach(function (p) { tienda.appendChild(p); });
  }

  chipsCat.forEach(function (c) {
    c.addEventListener('click', function () { estado.cat = c.getAttribute('data-filtro'); aplicar(); });
  });
  chipsPlat.forEach(function (c) {
    c.addEventListener('click', function () { estado.plat = c.getAttribute('data-plat'); aplicar(); });
  });
  buscar.addEventListener('input', function () { estado.q = buscar.value; aplicar(); });
  orden.addEventListener('change', ordenar);

  var params = new URLSearchParams(window.location.search);
  var cat = params.get('cat');
  if (cat && chipsCat.some(function (c) { return c.getAttribute('data-filtro') === cat; })) estado.cat = cat;
  aplicar();
})();

/* Producto: miniaturas, visor a pantalla completa y barra de compra. */
(function () {
  var galeria = document.querySelector('[data-galeria]');
  if (!galeria) return;

  var fotos = JSON.parse(galeria.getAttribute('data-fotos'));
  var principal = galeria.querySelector('[data-principal]');
  var thumbs = Array.prototype.slice.call(galeria.querySelectorAll('.thumb'));
  var actual = 0;

  function elegir(i) {
    actual = i;
    principal.style.opacity = '0';
    setTimeout(function () {
      principal.src = fotos[i];
      principal.style.opacity = '1';
    }, MOVIMIENTO_REDUCIDO ? 0 : 150);
    thumbs.forEach(function (t, j) {
      if (j === i) t.setAttribute('aria-current', 'true');
      else t.removeAttribute('aria-current');
    });
  }
  thumbs.forEach(function (t, i) {
    t.addEventListener('click', function () { elegir(i); });
  });

  var visor = document.getElementById('visor');
  var visorImg = document.getElementById('visor-img');
  var contador = document.getElementById('visor-contador');
  var prev = document.getElementById('visor-prev');
  var next = document.getElementById('visor-next');
  var cerrarBtn = document.getElementById('visor-cerrar');
  var abrirBtn = galeria.querySelector('[data-abrir]');
  var indice = 0;

  if (fotos.length <= 1) { prev.hidden = true; next.hidden = true; }

  function mostrar(i) {
    indice = (i + fotos.length) % fotos.length;
    visorImg.src = fotos[indice];
    visorImg.alt = principal.alt;
    contador.textContent = (indice + 1) + ' de ' + fotos.length;
  }
  function abrir() {
    mostrar(actual);
    visor.hidden = false;
    document.body.style.overflow = 'hidden';
    cerrarBtn.focus();
  }
  function cerrar() {
    visor.hidden = true;
    document.body.style.overflow = '';
    visorImg.src = '';
    abrirBtn.focus();
  }

  abrirBtn.addEventListener('click', abrir);
  cerrarBtn.addEventListener('click', cerrar);
  prev.addEventListener('click', function () { mostrar(indice - 1); });
  next.addEventListener('click', function () { mostrar(indice + 1); });
  visor.addEventListener('click', function (e) { if (e.target === visor) cerrar(); });
  document.addEventListener('keydown', function (e) {
    if (visor.hidden) return;
    if (e.key === 'Escape') cerrar();
    if (e.key === 'ArrowLeft') mostrar(indice - 1);
    if (e.key === 'ArrowRight') mostrar(indice + 1);
    if (e.key === 'Tab') {
      var foco = [cerrarBtn, prev, next].filter(function (b) { return !b.hidden; });
      var pos = foco.indexOf(document.activeElement);
      e.preventDefault();
      foco[(pos + (e.shiftKey ? -1 : 1) + foco.length) % foco.length].focus();
    }
  });

  /* Barra de compra fija en el celular: aparece cuando el botón principal sale de pantalla. */
  var barra = document.querySelector('.compra-fija');
  var cta = document.querySelector('.pd-cta');
  if (barra && cta && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (en) {
      barra.classList.toggle('visible', !en[0].isIntersecting && en[0].boundingClientRect.top < 0);
    }).observe(cta);
  } else if (barra) {
    barra.classList.add('visible');
  }
})();
