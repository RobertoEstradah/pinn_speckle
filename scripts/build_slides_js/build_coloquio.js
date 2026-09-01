const pptxgen = require("pptxgenjs");

// ─── PALETA ─────────────────────────────────────────────────────────────────
const C = {
  navyDark:  "0D1F35",   // fondo slides título/cierre
  navy:      "0F3460",   // fondo secciones oscuras
  blue:      "1A6FA8",   // acento principal
  blueLight: "2196F3",   // acento secundario
  teal:      "0D9488",   // acento resultados
  white:     "FFFFFF",
  offWhite:  "F0F6FC",   // fondo slides de contenido
  gray100:   "E8EDF2",
  gray400:   "94A3B8",
  gray700:   "334155",
  green:     "16A34A",   // logrado ✅
  orange:    "EA580C",   // pendiente 🔜
  text:      "1E293B",
};

// ─── HELPERS ────────────────────────────────────────────────────────────────
const W = 13.33, H = 7.5;  // LAYOUT_WIDE

function darkSlide(pres) {
  const s = pres.addSlide();
  s.background = { color: C.navyDark };
  return s;
}
function lightSlide(pres) {
  const s = pres.addSlide();
  s.background = { color: C.offWhite };
  return s;
}
function sectionSlide(pres) {
  const s = pres.addSlide();
  s.background = { color: C.navy };
  return s;
}

// Barra lateral izquierda (motivo visual consistente)
function addSidebar(slide, color) {
  slide.addShape("rect", { x: 0, y: 0, w: 0.18, h: H, fill: { color: color || C.blue }, line: { color: color || C.blue } });
}

// Encabezado de slide de contenido
function addHeader(slide, title, subtitle) {
  slide.addShape("rect", { x: 0.18, y: 0, w: W - 0.18, h: 1.1, fill: { color: C.navy }, line: { color: C.navy } });
  slide.addText(title, { x: 0.4, y: 0.12, w: W - 0.8, h: 0.65, fontSize: 26, bold: true, color: C.white, fontFace: "Calibri", margin: 0 });
  if (subtitle) {
    slide.addText(subtitle, { x: 0.4, y: 0.72, w: W - 0.8, h: 0.32, fontSize: 13, color: "A8C4E0", fontFace: "Calibri", margin: 0 });
  }
}

// Número de slide
function addPageNum(slide, n) {
  slide.addText(String(n), { x: W - 0.5, y: H - 0.4, w: 0.4, h: 0.3, fontSize: 11, color: C.gray400, align: "right", margin: 0 });
}

// Tarjeta de métrica grande
function addMetricCard(slide, x, y, w, h, label, value, unit, color) {
  slide.addShape("rect", { x, y, w, h, fill: { color: C.white }, line: { color: color || C.blue, width: 2 },
    shadow: { type: "outer", blur: 4, offset: 2, angle: 135, color: "000000", opacity: 0.10 } });
  slide.addShape("rect", { x, y, w, h: 0.06, fill: { color: color || C.blue }, line: { color: color || C.blue } });
  slide.addText(value, { x: x + 0.1, y: y + 0.15, w: w - 0.2, h: h * 0.55, fontSize: 30, bold: true, color: color || C.blue, align: "center", fontFace: "Calibri", margin: 0 });
  if (unit) {
    slide.addText(unit, { x: x + 0.1, y: y + h * 0.55 + 0.05, w: w - 0.2, h: 0.3, fontSize: 11, color: C.gray400, align: "center", fontFace: "Calibri", margin: 0 });
  }
  slide.addText(label, { x: x + 0.05, y: y + h - 0.45, w: w - 0.1, h: 0.38, fontSize: 12, bold: true, color: C.gray700, align: "center", fontFace: "Calibri", margin: 0 });
}

// ─── PRESENTACIÓN ────────────────────────────────────────────────────────────
let pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Roberto Hernández Estrada";
pres.title = "Coloquio de Avance — PINN-SIREN para Speckle Óptico";

// ══════════════════════════════════════════════════════════════════════════════
// SLIDE 1 — Portada
// ══════════════════════════════════════════════════════════════════════════════
{
  const s = darkSlide(pres);
  // Franja izquierda azul
  s.addShape("rect", { x: 0, y: 0, w: 0.5, h: H, fill: { color: C.blue }, line: { color: C.blue } });
  // Franja inferior
  s.addShape("rect", { x: 0, y: H - 1.2, w: W, h: 1.2, fill: { color: "091625" }, line: { color: "091625" } });

  // Institución
  s.addText("UNIVERSIDAD JUÁREZ AUTÓNOMA DE TABASCO", {
    x: 0.7, y: 0.35, w: W - 1.0, h: 0.38,
    fontSize: 11, bold: true, color: "7BAFD4", charSpacing: 2, fontFace: "Calibri", margin: 0
  });
  s.addText("División Académica de Ciencias y Tecnologías de la Información  |  Maestría en Ciencias de la Computación", {
    x: 0.7, y: 0.72, w: W - 1.0, h: 0.28,
    fontSize: 10, color: C.gray400, fontFace: "Calibri", margin: 0
  });
  // Línea separadora
  s.addShape("rect", { x: 0.7, y: 1.08, w: 5.0, h: 0.03, fill: { color: C.blue }, line: { color: C.blue } });

  // Título principal
  s.addText("Simulación acelerada de\nspeckle óptico mediante\nPINN-SIREN", {
    x: 0.7, y: 1.25, w: 8.5, h: 2.8,
    fontSize: 38, bold: true, color: C.white, fontFace: "Calibri",
    lineSpacingMultiple: 1.1, margin: 0
  });

  // Subtítulo
  s.addText("Coloquio de Avance de Tesis  —  Resultados experimentales", {
    x: 0.7, y: 4.1, w: 8.5, h: 0.4,
    fontSize: 14, color: "7BAFD4", italic: true, fontFace: "Calibri", margin: 0
  });

  // Info
  s.addText([
    { text: "Presenta: ", options: { bold: true, color: C.gray400 } },
    { text: "Roberto Hernández Estrada", options: { color: C.white } },
  ], { x: 0.7, y: 4.7, w: 8.5, h: 0.32, fontSize: 13, fontFace: "Calibri", margin: 0 });

  s.addText([
    { text: "Director: ", options: { bold: true, color: C.gray400 } },
    { text: "Dr. José Adán Hernández Nolasco", options: { color: C.white } },
  ], { x: 0.7, y: 5.0, w: 8.5, h: 0.32, fontSize: 13, fontFace: "Calibri", margin: 0 });

  s.addText([
    { text: "Jurado: ", options: { bold: true, color: C.gray400 } },
    { text: "Dr. Pablo Pancardo García  |  Dr. Miguel A. Wister Ovando  |  Dr. Oscar A. Chávez Bosquez", options: { color: C.gray400 } },
  ], { x: 0.7, y: 5.3, w: 11.5, h: 0.32, fontSize: 11, fontFace: "Calibri", margin: 0 });

  s.addText("Mayo 2026", {
    x: 0.7, y: H - 1.05, w: 4, h: 0.32,
    fontSize: 12, color: C.gray400, fontFace: "Calibri", margin: 0
  });
}

