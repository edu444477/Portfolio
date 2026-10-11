# Spec 001 — Portfolio Bilingüe

Estado: borrador

## Contexto y objetivo

El portfolio existe como escaparate profesional: cualquier empresa o persona que visite la URL debe entender quién soy, qué he construido y con qué, y poder enlazar directamente a un proyecto concreto. Hoy el repositorio tiene la estructura, los datos y el despliegue funcionando, pero no hay páginas: la web sirve un 404.

La web debe ser bilingüe (es/en) porque el perfil técnico se presenta tanto a empresas españolas como del resto del mundo, y debe distinguir el origen de cada tecnología mostrada para no presentar como experiencia laboral lo que es un proyecto personal.

## Usuarios / actores

- **Reclutador técnico**: busca el encaje de forma rápida. Llega desde LinkedIn o desde una oferta concreta.
- **Responsable de desarrollo / CTO**: evalúa la calidad del trabajo en proyectos concretos antes de una entrevista.
- **Colega o comunidad**: consulta por intereses técnicos (Ruby on Rails, React Native, IA aplicada).
- **Visitante no hispanohablante**: necesita leer el portfolio en inglés.
- **Propietario**: actualiza proyectos, experiencia y tecnologías sin tocar componentes.

## Historias de usuario

- **HU-1**: Como reclutador, quiero ver quién soy, mi experiencia y mis tecnologías de un vistazo, para decidir si tiene sentido seguir leyendo.
- **HU-2**: Como responsable técnico, quiero abrir el detalle de un proyecto, para valorar cómo trabajo y no solo qué herramientas toco.
- **HU-3**: Como visitante no hispanohablante, quiero cambiar el sitio a inglés, para no perderme nada por no entender español.
- **HU-4**: Como posible contacto, quiero enviar un mensaje desde la web, para escribirte sin salir de ella.
- **HU-5**: Como propietario, quiero editar proyectos, experiencia y tecnologías desde ficheros de contenido, para actualizar el portfolio sin depender de tocar componentes.
- **HU-6**: Como visitante en móvil, quiero usar todo el sitio con el dedo, para consultarlo desde cualquier sitio.

## Definiciones

- **Locale**: idioma del contenido, `es` o `en`.
- **Origen de una tecnología**: de dónde procede, a efectos de agrupación y honestidad: `cv` (declarada en el CV), `tfg` (del Trabajo de Fin de Grado), `portfolio` (de este proyecto de portfolio).
- **Contenido declarativo**: ficheros de contenido que alimentan la web, en lugar de valores escritos dentro de los componentes.
- **Sección**: bloque visible de la home con identificador propio, navegable por anclas.
- **URL con locale**: ruta que incluye el código de idioma, p. ej. `/es/`, `/en/`. La home sin locale (`/`) redirige según la regla de RF-11/RF-10.

## Requisitos funcionales

### Estructura y navegación

- **RF-1**: EL SISTEMA muestra en la home seis secciones, en este orden: hero, sobre mí, experiencia, proyectos, tecnologías y contacto. Si una sección no tiene contenido, el sistema oculta la sección completa en lugar de dejar un bloque vacío.
- **RF-2**: EL SISTEMA obtiene proyectos, experiencia, tecnologías e identidad (nombre, email, teléfono, ubicación, bio, enlaces GitHub/LinkedIn) desde el contenido declarativo, y ningún componente contiene datos de esos cuatro dominios escritos a mano.
- **RF-3**: CUANDO el visitante activa un ancla de la cabecera, ENTONCES EL SISTEMA desplaza la vista hasta la sección correspondiente con scroll suave y deja un margen de 80 px por encima para que el header fijo no tape el inicio de la sección.
- **RF-4**: CUANDO el viewport es inferior a 768px, EL SISTEMA muestra la navegación como panel desplegable en lugar de barra horizontal.
- **RF-5**: SI el visitante elige una sección desde el panel móvil, ENTONCES EL SISTEMA cierra el panel y desplaza a esa sección.
- **RF-6**: SI el visitante pulsa la tecla Escape con el panel móvil abierto, ENTONCES EL SISTEMA lo cierra.
- **RF-7**: CUANDO el visitante llega a una URL que no corresponde a ninguna página, EL SISTEMA muestra una página 404 con enlace a la home y a la sección de proyectos.

