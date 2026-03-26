@echo off
echo Moving DMV Throwers website files to organized structure...
echo.

REM Create directories if they don't exist
if not exist "assets\images" mkdir "assets\images"
if not exist "assets\images\events" mkdir "assets\images\events"
if not exist "assets\images\gallery" mkdir "assets\images\gallery"
if not exist "assets\images\logos" mkdir "assets\images\logos"
if not exist "assets\documents" mkdir "assets\documents"

echo Created directories.

REM Move main logo
if exist "logo.png" (
    move "logo.png" "assets\images\" >nul 2>&1
    if %errorlevel% equ 0 (
        echo Moved logo.png to assets\images\
    ) else (
        echo Failed to move logo.png
    )
)

REM Move Ko-fi banner
if exist "DMV Throwers Kofi Banner.png" (
    move "DMV Throwers Kofi Banner.png" "assets\images\" >nul 2>&1
    if %errorlevel% equ 0 (
        echo Moved DMV Throwers Kofi Banner.png to assets\images\
    ) else (
        echo Failed to move DMV Throwers Kofi Banner.png
    )
)

REM Move event images
if exist "DMV Throwers April 2026.png" move "DMV Throwers April 2026.png" "assets\images\events\" >nul 2>&1 && echo Moved DMV Throwers April 2026.png to assets\images\events\ || echo Failed to move DMV Throwers April 2026.png
if exist "DMV Throwers May 2026.png" move "DMV Throwers May 2026.png" "assets\images\events\" >nul 2>&1 && echo Moved DMV Throwers May 2026.png to assets\images\events\ || echo Failed to move DMV Throwers May 2026.png
if exist "DMV Throwers June 2026.png" move "DMV Throwers June 2026.png" "assets\images\events\" >nul 2>&1 && echo Moved DMV Throwers June 2026.png to assets\images\events\ || echo Failed to move DMV Throwers June 2026.png
if exist "DMV Throwers July 2026.png" move "DMV Throwers July 2026.png" "assets\images\events\" >nul 2>&1 && echo Moved DMV Throwers July 2026.png to assets\images\events\ || echo Failed to move DMV Throwers July 2026.png
if exist "DMV Throwers August 2026.png" move "DMV Throwers August 2026.png" "assets\images\events\" >nul 2>&1 && echo Moved DMV Throwers August 2026.png to assets\images\events\ || echo Failed to move DMV Throwers August 2026.png
if exist "DMV Throwers September 2026.png" move "DMV Throwers September 2026.png" "assets\images\events\" >nul 2>&1 && echo Moved DMV Throwers September 2026.png to assets\images\events\ || echo Failed to move DMV Throwers September 2026.png
if exist "DMV Throwers October 2026.png" move "DMV Throwers October 2026.png" "assets\images\events\" >nul 2>&1 && echo Moved DMV Throwers October 2026.png to assets\images\events\ || echo Failed to move DMV Throwers October 2026.png
if exist "DMV Throwers November 2026.png" move "DMV Throwers November 2026.png" "assets\images\events\" >nul 2>&1 && echo Moved DMV Throwers November 2026.png to assets\images\events\ || echo Failed to move DMV Throwers November 2026.png
if exist "DMV Throwers December 2026.png" move "DMV Throwers December 2026.png" "assets\images\events\" >nul 2>&1 && echo Moved DMV Throwers December 2026.png to assets\images\events\ || echo Failed to move DMV Throwers December 2026.png

