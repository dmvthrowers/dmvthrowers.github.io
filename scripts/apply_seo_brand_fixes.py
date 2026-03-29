import glob, re, os

html_files = glob.glob('*.html')

for path in html_files:
    text = open(path, encoding='utf-8').read()
    original = text

    # two key rel values for target blanks
    text = re.sub(r'target="_blank"\s+rel="noreferrer"', 'target="_blank" rel="noopener noreferrer"', text)
    text = re.sub(r'target="_blank"\s+rel="noopener noreferrer"', 'target="_blank" rel="noopener noreferrer"', text)
    text = re.sub(r'target="_blank"(?![^>]*rel=)', 'target="_blank" rel="noopener noreferrer"', text)

    # add og:image if missing and there is OG description
    if 'property="og:image"' not in text and 'property="og:description"' in text:
        text = re.sub(r'(property="og:description" content="[^"]*"/>)', r"\1\n  <meta property=\"og:image\" content=\"https://dmvthrowers.club/assets/images/logo.png\"/>\n  <meta property=\"og:site_name\" content=\"DMV Throwers\"/>\n  <meta name=\"twitter:card\" content=\"summary_large_image\"/>\n  <meta name=\"twitter:site\" content=\"@dmv_throwers\"/>", text)

    # enforce canonical starts with https (if exists)
    text = re.sub(r'<link rel="canonical" href="http://', '<link rel="canonical" href="https://', text)

    if text != original:
        open(path, 'w', encoding='utf-8').write(text)
        print(f"Updated {path}")

print('Done applying SEO/brand fixes.')
