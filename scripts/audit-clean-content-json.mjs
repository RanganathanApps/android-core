import fs from "node:fs";
import path from "node:path";

const contentPath = path.join(process.cwd(), "data", "content.json");
const content = JSON.parse(fs.readFileSync(contentPath, "utf8"));

function normalizeText(value = "") {
  return String(value).replace(/\s+/g, " ").trim();
}

function dedupeBy(items, keyFn) {
  const seen = new Set();
  const next = [];
  let removed = 0;

  for (const item of items || []) {
    const key = keyFn(item);
    if (key && seen.has(key)) {
      removed += 1;
      continue;
    }
    if (key) seen.add(key);
    next.push(item);
  }

  return { next, removed };
}

function cleanPoints(points = []) {
  return dedupeBy(
    points.map((point) => normalizeText(point)).filter(Boolean),
    (point) => point.toLowerCase(),
  );
}

const report = {
  duplicateSections: 0,
  duplicateTopics: 0,
  duplicateContentSections: 0,
  duplicatePoints: 0,
  duplicateSubtopics: 0,
  duplicateCodeBlocks: 0,
  emptyContentSections: 0,
};

const sectionDedupe = dedupeBy(content, (section) => normalizeText(section.id || section.title).toLowerCase());
report.duplicateSections = sectionDedupe.removed;
const cleanedContent = sectionDedupe.next;

for (const section of cleanedContent) {
  section.title = normalizeText(section.title);
  section.description = normalizeText(section.description);

  const topicDedupe = dedupeBy(section.topics || [], (topic) => normalizeText(topic.title).toLowerCase());
  report.duplicateTopics += topicDedupe.removed;
  section.topics = topicDedupe.next;

  for (const topic of section.topics) {
    topic.title = normalizeText(topic.title);
    topic.description = normalizeText(topic.description);

    const contentSectionDedupe = dedupeBy(topic.content_sections || [], (contentSection) =>
      normalizeText(contentSection.heading).toLowerCase(),
    );
    report.duplicateContentSections += contentSectionDedupe.removed;
    topic.content_sections = contentSectionDedupe.next;

    for (const contentSection of topic.content_sections) {
      contentSection.heading = normalizeText(contentSection.heading);

      const pointDedupe = cleanPoints(contentSection.points || []);
      report.duplicatePoints += pointDedupe.removed;
      contentSection.points = pointDedupe.next;

      const subtopicDedupe = dedupeBy(contentSection.subtopics || [], (subtopic) =>
        `${normalizeText(subtopic.title).toLowerCase()}::${normalizeText(subtopic.description).toLowerCase()}`,
      );
      report.duplicateSubtopics += subtopicDedupe.removed;
      contentSection.subtopics = subtopicDedupe.next.map((subtopic) => ({
        title: normalizeText(subtopic.title),
        description: normalizeText(subtopic.description),
      }));
    }

    const beforeEmpty = topic.content_sections.length;
    topic.content_sections = topic.content_sections.filter(
      (contentSection) =>
        normalizeText(contentSection.heading) ||
        (contentSection.points || []).length ||
        (contentSection.subtopics || []).length,
    );
    report.emptyContentSections += beforeEmpty - topic.content_sections.length;

    const codeDedupe = dedupeBy(topic.code_blocks || [], (block) =>
      `${normalizeText(block.title).toLowerCase()}::${normalizeText(block.language).toLowerCase()}::${normalizeText(block.code)}`,
    );
    report.duplicateCodeBlocks += codeDedupe.removed;
    topic.code_blocks = codeDedupe.next.map((block) => ({
      language: normalizeText(block.language || "text"),
      title: normalizeText(block.title || "Code Example"),
      code: String(block.code || "").trim(),
    }));
  }
}

fs.writeFileSync(contentPath, `${JSON.stringify(cleanedContent, null, 2)}\n`);
console.log(JSON.stringify(report, null, 2));
