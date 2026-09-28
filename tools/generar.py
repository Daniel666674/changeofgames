# Genera todas las páginas HTML del sitio a partir de productos.json.
# Uso: python3 tools/generar.py   (desde la raíz del repositorio)
# Para cambiar un precio, una foto o una descripción, edita tools/productos.json
# y vuelve a correr este script.

import json
import os
from html import escape
from urllib.parse import quote

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTOS = json.load(open(os.path.join(RAIZ, "tools", "productos.json"), encoding="utf-8"))
POR_SLUG = {p["slug"]: p for p in PRODUCTOS}

SITIO = "https://daniel666674.github.io/changeofgames/"
TEL = "573202082977"
TEL_VISIBLE = "320 208 2977"
DIRECCION = "Carrera 100 # 21 - 18, CC Codif, Local 01"
MAPA = "https://www.google.com/maps/search/?api=1&query=Carrera%20100%20%23%2021%20-%2018%2C%20CC%20Codif%2C%20Bogot%C3%A1%2C%20Colombia"
MAPA_EMBED = "https://www.google.com/maps?q=Carrera%20100%20%23%2021%20-%2018%2C%20CC%20Codif%2C%20Bogot%C3%A1%2C%20Colombia&output=embed"
INSTAGRAM = "https://www.instagram.com/changeofgames"
HORARIO = [
    ("Lunes a viernes", "8 a. m. – 6 p. m.", "1,2,3,4,5"),
    ("Sábados", "9 a. m. – 4 p. m.", "6"),
    ("Domingos y festivos", "9 a. m. – 12 m.", "0"),
]
PLURAL = {"Consola": "Consolas", "Control": "Controles", "Audífonos": "Audífonos"}


def wa(texto):
    return f"https://wa.me/{TEL}?text={quote(texto, safe='')}"


WA_GENERAL = wa("Hola Change of Games, quiero hacer una consulta.")
WA_TECNICO = wa("Hola Change of Games, necesito servicio técnico.\nEquipo: \nQué le pasa: ")


def plataforma(p):
    s = p["slug"]
    if "xbox" in s:
        return "Xbox"
    if "nintendo" in s:
        return "Nintendo"
    return "PlayStation"


def precio_num(p):
    return int(p["price"].replace("$", "").replace(".", ""))


def fmt_precio(n):
    return "$" + f"{n:,}".replace(",", ".")


def desde(cat):
    return fmt_precio(min(precio_num(p) for p in PRODUCTOS if p["cat"] == cat))


def cuantos(cat):
    return sum(1 for p in PRODUCTOS if p["cat"] == cat)


# ---------- Íconos ----------
def ico(nombre, t=20):
    trazos = {
        "wa": '<path d="M3.5 20.5l1.4-4.3A8.5 8.5 0 1 1 8 19.2l-4.5 1.3z"/><path d="M9 9.2c.3 1.6 1.8 3.6 3.8 4.6l1.1-1.1 2 .9-.3 1.5c-3.4.2-7.3-3.3-7.6-6.8l1.5-.4.9 1.9z" fill="currentColor" stroke="none"/>',
        "flecha": '<path d="M5 12h14M13 6l6 6-6 6"/>',
        "carrito": '<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2 3h3l2.4 11.2a2 2 0 0 0 2 1.6h8.3a2 2 0 0 0 2-1.5L21.5 7H6"/>',
        "pin": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
        "reloj": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "llave": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.1-3.1a6 6 0 0 1-7.6 7.6l-6.5 6.5a2.1 2.1 0 0 1-3-3l6.5-6.5a6 6 0 0 1 7.6-7.6z"/>',
        "escudo": '<path d="M12 21s7-3.5 7-9V5.5L12 3 5 5.5V12c0 5.5 7 9 7 9z"/><path d="M9 12l2 2 4-4"/>',
        "check": '<path d="M20 6L9 17l-5-5"/>',
        "tel": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
        "ig": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/>',
        "buscar": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>',
        "izq": '<path d="M15 5l-7 7 7 7"/>',
        "der": '<path d="M9 5l7 7-7 7"/>',
        "x": '<path d="M5 5l14 14M19 5L5 19"/>',
        "control": '<path d="M6.5 7h11a4.5 4.5 0 0 1 4.4 5.4l-1 4.9a2.6 2.6 0 0 1-4.6 1.1L14.5 16h-5l-1.8 2.4a2.6 2.6 0 0 1-4.6-1.1l-1-4.9A4.5 4.5 0 0 1 6.5 7z"/><path d="M7.5 10.5v3M6 12h3"/><circle cx="16" cy="11" r=".8" fill="currentColor"/><circle cx="17.5" cy="13" r=".8" fill="currentColor"/>',
        "audif": '<path d="M4 15v-3a8 8 0 0 1 16 0v3"/><rect x="3" y="14" width="4.5" height="7" rx="1.8"/><rect x="16.5" y="14" width="4.5" height="7" rx="1.8"/>',
        "consola": '<rect x="3" y="6" width="18" height="12" rx="2.5"/><path d="M7 12h3M8.5 10.5v3"/><circle cx="16" cy="11" r=".8" fill="currentColor"/><circle cx="16" cy="13.5" r=".8" fill="currentColor"/>',
        "juego": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M5 7h14M9 12.5h6M9 15.5h4"/>',
        "billete": '<rect x="2.5" y="6" width="19" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6 9.5v5M18 9.5v5"/>',
        "banco": '<path d="M3 10h18L12 4 3 10zM5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20h18"/>',
        "bolsa": '<path d="M5 8h14l-1.2 12H6.2L5 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
        "chat": '<path d="M21 12a8 8 0 0 1-11.8 7L4 20.5l1.5-4.7A8 8 0 1 1 21 12z"/><path d="M8.5 11h7M8.5 14h4"/>',
        "zoom": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5M11 8v6M8 11h6"/>',
        "chispa": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3z"/>',
    }
    return (f'<svg width="{t}" height="{t}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{trazos[nombre]}</svg>')