### Idioma

- **RF-8**: CUANDO el visitante cambia el idioma, ENTONCES EL SISTEMA navega a la URL del mismo recurso en el otro locale (p. ej. `/es/proyectos` → `/en/projects`), recargando la página para servir el HTML del idioma seleccionado. El selector de idioma debe estar disponible en el header y en el footer en todas las páginas.
- **RF-9**: EL SISTEMA persiste el idioma seleccionado en el almacenamiento local del navegador.
- **RF-10**: CUANDO el visitante vuelve al sitio en una visita posterior, EL SISTEMA redirige automáticamente a la URL con el idioma que había elegido (la persistencia manda sobre RF-11).
- **RF-11**: SI la URL no indica locale o indica uno no soportado, ENTONCES EL SISTEMA redirige a `/es/` (español por defecto), salvo que RF-10 se aplique.
- **RF-12**: EL SISTEMA sirve cada locale en su propia URL, de forma que un enlace a la versión inglesa sea compartible y no dependa del idioma del visitante.
- **RF-13**: EL SISTEMA marca el idioma de cada página con `lang` y `hreflang` en el HTML para que los buscadores indexen las versiones por separado.

### Contenido y detalle de proyecto

- **RF-14**: EL SISTEMA muestra los proyectos ordenados por fecha de inicio descendente, con los destacados antes que el resto.
- **RF-15**: CUANDO el visitante selecciona un proyecto, ENTONCES EL SISTEMA muestra una página de detalle con descripción, stack, retos, aprendizajes y el papel desarrollado.
- **RF-16**: EL SISTEMA muestra el proyecto TFG (La Nueva Era) y este propio proyecto de portfolio como entradas diferenciadas y con su ficha completa.
- **RF-17**: SI un proyecto no tiene URL de repositorio o de demo, ENTONCES EL SISTEMA omite ese enlace en lugar de mostrar uno vacío o roto.
- **RF-18**: EL SISTEMA muestra la experiencia laboral en orden cronológico inverso, indicando modalidad y fechas de cada puesto. Si un puesto tiene fecha de fin futura, se presenta como "actualidad"; si un puesto tiene dos tramos separados (mismo empleador, fechas no contiguas), se muestran como dos entradas distintas en el orden que corresponde a su tramo más reciente.
- **RF-19**: EL SISTEMA muestra la formación académica con su centro y su periodo.
- **RF-20**: EL SISTEMA agrupa las tecnologías bajo un encabezado por origen (`cv`, `tfg`, `portfolio`). Cada tecnología declara su origen en el campo `source` de su ficha de contenido y se agrupa en la sección correspondiente.

### Tecnologías

- **RF-21**: EL SISTEMA indica el nivel declarado de cada tecnología según la escala fija de cinco niveles, en orden de menor a mayor: `learning`, `beginner`, `intermediate`, `advanced`, `expert`. El nivel se muestra junto al nombre y se usa para ordenar dentro de cada grupo (mayor nivel primero).
- **RF-22**: SI dos tecnologías tienen el mismo nombre en distinto origen, ENTONCES EL SISTEMA las muestra una sola vez dentro del grupo que corresponde a su origen real, sin duplicar entradas. La regla de precedencia es: `cv` > `tfg` > `portfolio` (si la misma tecnología aparece en varios orígenes, se muestra solo en el de mayor precedencia).

### Formulario de contacto

- **RF-23**: CUANDO el visitante envía el formulario con nombre, email, asunto y mensaje válidos, ENTONCES EL SISTEMA envía el mensaje a Web3Forms y confirma el envío en pantalla con un mensaje accesible (`aria-live="polite"`).
- **RF-24**: SI falta un campo obligatorio, ENTONCES EL SISTEMA muestra un error junto a ese campo (todos los campos se validan a la vez y se acumulan los errores) y NO envía nada.
- **RF-25**: SI el email no tiene un formato válido, ENTONCES EL SISTEMA muestra un error junto al campo de email y NO envía nada.
- **RF-26**: SI el envío al servicio externo falla o agota su cuota, ENTONCES EL SISTEMA informa del fallo en pantalla y ofrece la dirección de email en texto plano como alternativa directa (el email ya está visible por RF-27).
- **RF-27**: EL SISTEMA muestra la dirección de email en texto plano en la sección de contacto, para que sea accesible si el formulario no funciona.

