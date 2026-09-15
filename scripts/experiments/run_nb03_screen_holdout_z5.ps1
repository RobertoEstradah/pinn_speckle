param(
    [int]$ThreadsPerRun = 2
)

$ErrorActionPreference = "Stop"
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$pythonExe = "C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$experiment = Join-Path $projectRoot "scripts\experiments\nb03_adaptive_slabs.py"
$resultsRoot = Join-Path $projectRoot "results\nb03_distance_pilot"
$logRoot = Join-Path $resultsRoot "batch_z5_multiscreen_logs"
New-Item -ItemType Directory -Path $logRoot -Force | Out-Null

$runs = @(
    @{
        Seed = 42
        Suffix = "_z1_corr0.10"
        Model = "results\nb03_refinement\pilot1\seed42_lbfgs32.pt"
        Resume = "results\nb03_distance_pilot\z2_screen42_net42_adaptive_slabs_v1"
    },
    @{
        Seed = 123
        Suffix = "_z1_seed123_corr0.10"
        Model = "results\nb03_refinement\pilot1\seed123_lbfgs32.pt"
        Resume = ""
    },
    @{
        Seed = 321
        Suffix = "_z1_seed321_corr0.10"
        Model = "results\nb03_refinement\confirmation3\seed321_lbfgs32.pt"
        Resume = ""
    },
    @{
        Seed = 777
        Suffix = "_z1_seed777_corr0.10"
        Model = "results\nb03_refinement\confirmation3\seed777_lbfgs32.pt"
        Resume = ""
    },
    @{
        Seed = 2026
        Suffix = "_z1_seed2026_corr0.10"
        Model = "results\nb03_refinement\confirmation3\seed2026_lbfgs32.pt"
        Resume = ""
    }
)

$processes = @()
foreach ($run in $runs) {
    $name = "z5_screen$($run.Seed)_net42_adaptive_slabs_v1"
    $summary = Join-Path (Join-Path $resultsRoot $name) "summary.json"
    if (Test-Path -LiteralPath $summary) {
        Write-Host "OMITIDA pantalla $($run.Seed): ya existe $summary"
        continue
    }
    $arguments = @(
        "-u", ('"' + $experiment + '"'),
        "--reference-suffix", $run.Suffix,
        "--first-model", $run.Model,
        "--screen-seed", "$($run.Seed)",
        "--network-seed", "42",
        "--target-distance", "5",
        "--adam-seconds", "60",
        "--lbfgs-seconds", "120",
        "--threads", "$ThreadsPerRun",
        "--name", $name
    )
    if ($run.Resume) {
        $arguments += @("--resume-dir", $run.Resume)
    }
    $stdout = Join-Path $logRoot "screen$($run.Seed).out.log"
    $stderr = Join-Path $logRoot "screen$($run.Seed).err.log"
    $process = Start-Process -FilePath $pythonExe -ArgumentList $arguments `
        -WorkingDirectory $projectRoot -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput $stdout -RedirectStandardError $stderr
    $processes += [pscustomobject]@{
        Seed = $run.Seed
        Process = $process
        Stdout = $stdout
        Stderr = $stderr
    }
    Write-Host "INICIADA pantalla $($run.Seed), PID $($process.Id)"
}

foreach ($item in $processes) {
    $item.Process.WaitForExit()
    $item.Process.Refresh()
    Write-Host "FINAL pantalla $($item.Seed), codigo $($item.Process.ExitCode)"
    if ($item.Process.ExitCode -ne 0) {
        Get-Content -LiteralPath $item.Stderr -Tail 30
        throw "Fallo la pantalla $($item.Seed)."
    }
    Get-Content -LiteralPath $item.Stdout -Tail 3
}