REM Move gallery images
if exist "club.PNG" move "club.PNG" "assets\images\gallery\" >nul 2>&1 && echo Moved club.PNG to assets\images\gallery\ || echo Failed to move club.PNG
if exist "club10.PNG" move "club10.PNG" "assets\images\gallery\" >nul 2>&1 && echo Moved club10.PNG to assets\images\gallery\ || echo Failed to move club10.PNG
if exist "club12.PNG" move "club12.PNG" "assets\images\gallery\" >nul 2>&1 && echo Moved club12.PNG to assets\images\gallery\ || echo Failed to move club12.PNG
if exist "club3.PNG" move "club3.PNG" "assets\images\gallery\" >nul 2>&1 && echo Moved club3.PNG to assets\images\gallery\ || echo Failed to move club3.PNG
if exist "club4.PNG" move "club4.PNG" "assets\images\gallery\" >nul 2>&1 && echo Moved club4.PNG to assets\images\gallery\ || echo Failed to move club4.PNG
if exist "club5.PNG" move "club5.PNG" "assets\images\gallery\" >nul 2>&1 && echo Moved club5.PNG to assets\images\gallery\ || echo Failed to move club5.PNG
if exist "club6.PNG" move "club6.PNG" "assets\images\gallery\" >nul 2>&1 && echo Moved club6.PNG to assets\images\gallery\ || echo Failed to move club6.PNG
if exist "club7.PNG" move "club7.PNG" "assets\images\gallery\" >nul 2>&1 && echo Moved club7.PNG to assets\images\gallery\ || echo Failed to move club7.PNG
if exist "club9.PNG" move "club9.PNG" "assets\images\gallery\" >nul 2>&1 && echo Moved club9.PNG to assets\images\gallery\ || echo Failed to move club9.PNG
if exist "IMG_4713.jpeg" move "IMG_4713.jpeg" "assets\images\gallery\" >nul 2>&1 && echo Moved IMG_4713.jpeg to assets\images\gallery\ || echo Failed to move IMG_4713.jpeg

REM Move logo variants
if exist "DMVT_Logo_10x10.jpeg" move "DMVT_Logo_10x10.jpeg" "assets\images\logos\" >nul 2>&1 && echo Moved DMVT_Logo_10x10.jpeg to assets\images\logos\ || echo Failed to move DMVT_Logo_10x10.jpeg
if exist "DMVT_Logo_3x3.jpeg" move "DMVT_Logo_3x3.jpeg" "assets\images\logos\" >nul 2>&1 && echo Moved DMVT_Logo_3x3.jpeg to assets\images\logos\ || echo Failed to move DMVT_Logo_3x3.jpeg
if exist "DMVT_Logo_Glyph b&W.png" move "DMVT_Logo_Glyph b&W.png" "assets\images\logos\" >nul 2>&1 && echo Moved "DMVT_Logo_Glyph b&W.png" to assets\images\logos\ || echo Failed to move DMVT_Logo_Glyph b&W.png
if exist "DMVT_Logo_Glyph.jpg" move "DMVT_Logo_Glyph.jpg" "assets\images\logos\" >nul 2>&1 && echo Moved DMVT_Logo_Glyph.jpg to assets\images\logos\ || echo Failed to move DMVT_Logo_Glyph.jpg
if exist "DMVT_Logo_LargePrint.ps" move "DMVT_Logo_LargePrint.ps" "assets\images\logos\" >nul 2>&1 && echo Moved DMVT_Logo_LargePrint.ps to assets\images\logos\ || echo Failed to move DMVT_Logo_LargePrint.ps
if exist "DMVT_Logo_wText.jpeg" move "DMVT_Logo_wText.jpeg" "assets\images\logos\" >nul 2>&1 && echo Moved DMVT_Logo_wText.jpeg to assets\images\logos\ || echo Failed to move DMVT_Logo_wText.jpeg
if exist "VAStateLogo_Final.png" move "VAStateLogo_Final.png" "assets\images\logos\" >nul 2>&1 && echo Moved VAStateLogo_Final.png to assets\images\logos\ || echo Failed to move VAStateLogo_Final.png
if exist "VAStateLogo_Final.svg" move "VAStateLogo_Final.svg" "assets\images\logos\" >nul 2>&1 && echo Moved VAStateLogo_Final.svg to assets\images\logos\ || echo Failed to move VAStateLogo_Final.svg
if exist "vastateyoyocontest.png" move "vastateyoyocontest.png" "assets\images\logos\" >nul 2>&1 && echo Moved vastateyoyocontest.png to assets\images\logos\ || echo Failed to move vastateyoyocontest.png

