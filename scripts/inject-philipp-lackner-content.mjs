import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const contentPath = path.join(root, "data", "content.json");
const feedPath = "C:\\tmp\\philipp-lackner-feed.xml";
const sectionId = "philipp-lackner-youtube-watchlist";

function decodeXml(value = "") {
  return value
    .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, "$1")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, "\"")
    .replace(/&#39;/g, "'")
    .replace(/&apos;/g, "'");
}

function textBetween(source, tagName) {
  const match = source.match(new RegExp(`<${tagName}(?:\\s[^>]*)?>([\\s\\S]*?)<\\/${tagName}>`));
  return decodeXml(match?.[1] || "").trim();
}

function attrValue(source, tagName, attrName) {
  const match = source.match(new RegExp(`<${tagName}[^>]*\\s${attrName}="([^"]+)"[^>]*>`));
  return decodeXml(match?.[1] || "").trim();
}

function extractTimestamps(description) {
  return [...description.matchAll(/(?:^|\n)(\d{1,2}:\d{2}(?::\d{2})?)\s*[-–]\s*([^\n]+)/g)]
    .slice(0, 8)
    .map((match) => `${match[1]} - ${match[2].trim()}`);
}

function summarizeVideo(title, description) {
  const firstLine = description
    .split("\n")
    .map((line) => line.trim())
    .find((line) => line && !line.startsWith("http") && !line.includes("utm_source"));

  if (firstLine) return firstLine;

  if (/system design/i.test(title)) {
    return "Mobile system design interview guidance, with focus on the major areas to reason about in an Android app.";
  }

  if (/compose|android studio|mobile dev news/i.test(title)) {
    return "Current Android ecosystem update useful for keeping senior-level answers fresh.";
  }

  if (/agent|ai|claude|cursor/i.test(title)) {
    return "AI-assisted Android development guidance, useful for modern engineering workflows and code review judgment.";
  }

  return "Selected Philipp Lackner Android/Kotlin learning resource extracted from the public YouTube feed.";
}

function mapTopic(title) {
  const lower = title.toLowerCase();
  if (lower.includes("system design")) return "Mobile system design";
  if (lower.includes("compose")) return "Jetpack Compose updates";
  if (lower.includes("cli") || lower.includes("android studio")) return "Android tooling";
  if (lower.includes("in-app purchases") || lower.includes("attackers")) return "Security and payments";
  if (lower.includes("agent") || lower.includes("ai") || lower.includes("claude") || lower.includes("cursor")) return "AI-assisted Android development";
  if (lower.includes("junior") || lower.includes("senior")) return "Career growth and senior expectations";
  return "Modern Android learning";
}

const feedXml = fs.readFileSync(feedPath, "utf8");
const entries = [...feedXml.matchAll(/<entry>([\s\S]*?)<\/entry>/g)]
  .map((match) => {
    const entry = match[1];
    const title = textBetween(entry, "title");
    const videoId = textBetween(entry, "yt:videoId");
    const published = textBetween(entry, "published");
    const description = textBetween(entry, "media:description");
    const thumbnail = attrValue(entry, "media:thumbnail", "url");
    const views = attrValue(entry, "media:statistics", "views");
    const timestamps = extractTimestamps(description);
    const url = `https://www.youtube.com/watch?v=${videoId}`;

    return {
      title,
      videoId,
      url,
      published,
      thumbnail,
      views,
      description,
      timestamps,
      topic: mapTopic(title),
      summary: summarizeVideo(title, description),
    };
  })
  .filter((video) => video.title && video.videoId)
  .slice(0, 12);

if (!entries.length) {
  throw new Error("No videos found in RSS feed.");
}

const content = JSON.parse(fs.readFileSync(contentPath, "utf8"));

function findVideoById(videoId) {
  return entries.find((video) => video.videoId === videoId);
}

function sourceLabel(videoId) {
  const video = findVideoById(videoId);
  return video ? `Source: ${video.title} (${video.url})` : "";
}

function upsertContentSection(sectionIdToUpdate, topicTitle, heading, points) {
  const targetSection = content.find((item) => item.id === sectionIdToUpdate);
  if (!targetSection) throw new Error(`Missing section: ${sectionIdToUpdate}`);

  const targetTopic = (targetSection.topics || []).find((topic) => topic.title === topicTitle);
  if (!targetTopic) throw new Error(`Missing topic: ${sectionIdToUpdate} / ${topicTitle}`);

  targetTopic.content_sections = (targetTopic.content_sections || []).filter((item) => item.heading !== heading);
  targetTopic.content_sections.push({
    heading,
    points,
    subtopics: [],
  });
}

const videoPointHeading = "Philipp Lackner Video Points";

upsertContentSection("system-design-for-mobile", "Mobile System Design Principles", videoPointHeading, [
  "For mobile system design interviews, frame the answer around client responsibilities first: UI/state, local persistence, sync, API contracts, auth, push/background work, observability, and failure handling.",
  "Start with product requirements and constraints before naming technologies; senior answers should explain why a choice fits latency, offline, consistency, privacy, and team-maintenance constraints.",
  "A strong mobile design answer makes trade-offs visible: what runs on-device, what belongs on the backend, what is cached, how conflict resolution works, and how the app degrades when the network or auth layer fails.",
  sourceLabel("OP6JHa21We8"),
]);

