param(
    [string]$Python = "python",
    [int[]]$ScreenSeeds = @(42, 123, 321, 777, 2026),
    [switch]$Overwrite
)

$ErrorActionPreference = "Stop"
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location -LiteralPath $projectRoot

function Invoke-PythonExperiment {
    param(
        [string]$Script,
        [string]$ExpectedOutput
    )
    if ((Test-Path -LiteralPath $ExpectedOutput) -and -not $Overwrite) {
        Write-Host "Reutilizando: $ExpectedOutput"
        return
    }
    & $Python -u $Script
    if ($LASTEXITCODE -ne 0) {
        throw "Fallo el experimento $Script con codigo $LASTEXITCODE."
    }
}

foreach ($screenSeed in $ScreenSeeds) {
    if ($screenSeed -eq 42) {
        $referenceSuffix = "_z1_corr0.10"
        $initialSuffix = "_z1_modal_scaled1"
        $finalSuffix = "_z1_modal_scaled1_finetune"
    }
    else {
        $referenceSuffix = "_z1_seed${screenSeed}_corr0.10"
        $initialSuffix = "_z1_screen${screenSeed}_scaled1"
        $finalSuffix = "_z1_screen${screenSeed}_scaled1_finetune"
    }

    Write-Host "Pantalla fisica $screenSeed"
    $env:NB03_REFERENCE_SEED = [string]$screenSeed
    $env:NB03_DISTANCE_LAMBDA = "1"
    $env:NB03_TARGET_Z_LAMBDA = "1"
    $env:NB03_REFERENCE_N_Z = "101"
    $env:NB03_REFERENCE_N_REALIZATIONS = "64"
    $env:NB03_PHASE_CORRELATION_LAMBDA = "0.10"
    $env:NB03_PHASE_STD_RAD = "2.0"
    $env:NB03_REFERENCE_SUFFIX = $referenceSuffix

    $referenceJson = Join-Path $projectRoot (
        "results\nb03_angular_spectrum_reference${referenceSuffix}.json"
    )
    Invoke-PythonExperiment `
        -Script "scripts/experiments/nb03_angular_spectrum_reference.py" `
        -ExpectedOutput $referenceJson

    $env:NB03_SEED = "42"
    $env:NB03_MODAL_EPOCHS = "5000"
    $env:NB03_MODAL_N_Z_TRAIN = "256"
    $env:NB03_MODAL_LR = "0.0002"
    $env:NB03_MODAL_FIRST_OMEGA = "30"
    $env:NB03_MODAL_HIDDEN_OMEGA = "1"
    $env:NB03_MODAL_HIDDEN_DIM = "128"
    $env:NB03_MODAL_NUM_LAYERS = "4"
    $env:NB03_MODAL_GRAD_CLIP = "1"
    $env:NB03_MODAL_VALIDATION_N_Z = "1001"
    $env:NB03_MODAL_RESUME_MODEL = ""
    $env:NB03_MODAL_OUTPUT_SUFFIX = $initialSuffix

    $initialModel = Join-Path $projectRoot (
        "results\models\nb03_modal_pinn_siren${initialSuffix}.pt"
    )
    Invoke-PythonExperiment `
        -Script "scripts/experiments/nb03_modal_pinn_siren.py" `
        -ExpectedOutput $initialModel

    $env:NB03_MODAL_EPOCHS = "3000"
    $env:NB03_MODAL_LR = "0.00005"
    $env:NB03_MODAL_RESUME_MODEL = (
        "results/models/nb03_modal_pinn_siren${initialSuffix}.pt"
    )
    $env:NB03_MODAL_OUTPUT_SUFFIX = $finalSuffix

    $finalModel = Join-Path $projectRoot (
        "results\models\nb03_modal_pinn_siren${finalSuffix}.pt"
    )
    Invoke-PythonExperiment `
        -Script "scripts/experiments/nb03_modal_pinn_siren.py" `
        -ExpectedOutput $finalModel
}

$requiredSeeds = @(42, 123, 321, 777, 2026)
$hasAllScreens = @($requiredSeeds | Where-Object {
    $ScreenSeeds -notcontains $_
}).Count -eq 0

if ($hasAllScreens) {
    & $Python -u "scripts/experiments/nb03_modal_multiseed_summary.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Fallo la consolidacion multisemilla."
    }
}
else {
    Write-Host "Consolidacion omitida: requiere las cinco semillas estandar."
}

Write-Host "Protocolo NB03 completado."
