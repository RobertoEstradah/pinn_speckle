import fs from "node:fs/promises";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";

const { importRuntimeModule } = await import(pathToFileURL("C:/Users/rober/.codex/plugins/cache/openai-primary-runtime/presentations/26.826.12353/skills/Presentations/container_tools/runtime_helpers.mjs").href);

const workspaceDir = path.resolve(process.argv[2]);
const pptxPath = path.resolve(process.argv[3]);
const outDir = path.join(workspaceDir, "template-inspect");
const tarExe = "C:/Windows/System32/tar.exe";

function run(args, encoding = undefined) {
  const result = spawnSync(tarExe, args, { encoding, maxBuffer: 100 * 1024 * 1024 });
  if (result.status !== 0) throw new Error(`tar failed: ${args.join(" ")}\n${result.stderr || ""}`);
  return result.stdout;
}

async function writeBlob(filePath, blob) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, new Uint8Array(await blob.arrayBuffer()));
}

async function main() {
  const { FileBlob, PresentationFile } = await importRuntimeModule("@oai/artifact-tool");
  await fs.rm(outDir, { recursive: true, force: true });
  const slidesDir = path.join(outDir, "source-slides");
  const layoutsDir = path.join(outDir, "layouts");
  const mediaDir = path.join(outDir, "assets", "ppt", "media");
  await fs.mkdir(slidesDir, { recursive: true });
  await fs.mkdir(layoutsDir, { recursive: true });

  const presentation = await PresentationFile.importPptx(await FileBlob.load(pptxPath));
  const slides = presentation.slides.items;
  const names = String(run(["-tf", pptxPath], "utf8")).split(/\r?\n/).filter(Boolean);

  for (let index = 0; index < slides.length; index += 1) {
    const slideNumber = index + 1;
    const padded = String(slideNumber).padStart(2, "0");
    await writeBlob(path.join(slidesDir, `source-slide-${padded}.png`), await presentation.export({ slide: slides[index], format: "png", scale: 1 }));
    await writeBlob(path.join(layoutsDir, `source-slide-${padded}.layout.json`), await presentation.export({ slide: slides[index], format: "layout" }));
  }

  const extractedMedia = [];
  for (const entry of names.filter((name) => name.startsWith("ppt/media/"))) {
    const target = path.join(mediaDir, path.basename(entry));
    await fs.mkdir(path.dirname(target), { recursive: true });
    await fs.writeFile(target, run(["-xOf", pptxPath, entry]));
    extractedMedia.push({ entry, path: target, bytes: (await fs.stat(target)).size });
  }

  const inspect = await presentation.inspect({ kind: "slide,textbox,shape,image,table,chart,notes,layout", maxChars: 300000 });
  await fs.writeFile(path.join(outDir, "template-inspect.ndjson"), inspect.ndjson || "", "utf8");

  const fonts = new Set();
  for (const entry of names.filter((name) => /^(ppt\/(?:slides|slideMasters|slideLayouts|theme)\/.*\.xml|ppt\/theme\/.*\.xml)$/.test(name))) {
    const xml = run(["-xOf", pptxPath, entry], "utf8");
    for (const match of xml.matchAll(/\btypeface="([^"]+)"/g)) fonts.add(match[1]);
  }

  const manifest = {
    sourcePptx: pptxPath,
    workspace: workspaceDir,
    outDir,
    generatedAt: new Date().toISOString(),
    slideCount: slides.length,
    extractedMedia,
    fonts: [...fonts].sort(),
    packageParts: {
      mediaCount: names.filter((name) => name.startsWith("ppt/media/")).length,
      slideXmlCount: names.filter((name) => /^ppt\/slides\/slide\d+\.xml$/.test(name)).length,
      chartCount: names.filter((name) => /^ppt\/(?:charts|embeddings\/charts)\/chart\d+\.xml$/.test(name)).length,
      tableSlideCount: names.filter((name) => /^ppt\/slides\/slide\d+\.xml$/.test(name)).filter((name) => run(["-xOf", pptxPath, name], "utf8").includes("<a:tbl>")).length,
    },
  };
  await fs.writeFile(path.join(outDir, "template-manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  console.log(path.join(outDir, "template-manifest.json"));
}

main().catch((error) => { console.error(error.stack || error.message || String(error)); process.exit(1); });
