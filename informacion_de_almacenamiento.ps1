Write-Host "-------------------------------------------"
Write-Host "SYSTEM DISK PARTITIONS"
Write-Host "-------------------------------------------"


$comando=Get-Partition | Select-Object -Property DriveLetter,Size,Type

foreach ($linea in $comando)
{
    Write-Host "Unidad: " $linea.DriveLetter "Tamaño de la unidad: " $linea.Size "Tipo de partición: " $linea.Type
}

Write-Host "-------------------------------------------"
Write-Host "LOCAL DISK STATUS"
Write-Host "-------------------------------------------"
$Estado=Get-Disk | Select-Object HealthStatus, PartitionStyle
$comando_local=Get-Partition | Where-Object DriveLetter -EQ C
foreach ($local in $comando_local)
{
    Write-Host "Disco: " $local.DriveLetter
    Write-Host "Estado del disco: " $Estado.HealthStatus
    Write-Host "Tamaño total del disco: " $local.Size
    Write-Host "Estilo de partición: " $Estado.PartitionStyle
}

Write-Host "-------------------------------------------"
Write-Host "SUMMARY"
Write-Host "-------------------------------------------"
Get-Volume