### Tema y presentación

- **RF-28**: CUANDO el visitante activa el conmutador de tema, ENTONCES EL SISTEMA alterna entre tema claro y oscuro.
- **RF-29**: EL SISTEMA persiste la preferencia de tema del visitante.
- **RF-30**: SI el visitante nunca ha elegido tema, ENTONCES EL SISTEMA aplica el tema por defecto del sistema operativo.

### Privacidad

- **RF-31**: EL SISTEMA muestra una página de privacidad accesible desde el enlace del footer, con la información legal mínima requerida por RGPD y el aviso de uso de Web3Forms para el formulario de contacto.

## Requisitos no funcionales

- **RFN-1**: La home entrega el contenido principal en el HTML inicial, sin depender de JavaScript para leerlo. El conmutador de tema y el selector de idioma son islas de React que se hidratan de forma opcional; su ausencia no impide leer el contenido.
- **RFN-2**: Los textos de interfaz, navegación, botones y mensajes de error existen en español e inglés. Ninguna cadena visible queda solo en un idioma. Incluye todas las cadenas que hoy están hardcodeadas en componentes (ej. "Mi historia", "Asunto", "Mensaje", "Enviando", "Volver", "Privacidad", "Cargando tema...", etiquetas del perfil: "Nombre", "Rol", "Ubicación", "Disponibilidad").
- **RFN-3**: La navegación por teclado alcanza todos los elementos interactivos, con indicador de foco visible en cada uno. El foco visible cumple: `focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2`.
- **RFN-4**: Existe un enlace para saltar al contenido principal como primer elemento focusable de la página.
- **RFN-5**: El contraste entre texto y fondo es de al menos 4.5:1 en ambos temas.
- **RFN-6**: La web se usa correctamente desde 320px de ancho sin desbordamiento horizontal.
- **RFN-7**: La web no expone credenciales privadas ni tokens de servidor. La clave pública de Web3Forms viaja al navegador por diseño del servicio; eso está permitido. Cualquier otra clave secreta (JWT, base de datos, Redis) queda exclusivamente en variables de entorno del servidor.
- **RFN-8**: El sitio declara título, descripción, idioma y URL canónica por página y por locale, con etiquetas `hreflang` para cada versión disponible.
- **RFN-9**: El build de producción finaliza sin errores ni avisos que impidan el despliegue.
- **RFN-10**: Lighthouse reporta ≥95 en las 4 categorías (Performance, Accessibility, Best Practices, SEO) en ambas versiones de idioma.
- **RFN-11**: WCAG 2.1 AA mínimo: contraste, foco visible, navegación por teclado, semántica HTML, `prefers-reduced-motion` respetado, nombres accesibles en todos los botones solo-icono, estructura de encabezados sin saltos, `role="img"` + `aria-label` en logos, `skip link` funcional.

## Casos límite

