export type ContentSubtopic = {
  title?: string;
  description?: string;
};

export type ContentSection = {
  heading?: string;
  points?: string[];
  subtopics?: ContentSubtopic[];
};

export type CodeBlock = {
  title?: string;
  language?: string;
  code?: string;
};

export type RoadmapTopic = {
  title?: string;
  description?: string;
  content_sections?: ContentSection[];
  code_blocks?: CodeBlock[];
};

export type RoadmapSection = {
  id?: string;
  title?: string;
  description?: string;
  topics?: RoadmapTopic[];
};

export type Priority = "must-know" | "important" | "advanced";

export function getTopicKey(
  section: RoadmapSection,
  topic: RoadmapTopic,
  sectionIndex: number,
  topicIndex: number,
) {
  return `${sectionIndex + 1}.${topicIndex + 1}:${section.title || ""}:${topic.title || ""}`;
}

export function normalizeSearchText(value: string) {
  return value.toLowerCase().replace(/\s+/g, " ").trim();
}

export function getSectionPriority(sectionTitle?: string): Priority {
  const title = String(sectionTitle || "").toLowerCase();

  if (
    title.includes("compose") ||
    title.includes("kotlin") ||
    title.includes("architecture") ||
    title.includes("jetpack") ||
    title.includes("testing")
  ) {
    return "must-know";
  }

  if (
    title.includes("system") ||
    title.includes("performance") ||
    title.includes("security") ||
    title.includes("interview")
  ) {
    return "important";
  }

  return "advanced";
}

export function getPriorityLabel(priority: Priority | "all") {
  const labels = {
    all: "All",
    "must-know": "Must Know",
    important: "Important",
    advanced: "Advanced",
  };

  return labels[priority];
}

export function estimateSectionDuration(section: RoadmapSection, priority: Priority) {
  const topicCount = section.topics?.length || 0;
  const contentWeight = (section.topics || []).reduce((total, topic) => {
    const contentSectionCount = topic.content_sections?.length || 0;
    const codeBlockCount = topic.code_blocks?.length || 0;
    return total + 20 + contentSectionCount * 12 + codeBlockCount * 10;
  }, 0);

  const priorityMultiplier = priority === "must-know" ? 1.15 : priority === "important" ? 1 : 0.85;
  const minutes = Math.max(25, Math.round((contentWeight * priorityMultiplier) / 15) * 15);
  const hours = Math.floor(minutes / 60);
  const remainder = minutes % 60;

  if (hours > 0 && remainder > 0) return `${hours}h ${remainder}m`;
  if (hours > 0) return `${hours}h`;
  return `${minutes}m`;
}

export function topicMatchesSearch(sectionTitle: string, topic: RoadmapTopic, topicNumber: string, searchTerm: string) {
  if (!searchTerm) return true;

  const haystack = [
    sectionTitle,
    topicNumber,
    topic.title,
    topic.description,
    ...(topic.content_sections || []).flatMap((contentSection) => [
      contentSection.heading,
      ...(contentSection.points || []),
      ...(contentSection.subtopics || []).flatMap((subtopic) => [subtopic.title, subtopic.description]),
    ]),
    ...(topic.code_blocks || []).flatMap((block) => [block.title, block.language, block.code]),
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();

  return haystack.includes(searchTerm);
}
