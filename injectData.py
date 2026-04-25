import json

from content import CONTENT

TEMPLATE_FILE = "techstackpage.html"
OUTPUT_FILE = "final.html"
PLACEHOLDER = "{{CONTENT_JSON}}"

with open(TEMPLATE_FILE, encoding="utf-8") as file:
    html_template = file.read()

final_html = html_template.replace(
    PLACEHOLDER,
    json.dumps(CONTENT, ensure_ascii=False, indent=2),
)

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write(final_html)

print(f"Generated {OUTPUT_FILE} from {TEMPLATE_FILE}")
