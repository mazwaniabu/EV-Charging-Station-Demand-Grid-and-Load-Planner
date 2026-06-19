# PowerShell script to verify the raw CSV dataset structures locally

$CarsPath = "data/raw/cars_2026.csv"
$StationsPath = "data/raw/charging_station.csv"

$ExpectedCarsColumns = "date_reg,type,maker,model,colour,fuel,state"
$ExpectedStationsColumns = "id,name,city,state_province,country_code,latitude,longitude,ports,power_kw,power_class,is_fast_dc"

Write-Host "Verifying raw datasets structure via PowerShell..." -ForegroundColor Cyan

# 1. Verify cars_2026.csv
if (Test-Path $CarsPath) {
    $CarsHeader = (Get-Content $CarsPath -First 1).Trim()
    if ($CarsHeader -eq $ExpectedCarsColumns) {
        $CarsCount = (Get-Content $CarsPath | Measure-Object -Line).Lines - 1
        Write-Host "[OK] '$CarsPath' is valid. Found $CarsCount records." -ForegroundColor Green
        $CarsOk = $true
    } else {
        Write-Host "[FAIL] '$CarsPath' schema mismatch!" -ForegroundColor Red
        Write-Host "  Expected: $ExpectedCarsColumns" -ForegroundColor Yellow
        Write-Host "  Found:    $CarsHeader" -ForegroundColor Yellow
        $CarsOk = $false
    }
} else {
    Write-Host "[FAIL] '$CarsPath' does not exist." -ForegroundColor Red
    $CarsOk = $false
}

# 2. Verify charging_station.csv
if (Test-Path $StationsPath) {
    $StationsHeader = (Get-Content $StationsPath -First 1).Trim()
    if ($StationsHeader -eq $ExpectedStationsColumns) {
        $StationsCount = (Get-Content $StationsPath | Measure-Object -Line).Lines - 1
        Write-Host "[OK] '$StationsPath' is valid. Found $StationsCount records." -ForegroundColor Green
        $StationsOk = $true
    } else {
        Write-Host "[FAIL] '$StationsPath' schema mismatch!" -ForegroundColor Red
        Write-Host "  Expected: $ExpectedStationsColumns" -ForegroundColor Yellow
        Write-Host "  Found:    $StationsHeader" -ForegroundColor Yellow
        $StationsOk = $false
    }
} else {
    Write-Host "[FAIL] '$StationsPath' does not exist." -ForegroundColor Red
    $StationsOk = $false
}

if ($CarsOk -and $StationsOk) {
    Write-Host "All raw datasets verified successfully!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "Verification failed." -ForegroundColor Red
    exit 1
}