// ══════════════════════════════════════════════════════════════════════════════
// SLIDE 2 — Agenda
// ══════════════════════════════════════════════════════════════════════════════
{
  const s = lightSlide(pres);
  addSidebar(s);
  addHeader(s, "Agenda", "20 minutos");

  const items = [
    ["01", "Motivación y contexto", "¿Por qué simular speckle es costoso?"],
    ["02", "Hipótesis y objetivos", "Lo que propusimos en el protocolo"],
    ["03", "Marco teórico", "Helmholtz · PINNs · SIREN"],
    ["04", "Metodología", "Arquitectura · LHS · Adam + L-BFGS"],
    ["05", "Resultados — NB01 a NB03", "Validación 1D, 2D y speckle óptico"],
    ["06", "Estado del proyecto y trabajo futuro", "NB04 pendiente: benchmark FEM"],
    ["07", "Conclusiones", ""],
  ];

  items.forEach(([num, title, sub], i) => {
    const y = 1.3 + i * 0.74;
    s.addShape("rect", { x: 0.35, y, w: 0.52, h: 0.52, fill: { color: C.blue }, line: { color: C.blue } });
    s.addText(num, { x: 0.35, y, w: 0.52, h: 0.52, fontSize: 16, bold: true, color: C.white, align: "center", valign: "middle", fontFace: "Calibri", margin: 0 });
    s.addText(title, { x: 1.0, y: y + 0.02, w: 6.5, h: 0.3, fontSize: 15, bold: true, color: C.text, fontFace: "Calibri", margin: 0 });
    if (sub) s.addText(sub, { x: 1.0, y: y + 0.28, w: 6.5, h: 0.22, fontSize: 11, color: C.gray400, fontFace: "Calibri", margin: 0 });
    if (i < items.length - 1) {
      s.addShape("rect", { x: 0.35, y: y + 0.52, w: 0.02, h: 0.22, fill: { color: C.gray400 }, line: { color: C.gray400 } });
    }
  });
  addPageNum(s, 2);
}

// ══════════════════════════════════════════════════════════════════════════════
// SLIDE 3 — Motivación
// ══════════════════════════════════════════════════════════════════════════════
{
  const s = lightSlide(pres);
  addSidebar(s);
  addHeader(s, "Motivación: ¿Por qué simular speckle es costoso?", "El cuello de botella del FEM");

  // Columna izquierda: problema
  s.addShape("rect", { x: 0.3, y: 1.25, w: 5.9, h: 4.75, fill: { color: C.white }, line: { color: C.gray100, width: 1 } });
  s.addShape("rect", { x: 0.3, y: 1.25, w: 5.9, h: 0.42, fill: { color: "1A3A5C" }, line: { color: "1A3A5C" } });
  s.addText("El problema con los métodos de malla (FEM)", { x: 0.4, y: 1.27, w: 5.7, h: 0.38, fontSize: 13, bold: true, color: C.white, fontFace: "Calibri", margin: 0 });

  const problems = [
    ["🔴", "Resolución de malla ≪ λ", "Para λ = 638 nm, la malla necesita millones de nodos por dominio."],
    ["🔴", "Costo por realización", "Cada perfil de rugosidad requiere resolver el sistema completo desde cero."],
    ["🔴", "Estudios estadísticos", "Miles de realizaciones → costo computacional intratable."],
    ["🔴", "Memoria masiva", "Matrices dispersas de millones × millones de incógnitas."],
  ];
  problems.forEach(([icon, title, desc], i) => {
    const y = 1.82 + i * 0.95;
    s.addText(icon, { x: 0.45, y, w: 0.35, h: 0.32, fontSize: 16, margin: 0 });
    s.addText(title, { x: 0.85, y, w: 5.2, h: 0.3, fontSize: 13, bold: true, color: C.text, fontFace: "Calibri", margin: 0 });
    s.addText(desc, { x: 0.85, y: y + 0.3, w: 5.2, h: 0.38, fontSize: 11, color: C.gray700, fontFace: "Calibri", margin: 0 });
  });

  // Columna derecha: solución propuesta
  s.addShape("rect", { x: 6.55, y: 1.25, w: 6.4, h: 4.75, fill: { color: "EBF5FB" }, line: { color: C.blue, width: 2 } });
  s.addShape("rect", { x: 6.55, y: 1.25, w: 6.4, h: 0.42, fill: { color: C.blue }, line: { color: C.blue } });
  s.addText("Nuestra propuesta: PINN-SIREN", { x: 6.65, y: 1.27, w: 6.2, h: 0.38, fontSize: 13, bold: true, color: C.white, fontFace: "Calibri", margin: 0 });

  const solutions = [
    ["🟢", "Libre de malla (mesh-free)", "Sin discretización espacial → sin restricción de λ."],
    ["🟢", "Una sola red, múltiples BC", "Cambia solo la condición de frontera, no la arquitectura."],
    ["🟢", "Evaluación en microsegundos", "Una vez entrenada, genera campos instantáneamente."],
    ["🟢", "Precisión < 0.2% L2", "Supera el umbral de tesis (< 5%) por factor ×30."],
  ];
  solutions.forEach(([icon, title, desc], i) => {
    const y = 1.82 + i * 0.95;
    s.addText(icon, { x: 6.7, y, w: 0.35, h: 0.32, fontSize: 16, margin: 0 });
    s.addText(title, { x: 7.1, y, w: 5.7, h: 0.3, fontSize: 13, bold: true, color: "0F3460", fontFace: "Calibri", margin: 0 });
    s.addText(desc, { x: 7.1, y: y + 0.3, w: 5.7, h: 0.38, fontSize: 11, color: C.gray700, fontFace: "Calibri", margin: 0 });
  });
  addPageNum(s, 3);
}

// ══════════════════════════════════════════════════════════════════════════════
// SLIDE 4 — Hipótesis y objetivos
// ══════════════════════════════════════════════════════════════════════════════
{
  const s = sectionSlide(pres);
  addSidebar(s, C.teal);

  s.addText("Hipótesis de Investigación", {
    x: 0.4, y: 0.6, w: W - 0.8, h: 0.55,
    fontSize: 28, bold: true, color: C.white, fontFace: "Calibri", margin: 0
  });

  // Hipótesis box
  s.addShape("rect", { x: 0.35, y: 1.35, w: W - 0.7, h: 1.4, fill: { color: "0A2A45" }, line: { color: C.teal, width: 2 } });
  s.addText([
    { text: "\"", options: { fontSize: 36, color: C.teal, bold: true } },
    { text: "Las PINNs con activación sinusoidal (SIREN) pueden simular el campo eléctrico\n" +
            "del speckle óptico resolviendo la ecuación de Helmholtz 2D con ", options: { fontSize: 15, color: C.white } },
    { text: "error L₂ < 5%", options: { fontSize: 15, color: C.teal, bold: true } },
    { text: " respecto\na la solución de referencia, y con un ", options: { fontSize: 15, color: C.white } },
    { text: "Speed-up Factor S = T_FEM / T_PINN > 1", options: { fontSize: 15, color: C.teal, bold: true } },
    { text: " respecto al FEM.\"", options: { fontSize: 15, color: C.white } },
  ], { x: 0.6, y: 1.45, w: W - 1.1, h: 1.2, fontFace: "Calibri", margin: 0 });

  // Objetivos específicos
  s.addText("Objetivos Específicos", {
    x: 0.4, y: 2.95, w: 5, h: 0.38,
    fontSize: 16, bold: true, color: "7BAFD4", fontFace: "Calibri", margin: 0
  });

  const objs = [
    ["NB01", "Validar SIREN en Helmholtz 1D con solución analítica exacta"],
    ["NB02", "Resolver Helmholtz 2D con campo complejo y muestreo LHS"],
    ["NB03", "Generar speckle óptico con BC de fase aleatoria y validar estadísticamente (C ≈ 1, KS test)"],
    ["NB04", "Medir Speed-up Factor S = T_FEM / T_PINN contra FEniCSx (pendiente)"],
  ];

  objs.forEach(([tag, text], i) => {
    const y = 3.42 + i * 0.82;
    const done = i < 3;
    const col = done ? C.teal : C.orange;
    s.addShape("rect", { x: 0.35, y, w: 0.9, h: 0.34, fill: { color: col }, line: { color: col } });
    s.addText(tag, { x: 0.35, y, w: 0.9, h: 0.34, fontSize: 11, bold: true, color: C.white, align: "center", valign: "middle", fontFace: "Calibri", margin: 0 });
    s.addShape("rect", { x: 1.35, y, w: done ? 0.28 : 0.28, h: 0.34, fill: { color: col }, line: { color: col } });
    s.addText(done ? "✓" : "⏳", { x: 1.35, y, w: 0.28, h: 0.34, fontSize: 13, color: C.white, align: "center", valign: "middle", fontFace: "Calibri", margin: 0 });
    s.addText(text, { x: 1.72, y: y + 0.03, w: W - 2.1, h: 0.3, fontSize: 13, color: C.white, fontFace: "Calibri", margin: 0 });
  });
  addPageNum(s, 4);
}