ACTUAL = ' aria-current="page"'
ACTUAL_FOTO = ' aria-current="true"'

SUP = ('<sup class="sup"><a href="contacto.html#asumimos" title="Esto es un supuesto nuestro. Ver Qué asumimos." '
       'aria-label="Supuesto, ver Qué asumimos">*</a></sup>')


# ---------- Piezas compartidas ----------
def cabecera(actual):
    enlaces = [("index.html", "Inicio"), ("tienda.html", "Tienda"), ("servicios.html", "Servicios"),
               ("nosotros.html", "Nosotros"), ("contacto.html", "Contacto")]
    items = "\n".join(
        f'        <li><a href="{h}"{ACTUAL if h == actual else ""}>{t}</a></li>' for h, t in enlaces)
    return f'''<a class="salto" href="#contenido">Saltar al contenido</a>
<div class="franja"><p>Propuesta de sitio para Change of Games. No es su página oficial. <a href="contacto.html#asumimos">Qué asumimos</a></p></div>
<header class="cab" data-cab>
  <div class="wrap cab-in">
    <a class="marca" href="index.html"><img src="img/logo.png" width="44" height="44" alt=""><span>Change <em>of</em> Games</span></a>
    <nav class="menu" id="menu" aria-label="Principal">
      <ul>
{items}
      </ul>
      <div class="menu-pie">
        <a class="btn btn-wa btn-lg" href="{WA_GENERAL}" target="_blank" rel="noopener">{ico("wa")}Escribir por WhatsApp</a>
        <p>{DIRECCION}<br>Bogotá · <a href="tel:+{TEL}">{TEL_VISIBLE}</a></p>
      </div>
    </nav>
    <div class="cab-acc">
      <span class="estado" data-estado><i></i><span>Abierto todos los días</span></span>
      <a class="btn btn-oro btn-sm cab-wa" href="{WA_GENERAL}" target="_blank" rel="noopener">{ico("wa", 18)}<span>Escríbenos</span></a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu" aria-label="Abrir menú"><span></span><span></span></button>
    </div>
  </div>
</header>'''


def pie():
    horas = "".join(f"<li><span>{d}</span><span>{h}</span></li>" for d, h, _ in HORARIO)
    return f'''<footer class="pie">
  <div class="wrap">
    <div class="pie-cta" data-r>
      <div>
        <p class="kicker">¿Qué vas a jugar hoy?</p>
        <h2 class="h2">Escríbenos y te lo <span class="oro">separamos.</span></h2>
      </div>
      <a class="btn btn-oro btn-lg" href="{WA_GENERAL}" target="_blank" rel="noopener">{ico("wa")}Escribir por WhatsApp</a>
    </div>
    <div class="pie-cols">
      <div class="pie-marca">
        <a class="marca" href="index.html"><img src="img/logo.png" width="44" height="44" alt=""><span>Change <em>of</em> Games</span></a>
        <p>Videojuegos, consolas, accesorios y servicio técnico en Bogotá.</p>
        <div class="redes">
          <a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram @changeofgames">{ico("ig")}</a>
          <a href="{WA_GENERAL}" target="_blank" rel="noopener" aria-label="WhatsApp">{ico("wa")}</a>
          <a href="tel:+{TEL}" aria-label="Llamar al {TEL_VISIBLE}">{ico("tel")}</a>
        </div>
      </div>
      <div>
        <h2>Sitio</h2>
        <ul class="pie-links">
          <li><a href="tienda.html">Tienda</a></li>
          <li><a href="servicios.html">Servicios</a></li>
          <li><a href="nosotros.html">Nosotros</a></li>
          <li><a href="contacto.html">Contacto</a></li>
        </ul>
      </div>
      <div>
        <h2>Horario</h2>
        <ul class="pie-horas">{horas}</ul>
      </div>
      <div>
        <h2>Visítanos</h2>
        <p>{DIRECCION}<br>Bogotá</p>
        <p><a href="{MAPA}" target="_blank" rel="noopener">Abrir en Google Maps</a></p>
        <p><a href="tel:+{TEL}">{TEL_VISIBLE}</a> · <a href="{INSTAGRAM}" target="_blank" rel="noopener">@changeofgames</a></p>
      </div>
    </div>
    <p class="nota">Propuesta de sitio para Change of Games. No es la página oficial del negocio.</p>
  </div>
</footer>'''


def pagina(archivo, titulo, desc, cuerpo, actual=None, imagen="img/logo.png", wa_fijo=True, clase=""):
    t = escape(titulo)
    d = escape(desc)
    fijo = (f'<a class="wa-fijo" href="{WA_GENERAL}" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">'
            f'{ico("wa", 28)}</a>\n') if wa_fijo else ""
    html = f'''<!DOCTYPE html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#08090d">
<meta name="color-scheme" content="dark">
<title>{t}</title>
<meta name="description" content="{d}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_CO">
<meta property="og:site_name" content="Change of Games">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{SITIO}{archivo}">
<meta property="og:image" content="{SITIO}{imagen}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{SITIO}{imagen}">
<link rel="icon" href="img/logo.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@600;700;800&family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body{f' class="{clase}"' if clase else ""}>
{cabecera(actual)}
<main id="contenido">
{cuerpo}
</main>
{pie()}
{fijo}<script src="script.js"></script>
</body>
</html>
'''
    with open(os.path.join(RAIZ, archivo), "w", encoding="utf-8") as f:
        f.write(html)


