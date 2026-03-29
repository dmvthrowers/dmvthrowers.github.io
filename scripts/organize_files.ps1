# PowerShell script to organize DMV Throwers website files
# Run this script from the root directory of the website

Write-Host "Organizing DMV Throwers website files..."

# Create directories if they don't exist
$directories = @(
    "assets\images",
    "assets\images\events",
    "assets\images\gallery",
    "assets\images\logos",
    "assets\documents"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
        Write-Host "Created directory: $dir"
    }
}

# Move main logo
if (Test-Path "logo.png") {
    Move-Item "logo.png" "assets\images\" -Force
    Write-Host "Moved logo.png to assets\images\"
}

# Move Ko-fi banner
if (Test-Path "DMV Throwers Kofi Banner.png") {
    Move-Item "DMV Throwers Kofi Banner.png" "assets\images\" -Force
    Write-Host "Moved DMV Throwers Kofi Banner.png to assets\images\"
}

# Move event images
$eventImages = @(
    "DMV Throwers April 2026.png",
    "DMV Throwers May 2026.png",
    "DMV Throwers June 2026.png",
    "DMV Throwers July 2026.png",
    "DMV Throwers August 2026.png",
    "DMV Throwers September 2026.png",
    "DMV Throwers October 2026.png",
    "DMV Throwers November 2026.png",
    "DMV Throwers December 2026.png"
)

foreach ($image in $eventImages) {
    if (Test-Path $image) {
        Move-Item $image "assets\images\events\" -Force
        Write-Host "Moved $image to assets\images\events\"
    }
}

# Move gallery images
$galleryImages = @(
    "DMV Throwers Club.png",
    "DMV Throwers Logo.png",
    "DMV Throwers Logo White.png",
    "DMV Throwers Logo Black.png",
    "DMV Throwers Logo Red.png",
    "DMV Throwers Logo Navy.png",
    "DMV Throwers Logo Cream.png",
    "DMV Throwers Logo Transparent.png",
    "DMV Throwers Logo Square.png"
)

foreach ($image in $galleryImages) {
    if (Test-Path $image) {
        Move-Item $image "assets\images\gallery\" -Force
        Write-Host "Moved $image to assets\images\gallery\"
    }
}

# Move logo variants
$logoVariants = @(
    "DMVT_Logo_10x10.jpeg",
    "DMVT_Logo_3x3.jpeg",
    "DMVT_Logo_Glyph b&W.png",
    "DMVT_Logo_Glyph.jpg",
    "DMVT_Logo_LargePrint.ps",
    "DMVT_Logo_wText.jpeg",
    "VAStateLogo_Final.png",
    "VAStateLogo_Final.svg",
    "vastateyoyocontest.png"
)

foreach ($logo in $logoVariants) {
    if (Test-Path $logo) {
        Move-Item $logo "assets\images\logos\" -Force
        Write-Host "Moved $logo to assets\images\logos\"
    }
}

# Move club photos
$clubPhotos = Get-ChildItem "club*.PNG" -File
foreach ($photo in $clubPhotos) {
    Move-Item $photo.FullName "assets\images\gallery\" -Force
    Write-Host "Moved $($photo.Name) to assets\images\gallery\"
}

# Move other images
$otherImages = @(
    "IMG_4713.jpeg"
)

foreach ($image in $otherImages) {
    if (Test-Path $image) {
        Move-Item $image "assets\images\" -Force
        Write-Host "Moved $image to assets\images\"
    }
}

# Move documents
$documents = @(
    "DMV Throwers Charter v5.docx",
    "DMV Throwers Event Checklist.docx",
    "DMV Throwers FAQ.docx",
    "DMV Throwers Officer Roles.docx",
    "DMV Throwers Workshop Run Sheet.docx",
    "DMV Throwers Press Kit.pdf",
    "DMV Throwers Maintenance Guide 2.pptx",
    "DMV Throwers Trick Reference Guide.pptx",
    "VSYC26 Industry Pitch v4.pdf",
    "VSYC26 Local Pitch v4.pdf",
    "VSYC26 Sponsor Package v26g.pdf",
    "Yoyo Club slides to share.pdf",
    "Yoyo Maintenence .pdf"
)

foreach ($doc in $documents) {
    if (Test-Path $doc) {
        Move-Item $doc "assets\documents\" -Force
        Write-Host "Moved $doc to assets\documents\"
    }
}

Write-Host "File organization complete!"
Write-Host "Please verify that all HTML pages still load correctly."