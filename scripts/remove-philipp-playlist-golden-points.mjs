import fs from "node:fs";
import path from "node:path";

const contentPath = path.join(process.cwd(), "data", "content.json");
const content = JSON.parse(fs.readFileSync(contentPath, "utf8"));
const headingToRemove = "Philipp Lackner Playlist Golden Points";

let removed = 0;

for (const section of content) {
  for (const topic of section.topics || []) {
    const before = topic.content_sections?.length || 0;
    topic.content_sections = (topic.content_sections || []).filter((contentSection) => contentSection.heading !== headingToRemove);
    removed += before - topic.content_sections.length;
  }
}

fs.writeFileSync(contentPath, `${JSON.stringify(content, null, 2)}\n`);
console.log(`Removed ${removed} "${headingToRemove}" sections`);
