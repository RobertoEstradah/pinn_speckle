# 📋 Guía de configuración del repositorio

## Comandos para crear el repositorio en tu laptop

### Paso 1 — Crear la carpeta local

```bash
# En tu terminal (PowerShell o Git Bash)
cd C:\Users\TU_USUARIO\Documents
mkdir pinn_speckle
cd pinn_speckle
```

### Paso 2 — Inicializar Git

```bash
git init
git branch -M main
```

### Paso 3 — Copiar los archivos de este repo

Copia todos los archivos descargados dentro de la carpeta `pinn_speckle/`.

### Paso 4 — Primer commit

```bash
git add .
git commit -m "feat: estructura inicial del proyecto PINN Speckle"
```

### Paso 5 — Conectar con GitHub

```bash
# Reemplaza TU_USUARIO con tu nombre de GitHub
git remote add origin https://github.com/TU_USUARIO/pinn_speckle.git
git push -u origin main
```

---

## Comandos Git para uso diario

```bash
# Ver estado de cambios
git status

# Agregar cambios
git add notebooks/01_teoria_pinns.ipynb

# Hacer commit con mensaje descriptivo
git commit -m "feat: notebook 01 - error L2 = 0.002%"

# Subir a GitHub
git push

# Descargar cambios de GitHub
git pull
```

## Convención de mensajes de commit

```
feat:  nueva funcionalidad       → feat: notebook 02 helmholtz 2D
fix:   corrección de bug         → fix: corregir lambda comentario CONFIG
docs:  documentación             → docs: actualizar README con resultados
exp:   experimento nuevo         → exp: probar lambda_phys=0.001
res:   resultados obtenidos      → res: error L2 0.002% notebook 01
```
