import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all font-size: 1.2rem with 1.8rem in paragraph tags
content = re.sub(r'(<p[^>]*font-size:\s*)1\.2rem', r'\g<1>1.8rem', content)
content = re.sub(r'(<p[^>]*font-size:\s*)1\.3rem', r'\g<1>1.8rem', content)
content = re.sub(r'(<p[^>]*font-size:\s*)1\.1rem', r'\g<1>1.8rem', content)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated all paragraph font sizes to 1.8rem')
