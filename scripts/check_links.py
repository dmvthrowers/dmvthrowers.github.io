import re, glob, os
files = glob.glob('*.html')
print('files', files)
problems = []
for f in files:
    text = open(f, encoding='utf-8').read()
    for m in re.finditer(r'href=["\']([^"\']+)["\']', text):
        href = m.group(1)
        if href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:') or href.startswith('http'):
            continue
        if href.startswith('/'):
            path = href.lstrip('/')
        else:
            path = os.path.normpath(os.path.join(os.path.dirname(f), href))
        path = path.split('?', 1)[0].split('#', 1)[0]
        if not os.path.exists(path):
            problems.append((f, href, path))
print('broken', len(problems))
for p in problems:
    print(p)