- Una entrada de contenido a la que le falta un campo obligatorio hace fallar el build. Debe señalarse el fichero exacto, no producir una página vacía.
- Un proyecto sin fecha de fin en curso se presenta como "actualidad".
- El nombre del proyecto o del puesto es más largo que el ancho disponible: debe partirse o reducirse, nunca desbordar la tarjeta.
- Un locale mal formado en la URL (`/xx/`, `/projects//`, `/es/projects/en/`) se resuelve a la home del idioma por defecto en lugar de devolver error.
- El servicio de contacto está caído o agota su cuota: el visitante no debe quedarse sin salida (ver RF-26 y RF-27).
- El visitante bloquea el almacenamiento local: el sitio funciona igual, solo pierde la persistencia de idioma y tema.
- Un proyecto aparece en el listado pero su detalle no existe: el enlace no debe llevar a un 404. El sistema no genera el enlace si el slug no tiene una ficha de contenido correspondiente.
- Un texto de proyecto contiene tablas o bloques de código: debe renderizarse sin romper el diseño.
- El contenido bilingüe está desincronizado: si una entrada existe en un locale y no en el otro, el sistema muestra un aviso visible en la página del locale ausente y ofrece un enlace al locale disponible.
- Conteo de tecnologías desincronizado: si una entrada de tecnología carece del campo `source`, el build falla y señala la entrada exacta.
- Nivel de tecnología ausente: el schema Zod lo requiere; si falta, el build falla señalando la entrada.
- Un puesto de trabajo en curso (fecha de fin futura) se presenta como "actualidad". Un puesto con dos tramos separados (mismo empleador, fechas no contiguas) se muestra como dos entradas según RF-18.
- Solapamiento de fechas en la experiencia: el sistema no modifica las fechas, solo las muestra en el orden cronológico inverso que corresponda a cada tramo.
- Cadenas visibles ya existentes en un solo idioma: todas las cadenas que hoy están hardcodeadas en componentes (ver RFN-2) deben migrarse a ficheros de traducción antes de considerar la spec completa.
- Anclas decorativas dentro de la jerarquía de encabezados: la flecha del Hero tiene `aria-hidden="true"` y `tabindex="-1"`; no es un elemento interactivo ni forma parte de la jerarquía de navegación.
- Fallo de red al cambiar de idioma: si la navegación al otro locale falla, el navegador muestra su error nativo; el selector de idioma permanece en el estado anterior y no cambia de forma engañosa.
- Campos con error de validación simultáneos: RF-24 requiere que se validen los cuatro campos a la vez y se acumulen todos los errores en pantalla.

## Fuera de alcance

- Blog o sección de artículos.
- Panel de administración o CMS para editar contenido desde la web.
- Analítica de visitas.
- Descarga del CV en PDF (el fichero existe pero el botón no entra en esta versión).
- Panel de contacto con bandeja de entrada propia: el envío va a un servicio externo.
- Versionado del contenido: las entradas borradas desaparecen sin historial.
- Modo de lectura de los artículos del blog o generación de RSS.
- Internacionalización de formatos de fecha y moneda por locale más allá de español e inglés.

## Criterios de finalización

- Todos los RF y RFN están implementados o explícitamente descartados con motivo.
- El build de producción finaliza en verde.
- La web es navegable por teclado y el contraste se verifica en tema claro y oscuro.
- La home se ve correcta a 320px, 768px y 1440px en ambos idiomas: sin desbordamiento horizontal, con foco visible, y las seis secciones visibles en orden.
- El formulario rechaza entradas inválidas y confirma las válidas con `aria-live`.
- El cambio de idioma navega a la URL del otro locale, persiste la elección y restaura en visitas posteriores.
- No hay errores en la consola del navegador al navegar por la home, un detalle de proyecto, la 404 y la página de privacidad.
- Lighthouse ≥95 en las 4 categorías en ambos idiomas.
- WCAG 2.1 AA: contraste ≥4.5:1, foco visible, teclado completo, skip link, semántica HTML, `prefers-reduced-motion`, nombres accesibles, `role="img"` + `aria-label`, estructura de encabezados sin saltos.

## Decisiones tomadas en la fase de especificación

Estas decisiones quedaron resueltas durante la entrevista previa y se aplican a esta spec:

| Decisión | Valor |
|---|---|
| Origen de los datos | Fichero de contenido declarativo, no valores en componentes |
| Idiomas | Español e inglés, ambos completos (routing por locale con recarga) |
| Origen de tecnologías | Tres grupos: CV, TFG, portfolio (precedencia cv > tfg > portfolio) |
| Envío del formulario | Web3Forms, con email en texto plano como alternativa |
| Estructura de la home | Seis secciones en orden fijo, se oculta si vacía |
| Contenido | CV 2026 como fuente de identidad, experiencia, formación y stack |
| Dominio de despliegue | `https://portfolio-delta-eight-yx2zi6pmny.vercel.app` |
| Escala de nivel tecnológico | `learning`, `beginner`, `intermediate`, `advanced`, `expert` |
| Precedencia de origen | `cv` > `tfg` > `portfolio` |

## Dudas abiertas

Ninguna. Las decisiones que quedaban abiertas se resolvieron en la entrevista y en esta revisión QA. La spec está lista para `/sdd-plan`.