def tarjeta(p, lazy=True):
    nombre = escape(p["name"])
    plat = plataforma(p)
    comprar = wa(f"Hola Change of Games, quiero comprar: {p['name']} ({p['price']}).")
    return f'''<article class="card-p" data-cat="{p["cat"]}" data-plat="{plat}" data-precio="{precio_num(p)}" data-nombre="{nombre.lower()}">
  <div class="stage"><span class="tag tag-{plat.lower()}">{plat}</span><img src="{p["imgs"][0]}" alt="{nombre}" loading="{"lazy" if lazy else "eager"}" decoding="async"></div>
  <div class="card-body">
    <p class="card-cat">{p["cat"]}</p>
    <h3><a href="{p["slug"]}.html">{nombre}</a></h3>
    <div class="card-foot">
      <p class="precio">{p["price"]}</p>
      <a class="btn-ico" href="{comprar}" target="_blank" rel="noopener" aria-label="Comprar {nombre} por WhatsApp">{ico("wa", 20)}</a>
    </div>
  </div>
</article>'''


def horario_panel(titulo_tag="h3"):
    filas = "".join(f'<li data-dias="{dias}"><span>{d}</span><span>{h}</span></li>' for d, h, dias in HORARIO)
    return f'''<div class="panel visita" data-r>
      <p class="kicker">Dónde y cuándo</p>
      <{titulo_tag} class="h3">{DIRECCION}</{titulo_tag}>
      <p class="muted">Bogotá. Abrimos todos los días.</p>
      <span class="estado estado-grande" data-estado><i></i><span>Abierto todos los días</span></span>
      <ul class="horario" data-horario>{filas}</ul>
      <div class="acciones">
        <a class="btn btn-oro" href="{WA_GENERAL}" target="_blank" rel="noopener">{ico("wa")}Escribir por WhatsApp</a>
        <a class="btn btn-linea" href="{MAPA}" target="_blank" rel="noopener">{ico("pin")}Cómo llegar</a>
      </div>
    </div>
    <div class="mapa-caja" data-r style="--d:.1s">
      <iframe class="mapa" title="Mapa de Google con la dirección de Change of Games" src="{MAPA_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>'''


def pasos_compra():
    pasos = [
        ("carrito", "Elige", "Mira fotos y precios en la tienda. Todo está a la vista."),
        ("wa", "Escríbenos", "Un toque abre WhatsApp con el producto ya escrito. Te confirmamos precio y disponibilidad."),
        ("bolsa", "Recoge y juega", f"Pagas y recoges en el local de la Cra. 100, o acordamos la entrega por el chat.{SUP}"),
    ]
    items = "".join(
        f'<li data-r style="--d:{i * 0.1:.1f}s"><span class="paso-ico">{ico(ic, 26)}</span><span class="paso-n">0{i + 1}</span><h3>{t}</h3><p>{d}</p></li>'
        for i, (ic, t, d) in enumerate(pasos))
    return f'<ol class="pasos">{items}</ol>'


# ---------- Inicio ----------
def inicio():
    ps5, ctrl, sw = POR_SLUG["playstation-5"], POR_SLUG["control-xbox"], POR_SLUG["nintendo-switch"]
    flotas = ""
    for i, p in enumerate([ps5, ctrl, sw], 1):
        flotas += (f'<a class="flota flota-{i}" href="{p["slug"]}.html" tabindex="-1" aria-hidden="true">'
                   f'<img src="{p["imgs"][0]}" alt="" loading="eager" decoding="async"><span class="chip-precio">{p["price"]}</span></a>')

    ticker_items = "".join(f'<li>{escape(p["name"])} <b>{p["price"]}</b></li>' for p in PRODUCTOS)

    destacados = ["playstation-5", "xbox-series-x", "nintendo-switch", "control-dualsense-spiderman-2",
                  "control-xbox-elite-series-2", "audifonos-xbox", "xbox-series-s", "control-dualsense-camuflado"]
    riel = "\n".join(tarjeta(POR_SLUG[s]) for s in destacados)

    razones = [
        ("pin", "Tienda física en Bogotá", "No somos solo una página. Tenemos local en el CC Codif para que veas y recojas tu producto.", ""),
        ("llave", "Servicio técnico propio", "Si tu consola o control necesita revisión, la recibimos directamente en el local.", ""),
        ("chat", "Atención directa por WhatsApp", "Hablas con nosotros, sin bots ni formularios. Te respondemos rápido.", ""),
        ("escudo", "Garantía por defectos de fábrica", "Si algo llega mal de fábrica, lo resolvemos contigo.", SUP),
    ]
    feats = "".join(
        f'<article class="feat" data-r style="--d:{i * 0.08:.2f}s"><span class="feat-n">0{i + 1}</span>'
        f'<span class="feat-ico">{ico(ic, 26)}</span><h3>{t}{s}</h3><p>{d}</p></article>'
        for i, (ic, t, d, s) in enumerate(razones))

    cuerpo = f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-texto">
      <p class="pill" data-r><span class="estado-punto" data-estado-punto></span>Bogotá · CC Codif, Local 01</p>
      <h1 class="h1" data-r style="--d:.05s">Tu próximo nivel empieza en la <span class="oro">Cra.&nbsp;100.</span></h1>
      <p class="lead" data-r style="--d:.1s">Consolas, controles, audífonos y videojuegos con precio claro. Escríbenos por WhatsApp y recógelo hoy en el local.</p>
      <div class="acciones" data-r style="--d:.15s">
        <a class="btn btn-oro btn-lg" href="tienda.html">{ico("carrito")}Ver la tienda</a>
        <a class="btn btn-linea btn-lg" href="{WA_GENERAL}" target="_blank" rel="noopener">{ico("wa")}Escribir por WhatsApp</a>
      </div>
      <dl class="prueba" data-r style="--d:.2s">
        <div><dt>{len(PRODUCTOS)}</dt><dd>productos con precio</dd></div>
        <div><dt>7</dt><dd>días a la semana</dd></div>
        <div><dt>1</dt><dd>chat para todo</dd></div>
      </dl>
    </div>
    <div class="escena" aria-hidden="true">
      <div class="orbita"></div>
      <div class="medallon"><img src="img/logo.png" alt="" width="360" height="360"></div>
      {flotas}
    </div>
  </div>