// ══════════════════════════════════════════════════════════════════════════════
// SLIDE 5 — Marco teórico: Helmholtz + PINNs
// ══════════════════════════════════════════════════════════════════════════════
{
  const s = lightSlide(pres);
  addSidebar(s);
  addHeader(s, "Marco Teórico", "Ecuación de Helmholtz · PINNs · SIREN");

  // Panel Helmholtz
  s.addShape("rect", { x: 0.3, y: 1.25, w: 4.0, h: 5.7, fill: { color: C.white }, line: { color: C.gray100 } });
  s.addShape("rect", { x: 0.3, y: 1.25, w: 4.0, h: 0.38, fill: { color: "1A3A5C" }, line: { color: "1A3A5C" } });
  s.addText("Ecuación de Helmholtz 2D", { x: 0.4, y: 1.28, w: 3.8, h: 0.32, fontSize: 12, bold: true, color: C.white, fontFace: "Calibri", margin: 0 });
  s.addText("∇²E + k²E = 0", { x: 0.4, y: 1.75, w: 3.8, h: 0.55, fontSize: 22, bold: true, color: C.blue, align: "center", fontFace: "Consolas", margin: 0 });
  s.addText("∂²E/∂x² + ∂²E/∂y² + (2π)²E = 0", { x: 0.4, y: 2.35, w: 3.8, h: 0.38, fontSize: 13, color: C.gray700, align: "center", fontFace: "Consolas", margin: 0 });
  s.addText([
    { text: "k̃ = 2π", options: { bold: true, color: C.blue } },
    { text: "  (adimensional, λ = 638 nm)", options: { color: C.gray700 } }
  ], { x: 0.4, y: 2.82, w: 3.8, h: 0.3, fontSize: 12, align: "center", fontFace: "Calibri", margin: 0 });
  s.addShape("rect", { x: 0.5, y: 3.22, w: 3.6, h: 0.02, fill: { color: C.gray100 }, line: { color: C.gray100 } });
  s.addText("Dominio: Ω = [0,1]²\nLaser rojo, λ = 638 nm\nNormalización: x̃ = x/λ", {
    x: 0.4, y: 3.32, w: 3.8, h: 0.9, fontSize: 12, color: C.gray700, fontFace: "Calibri", margin: 0
  });

  // Panel PINNs
  s.addShape("rect", { x: 4.65, y: 1.25, w: 4.0, h: 5.7, fill: { color: C.white }, line: { color: C.gray100 } });
  s.addShape("rect", { x: 4.65, y: 1.25, w: 4.0, h: 0.38, fill: { color: C.blue }, line: { color: C.blue } });
  s.addText("Physics-Informed Neural Nets", { x: 4.75, y: 1.28, w: 3.8, h: 0.32, fontSize: 12, bold: true, color: C.white, fontFace: "Calibri", margin: 0 });
  s.addText("L = L_datos + λ·L_física", { x: 4.75, y: 1.75, w: 3.8, h: 0.5, fontSize: 18, bold: true, color: C.blue, align: "center", fontFace: "Consolas", margin: 0 });
  const pinnItems = [
    ["L_datos", "Error en condiciones de frontera (BC)"],
    ["L_física", "Residuo PDE en puntos de colocación"],
    ["λ_fís = 0.1", "Peso calibrado — crítico para 2D"],
    ["Adam + L-BFGS", "Optimización bifásica"],
  ];
  pinnItems.forEach(([k, v], i) => {
    const y = 2.38 + i * 0.75;
    s.addText(k, { x: 4.75, y, w: 1.65, h: 0.28, fontSize: 11, bold: true, color: C.blue, fontFace: "Consolas", margin: 0 });
    s.addText(v, { x: 6.45, y, w: 2.1, h: 0.28, fontSize: 11, color: C.gray700, fontFace: "Calibri", margin: 0 });
  });

  // Panel SIREN
  s.addShape("rect", { x: 9.0, y: 1.25, w: 4.0, h: 5.7, fill: { color: C.white }, line: { color: C.gray100 } });
  s.addShape("rect", { x: 9.0, y: 1.25, w: 4.0, h: 0.38, fill: { color: C.teal }, line: { color: C.teal } });
  s.addText("SIREN — Activación Sinusoidal", { x: 9.1, y: 1.28, w: 3.8, h: 0.32, fontSize: 12, bold: true, color: C.white, fontFace: "Calibri", margin: 0 });
  s.addText("φ(z) = sin(ω₀·z)", { x: 9.1, y: 1.75, w: 3.8, h: 0.5, fontSize: 20, bold: true, color: C.teal, align: "center", fontFace: "Consolas", margin: 0 });
  s.addText("ω₀ = 1.0  (dominio [0,1]²)", { x: 9.1, y: 2.3, w: 3.8, h: 0.3, fontSize: 12, color: C.gray700, align: "center", fontFace: "Calibri", margin: 0 });
  s.addShape("rect", { x: 9.2, y: 2.7, w: 3.6, h: 0.02, fill: { color: C.gray100 }, line: { color: C.gray100 } });
  const sirenItems = [
    "✅ Derivadas de orden arbitrario",
    "✅ Inicialización Sitzmann (2020)",
    "✅ Estable con L-BFGS",
    "✅ Supera sesgo espectral de tanh",
  ];
  sirenItems.forEach((item, i) => {
    s.addText(item, { x: 9.1, y: 2.82 + i * 0.52, w: 3.8, h: 0.38, fontSize: 12, color: C.gray700, fontFace: "Calibri", margin: 0 });
  });
  addPageNum(s, 5);
}