upsertContentSection("advanced-modern-android-topics", "LLM Integration", videoPointHeading, [
  "AI-assisted Android development is a workflow change, not a replacement for engineering judgment: the developer still owns architecture, code review, security, tests, and release risk.",
  "Useful AI-agent work needs explicit constraints: existing architecture rules, module boundaries, style conventions, acceptance criteria, test expectations, and small reviewable tasks.",
  "Understand core AI vocabulary for product and engineering discussions: tokens, embeddings, temperature, hallucination, agents, skills, MCP, RAG, and context windows.",
  "Know the limits too: hallucinations, synthetic-data quality, frame/context problems, and cost all affect whether AI belongs in a production Android workflow or feature.",
  sourceLabel("OcBkJUwjDqg"),
  sourceLabel("HhaVpPRInDU"),
  sourceLabel("eVbhHlQNieU"),
]);

upsertContentSection("advanced-modern-android-topics", "Modern Android Development", videoPointHeading, [
  "Native Android can become more attractive when AI tools reduce boilerplate and iteration cost, but teams still need clear architecture and platform-specific quality checks.",
  "When comparing tools such as Claude Code and Cursor, evaluate maintainability, architectural fit, correctness, testability, and how easy the output is to review, not just how fast code appears.",
  "Use AI-assisted app generation as a starting point for implementation and exploration, then bring it back through normal Android review: lifecycle safety, state handling, threading, persistence, security, and build verification.",
  sourceLabel("BDaGLTMbdwY"),
  sourceLabel("aRNVncOYd5c"),
  sourceLabel("QSELS0H6aMg"),
]);

upsertContentSection("build-release-ci-cd", "Gradle & Build System", videoPointHeading, [
  "Android CLI and command-line-first workflows matter more as AI agents become part of development, because repeatable commands give agents and humans the same build, test, and validation surface.",
  "A senior setup should make common actions scriptable: create/build variants, run tests, inspect dependencies, verify lint, and reproduce CI failures locally.",
  "Treat CLI tooling as part of developer experience: document installation, expected SDK versions, environment assumptions, and failure recovery so automation does not depend on one machine.",
  sourceLabel("MLDkhDyvTVI"),
]);

upsertContentSection("security-privacy-app-integrity", "Code Security", videoPointHeading, [
  "In-app purchase and premium-access logic must assume the client can be inspected or modified; never trust local flags as the only source of entitlement truth.",
  "Protect purchases with server-side or trusted backend validation where possible, Play Billing verification, replay protection, tamper detection, and careful handling of cached entitlement state.",
  "Obfuscation and hardening can raise attack cost, but the architecture should still fail safely when billing state, network checks, or local storage are manipulated.",
  sourceLabel("WHfmXHqEmnM"),
]);

upsertContentSection("ui-toolkit-views-jetpack-compose", "Jetpack Compose (Modern UI)", videoPointHeading, [
  "Track Compose releases because layout primitives, adaptive UI APIs, and Android Studio support can change what is practical or recommended in production UI code.",
  "When new Compose APIs land, evaluate them against existing app constraints: performance, readability, design-system fit, testability, and migration cost.",
  "Senior interview answers should distinguish between knowing a new API exists and knowing when it should replace an established custom layout or component pattern.",
  sourceLabel("QViURZf9x1s"),
]);

upsertContentSection("data-management-persistence", "Room Database", videoPointHeading, [
  "Room and persistence updates should be evaluated through migration safety, schema compatibility, generated SQL quality, test coverage, and rollback plans.",
  "When platform news mentions major persistence changes, convert it into concrete team questions: what breaks, what improves, what migration is required, and how will we validate it in CI?",
  sourceLabel("GpVJ3bTqX4Y"),
]);

upsertContentSection("interview-preparation-strategy", "Before the Interview", videoPointHeading, [
  "Avoid the junior-developer trap of collecting tools without building judgment; interview preparation should produce clear explanations, trade-off language, and production examples.",
  "Before interviews, turn each learning resource into an answer you can defend: problem context, options considered, chosen approach, risk, measurement, and outcome.",
  sourceLabel("NG2D1lGpdlQ"),
]);
const section = {
  id: sectionId,
  title: "Philipp Lackner YouTube Watchlist",
  description:
    "Recent Philipp Lackner Android, Kotlin, mobile system design, and AI-assisted development videos extracted from the public YouTube RSS feed for targeted interview preparation.",
  topics: [
    {
      title: "Recent Android & Kotlin Videos",
      icon: "",
      description:
        "A curated watchlist generated from Philipp Lackner's public YouTube feed, grouped by the practical senior Android concept each video supports.",
      content_sections: [
        {
          heading: "How to Use This Watchlist",
          points: [
            "Use these videos as refreshers next to the roadmap topics rather than as passive binge watching.",
            "For each video, write down one production trade-off, one interview talking point, and one code or architecture decision you would defend.",
            "Revisit the system design, AI-assisted Android development, tooling, security, and Compose update videos before senior Android interviews.",
          ],
          subtopics: [],
        },
        {
          heading: "Extracted Videos",
          points: entries.map((video) => {
            const date = video.published ? video.published.slice(0, 10) : "Unknown date";
            const views = video.views ? ` | ${Number(video.views).toLocaleString("en-US")} views` : "";
            return `${date} | ${video.topic}: ${video.title} - ${video.summary} ${video.url}${views}`;
          }),
          subtopics: entries.map((video) => ({
            title: video.title,
            description: [
              `Topic fit: ${video.topic}.`,
              video.summary,
              `URL: ${video.url}`,
              video.timestamps.length ? `Timestamps: ${video.timestamps.join("; ")}` : "",
            ]
              .filter(Boolean)
              .join(" "),
          })),
        },
      ],
      code_blocks: [],
    },
  ],
};

const nextContent = content.filter((item) => item.id !== sectionId);
nextContent.push(section);
fs.writeFileSync(contentPath, `${JSON.stringify(nextContent, null, 2)}\n`);

console.log(`Injected ${entries.length} Philipp Lackner videos into ${contentPath}`);