</section>

<div class="ticker" aria-label="Precios de referencia">
  <div class="ticker-pista">
    <ul>{ticker_items}</ul>
    <ul aria-hidden="true">{ticker_items}</ul>
  </div>
</div>

<section class="sec">
  <div class="wrap">
    <div class="sec-head" data-r>
      <div><p class="kicker">Categorías</p><h2 class="h2">Todo para jugar, en un solo local.</h2></div>
      <a class="link-flecha" href="tienda.html">Ver toda la tienda {ico("flecha", 18)}</a>
    </div>
    <div class="bento">
      <a class="b b-1" href="tienda.html?cat=Consola" data-r>
        <div class="b-stage">
          <img class="bi bi-a" src="{POR_SLUG["xbox-series-x"]["imgs"][0]}" alt="" loading="lazy">
          <img class="bi bi-b" src="{POR_SLUG["playstation-5"]["imgs"][0]}" alt="" loading="lazy">
          <img class="bi bi-c" src="{POR_SLUG["nintendo-switch"]["imgs"][0]}" alt="" loading="lazy">
        </div>
        <div class="b-txt"><span class="b-ico">{ico("consola", 22)}</span><h3>Consolas</h3><p>{cuantos("Consola")} modelos · desde <b>{desde("Consola")}</b></p><span class="b-flecha">{ico("flecha", 20)}</span></div>
      </a>
      <a class="b b-2" href="tienda.html?cat=Control" data-r style="--d:.08s">
        <div class="b-stage">
          <img class="bi bi-a" src="{POR_SLUG["control-dualsense-spiderman-2"]["imgs"][0]}" alt="" loading="lazy">
          <img class="bi bi-b" src="{POR_SLUG["control-xbox-elite-series-2"]["imgs"][0]}" alt="" loading="lazy">
        </div>
        <div class="b-txt"><span class="b-ico">{ico("control", 22)}</span><h3>Controles</h3><p>{cuantos("Control")} modelos · desde <b>{desde("Control")}</b></p><span class="b-flecha">{ico("flecha", 20)}</span></div>
      </a>
      <a class="b b-3" href="tienda.html?cat=Audífonos" data-r style="--d:.12s">
        <div class="b-stage"><img class="bi bi-a" src="{POR_SLUG["audifonos-xbox"]["imgs"][0]}" alt="" loading="lazy"></div>
        <div class="b-txt"><span class="b-ico">{ico("audif", 22)}</span><h3>Audífonos</h3><p>Desde <b>{desde("Audífonos")}</b></p><span class="b-flecha">{ico("flecha", 20)}</span></div>
      </a>
      <a class="b b-4" href="servicios.html#videojuegos" data-r style="--d:.16s">
        <div class="b-txt"><span class="b-ico">{ico("juego", 22)}</span><h3>Videojuegos</h3><p>Dinos el título y la consola. Te confirmamos si lo tenemos.</p><span class="b-flecha">{ico("flecha", 20)}</span></div>
      </a>
      <a class="b b-5" href="servicios.html#servicio-tecnico" data-r style="--d:.2s">
        <div class="b-txt"><span class="b-ico">{ico("llave", 22)}</span><h3>Servicio técnico</h3><p>Cuéntanos qué le pasa a tu consola o control.</p><span class="b-flecha">{ico("flecha", 20)}</span></div>
      </a>
    </div>
  </div>
</section>

<section class="sec sec-alt">
  <div class="wrap">
    <div class="sec-head" data-r>
      <div><p class="kicker">Lo más buscado</p><h2 class="h2">Con precio y foto. Sin letra pequeña.</h2>
      <p class="muted sec-sub">Precios de referencia según el mercado actual{SUP}. Te confirmamos el valor final por chat.</p></div>
      <div class="riel-nav">
        <button class="riel-btn" type="button" data-riel="-1" aria-label="Ver anteriores">{ico("izq")}</button>
        <button class="riel-btn" type="button" data-riel="1" aria-label="Ver siguientes">{ico("der")}</button>
      </div>
    </div>
    <div class="riel" data-riel-pista>
{riel}
    </div>
    <div class="centro"><a class="btn btn-linea btn-lg" href="tienda.html">Ver los {len(PRODUCTOS)} productos {ico("flecha", 18)}</a></div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head" data-r>
      <div><p class="kicker">Por qué comprar aquí</p><h2 class="h2">Compra tranquilo.</h2></div>
    </div>
    <div class="feats">{feats}</div>
  </div>
</section>

