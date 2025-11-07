Param(
  [string]$SpecUrl = "http://localhost:8000/openapi.json",
  [string]$OutDir = "healthcare_sdk"
)

npx --yes @openapitools/openapi-generator-cli generate `
  -i $SpecUrl `
  -g python `
  -o $OutDir

Write-Host "SDK generated at $OutDir"