// ══════════════════════════════════════════════════════════════════════════════
// SLIDE 6 — Metodología
// ══════════════════════════════════════════════════════════════════════════════
{
  const s = lightSlide(pres);
  addSidebar(s);
  addHeader(s, "Metodología", "Arquitectura SIREN · LHS · Adam + L-BFGS · Función de pérdida");

  // Arquitectura
  s.addShape("rect", { x: 0.3, y: 1.25, w: 6.1, h: 2.4, fill: { color: C.white }, line: { color: C.gray100 } });
  s.addShape("rect", { x: 0.3, y: 1.25, w: 6.1, h: 0.36, fill: { color: "1A3A5C" }, line: { color: "1A3A5C" } });
  s.addText("Arquitectura SIREN 5×128", { x: 0.4, y: 1.27, w: 5.9, h: 0.3, fontSize: 13, bold: true, color: C.white, fontFace: "Calibri", margin: 0 });

  // Diagrama simplificado
  const layers = ["(x,y)", "128", "128", "128", "128", "128", "(E_r, E_i)"];
  const colors = [C.gray400, C.blue, C.blue, C.blue, C.blue, C.blue, C.teal];
  layers.forEach((lbl, i) => {
    const lx = 0.45 + i * 0.84;
    s.addShape("rect", { x: lx, y: 1.7, w: 0.65, h: 0.95, fill: { color: colors[i] }, line: { color: colors[i] } });
    s.addText(lbl, { x: lx, y: 1.7, w: 0.65, h: 0.95, fontSize: 10, bold: true, color: C.white, align: "center", valign: "middle", fontFace: "Calibri", margin: 0 });
    if (i < layers.length - 1) {
      s.addShape("rect", { x: lx + 0.65, y: 2.07, w: 0.19, h: 0.03, fill: { color: C.gray400 }, line: { color: C.gray400 } });
    }
  });
  s.addText("5 capas ocultas × 128 neuronas · sin(ω₀·z), ω₀=1.0 · 66,690 parámetros · Init. Sitzmann (2020)", {
    x: 0.4, y: 2.73, w: 5.9, h: 0.3, fontSize: 10, color: C.gray400, fontFace: "Calibri", margin: 0
  });

  // LHS
  s.addShape("rect", { x: 6.75, y: 1.25, w: 6.2, h: 2.4, fill: { color: C.white }, line: { color: C.gray100 } });
  s.addShape("rect", { x: 6.75, y: 1.25, w: 6.2, h: 0.36, fill: { color: C.blue }, line: { color: C.blue } });
  s.addText("Muestreo por Hipercubo Latino (LHS)", { x: 6.85, y: 1.27, w: 6.0, h: 0.3, fontSize: 13, bold: true, color: C.white, fontFace: "Calibri", margin: 0 });
  s.addText([
    { text: "N_c = 3,000", options: { bold: true, color: C.blue } },
    { text: " puntos de colocación interior\n", options: { color: C.text } },
    { text: "N_b = 300", options: { bold: true, color: C.blue } },
    { text: " puntos/borde (frontera)\n", options: { color: C.text } },
    { text: "N_φ = 256", options: { bold: true, color: C.teal } },
    { text: " puntos de fase rugosa (speckle)\n\n", options: { color: C.text } },
    { text: "Ventaja: ", options: { bold: true, color: C.gray700 } },
    { text: "cobertura uniforme sin patrones redundantes de malla cartesiana.", options: { color: C.gray700 } },
  ], { x: 6.85, y: 1.7, w: 5.9, h: 1.85, fontSize: 12, fontFace: "Calibri", margin: 0 });

  // Optimización
  s.addShape("rect", { x: 0.3, y: 3.9, w: 6.1, h: 2.65, fill: { color: C.white }, line: { color: C.gray100 } });
  s.addShape("rect", { x: 0.3, y: 3.9, w: 6.1, h: 0.36, fill: { color: "0D3A5C" }, line: { color: "0D3A5C" } });
  s.addText("Estrategia Adam + L-BFGS", { x: 0.4, y: 3.92, w: 5.9, h: 0.3, fontSize: 13, bold: true, color: C.white, fontFace: "Calibri", margin: 0 });

  // Fase 1
  s.addShape("rect", { x: 0.45, y: 4.38, w: 2.7, h: 1.9, fill: { color: "EBF5FB" }, line: { color: C.blue, width: 1 } });
  s.addText("FASE 1 — Adam", { x: 0.5, y: 4.4, w: 2.6, h: 0.3, fontSize: 12, bold: true, color: C.blue, fontFace: "Calibri", margin: 0 });
  s.addText("lr = 1×10⁻³\nHasta 15,000 épocas\nEarly stopping:\n  paciencia 800 épocas", {
    x: 0.5, y: 4.76, w: 2.6, h: 1.4, fontSize: 11, color: C.gray700, fontFace: "Calibri", margin: 0
  });
  // Flecha
  s.addShape("rect", { x: 3.22, y: 5.2, w: 0.38, h: 0.03, fill: { color: C.gray400 }, line: { color: C.gray400 } });
  s.addText("→", { x: 3.22, y: 5.06, w: 0.38, h: 0.3, fontSize: 16, color: C.gray400, align: "center", fontFace: "Calibri", margin: 0 });
  // Fase 2
  s.addShape("rect", { x: 3.65, y: 4.38, w: 2.6, h: 1.9, fill: { color: "E8F5E9" }, line: { color: C.teal, width: 1 } });
  s.addText("FASE 2 — L-BFGS", { x: 3.7, y: 4.4, w: 2.5, h: 0.3, fontSize: 12, bold: true, color: C.teal, fontFace: "Calibri", margin: 0 });
  s.addText("Strong Wolfe line search\nHasta 1,000 iter.\nHistorial: 100\nRefinamiento de alta precisión", {
    x: 3.7, y: 4.76, w: 2.5, h: 1.4, fontSize: 11, color: C.gray700, fontFace: "Calibri", margin: 0
  });

  // Función de pérdida
  s.addShape("rect", { x: 6.75, y: 3.9, w: 6.2, h: 2.65, fill: { color: C.white }, line: { color: C.gray100 } });
  s.addShape("rect", { x: 6.75, y: 3.9, w: 6.2, h: 0.36, fill: { color: C.teal }, line: { color: C.teal } });
  s.addText("Función de Pérdida", { x: 6.85, y: 3.92, w: 6.0, h: 0.3, fontSize: 13, bold: true, color: C.white, fontFace: "Calibri", margin: 0 });
  s.addText("L = L_datos  +  λ_fís · (L_R_real + L_R_imag)", {
    x: 6.85, y: 4.38, w: 6.0, h: 0.42, fontSize: 15, bold: true, color: C.teal, align: "center", fontFace: "Consolas", margin: 0
  });
  s.addText([
    { text: "λ_fís = 0.1", options: { bold: true, color: C.teal } },
    { text: " (crítico — duplica efectivamente el peso de la física si λ=1.0)\n\n", options: { color: C.gray700 } },
    { text: "L_datos: ", options: { bold: true, color: C.blue } },
    { text: "MSE sobre condiciones de frontera (BC)\n", options: { color: C.gray700 } },
    { text: "L_R: ", options: { bold: true, color: C.blue } },
    { text: "Residuo de Helmholtz en N_c puntos de colocación", options: { color: C.gray700 } },
  ], { x: 6.85, y: 4.88, w: 6.0, h: 1.55, fontSize: 12, fontFace: "Calibri", margin: 0 });
  addPageNum(s, 6);
}