<section class="sec sec-alt">
  <div class="wrap">
    <div class="sec-head" data-r>
      <div><p class="kicker">Cómo comprar</p><h2 class="h2">Tres pasos. Cero complicaciones.</h2></div>
    </div>
    {pasos_compra()}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="banner" data-r>
      <div class="banner-txt">
        <p class="kicker kicker-claro">Servicio técnico{SUP}</p>
        <h2 class="h2">¿Tu consola o tu control fallan?</h2>
        <p>Cuéntanos qué equipo es y qué le pasa. Con eso te decimos cómo seguir, y lo recibimos en el local.</p>
        <div class="acciones">
          <a class="btn btn-oscuro btn-lg" href="{WA_TECNICO}" target="_blank" rel="noopener">{ico("wa")}Consultar por servicio técnico</a>
        </div>
      </div>
      <div class="banner-arte" aria-hidden="true">{ico("llave", 220)}</div>
    </div>
  </div>
</section>

<section class="sec sec-alt">
  <div class="wrap visita-grid">
    {horario_panel("h2")}
  </div>
</section>
'''
    pagina("index.html", "Change of Games — Videojuegos, consolas y accesorios en Bogotá",
           f"Videojuegos, consolas, accesorios y servicio técnico. {DIRECCION}, Bogotá. Propuesta de sitio.",
           cuerpo, "index.html")


# ---------- Tienda ----------
def tienda():
    cats = ["Consola", "Control", "Audífonos"]
    chips = f'<button type="button" class="chip" data-filtro="todos" aria-pressed="true">Todos <span>{len(PRODUCTOS)}</span></button>'
    chips += "".join(
        f'<button type="button" class="chip" data-filtro="{c}" aria-pressed="false">{PLURAL[c]} <span>{cuantos(c)}</span></button>'
        for c in cats)
    plats = '<button type="button" class="chip chip-plat" data-plat="todas" aria-pressed="true">Todas</button>'
    plats += "".join(
        f'<button type="button" class="chip chip-plat" data-plat="{pl}" aria-pressed="false"><i class="punto punto-{pl.lower()}"></i>{pl}</button>'
        for pl in ["PlayStation", "Xbox", "Nintendo"])
    grid = "\n".join(tarjeta(p, lazy=i > 7) for i, p in enumerate(PRODUCTOS))
    cuerpo = f'''
<section class="phero">
  <div class="wrap">
    <p class="migas"><a href="index.html">Inicio</a><span>/</span>Tienda</p>
    <h1 class="h1 h1-p">La <span class="oro">tienda.</span></h1>
    <p class="lead">Precio, foto y disponibilidad. Son precios de referencia según el mercado actual{SUP}: al escribirnos te confirmamos el valor final y si está disponible.</p>
  </div>
</section>

<div class="barra" data-barra>
  <div class="wrap barra-in">
    <label class="buscar"><span class="sr">Buscar producto</span>{ico("buscar", 18)}<input type="search" id="buscar" placeholder="Buscar: PS5, Elite, Switch…" autocomplete="off"></label>
    <div class="chips" id="filtros" role="group" aria-label="Filtrar por categoría">{chips}</div>
    <div class="chips" id="plataformas" role="group" aria-label="Filtrar por plataforma">{plats}</div>
    <label class="orden"><span class="sr">Ordenar</span>
      <select id="orden">
        <option value="nuevo">Destacados</option>
        <option value="menor">Precio: menor a mayor</option>
        <option value="mayor">Precio: mayor a menor</option>
      </select>
    </label>
  </div>
</div>

<section class="sec sec-tienda">
  <div class="wrap">
    <p class="conteo" id="conteo" aria-live="polite">{len(PRODUCTOS)} productos</p>
    <div class="grid-p" id="tienda">
{grid}
    </div>
    <div class="vacio" id="sin-resultados" hidden>
      <span class="vacio-ico">{ico("buscar", 32)}</span>
      <h2 class="h3">No encontramos eso en la tienda.</h2>
      <p class="muted">Puede que lo tengamos y no esté publicado todavía.</p>
      <a class="btn btn-oro" href="{wa("Hola Change of Games, quiero consultar por un producto.")}" target="_blank" rel="noopener">{ico("wa")}Preguntar por WhatsApp</a>
    </div>
  </div>
</section>

<section class="sec sec-alt">
  <div class="wrap">
    <div class="banner banner-oro" data-r>
      <div class="banner-txt">
        <p class="kicker kicker-oscuro">¿No ves lo que buscas?</p>
        <h2 class="h2">Pregúntanos por WhatsApp.</h2>
        <p>Puede que lo tengamos y no esté todavía en esta tienda. Juegos, accesorios, ediciones especiales: dinos qué buscas.</p>
        <div class="acciones"><a class="btn btn-oscuro btn-lg" href="{wa("Hola Change of Games, quiero consultar por un producto.")}" target="_blank" rel="noopener">{ico("wa")}Escribir por WhatsApp</a></div>
      </div>
      <div class="banner-arte" aria-hidden="true">{ico("control", 240)}</div>
    </div>
  </div>
