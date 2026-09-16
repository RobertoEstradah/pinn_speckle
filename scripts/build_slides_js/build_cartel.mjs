import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

// ADVERTENCIA: este script NO se ejecuta tal cual hoy. Depende del runtime de
// presentaciones de Codex, clavado a la version 26.826.12353, que ya no esta
// instalada en esta maquina (solo 26.909.11809). Se conserva como registro de
// como se construyo el cartel, no como pipeline vivo. Ver el README de
// slides/congreso_smf/.
const RUNTIME_VERSION = process.env.CODEX_PRESENTATIONS_VERSION || "26.826.12353";
const runtimePath = `${process.env.USERPROFILE || process.env.HOME}/.codex/plugins/cache/openai-primary-runtime/presentations/${RUNTIME_VERSION}/skills/Presentations/container_tools/runtime_helpers.mjs`;
const { importRuntimeModule } = await import(pathToFileURL(runtimePath).href);

// Rutas relativas a la raiz del proyecto, deducida de la ubicacion del script.
const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const sourceDir = path.join(projectRoot, "slides", "congreso_smf", "fuente");
const starterPptx = path.join(sourceDir, "template-starter.pptx");
const outputDir = path.join(projectRoot, "slides", "congreso_smf");
const finalPptx = path.join(outputDir, "cartel_pinn_siren_2d.pptx");
const thesisFigures = path.join(projectRoot, "tesis", "Tesis_Actual", "figures");

// Salidas intermedias (vistas previas, montajes, inspeccion): fuera del
// repositorio. Antes se escribian en tmp/smf_cartel y ocupaban 27 MB.
const tmpDir = process.env.CARTEL_TMP_DIR || path.join(projectRoot, "tmp", "smf_cartel");

async function writeBlob(filePath, blob) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, new Uint8Array(await blob.arrayBuffer()));
}

const textStyle = (overrides = {}) => ({
  fontSize: "45.33px",
  typeface: "Arial",
  ...overrides,
});

const run = (text, overrides = {}) => ({ run: text, textStyle: textStyle(overrides) });
const paragraph = (runs, alignment = "justify") => ({ runs, paragraphStyle: { alignment } });
const blank = () => paragraph([run(" ")], "left");

function setSection(shape, heading, paragraphs, options = {}) {
  const color = options.color ?? "tx1";
  const headingColor = options.headingColor ?? color;
  const bodySize = options.bodySize ?? "45.33px";
  const headingSize = options.headingSize ?? "45.33px";
  const data = [
    paragraph([run(heading, { fontSize: headingSize, bold: true, color: headingColor })], "center"),
    ...paragraphs.map((item) => {
      if (item === null) return blank();
      if (Array.isArray(item)) return paragraph(item, "justify");
      return paragraph([run(item, { fontSize: bodySize, color })], "justify");
    }),
  ];
  const frame = shape.frame;
  shape.text.set(data);
  shape.frame = frame;
}

function getShape(slide, name) {
  const shape = slide.shapes.items.find((item) => item.name === name);
  if (!shape) throw new Error(`Missing source shape: ${name}`);
  return shape;
}

function getImage(slide, name) {
  const image = slide.images.items.find((item) => item.name === name);
  if (!image) throw new Error(`Missing source image: ${name}`);
  return image;
}

async function replaceImage(image, filePath, alt) {
  const bytes = await fs.readFile(filePath);
  const frame = image.frame;
  const geometry = image.geometry;
  const borderRadius = image.borderRadius;
  image.replace({ blob: bytes, contentType: "image/png", alt, fit: "contain" });
  image.frame = frame;
  image.crop = { left: 0, top: 0, right: 0, bottom: 0 };
  if (geometry) image.geometry = geometry;
  if (borderRadius !== undefined) image.borderRadius = borderRadius;
  image.rotation = 0;
  image.verticalFlip = false;
  image.flipHorizontal = false;
  image.flipVertical = false;
}

