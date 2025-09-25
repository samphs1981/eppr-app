# Set the root project directory name
$root = "eppr_app"

# Define the folder structure as a hash table
$folders = @{
    "db"       = @("migrations")
    "ui"       = @("screens", "widgets", "styles")
    "models"   = @("schemas")
    "services" = @("db_ops", "validators")
    "assets"   = @("icons", "images", "docs")
    "tests"    = @("db_tests", "ui_tests")
}

# --- Script Execution ---

# Create the root directory if it doesn't exist
if (-not (Test-Path -Path $root)) {
    Write-Host "Creating root directory: $root"
    New-Item -ItemType Directory -Path $root | Out-Null
}

# Change directory into the root folder
Set-Location -Path $root

# Create all the subfolders
foreach ($folder in $folders.Keys) {
    # Create the main subfolder (e.g., 'db', 'ui')
    Write-Host "Creating folder: $folder"
    New-Item -ItemType Directory -Path $folder -Force | Out-Null
    
    # Create the nested folders within it (e.g., 'migrations')
    foreach ($sub in $folders[$folder]) {
        $subPath = Join-Path $folder $sub
        Write-Host "Creating subfolder: $subPath"
        New-Item -ItemType Directory -Path $subPath -Force | Out-Null
    }
}

Write-Host "Folder structure for '$root' created successfully!"
# To return to the parent directory after running
Set-Location ..