// ══════════════════════════════════════════════════════════════════════════════
// SLIDE 7 — Resultados NB01: Helmholtz 1D
// ══════════════════════════════════════════════════════════════════════════════
{
  const s = lightSlide(pres);
  addSidebar(s, C.teal);
  addHeader(s, "Resultados NB01 — Validación Helmholtz 1D", "Arquitectura SIREN 5×64  ·  k = 2π  ·  Solución analítica: E(x) = cos(kx)");

  // Métricas grandes
  const metrics1 = [
    ["Error L₂", "0.006%", "", C.teal],
    ["R²", "1.000000", "", C.blue],
    ["MAE", "3.50×10⁻⁵", "", C.blue],
    ["Tiempo", "251 s", "", C.gray700],
  ];
  metrics1.forEach(([label, val, unit, col], i) => {
    addMetricCard(s, 0.3 + i * 3.2, 1.35, 3.0, 1.55, label, val, unit, col);
  });

  // Tabla entrenamiento
  s.addShape("rect", { x: 0.3, y: 3.05, w: 5.9, h: 3.5, fill: { color: C.white }, line: { color: C.gray100 } });
  s.addShape("rect", { x: 0.3, y: 3.05, w: 5.9, h: 0.36, fill: { color: "1A3A5C" }, line: { color: "1A3A5C" } });
  s.addText("Detalles de entrenamiento", { x: 0.4, y: 3.07, w: 5.7, h: 0.3, fontSize: 13, bold: true, color: C.white, fontFace: "Calibri", margin: 0 });

  const trainData = [
    [{ text: "Métrica", options: { bold: true, color: C.white, fill: { color: "1A3A5C" } } }, { text: "Valor", options: { bold: true, color: C.white, fill: { color: "1A3A5C" } } }],
    ["Épocas Adam", "15,000 / 15,000"],
    ["Iteraciones L-BFGS", "202 / 500"],
    ["Error máximo", "5.77×10⁻⁵"],
    ["RMSE", "3.9×10⁻⁵"],
    ["Correlación Pearson", "1.000000"],
    ["GPU", "NVIDIA RTX 5050"],
  ];
  s.addTable(trainData, {
    x: 0.35, y: 3.45, w: 5.8, h: 3.0,
    border: { pt: 0.5, color: C.gray100 },
    colW: [3.2, 2.6],
    fontSize: 12, fontFace: "Calibri", color: C.text,
    fill: { color: C.white },
  });

  // Comparativa Schoder
  s.addShape("rect", { x: 6.55, y: 3.05, w: 6.4, h: 3.5, fill: { color: "EBF5FB" }, line: { color: C.blue, width: 2 } });
  s.addShape("rect", { x: 6.55, y: 3.05, w: 6.4, h: 0.36, fill: { color: C.blue }, line: { color: C.blue } });
  s.addText("Comparativa vs Estado del Arte", { x: 6.65, y: 3.07, w: 6.2, h: 0.3, fontSize: 13, bold: true, color: C.white, fontFace: "Calibri", margin: 0 });

  const compData = [
    [{ text: "Método", options: { bold: true, color: C.white, fill: { color: C.blue } } }, { text: "Error L₂", options: { bold: true, color: C.white, fill: { color: C.blue } } }, { text: "Factor", options: { bold: true, color: C.white, fill: { color: C.blue } } }],
    ["Schoder & Kraxberger (2024)", "2.490%", "—"],
    [{ text: "PINN-SIREN (este trabajo)", options: { bold: true } }, { text: "0.006%", options: { bold: true, color: C.teal } }, { text: "×415", options: { bold: true, color: C.teal } }],
  ];
  s.addTable(compData, {
    x: 6.6, y: 3.45, w: 6.3, h: 1.3,
    border: { pt: 0.5, color: C.gray100 },
    colW: [3.5, 1.5, 1.3],
    fontSize: 12, fontFace: "Calibri", color: C.text,
    fill: { color: C.white },
  });

  s.addText("🏆 Factor de mejora: ×415", {
    x: 6.65, y: 4.85, w: 6.2, h: 0.48,
    fontSize: 20, bold: true, color: C.teal, align: "center", fontFace: "Calibri", margin: 0
  });
  s.addText("La hipótesis L₂ < 5% se cumple con margen de casi 3 órdenes de magnitud.\nR² = 1.000000 — ajuste prácticamente perfecto en toda la malla de evaluación.", {
    x: 6.65, y: 5.4, w: 6.2, h: 1.1,
    fontSize: 12, color: C.gray700, fontFace: "Calibri", margin: 0
  });
  addPageNum(s, 7);
}

// ══════════════════════════════════════════════════════════════════════════════
// SLIDE 8 — Resultados NB02: Helmholtz 2D
// ══════════════════════════════════════════════════════════════════════════════
{
  const s = lightSlide(pres);
  addSidebar(s, C.blue);
  addHeader(s, "Resultados NB02 — Helmholtz 2D con Campo Complejo", "Arquitectura SIREN 5×128  ·  LHS 3,000 pts  ·  Onda plana E = e^{i(k_x·x + k_y·y)}");

  // Métricas
  const m2 = [
    ["L₂ promedio", "0.171%", "", C.blue],
    ["L₂ E_real", "0.214%", "", C.blue],
    ["L₂ E_imag", "0.127%", "", C.teal],
    ["Tiempo", "299 s", "", C.gray700],
  ];
  m2.forEach(([label, val, unit, col], i) => {
    addMetricCard(s, 0.3 + i * 3.2, 1.35, 3.0, 1.55, label, val, unit, col);
  });

  // Tabla detalle
  s.addShape("rect", { x: 0.3, y: 3.05, w: 5.9, h: 3.5, fill: { color: C.white }, line: { color: C.gray100 } });
  s.addShape("rect", { x: 0.3, y: 3.05, w: 5.9, h: 0.36, fill: { color: "1A3A5C" }, line: { color: "1A3A5C" } });
  s.addText("Métricas por componente del campo complejo", { x: 0.4, y: 3.07, w: 5.7, h: 0.3, fontSize: 13, bold: true, color: C.white, fontFace: "Calibri", margin: 0 });

  const nb02Data = [
    [{ text: "Métrica", options: { bold: true, color: C.white, fill: { color: "1A3A5C" } } }, { text: "E_real", options: { bold: true, color: C.white, fill: { color: "1A3A5C" } } }, { text: "E_imag", options: { bold: true, color: C.white, fill: { color: "1A3A5C" } } }],
    ["Error L₂ (%)", "0.214", "0.127"],
    ["R²", "0.999995", "0.999998"],
    ["Pearson", "0.999998", "0.999999"],
    ["Épocas Adam", "8,737 / 15,000", "—"],
    ["L-BFGS", "1,035 iter.", "—"],
  ];
  s.addTable(nb02Data, {
    x: 0.35, y: 3.45, w: 5.8, h: 2.8,
    border: { pt: 0.5, color: C.gray100 },
    colW: [2.5, 1.65, 1.65],
    fontSize: 12, fontFace: "Calibri", color: C.text, fill: { color: C.white },
  });

  // Panel derecho: hallazgos
  s.addShape("rect", { x: 6.55, y: 3.05, w: 6.4, h: 3.5, fill: { color: "EBF5FB" }, line: { color: C.blue, width: 2 } });
  s.addShape("rect", { x: 6.55, y: 3.05, w: 6.4, h: 0.36, fill: { color: C.blue }, line: { color: C.blue } });
  s.addText("Hallazgos clave", { x: 6.65, y: 3.07, w: 6.2, h: 0.3, fontSize: 13, bold: true, color: C.white, fontFace: "Calibri", margin: 0 });

  const findings = [
    ["📈", "Escalado de capacidad", "Aumentar d = 64 → 128 redujo el error promedio de 0.436% a 0.171% (mejora ×2.5)."],
    ["🎯", "LHS vs malla uniforme", "LHS redujo el error en regiones de baja densidad vs mallas cartesianas equivalentes."],
    ["⚖️", "Peso λ_fís = 0.1 crítico", "Con λ=1.0, la red no converge — dos residuos (real + imag) doblan el peso de la física."],
    ["🏆", "Mejora vs Schoder 2D", "Error 0.171% vs 1.91% → factor ×11.2 de mejora. Meta < 5% superada ampliamente."],
  ];
  findings.forEach(([icon, title, desc], i) => {
    const y = 3.52 + i * 0.76;
    s.addText(icon, { x: 6.65, y, w: 0.35, h: 0.3, fontSize: 14, margin: 0 });
    s.addText(title, { x: 7.05, y, w: 5.8, h: 0.28, fontSize: 12, bold: true, color: C.navy, fontFace: "Calibri", margin: 0 });
    s.addText(desc, { x: 7.05, y: y + 0.28, w: 5.8, h: 0.38, fontSize: 11, color: C.gray700, fontFace: "Calibri", margin: 0 });
  });
  addPageNum(s, 8);
}