REM Move documents
if exist "DMV Throwers Charter v5.docx" move "DMV Throwers Charter v5.docx" "assets\documents\" >nul 2>&1 && echo Moved DMV Throwers Charter v5.docx to assets\documents\ || echo Failed to move DMV Throwers Charter v5.docx
if exist "DMV Throwers Club Display Loop.pptx" move "DMV Throwers Club Display Loop.pptx" "assets\documents\" >nul 2>&1 && echo Moved DMV Throwers Club Display Loop.pptx to assets\documents\ || echo Failed to move DMV Throwers Club Display Loop.pptx
if exist "DMV Throwers Event Checklist.docx" move "DMV Throwers Event Checklist.docx" "assets\documents\" >nul 2>&1 && echo Moved DMV Throwers Event Checklist.docx to assets\documents\ || echo Failed to move DMV Throwers Event Checklist.docx
if exist "DMV Throwers FAQ.docx" move "DMV Throwers FAQ.docx" "assets\documents\" >nul 2>&1 && echo Moved DMV Throwers FAQ.docx to assets\documents\ || echo Failed to move DMV Throwers FAQ.docx
if exist "DMV Throwers Maintenance Guide 2.pptx" move "DMV Throwers Maintenance Guide 2.pptx" "assets\documents\" >nul 2>&1 && echo Moved DMV Throwers Maintenance Guide 2.pptx to assets\documents\ || echo Failed to move DMV Throwers Maintenance Guide 2.pptx
if exist "DMV Throwers Officer Roles.docx" move "DMV Throwers Officer Roles.docx" "assets\documents\" >nul 2>&1 && echo Moved DMV Throwers Officer Roles.docx to assets\documents\ || echo Failed to move DMV Throwers Officer Roles.docx
if exist "DMV Throwers Press Kit.pdf" move "DMV Throwers Press Kit.pdf" "assets\documents\" >nul 2>&1 && echo Moved DMV Throwers Press Kit.pdf to assets\documents\ || echo Failed to move DMV Throwers Press Kit.pdf
if exist "DMV Throwers Trick Reference Guide.pptx" move "DMV Throwers Trick Reference Guide.pptx" "assets\documents\" >nul 2>&1 && echo Moved DMV Throwers Trick Reference Guide.pptx to assets\documents\ || echo Failed to move DMV Throwers Trick Reference Guide.pptx
if exist "DMV Throwers Workshop Run Sheet.docx" move "DMV Throwers Workshop Run Sheet.docx" "assets\documents\" >nul 2>&1 && echo Moved DMV Throwers Workshop Run Sheet.docx to assets\documents\ || echo Failed to move DMV Throwers Workshop Run Sheet.docx
if exist "VSYC26 Industry Pitch v4.pdf" move "VSYC26 Industry Pitch v4.pdf" "assets\documents\" >nul 2>&1 && echo Moved VSYC26 Industry Pitch v4.pdf to assets\documents\ || echo Failed to move VSYC26 Industry Pitch v4.pdf
if exist "VSYC26 Local Pitch v4.pdf" move "VSYC26 Local Pitch v4.pdf" "assets\documents\" >nul 2>&1 && echo Moved VSYC26 Local Pitch v4.pdf to assets\documents\ || echo Failed to move VSYC26 Local Pitch v4.pdf
if exist "VSYC26 Sponsor Package v26g.pdf" move "VSYC26 Sponsor Package v26g.pdf" "assets\documents\" >nul 2>&1 && echo Moved VSYC26 Sponsor Package v26g.pdf to assets\documents\ || echo Failed to move VSYC26 Sponsor Package v26g.pdf
if exist "Yoyo Club slides to share.pdf" move "Yoyo Club slides to share.pdf" "assets\documents\" >nul 2>&1 && echo Moved Yoyo Club slides to share.pdf to assets\documents\ || echo Failed to move Yoyo Club slides to share.pdf
if exist "Yoyo Maintenence .pdf" move "Yoyo Maintenence .pdf" "assets\documents\" >nul 2>&1 && echo Moved "Yoyo Maintenence .pdf" to assets\documents\ || echo Failed to move Yoyo Maintenence .pdf

echo.
echo File organization complete!
echo Check the output above for any files that failed to move.
pause