async function main() {
  const { FileBlob, PresentationFile } = await importRuntimeModule("@oai/artifact-tool");
  const presentation = await PresentationFile.importPptx(await FileBlob.load(starterPptx));
  const slide = presentation.slides.items[0];

  setSection(getShape(slide, "Título 1"), "Solución mesh-free de la ecuación de Helmholtz\nmediante redes neuronales físicamente informadas (PINN-SIREN)", [
    [run("Roberto Hernández Estrada¹ · José Adán Hernández Nolasco¹", { fontSize: "53.33px", bold: true, color: "#000000" })],
    [run("Ibis Ricárdez Vargas² · Óscar Andrés Flores Vargas²", { fontSize: "53.33px", bold: true, color: "#000000" })],
    [run("¹ División Académica de Ciencias y Tecnologías de la Información · ² División Académica de Ciencias Básicas", { fontSize: "53.33px" })],
    [run("Universidad Juárez Autónoma de Tabasco · Sesión de Óptica · LXIX Congreso Nacional de Física · 15 de octubre de 2026", { fontSize: "48px" })],
  ], { headingSize: "74.67px", bodySize: "53.33px", color: "#000000", headingColor: "#000000" });

  setSection(getShape(slide, "CuadroTexto 7"), "1. RESUMEN.", [
    "Se propone un modelo PINN-SIREN para resolver la ecuación de Helmholtz y acelerar la simulación de speckle óptico en dominios 2D.",
    "El campo eléctrico complejo se aprende directamente desde la EDP y sus condiciones de frontera, sin construir una malla de elementos finitos.",
    "El modelo alcanza εL² = 0.006% en 1D y 0.171% en 2D, ambos por debajo del umbral de tesis (< 5%).",
  ], { color: "bg1", headingColor: "bg1" });

  setSection(getShape(slide, "CuadroTexto 6"), "2. OBJETIVO.", [
    "Construir y validar un modelo PINN-SIREN que resuelva la ecuación de Helmholtz 2D con campo complejo y reproduzca patrones de speckle óptico con alta precisión.",
  ]);

  setSection(getShape(slide, "CuadroTexto 17"), "PROBLEMA FÍSICO.", [
    "El speckle óptico surge por la interferencia de luz coherente dispersada. Su simulación exige resolver campos oscilatorios con gran resolución espacial.",
    "Los métodos basados en malla pueden ser costosos para estudios con muchas realizaciones. Las PINNs imponen la EDP en puntos de colocación y SIREN representa mejor las oscilaciones.",
  ]);

  setSection(getShape(slide, "CuadroTexto 25"), "ALCANCE DEL ESTUDIO.", [
    "• Casos 1D y 2D; el desarrollo 3D queda fuera del alcance.",
    "• Dominio normalizado Ω = [0,1]², k = 2π y campo complejo en 2D.",
    "• Validación analítica mediante error L² y evaluación estadística del speckle.",
  ]);

  setSection(getShape(slide, "CuadroTexto 28"), "FORMULACIÓN.", [
    "Helmholtz: ∇²E + k²E = 0.",
    "1D: E(x) = cos(kx).  2D: E(x,y) = e^{i(kₓx + kᵧy)}.",
  ]);

  setSection(getShape(slide, "CuadroTexto 15"), "3. METODOLOGÍA.", [
    "1. NB01 — Validación 1D: SIREN 5 × 64 contra E(x) = cos(kx).",
    "2. NB02 — Validación 2D: SIREN 5 × 128, salida (Ereal, Eimag), LHS con Nc = 3,000 y Nb = 300 por borde.",
    "3. NB03 — Speckle 2D: frontera E(x,0) = e^{iψ(x)}, ψ ~ U(0, 2π), con bordes libres.",
    "Optimización bifásica Adam + L-BFGS; λfis = 0.1; evaluación en malla 100 × 100.",
    "Las figuras muestran la validación analítica 1D y la aplicación 2D al patrón de speckle.",
  ]);

  setSection(getShape(slide, "CuadroTexto 22"), "VALIDACIÓN 2D.", [
    "Onda plana compleja en Ω = [0,1]²; se comparan Ereal y Eimag con la solución analítica. La diferencia visual es mínima.",
  ]);

  setSection(getShape(slide, "CuadroTexto 3"), "4. RESULTADOS.", [
    "El modelo reproduce la solución analítica con alta precisión en 1D y en ambas componentes del campo complejo 2D.",
    "NB01 | εL² = 0.006% | R² = 1.000000.",
    "NB02 | εL² promedio = 0.171% | R² > 0.9999.",
    "La arquitectura 5 × 128 reduce el error 2.5× frente a 5 × 64; la variación entre semillas es 0.155 ± 0.020%.",
    "Speckle 2D: contraste C = 1.0253, consistente con speckle completamente desarrollado.",
  ]);

  setSection(getShape(slide, "CuadroTexto 46"), "5. CONCLUSIONES.", [
    "PINN-SIREN resuelve Helmholtz con precisión subporcentual: 0.006% en 1D y 0.171% en 2D.",
    "La representación sinusoidal, el muestreo LHS y Adam + L-BFGS favorecen la convergencia del campo complejo.",
    "La frontera de fase aleatoria produce speckle 2D con contraste C = 1.0253, conforme al criterio de Goodman.",
  ], { color: "bg1", headingColor: "bg1" });

  setSection(getShape(slide, "CuadroTexto 11"), "6. AGRADECIMIENTOS.", [
    "Agradecemos al Dr. José Adán Hernández Nolasco por la dirección de este trabajo y a la UJAT por el apoyo académico.",
  ]);

  setSection(getShape(slide, "CuadroTexto 21"), "7. FUENTES CITADAS.", [
    "[1] Raissi, M., Perdikaris, P. & Karniadakis, G. (2019). Physics-informed neural networks. Journal of Computational Physics.",
    "[2] Sitzmann, V. et al. (2020). Implicit neural representations with periodic activation functions. NeurIPS.",
    "[3] Goodman, J. W. (2007). Speckle Phenomena in Optics: Theory and Applications.",
    "[4] McKay, M. D., Beckman, R. J. & Conover, W. J. (1979). Latin hypercube sampling. Technometrics.",
  ], { bodySize: "42.67px", headingSize: "42.67px" });

  const frames = {
    "Rectángulo 32": { left: 0, top: 0, width: 3401.5, height: 530.61 },
    "Título 1": { left: 15.92, top: 30.93, width: 3385.58, height: 507.17 },
    "CuadroTexto 7": { left: 74.69, top: 634.06, width: 1011.82, height: 700 },
    "CuadroTexto 6": { left: 84.17, top: 1370, width: 1002.33, height: 280 },
    "CuadroTexto 17": { left: 74.69, top: 1710, width: 1002.33, height: 770 },
    "CuadroTexto 25": { left: 74.69, top: 3000, width: 1011.97, height: 720 },
    "CuadroTexto 28": { left: 1200.1, top: 634.13, width: 1017.22, height: 240 },
    "CuadroTexto 15": { left: 1200.1, top: 920, width: 1017.22, height: 760 },
    "CuadroTexto 22": { left: 2318.44, top: 629.73, width: 1022, height: 250 },
    "CuadroTexto 3": { left: 2327.66, top: 1600, width: 992.64, height: 780 },
    "CuadroTexto 46": { left: 2324.69, top: 3710, width: 976.86, height: 570 },
    "CuadroTexto 11": { left: 2330.83, top: 4320, width: 965.24, height: 270 },
    "CuadroTexto 21": { left: 72.87, top: 4646.01, width: 3190.86, height: 216.49 },
  };
  for (const [name, frame] of Object.entries(frames)) getShape(slide, name).frame = frame;
  getShape(slide, "Título 1").text.alignment = "center";
  getShape(slide, "Título 1").text.verticalAlignment = "middle";

  await replaceImage(getImage(slide, "Imagen 27"), path.join(thesisFigures, "resultados_pinn_1d.png"), "Validación PINN-SIREN 1D frente a la solución analítica");
  await replaceImage(getImage(slide, "Imagen 8"), path.join(thesisFigures, "metricas_adicionales_1d.png"), "Métricas adicionales de entrenamiento NB01");
  await replaceImage(getImage(slide, "Imagen 20"), path.join(thesisFigures, "resultados_pinn_2d.png"), "Validación PINN-SIREN 2D para el campo complejo");
  await replaceImage(getImage(slide, "Imagen 5"), path.join(thesisFigures, "metricas_adicionales_2d.png"), "Métricas adicionales y mapas de error NB02");
  await replaceImage(getImage(slide, "Imagen 23"), path.join(thesisFigures, "resultados_speckle_nb03.png"), "Patrón de speckle óptico simulado en 2D");
  await replaceImage(getImage(slide, "Imagen 33"), path.join(thesisFigures, "estadistica_speckle_nb03.png"), "Validación estadística del speckle óptico");
  const imageFrames = {
    "Imagen 27": { left: 1190, top: 1810, width: 1025, height: 490 },
    "Imagen 8": { left: 90, top: 2500, width: 980, height: 420 },
    "Imagen 20": { left: 2340, top: 920, width: 980, height: 610 },
    "Imagen 5": { left: 2340, top: 3150, width: 980, height: 520 },
    "Imagen 23": { left: 1190, top: 3000, width: 1025, height: 490 },
    "Imagen 33": { left: 2340, top: 2500, width: 980, height: 550 },
  };
  for (const [name, frame] of Object.entries(imageFrames)) getImage(slide, name).frame = frame;
  getImage(slide, "Imagen 30").delete();
  getImage(slide, "Imagen 2").delete();

  slide.speakerNotes.textFrame.setText([
    "Cartel adaptado de la tesis hasta el caso 2D. El desarrollo 3D no forma parte de este material.",
    "[Sources]",
    "- Tesis y resultados: C:/roberto/Tesis_Maestria/tesis/Tesis_Actual/main.pdf, chapters/Cap1-Generalidades.tex, chapters/Cap3-Modelo.tex, chapters/Cap4-Resultados.tex.",
    "- Figuras: C:/roberto/Tesis_Maestria/tesis/Tesis_Actual/figures/*.png.",
    "- Título, autores y datos del congreso: C:/Users/rober/Downloads/CNF LXIX-014674.pdf.",
    "- Estructura visual y logotipos: C:/roberto/Tesis_Maestria/master_supporting_docs/supporting_slides/CARTEL/GENERACIÓN DE SONIDO MEDIANTE EFECTO TERMOACÚSTICO EMPLEANDO ÓXIDO DE GRAFENO..pptx.",
    "[/Sources]",
  ]);
  slide.speakerNotes.setVisible(true);

  const previewDir = path.join(tmpDir, "final-preview");
  const layoutDir = path.join(tmpDir, "final-layout");
  await fs.mkdir(previewDir, { recursive: true });
  await fs.mkdir(layoutDir, { recursive: true });
  await writeBlob(path.join(previewDir, "slide-01.png"), await presentation.export({ slide, format: "png", scale: 1 }));
  await fs.writeFile(path.join(layoutDir, "slide-01.layout.json"), await (await slide.export({ format: "layout" })).text(), "utf8");
  await writeBlob(path.join(tmpDir, "final-montage.webp"), await presentation.export({ format: "webp", montage: true, scale: 1 }));
  await fs.writeFile(path.join(tmpDir, "final-inspect.ndjson"), (await presentation.inspect({ kind: "slide,textbox,shape,image,notes,layout", maxChars: 300000 })).ndjson || "", "utf8");

  await fs.mkdir(outputDir, { recursive: true });
  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(finalPptx);
  console.log(JSON.stringify({ finalPptx, preview: path.join(previewDir, "slide-01.png"), layout: path.join(layoutDir, "slide-01.layout.json") }, null, 2));
}

main().catch((error) => { console.error(error.stack || error.message || String(error)); process.exit(1); });