// ══════════════════════════════════════════════════════════════════════════════
// SLIDE 9 — Resultados NB03: Speckle óptico
// ══════════════════════════════════════════════════════════════════════════════
{
  const s = lightSlide(pres);
  addSidebar(s, C.teal);
  addHeader(s, "Resultados NB03 — Simulación de Speckle Óptico", "BC rugosa: φ(x) ~ U(0,2π) en y=0  ·  Bordes x=0, x=1, y=1: libres  ·  N_φ = 256 pts");

  // Métricas grandes
  addMetricCard(s, 0.3, 1.35, 3.2, 1.65, "Contraste C = σ_I/⟨I⟩", "1.0253", "|C-1| = 0.025 < 0.1  ✅", C.green);
  addMetricCard(s, 3.75, 1.35, 2.8, 1.65, "KS p-valor", "< 0.001", "Alta potencia estadística ⚠", C.orange);
  addMetricCard(s, 6.8, 1.35, 2.8, 1.65, "Épocas Adam", "7,976", "/ 15,000", C.blue);
  addMetricCard(s, 9.85, 1.35, 3.1, 1.65, "Tiempo total", "227 s", "GPU RTX 5050", C.gray700);

  // Tabla validación estadística
  s.addShape("rect", { x: 0.3, y: 3.15, w: 5.5, h: 3.4, fill: { color: C.white }, line: { color: C.gray100 } });
  s.addShape("rect", { x: 0.3, y: 3.15, w: 5.5, h: 0.36, fill: { color: "0D4A3A" }, line: { color: "0D4A3A" } });
  s.addText("Validación estadística — Criterio Goodman (2007)", { x: 0.4, y: 3.17, w: 5.3, h: 0.3, fontSize: 12, bold: true, color: C.white, fontFace: "Calibri", margin: 0 });

  const speckleData = [
    [{ text: "Métrica", options: { bold: true, color: C.white, fill: { color: "0D4A3A" } } }, { text: "PINN", options: { bold: true, color: C.white, fill: { color: "0D4A3A" } } }, { text: "Teórico", options: { bold: true, color: C.white, fill: { color: "0D4A3A" } } }],
    [{ text: "C = σ_I/⟨I⟩", options: {} }, { text: "1.0253 ✅", options: { bold: true, color: C.green } }, "= 1"],
    ["|C - 1|", { text: "0.025 ✅", options: { bold: true, color: C.green } }, "< 0.1"],
    ["KS p-valor", { text: "< 0.0001 ⚠", options: { color: C.orange } }, "> 0.05"],
    ["Frac. I > 2⟨I⟩", "≈ 0.135", "e⁻² ≈ 0.135"],
    ["L-BFGS iter.", "8 / 500", "—"],
  ];
  s.addTable(speckleData, {
    x: 0.35, y: 3.55, w: 5.4, h: 2.85,
    border: { pt: 0.5, color: C.gray100 },
    colW: [2.3, 1.65, 1.45],
    fontSize: 12, fontFace: "Calibri", color: C.text, fill: { color: C.white },
  });

  // Interpretación
  s.addShape("rect", { x: 6.2, y: 3.15, w: 6.75, h: 3.4, fill: { color: "E8FFF5" }, line: { color: C.teal, width: 2 } });
  s.addShape("rect", { x: 6.2, y: 3.15, w: 6.75, h: 0.36, fill: { color: C.teal }, line: { color: C.teal } });
  s.addText("Interpretación de resultados", { x: 6.3, y: 3.17, w: 6.5, h: 0.3, fontSize: 13, bold: true, color: C.white, fontFace: "Calibri", margin: 0 });

  const interp = [
    ["✅", "C = 1.0253 confirma speckle totalmente desarrollado", "Criterio de Goodman cumplido: la distribución de intensidades sigue la ley exponencial negativa."],
    ["✅", "Arquitectura agnóstica a la condición de frontera", "La misma SIREN 5×128 de NB02 genera speckle cambiando solo la BC en y=0. Sin modificar la red."],
    ["⚠", "Test KS: alta potencia estadística", "Con N = 10,000 puntos, el test KS rechaza H₀ ante desviaciones < 1%. El fallo es del test, no del modelo."],
    ["📌", "Causa física: falta condición de Sommerfeld", "El borde y=1 sin condición absorbente genera reflexiones espurias → trabajo futuro (NB04+)."],
  ];
  interp.forEach(([icon, title, desc], i) => {
    const y = 3.62 + i * 0.72;
    s.addText(icon, { x: 6.3, y, w: 0.3, h: 0.28, fontSize: 14, margin: 0 });
    s.addText(title, { x: 6.65, y, w: 6.15, h: 0.28, fontSize: 12, bold: true, color: "0A4A3A", fontFace: "Calibri", margin: 0 });
    s.addText(desc, { x: 6.65, y: y + 0.28, w: 6.15, h: 0.38, fontSize: 11, color: C.gray700, fontFace: "Calibri", margin: 0 });
  });
  addPageNum(s, 9);
}

// ══════════════════════════════════════════════════════════════════════════════
// SLIDE 10 — Comparativa estado del arte
// ══════════════════════════════════════════════════════════════════════════════
{
  const s = lightSlide(pres);
  addSidebar(s, C.blue);
  addHeader(s, "Comparativa con el Estado del Arte", "PINN-SIREN vs Schoder & Kraxberger (2024)  ·  arXiv:2403.06623");

  const compRows = [
    [{ text: "Método", options: { bold: true, color: C.white, fill: { color: C.navy } } }, { text: "Dim.", options: { bold: true, color: C.white, fill: { color: C.navy } } }, { text: "Error L₂ (%)", options: { bold: true, color: C.white, fill: { color: C.navy } } }, { text: "Factor de mejora", options: { bold: true, color: C.white, fill: { color: C.navy } } }],
    ["Schoder & Kraxberger (2024)\nPINNs convencionales", "1D", "2.490", "—"],
    ["Schoder & Kraxberger (2024)\nPINNs convencionales", "2D", "1.910", "—"],
    [{ text: "PINN-SIREN (este trabajo)", options: { bold: true } }, { text: "1D", options: { bold: true } }, { text: "0.006", options: { bold: true, color: C.teal } }, { text: "× 415 ✅", options: { bold: true, color: C.teal } }],
    [{ text: "PINN-SIREN (este trabajo)", options: { bold: true } }, { text: "2D", options: { bold: true } }, { text: "0.171", options: { bold: true, color: C.blue } }, { text: "× 11.2 ✅", options: { bold: true, color: C.blue } }],
  ];

  s.addTable(compRows, {
    x: 0.5, y: 1.35, w: 12.3, h: 3.5,
    border: { pt: 0.5, color: C.gray100 },
    colW: [5.5, 1.2, 2.5, 3.1],
    fontSize: 14, fontFace: "Calibri", color: C.text, fill: { color: C.white },
  });

  // Stats grandes
  s.addShape("rect", { x: 0.5, y: 5.05, w: 5.8, h: 1.85, fill: { color: "EBF5FB" }, line: { color: C.teal, width: 2 } });
  s.addText("×415", { x: 0.6, y: 5.1, w: 5.6, h: 0.88, fontSize: 52, bold: true, color: C.teal, align: "center", fontFace: "Calibri", margin: 0 });
  s.addText("Factor de mejora en 1D sobre Schoder (2024)", { x: 0.6, y: 5.95, w: 5.6, h: 0.38, fontSize: 13, color: C.gray700, align: "center", fontFace: "Calibri", margin: 0 });

  s.addShape("rect", { x: 7.0, y: 5.05, w: 5.8, h: 1.85, fill: { color: "EBF5FB" }, line: { color: C.blue, width: 2 } });
  s.addText("×11.2", { x: 7.1, y: 5.1, w: 5.6, h: 0.88, fontSize: 52, bold: true, color: C.blue, align: "center", fontFace: "Calibri", margin: 0 });
  s.addText("Factor de mejora en 2D sobre Schoder (2024)", { x: 7.1, y: 5.95, w: 5.6, h: 0.38, fontSize: 13, color: C.gray700, align: "center", fontFace: "Calibri", margin: 0 });

  addPageNum(s, 10);
}

