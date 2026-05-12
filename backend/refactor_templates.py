import os
import re

template_dirs = [
    r'd:\database project\Residential Property Marketplace\Residential-Property-Marketplace\backend\templates',
    r'd:\database project\Residential Property Marketplace\Residential-Property-Marketplace\backend\templates\reports'
]

for template_dir in template_dirs:
    if not os.path.exists(template_dir):
        continue
    for file in os.listdir(template_dir):
        if file.endswith('.html') and file not in ['base.html', 'index.html']:
            filepath = os.path.join(template_dir, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Skip if already extending
            if '{% extends' in content:
                continue

            extracted = ""
            
            # Match <main> ... </main>
            main_match = re.search(r'(<main[^>]*>.*?</main>)', content, re.DOTALL | re.IGNORECASE)
            if main_match:
                extracted = main_match.group(1)
            else:
                # Match body
                body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
                if body_match:
                    extracted = body_match.group(1).strip()
                else:
                    # Just take the whole thing if no body found
                    extracted = content

            # Generate new file
            new_content = f"{{% extends 'base.html' %}}\n\n{{% block title %}}{file.replace('.html', '').title()}{{% endblock %}}\n\n{{% block content %}}\n{extracted}\n{{% endblock content %}}\n"

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

print('All templates refactored to use base.html!')