</section>
'''
    pagina("tienda.html", "Tienda — Change of Games",
           "Consolas, controles y accesorios con precio, descripción y forma de pago. Change of Games, Bogotá.",
           cuerpo, "tienda.html")


# ---------- Producto ----------
def producto(p):
    nombre = escape(p["name"])
    plat = plataforma(p)
    comprar = wa(f"Hola Change of Games, quiero comprar: {p['name']} ({p['price']}).")
    fotos = p["imgs"]
    thumbs = ""
    if len(fotos) > 1:
        thumbs = '<div class="thumbs">' + "".join(
            f'<button class="thumb" type="button" data-foto="{i}" aria-label="Ver foto {i + 1} de {len(fotos)}"{ACTUAL_FOTO if i == 0 else ""}>'
            f'<img src="{f}" alt="" loading="lazy" decoding="async"></button>'
            for i, f in enumerate(fotos)) + "</div>"
    fotos_json = escape(json.dumps(fotos))
    incluye = "".join(f'<li>{ico("check", 18)}<span>{escape(x)}</span></li>' for x in p["incluye"])
    confianza = [
        ("pin", "Tienda física en Bogotá"),
        ("llave", "Servicio técnico propio"),
        ("chat", "Atención directa, sin bots"),
        ("escudo", f"Garantía por defectos de fábrica{SUP}"),
    ]
    conf = "".join(f'<li>{ico(i, 18)}<span>{t}</span></li>' for i, t in confianza)
    pagos = [
        ("billete", "En el local", "Efectivo o datáfono al recoger."),
        ("banco", "Transferencia", "Nequi, Daviplata o transferencia antes de la entrega."),
        ("bolsa", "Sepáralo", "Aparta el producto con un abono por WhatsApp."),
    ]
    pag = "".join(
        f'<li data-r style="--d:{i * 0.08:.2f}s"><span class="pago-ico">{ico(ic, 24)}</span><h3>{t}</h3><p>{d}</p></li>'
        for i, (ic, t, d) in enumerate(pagos))
    relacionados = [x for x in PRODUCTOS if x["cat"] == p["cat"] and x["slug"] != p["slug"]]
    relacionados += [x for x in PRODUCTOS if x["cat"] != p["cat"]]
    rel = "\n".join(tarjeta(x) for x in relacionados[:4])

    cuerpo = f'''
<section class="pd-sec">
  <div class="wrap">
    <p class="migas"><a href="index.html">Inicio</a><span>/</span><a href="tienda.html">Tienda</a><span>/</span><a href="tienda.html?cat={quote(p["cat"])}">{PLURAL[p["cat"]]}</a><span>/</span>{nombre}</p>
    <div class="pd">
      <div class="galeria" data-galeria data-fotos="{fotos_json}">
        <button class="stage stage-xl" type="button" data-abrir aria-label="Ampliar foto de {nombre}">
          <span class="tag tag-{plat.lower()}">{plat}</span>
          <img src="{fotos[0]}" alt="{nombre}" data-principal loading="eager" decoding="async">
          <span class="zoom">{ico("zoom", 18)}</span>
        </button>
        {thumbs}
      </div>
      <div class="pd-info">
        <p class="kicker">{p["cat"]} · {plat}</p>
        <h1 class="pd-titulo">{nombre}</h1>
        <div class="pd-precio">
          <p class="precio-xl">{p["price"]}</p>
          <span class="disp">{ico("check", 16)}Disponible</span>
        </div>
        <p class="muted pd-nota">Precio de referencia{SUP}. Te lo confirmamos por WhatsApp antes de pagar.</p>
        <p class="pd-desc">{escape(p["desc"])}</p>
        <div class="pd-cta">
          <a class="btn btn-wa btn-lg" href="{comprar}" target="_blank" rel="noopener">{ico("wa")}Comprar por WhatsApp</a>
          <a class="btn btn-linea btn-lg" href="tel:+{TEL}">{ico("tel")}Llamar</a>
        </div>
        <ul class="pd-conf">{conf}</ul>
      </div>
    </div>
  </div>
</section>

<section class="sec sec-alt">
  <div class="wrap pd-detalles">
    <div class="panel" data-r>
      <p class="kicker">Detalles</p>
      <h2 class="h3">Qué incluye.</h2>
      <ul class="incluye">{incluye}</ul>
    </div>
    <div class="panel" data-r style="--d:.08s">
      <p class="kicker">Cómo pagas{SUP}</p>
      <h2 class="h3">Pagas cuando confirmes tu compra.</h2>
      <ol class="pagos">{pag}</ol>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head" data-r>
      <div><p class="kicker">También te puede gustar</p><h2 class="h2">Sigue mirando.</h2></div>
      <a class="link-flecha" href="tienda.html">Ver toda la tienda {ico("flecha", 18)}</a>
    </div>
    <div class="grid-p">
{rel}
    </div>
  </div>
</section>

<div class="visor" id="visor" hidden role="dialog" aria-modal="true" aria-label="Fotos de {nombre}">
  <button class="visor-btn visor-cerrar" id="visor-cerrar" type="button" aria-label="Cerrar">{ico("x", 26)}</button>
  <button class="visor-btn visor-prev" id="visor-prev" type="button" aria-label="Foto anterior">{ico("izq", 28)}</button>
  <figure><img id="visor-img" src="" alt=""><figcaption id="visor-contador"></figcaption></figure>
  <button class="visor-btn visor-next" id="visor-next" type="button" aria-label="Foto siguiente">{ico("der", 28)}</button>
</div>

<div class="compra-fija">
  <div><p class="compra-nombre">{nombre}</p><p class="precio">{p["price"]}</p></div>
  <a class="btn btn-wa" href="{comprar}" target="_blank" rel="noopener">{ico("wa")}Comprar</a>