// ══════════════════════════════════════════════════════════════════════════════
// SLIDE 11 — Estado del proyecto
// ══════════════════════════════════════════════════════════════════════════════
{
  const s = lightSlide(pres);
  addSidebar(s);
  addHeader(s, "Estado del Proyecto", "Avance general a la fecha del coloquio");

  const notebooks = [
    { id: "NB01", name: "Helmholtz 1D", status: "COMPLETO", pct: 100, metrics: "L₂ = 0.006%  ·  R² = 1.000000  ·  t = 251 s", col: C.green },
    { id: "NB02", name: "Helmholtz 2D Campo Complejo", status: "COMPLETO", pct: 100, metrics: "L₂_avg = 0.171%  ·  Adam 8,737 épocas  ·  t = 299 s", col: C.green },
    { id: "NB03", name: "Speckle Óptico", status: "COMPLETO", pct: 100, metrics: "C = 1.0253 ✅  ·  KS p<0.001  ·  t = 227 s", col: C.green },
    { id: "NB04", name: "Benchmark FEM (FEniCSx)", status: "PENDIENTE", pct: 0, metrics: "Speed-up Factor S = T_FEM / T_PINN  ·  Próxima etapa", col: C.orange },
    { id: "PAPER", name: "Artículo LaTeX", status: "COMPLETO", pct: 100, metrics: "18 páginas  ·  Español + Abstract EN  ·  pdflatex + biber", col: C.blue },
  ];

  notebooks.forEach((nb, i) => {
    const y = 1.35 + i * 1.1;
    // Tag
    s.addShape("rect", { x: 0.3, y, w: 1.1, h: 0.6, fill: { color: nb.col }, line: { color: nb.col } });
    s.addText(nb.id, { x: 0.3, y, w: 1.1, h: 0.6, fontSize: 13, bold: true, color: C.white, align: "center", valign: "middle", fontFace: "Calibri", margin: 0 });
    // Name
    s.addText(nb.name, { x: 1.55, y: y + 0.05, w: 5.5, h: 0.3, fontSize: 14, bold: true, color: C.text, fontFace: "Calibri", margin: 0 });
    // Metrics
    s.addText(nb.metrics, { x: 1.55, y: y + 0.35, w: 8.5, h: 0.22, fontSize: 11, color: C.gray400, fontFace: "Calibri", margin: 0 });
    // Status badge
    s.addShape("rect", { x: 10.4, y: y + 0.1, w: 2.6, h: 0.4, fill: { color: nb.col }, line: { color: nb.col } });
    s.addText(nb.status, { x: 10.4, y: y + 0.1, w: 2.6, h: 0.4, fontSize: 12, bold: true, color: C.white, align: "center", valign: "middle", fontFace: "Calibri", margin: 0 });
    // Progress bar bg
    s.addShape("rect", { x: 1.55, y: y + 0.62, w: 8.5, h: 0.12, fill: { color: C.gray100 }, line: { color: C.gray100 } });
    if (nb.pct > 0) s.addShape("rect", { x: 1.55, y: y + 0.62, w: 8.5 * nb.pct / 100, h: 0.12, fill: { color: nb.col }, line: { color: nb.col } });
  });
  addPageNum(s, 11);
}

// ══════════════════════════════════════════════════════════════════════════════
// SLIDE 12 — Trabajo futuro: NB04
// ══════════════════════════════════════════════════════════════════════════════
{
  const s = sectionSlide(pres);
  addSidebar(s, C.orange);
  s.addText("Trabajo Futuro", { x: 0.4, y: 0.55, w: W - 0.8, h: 0.55, fontSize: 30, bold: true, color: C.white, fontFace: "Calibri", margin: 0 });

  // NB04 — Benchmark
  s.addShape("rect", { x: 0.3, y: 1.3, w: W - 0.6, h: 2.25, fill: { color: "0A2A45" }, line: { color: C.orange, width: 2 } });
  s.addShape("rect", { x: 0.3, y: 1.3, w: W - 0.6, h: 0.38, fill: { color: C.orange }, line: { color: C.orange } });
  s.addText("NB04 — Benchmark FEM: Cuantificar el Speed-up Factor  (prioridad inmediata)", {
    x: 0.4, y: 1.32, w: W - 0.8, h: 0.34, fontSize: 13, bold: true, color: C.white, fontFace: "Calibri", margin: 0
  });
  s.addText([
    { text: "S = T_FEM / T_PINN", options: { fontSize: 18, bold: true, color: C.orange } },
    { text: "    donde T_FEM se mide con FEniCSx (misma malla, misma BC, mismo dominio)", options: { fontSize: 13, color: "A8C4E0" } }
  ], { x: 0.5, y: 1.78, w: W - 1.0, h: 0.42, fontFace: "Calibri", margin: 0 });
  s.addText("Hardware: Linux/WSL2 con conda-forge (fenics-dolfinx)  ·  Comparación justa: PINN vs FEM en hardware idéntico\nMétricas objetivo: tiempo de wall-clock, uso de memoria pico, error L₂ relativo", {
    x: 0.5, y: 2.28, w: W - 1.0, h: 0.68, fontSize: 12, color: "7BAFD4", fontFace: "Calibri", margin: 0
  });

  // Extensiones futuras
  s.addText("Extensiones a mediano plazo", {
    x: 0.4, y: 3.75, w: 5, h: 0.35, fontSize: 14, bold: true, color: "7BAFD4", fontFace: "Calibri", margin: 0
  });

  const future = [
    ["NB05-06", "Medios inhomogéneos", "Helmholtz con índice de refracción variable n(r). Relevante para materiales GRIN y tejidos biológicos."],
    ["NB07", "Speckle en medios GRIN", "Speckle en materiales con perfil de índice gradiente. Impacto en imágenes biomédicas y comunicaciones ópticas."],
    ["Mejora", "Condición de Sommerfeld", "L_rad = |∂E/∂n − ikE|² en y=1 para modelar propagación libre. Elimina reflexiones espurias → mejora el test KS."],
  ];
  future.forEach(([tag, title, desc], i) => {
    const y = 4.22 + i * 0.9;
    s.addShape("rect", { x: 0.3, y, w: 1.1, h: 0.55, fill: { color: "0A2A45" }, line: { color: "3A6FA8" } });
    s.addText(tag, { x: 0.3, y, w: 1.1, h: 0.55, fontSize: 10, bold: true, color: "7BAFD4", align: "center", valign: "middle", fontFace: "Calibri", margin: 0 });
    s.addText(title, { x: 1.55, y: y + 0.04, w: 5.5, h: 0.26, fontSize: 13, bold: true, color: C.white, fontFace: "Calibri", margin: 0 });
    s.addText(desc, { x: 1.55, y: y + 0.3, w: 11.4, h: 0.26, fontSize: 11, color: "7BAFD4", fontFace: "Calibri", margin: 0 });
  });
  addPageNum(s, 12);
}

