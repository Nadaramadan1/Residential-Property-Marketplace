import os

template_dir = r'd:\database project\Residential Property Marketplace\Residential-Property-Marketplace\backend\templates'

mappings = {
    'href="/home/"': 'href="{% url \'home\' %}"',
    'href="/dashboard/"': 'href="{% url \'admin_dashboard\' %}"',
    'href="/agreement/"': 'href="{% url \'legal_agreement\' %}"',
    'href="/property-details/"': 'href="{% url \'property_details\' %}"',
    'href="/property-listing/"': 'href="{% url \'property_listing\' %}"',
    'href="/property-manager/"': 'href="{% url \'property_manager\' %}"',
    'href="/reports/"': 'href="{% url \'reports\' %}"',
    'href="/start/"': 'href="{% url \'start\' %}"',
    'href="/tour-scheduling/"': 'href="{% url \'tour_scheduling\' %}"',
    'href="/profile/"': 'href="{% url \'user_rep_profile\' %}"',
    'href="/"': 'href="{% url \'index\' %}"',
}

for root, _, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Replace hrefs
            for old_url, new_url in mappings.items():
                content = content.replace(old_url, new_url)
                
            # Replace pagination buttons in propertyListing.html to use anchors
            if file == 'propertyListing.html':
                content = content.replace('<button class="w-10 h-10 flex items-center justify-center rounded-lg bg-primary-container text-on-primary font-bold">1</button>', '<a href="?page=1" class="w-10 h-10 flex items-center justify-center rounded-lg bg-primary-container text-on-primary font-bold">1</a>')
                content = content.replace('<button class="w-10 h-10 flex items-center justify-center rounded-lg border border-outline-variant hover:bg-surface-container transition-colors font-bold">2</button>', '<a href="?page=2" class="w-10 h-10 flex items-center justify-center rounded-lg border border-outline-variant hover:bg-surface-container transition-colors font-bold">2</a>')
                content = content.replace('<button class="w-10 h-10 flex items-center justify-center rounded-lg border border-outline-variant hover:bg-surface-container transition-colors font-bold">3</button>', '<a href="?page=3" class="w-10 h-10 flex items-center justify-center rounded-lg border border-outline-variant hover:bg-surface-container transition-colors font-bold">3</a>')
                content = content.replace('<button class="w-10 h-10 flex items-center justify-center rounded-lg border border-outline-variant hover:bg-surface-container transition-colors font-bold">12</button>', '<a href="?page=12" class="w-10 h-10 flex items-center justify-center rounded-lg border border-outline-variant hover:bg-surface-container transition-colors font-bold">12</a>')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

print('Templates updated!')
