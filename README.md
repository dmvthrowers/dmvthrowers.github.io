# dmvthrowers.github.io
DMV throwers yoyo and skill toy club: the premier DC area skill and flow based events and activities club

## File Structure

```
/ (root)
├── index.html              # Homepage
├── about.html              # About page
├── events.html             # Events page
├── gallery.html            # Gallery page
├── resources.html          # Resources page
├── contact.html            # Contact page
├── faq.html                # FAQ page
├── vsyc26.html             # VSYC-26 contest page
├── CNAME                   # GitHub Pages domain
├── README.md               # This file
├── organize_files.ps1      # File organization script
└── assets/
    ├── images/
    │   ├── logo.png                    # Main logo
    │   ├── DMV Throwers Kofi Banner.png # Donation banner
    │   ├── IMG_4713.jpeg              # Miscellaneous image
    │   ├── events/                    # Monthly event images
    │   │   ├── DMV Throwers April 2026.png
    │   │   ├── DMV Throwers May 2026.png
    │   │   └── ... (other monthly images)
    │   ├── gallery/                   # Gallery images
    │   │   ├── club*.PNG              # Club photos
    │   │   ├── DMV Throwers Club.png
    │   │   └── ... (logo variants)
    │   └── logos/                     # Logo variants and state logos
    │       ├── DMVT_Logo_*.jpeg/png   # Logo variants
    │       ├── VAStateLogo_Final.*    # State logos
    │       └── vastateyoyocontest.png
    └── documents/                     # PDFs, docs, presentations
        ├── DMV Throwers Charter v5.docx
        ├── DMV Throwers Event Checklist.docx
        ├── DMV Throwers FAQ.docx
        ├── DMV Throwers Officer Roles.docx
        ├── DMV Throwers Workshop Run Sheet.docx
        ├── DMV Throwers Press Kit.pdf
        ├── DMV Throwers Maintenance Guide 2.pptx
        ├── DMV Throwers Trick Reference Guide.pptx
        ├── VSYC26 Industry Pitch v4.pdf
        ├── VSYC26 Local Pitch v4.pdf
        ├── VSYC26 Sponsor Package v26g.pdf
        ├── Yoyo Club slides to share.pdf
        └── Yoyo Maintenence .pdf
```

## Setup

1. Clone the repository
2. Run the organization script: `.\organize_files.ps1`
3. The script will create the proper directory structure and move files
4. Verify that all pages load correctly

## Development

- HTML pages are in the root directory
- All assets (images, documents) are organized in the `/assets/` folder
- Use relative paths like `assets/images/logo.png` in HTML files