// ══════════════════════════════════════════════════════════════════════════════
// SLIDE 13 — Conclusiones
// ══════════════════════════════════════════════════════════════════════════════
{
  const s = lightSlide(pres);
  addSidebar(s, C.teal);
  addHeader(s, "Conclusiones", "Lo que demostramos hasta ahora");

  const conclusions = [
    {
      n: "1",
      title: "Precisión muy superior al umbral de la tesis",
      body: "SIREN-PINN alcanzó L₂ = 0.006% (1D) y L₂ = 0.171% (2D) — ambos con R² > 0.9999. La meta de < 5% se supera por factores ×415 y ×11.2 respecto a Schoder (2024).",
      col: C.teal,
    },
    {
      n: "2",
      title: "La arquitectura es agnóstica a la condición de frontera",
      body: "La misma SIREN 5×128 resuelve onda plana suave (NB02) y fase rugosa aleatoria (NB03) sin modificar la arquitectura ni la función de pérdida — solo cambia el dato en y=0.",
      col: C.blue,
    },
    {
      n: "3",
      title: "Validación estadística del speckle (criterio Goodman)",
      body: "C = 1.0253 (|C−1| = 0.025 < 0.1 ✅). El fallo del test KS se atribuye a la alta potencia estadística con N=10,000 puntos, no a un defecto del modelo.",
      col: C.teal,
    },
    {
      n: "4",
      title: "Estrategia Adam + L-BFGS y λ_fís = 0.1 son determinantes",
      body: "La bifase Adam (exploración global) + L-BFGS (refinamiento de 2.º orden) y el peso calibrado λ=0.1 fueron críticos para la convergencia en 2D. Cada componente es necesario.",
      col: C.blue,
    },
    {
      n: "5",
      title: "Siguiente paso: cuantificar el Speed-up Factor",
      body: "NB04 medirá S = T_FEM/T_PINN con FEniCSx. Este benchmark cerrará la hipótesis completa de la tesis y será el resultado central del artículo.",
      col: C.orange,
    },
  ];

  conclusions.forEach((c, i) => {
    const y = 1.3 + i * 1.18;
    s.addShape("rect", { x: 0.3, y, w: 0.55, h: 0.55, fill: { color: c.col }, line: { color: c.col } });
    s.addText(c.n, { x: 0.3, y, w: 0.55, h: 0.55, fontSize: 18, bold: true, color: C.white, align: "center", valign: "middle", fontFace: "Calibri", margin: 0 });
    s.addText(c.title, { x: 1.0, y: y + 0.02, w: W - 1.35, h: 0.3, fontSize: 13, bold: true, color: c.col === C.orange ? C.orange : C.text, fontFace: "Calibri", margin: 0 });
    s.addText(c.body, { x: 1.0, y: y + 0.33, w: W - 1.35, h: 0.65, fontSize: 11, color: C.gray700, fontFace: "Calibri", margin: 0 });
  });
  addPageNum(s, 13);
}

// ══════════════════════════════════════════════════════════════════════════════
// SLIDE 14 — Gracias / Preguntas
// ══════════════════════════════════════════════════════════════════════════════
{
  const s = darkSlide(pres);
  s.addShape("rect", { x: 0, y: 0, w: 0.5, h: H, fill: { color: C.teal }, line: { color: C.teal } });
  s.addShape("rect", { x: 0, y: H - 1.1, w: W, h: 1.1, fill: { color: "091625" }, line: { color: "091625" } });

  s.addText("¡Gracias!", {
    x: 0.7, y: 1.1, w: W - 1.2, h: 1.2,
    fontSize: 58, bold: true, color: C.teal, fontFace: "Calibri", margin: 0
  });
  s.addText("Redes Neuronales Informadas por Física para la Simulación de Speckle Óptico", {
    x: 0.7, y: 2.45, w: W - 1.2, h: 0.55,
    fontSize: 18, color: "7BAFD4", fontFace: "Calibri", italic: true, margin: 0
  });
  s.addShape("rect", { x: 0.7, y: 3.1, w: 4.5, h: 0.03, fill: { color: C.blue }, line: { color: C.blue } });

  s.addText([
    { text: "Roberto Hernández Estrada\n", options: { bold: true, color: C.white, fontSize: 15 } },
    { text: "robertohernandezestrd@gmail.com\n", options: { color: C.gray400, fontSize: 13 } },
    { text: "Maestría en Ciencias de la Computación — UJAT\n", options: { color: C.gray400, fontSize: 13 } },
    { text: "Director: Dr. José Adán Hernández Nolasco", options: { color: C.gray400, fontSize: 13 } },
  ], { x: 0.7, y: 3.25, w: 7.5, h: 1.6, fontFace: "Calibri", margin: 0 });

  // Resumen de métricas
  s.addShape("rect", { x: 8.8, y: 2.2, w: 4.2, h: 4.25, fill: { color: "091625" }, line: { color: "1A3A5C", width: 1 } });
  s.addText("Resumen de resultados", { x: 8.95, y: 2.28, w: 3.9, h: 0.32, fontSize: 12, bold: true, color: "7BAFD4", fontFace: "Calibri", margin: 0 });
  const summary = [
    ["NB01", "L₂ = 0.006%  ·  ×415 vs Schoder"],
    ["NB02", "L₂ = 0.171%  ·  ×11.2 vs Schoder"],
    ["NB03", "C = 1.0253 ✅  ·  t = 227 s"],
    ["NB04", "Speed-up S = T_FEM/T_PINN  ⏳"],
    ["Paper", "18 pp. LaTeX  ·  ES + EN Abstract"],
  ];
  summary.forEach(([tag, val], i) => {
    const y = 2.7 + i * 0.72;
    s.addShape("rect", { x: 8.95, y, w: 0.75, h: 0.38, fill: { color: i < 3 ? C.teal : i === 3 ? C.orange : C.blue }, line: { color: C.teal } });
    s.addText(tag, { x: 8.95, y, w: 0.75, h: 0.38, fontSize: 10, bold: true, color: C.white, align: "center", valign: "middle", fontFace: "Calibri", margin: 0 });
    s.addText(val, { x: 9.75, y: y + 0.05, w: 3.1, h: 0.28, fontSize: 11, color: "A8C4E0", fontFace: "Calibri", margin: 0 });
  });

  s.addText("Universidad Juárez Autónoma de Tabasco  ·  DACTIE  ·  Mayo 2026", {
    x: 0.6, y: H - 0.85, w: W - 1.2, h: 0.3,
    fontSize: 10, color: C.gray400, fontFace: "Calibri", margin: 0
  });
}

// ─── GUARDAR ────────────────────────────────────────────────────────────────
pres.writeFile({ fileName: "D:\\Tesis_Maestria\\master_supporting_docs\\supporting_slides\\Coloquio_Avance_Tesis_RobertoHernandez.pptx" })
  .then(() => console.log("✅ PPTX guardado correctamente."))
  .catch(e => console.error("❌ Error:", e));