</div>
'''
    pagina(p["slug"] + ".html", f"{p['name']} — Change of Games", f"{p['name']}: {p['price']}. {p['desc']}",
           cuerpo, "tienda.html", imagen=fotos[0], wa_fijo=False, clase="con-compra")


# ---------- Nosotros ----------
def nosotros():
    datos = [
        ("Local 01", "CC Codif, Carrera 100 # 21 - 18, Bogotá."),
        ("7 días", "Abrimos toda la semana, festivos incluidos."),
        (str(len(PRODUCTOS)), "Productos con precio y foto en la tienda."),
        ("1 chat", "WhatsApp para preguntar, separar y coordinar."),
    ]
    dd = "".join(f'<div class="dato" data-r style="--d:{i * 0.08:.2f}s"><dt>{a}</dt><dd>{b}</dd></div>' for i, (a, b) in enumerate(datos))
    cuerpo = f'''
<section class="phero phero-split">
  <div class="wrap nos-grid">
    <div>
      <p class="migas"><a href="index.html">Inicio</a><span>/</span>Nosotros</p>
      <h1 class="h1 h1-p">Una tienda de videojuegos <span class="oro">en Bogotá.</span></h1>
      <p class="lead">Somos Change of Games. Vendemos videojuegos, consolas y accesorios. También tenemos servicio técnico.</p>
      <p class="muted">Si buscas algo en particular, escríbenos antes de venir. Te decimos si lo tenemos.{SUP}</p>
      <div class="acciones">
        <a class="btn btn-oro btn-lg" href="tienda.html">{ico("carrito")}Ver la tienda</a>
        <a class="btn btn-linea btn-lg" href="{WA_GENERAL}" target="_blank" rel="noopener">{ico("wa")}Escríbenos</a>
      </div>
    </div>
    <div class="escena escena-sola" aria-hidden="true">
      <div class="orbita"></div>
      <div class="medallon"><img src="img/logo.png" alt="" width="360" height="360"></div>
    </div>
  </div>
</section>

<section class="sec sec-alt">
  <div class="wrap">
    <dl class="datos">{dd}</dl>
  </div>
</section>

<section class="sec">
  <div class="wrap historia">
    <img class="sello" src="img/logo.png" width="220" height="220" alt="Logo de Change of Games: un personaje con gorra roja y una moneda en la mano, dentro de un aro dorado" loading="lazy" data-r>
    <div data-r style="--d:.08s">
      <p class="kicker">Nuestra marca</p>
      <h2 class="h2">Aro dorado, <span class="rojo">gorra roja.</span></h2>
      <p class="lead">Ese es nuestro logo: un personaje con una moneda en la mano, dentro de un aro dorado. De ahí salen los colores de este sitio: negro, dorado y rojo.</p>
      <div class="paleta" aria-hidden="true"><span style="background:#08090d"></span><span style="background:#f0c35a"></span><span style="background:#e5412d"></span></div>
    </div>
  </div>
</section>

<section class="sec sec-alt">
  <div class="wrap">
    <div class="ig-card" data-r>
      <span class="ig-ico">{ico("ig", 34)}</span>
      <div>
        <p class="kicker">En redes</p>
        <h2 class="h2">Nos ves en Instagram.</h2>
        <p class="muted">Estamos como @changeofgames.</p>
      </div>
      <a class="btn btn-oro btn-lg" href="{INSTAGRAM}" target="_blank" rel="noopener">Abrir Instagram {ico("flecha", 18)}</a>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap visita-grid">
    {horario_panel("h2")}
  </div>
</section>
'''
    pagina("nosotros.html", "Nosotros — Change of Games",
           "Change of Games: videojuegos, consolas, accesorios y servicio técnico en el CC Codif, Bogotá.",
           cuerpo, "nosotros.html")


# ---------- Servicios ----------
def servicios():
    servs = [
        ("videojuegos", "juego", "Videojuegos", "Dinos el título y la consola en la que juegas. Te confirmamos si lo tenemos.",
         wa("Hola Change of Games, quiero consultar por un videojuego.\nTítulo: \nConsola: "), "Preguntar por un videojuego", False, ""),
        ("consolas", "consola", "Consolas", f"PlayStation, Xbox y Nintendo. {cuantos('Consola')} modelos en la tienda desde {desde('Consola')}. Te confirmamos disponibilidad y valor por el chat.",
         wa("Hola Change of Games, quiero consultar por una consola.\n¿Cuál tienen disponible? Busco: "), "Preguntar por una consola", True, ""),
        ("accesorios", "control", "Accesorios", f"Controles, audífonos y más, desde {desde('Control')}. Dinos qué accesorio necesitas y para qué consola.",
         wa("Hola Change of Games, quiero consultar por un accesorio.\nAccesorio: \nConsola: "), "Preguntar por un accesorio", True, ""),
        ("servicio-tecnico", "llave", "Servicio técnico", "Cuéntanos qué equipo es y qué le pasa. Con eso te decimos cómo seguir.",
         WA_TECNICO, "Consultar por servicio técnico", False, SUP),
    ]
    cards = ""
    for i, (id_, ic, t, d, link, btn, precios, sup) in enumerate(servs):
        extra = f'<a class="btn btn-linea" href="tienda.html">Ver precios</a>' if precios else ""
        cards += f'''<article class="serv" id="{id_}" data-r style="--d:{(i % 2) * 0.08:.2f}s">
        <span class="serv-n">0{i + 1}</span>
        <span class="feat-ico">{ico(ic, 28)}</span>
        <h2 class="h3">{t}{sup}</h2>
        <p>{d}</p>
        <div class="acciones"><a class="btn btn-oro" href="{link}" target="_blank" rel="noopener">{ico("wa")}{btn}</a>{extra}</div>
      </article>'''
    cuerpo = f'''
<section class="phero">
  <div class="wrap">
    <p class="migas"><a href="index.html">Inicio</a><span>/</span>Servicios</p>
    <h1 class="h1 h1-p">Qué tenemos y <span class="oro">cómo pedirlo.</span></h1>
    <p class="lead">Consulta precios y fotos en la <a href="tienda.html">tienda</a>, o escríbenos directo por WhatsApp. Cada botón abre el chat con el mensaje ya escrito: solo lo completas y lo envías.</p>
  </div>
</section>

<section class="sec sec-top0">
  <div class="wrap servs">
    {cards}
  </div>
</section>

<section class="sec sec-alt">
  <div class="wrap">
    <div class="sec-head" data-r>
      <div><p class="kicker">Paso a paso</p><h2 class="h2">Cómo pedir.</h2></div>
    </div>
    {pasos_compra()}
  </div>
</section>

<section class="sec">
  <div class="wrap visita-grid">
    {horario_panel("h2")}
  </div>
</section>
'''
    pagina("servicios.html", "Servicios — Change of Games",
           "Videojuegos, consolas, accesorios y servicio técnico. Pide por WhatsApp o pasa por el local en el CC Codif, Bogotá.",
           cuerpo, "servicios.html")


# ---------- Contacto ----------
def contacto():
    supuestos = [
        ("Los precios de la tienda son de referencia.", "No encontramos precios ni catálogo publicados, así que los calculamos según el mercado actual en Colombia. El valor real y la disponibilidad se confirman por WhatsApp."),
        ("La forma de pago que mostramos es un supuesto.", "Pusimos efectivo, datáfono, transferencia o abono por WhatsApp por ser lo más común en tiendas similares. No sabemos cuáles maneja realmente el negocio."),
        ("La garantía por defectos de fábrica es un supuesto.", "No encontramos una política de garantía publicada; toca confirmarla con el negocio antes de prometérsela a un cliente."),
        ("Los pedidos se coordinan por WhatsApp.", "Ahí se confirma si hay disponibilidad y el valor final."),
        ("La entrega se acuerda con cada cliente.", "No sabemos si hacen envíos ni a qué ciudades."),
        ("El servicio técnico recibe consolas y controles.", "No sabemos qué equipos atienden ni si se puede consultar por chat antes de llevarlos."),
        ("El 320 208 2977 sirve para llamadas y para WhatsApp.", "Es el único número que encontramos."),
        ("Los horarios de Google Maps siguen vigentes.", "Incluido el horario de domingos y festivos."),
        ("Antes de venir, se puede escribir para saber si tienen un producto.", ""),
        ("Los colores salen del logo.", "Negro, dorado y rojo. El resto son neutros."),
    ]
    sup_html = "".join(f"<li><strong>{a}</strong>{(' ' + b) if b else ''}</li>" for a, b in supuestos)
    cuerpo = f'''
<section class="phero">
  <div class="wrap">
    <p class="migas"><a href="index.html">Inicio</a><span>/</span>Contacto</p>
    <h1 class="h1 h1-p">Escríbenos o <span class="oro">pasa por el local.</span></h1>
    <p class="lead">Escríbenos por WhatsApp o llámanos al {TEL_VISIBLE}. Te respondemos nosotros, no un bot.</p>
  </div>
</section>

<section class="sec sec-top0">
  <div class="wrap canales">
    <a class="canal canal-wa" href="{WA_GENERAL}" target="_blank" rel="noopener" data-r>
      <span class="canal-ico">{ico("wa", 30)}</span>
      <h2 class="h3">WhatsApp</h2>
      <p>La forma más rápida. Pregunta, separa y coordina.</p>
      <span class="canal-dato">{TEL_VISIBLE} {ico("flecha", 18)}</span>
    </a>
    <a class="canal" href="tel:+{TEL}" data-r style="--d:.08s">
      <span class="canal-ico">{ico("tel", 30)}</span>
      <h2 class="h3">Llamada</h2>
      <p>Mismo número, si prefieres hablar.</p>
      <span class="canal-dato">{TEL_VISIBLE} {ico("flecha", 18)}</span>
    </a>
    <a class="canal" href="{INSTAGRAM}" target="_blank" rel="noopener" data-r style="--d:.16s">
      <span class="canal-ico">{ico("ig", 30)}</span>
      <h2 class="h3">Instagram</h2>
      <p>Mira lo que vamos publicando.</p>
      <span class="canal-dato">@changeofgames {ico("flecha", 18)}</span>
    </a>
  </div>
</section>

<section class="sec sec-alt">
  <div class="wrap visita-grid">
    {horario_panel("h2")}
  </div>
</section>

<section class="sec" id="asumimos">
  <div class="wrap">
    <div class="asumimos" data-r>
      <p class="kicker">Para el dueño</p>
      <h2 class="h2">Qué asumimos.</h2>
      <p class="lead">Armamos esta propuesta sin haber hablado con ustedes. Todo sale de lo que publican en Google Maps e Instagram. Donde faltaba información, supusimos. Si algo está mal, corrígenos y lo cambiamos.</p>
      <ul class="supuestos">{sup_html}</ul>
      <p class="muted afuera">Dejamos afuera lo que no encontramos publicado: reseñas de clientes, historia del negocio, años de experiencia y nombres del equipo.</p>
    </div>
  </div>
</section>
'''
    pagina("contacto.html", "Contacto — Change of Games",
           f"WhatsApp y teléfono {TEL_VISIBLE}. {DIRECCION}, Bogotá. Abrimos todos los días.",
           cuerpo, "contacto.html")


if __name__ == "__main__":
    inicio()
    tienda()
    nosotros()
    servicios()
    contacto()
    for p in PRODUCTOS:
        producto(p)
    print(f"Listo: {5 + len(PRODUCTOS)} páginas generadas.")
