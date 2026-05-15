import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const contentPath = path.join(root, "data", "content.json");
const playlistsPagePath = "C:\\tmp\\philipp-playlists.html";
const channelPlaylistsUrl = "https://www.youtube.com/@PhilippLackner/playlists";
const sectionId = "philipp-lackner-playlist-golden-data";
const existingHeading = "Philipp Lackner Playlist Golden Points";

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

function cleanText(value = "") {
  return value
    .replace(/\r/g, "")
    .replace(/[^\S\n]+/g, " ")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function extractTimestamps(description) {
  return [...description.matchAll(/(?:^|\n)(\d{1,2}:\d{2}(?::\d{2})?)\s*[-–]\s*([^\n]+)/g)]
    .slice(0, 10)
    .map((match) => `${match[1]} - ${cleanText(match[2])}`);
}

function firstUsefulLine(description) {
  return (
    description
      .split("\n")
      .map((line) => cleanText(line))
      .find(
        (line) =>
          line &&
          !line.startsWith("http") &&
          !line.includes("utm_source") &&
          !line.startsWith("00:") &&
          !line.startsWith("0:") &&
          !/^(course|courses|download|checkout|become|apply|get the initial code)/i.test(line),
      ) || ""
  );
}

function summarizeVideo(video) {
  const line = firstUsefulLine(video.description);
  if (line) return line;

  const title = video.title.toLowerCase();
  if (title.includes("test")) return "Testing-focused Android lesson with practical validation and maintainability concerns.";
  if (title.includes("room")) return "Persistence lesson focused on local database modeling and Android data access.";
  if (title.includes("compose")) return "Jetpack Compose lesson focused on declarative UI structure and state-driven screens.";
  if (title.includes("navigation")) return "Navigation lesson focused on screen flow, back stack behavior, and route structure.";
  if (title.includes("firebase")) return "Firebase lesson focused on backend-backed Android app behavior.";
  if (title.includes("flow")) return "Kotlin Flow lesson focused on reactive streams and state propagation.";
  if (title.includes("kmp") || title.includes("multiplatform")) return "Kotlin Multiplatform lesson focused on shared business logic across platforms.";
  return "Android/Kotlin lesson extracted from Philipp Lackner's public playlist feed.";
}

function extractCodeLinks(description) {
  return [...description.matchAll(/https?:\/\/(?:github\.com|gist\.github\.com)\/[^\s<)]+/gi)].map((match) => match[0]);
}

function playlistCategory(title) {
  const lower = title.toLowerCase();
  if (lower.includes("navigation")) return "Navigation";
  if (lower.includes("material") || lower.includes("ux") || lower.includes("compose") || lower.includes("pokédex")) return "Compose UI";
  if (lower.includes("kmp") || lower.includes("kmm") || lower.includes("multiplatform")) return "Kotlin Multiplatform";
  if (lower.includes("flow") || lower.includes("io essentials") || lower.includes("kotlin")) return "Kotlin";
  if (lower.includes("room") || lower.includes("storage")) return "Persistence";
  if (lower.includes("ktor") || lower.includes("retrofit") || lower.includes("newsapp") || lower.includes("chat")) return "Networking";
  if (lower.includes("security")) return "Security";
  if (lower.includes("testing")) return "Testing";
  if (lower.includes("git")) return "Build & Delivery";
  if (lower.includes("firebase")) return "Firebase";
  if (lower.includes("spring boot")) return "Full-Stack Kotlin";
  if (lower.includes("camerax")) return "Camera & Media";
  if (lower.includes("android basics")) return "Android Fundamentals";
  if (lower.includes("news")) return "Android Ecosystem";
  return "Android Practice";
}

function goldenPlaylistPoints(playlist) {
  const category = playlistCategory(playlist.title);
  const timestampCount = playlist.videos.reduce((sum, video) => sum + video.timestamps.length, 0);
  const codeLinks = playlist.videos.flatMap((video) => video.codeLinks);

  return [
    `${category}: ${playlist.title} contains ${playlist.videos.length} public RSS video entries from Philipp Lackner's playlist feed.`,
    timestampCount
      ? `The playlist includes ${timestampCount} extracted timestamp markers; use them as a fast review path before interviews.`
      : "The playlist feed does not expose detailed timestamps for every video, so the roadmap points are summarized from titles and descriptions.",
    codeLinks.length
      ? `Code links found in descriptions: ${[...new Set(codeLinks)].slice(0, 5).join(", ")}`
      : "No public GitHub code links were exposed in the extracted RSS descriptions for this playlist.",
    `Best use: pair each video with one production note, one interview explanation, and one implementation trade-off in the ${category} area.`,
  ];
}

function videoPoint(video) {
  const date = video.published ? video.published.slice(0, 10) : "Unknown date";
  const timestamps = video.timestamps.length ? ` Key timestamps: ${video.timestamps.slice(0, 4).join("; ")}.` : "";
  const codeLinks = video.codeLinks.length ? ` Code: ${video.codeLinks.join(", ")}.` : "";
  return `${date}: ${video.title} - ${video.summary} ${video.url}.${timestamps}${codeLinks}`;
}

function codeBlocksForPlaylist(title) {
  const lower = title.toLowerCase();

  if (lower.includes("navigation")) {
    return [
      {
        language: "kotlin",
        title: "Type-Safe Navigation Route",
        code: "@Serializable\nobject ProfileRoute\n\n@Serializable\ndata class DetailsRoute(val itemId: String)\n\nfun NavGraphBuilder.profileGraph(\n    onOpenDetails: (String) -> Unit\n) {\n    composable<ProfileRoute> {\n        ProfileScreen(onOpenDetails = onOpenDetails)\n    }\n\n    composable<DetailsRoute> { entry ->\n        val route = entry.toRoute<DetailsRoute>()\n        DetailsScreen(itemId = route.itemId)\n    }\n}",
      },
    ];
  }

  if (lower.includes("compose") || lower.includes("material") || lower.includes("ux") || lower.includes("pokédex")) {
    return [
      {
        language: "kotlin",
        title: "State-Driven Compose Screen",
        code: "@Composable\nfun LearningScreen(\n    state: LearningUiState,\n    onAction: (LearningAction) -> Unit\n) {\n    Scaffold(\n        topBar = { TopAppBar(title = { Text(state.title) }) }\n    ) { padding ->\n        LazyColumn(contentPadding = padding) {\n            items(state.items) { item ->\n                ListItem(\n                    headlineContent = { Text(item.title) },\n                    supportingContent = { Text(item.summary) }\n                )\n            }\n        }\n    }\n}",
      },
    ];
  }

  if (lower.includes("flow")) {
    return [
      {
        language: "kotlin",
        title: "Flow to UI State",
        code: "val uiState: StateFlow<DashboardUiState> = repository.observeItems()\n    .map { items -> DashboardUiState.Content(items) }\n    .catch { emit(DashboardUiState.Error) }\n    .stateIn(\n        scope = viewModelScope,\n        started = SharingStarted.WhileSubscribed(5_000),\n        initialValue = DashboardUiState.Loading\n    )",
      },
    ];
  }

  if (lower.includes("room")) {
    return [
      {
        language: "kotlin",
        title: "Room Relation Query",
        code: "data class PlaylistWithTracks(\n    @Embedded val playlist: PlaylistEntity,\n    @Relation(\n        parentColumn = \"id\",\n        entityColumn = \"playlistId\"\n    ) val tracks: List<TrackEntity>\n)\n\n@Transaction\n@Query(\"SELECT * FROM playlists WHERE id = :id\")\nfun observePlaylist(id: String): Flow<PlaylistWithTracks>",
      },
    ];
  }

  if (lower.includes("testing")) {
    return [
      {
        language: "kotlin",
        title: "Coroutine ViewModel Test",
        code: "@Test\nfun `loading items exposes content state`() = runTest {\n    repository.items.value = listOf(Item(\"Compose\"))\n\n    val viewModel = LearningViewModel(repository)\n\n    assertEquals(\n        LearningUiState.Content(listOf(Item(\"Compose\"))),\n        viewModel.uiState.value\n    )\n}",
      },
    ];
  }

  if (lower.includes("ktor") || lower.includes("retrofit") || lower.includes("newsapp") || lower.includes("chat")) {
    return [
      {
        language: "kotlin",
        title: "Repository Response Mapping",
        code: "suspend fun loadArticles(): Result<List<Article>> = runCatching {\n    api.getArticles()\n        .articles\n        .map { dto -> dto.toDomain() }\n}",
      },
    ];
  }

  if (lower.includes("firebase")) {
    return [
      {
        language: "kotlin",
        title: "Firebase Auth State Boundary",
        code: "val authState: Flow<User?> = callbackFlow {\n    val listener = FirebaseAuth.AuthStateListener { auth ->\n        trySend(auth.currentUser?.toDomain())\n    }\n    firebaseAuth.addAuthStateListener(listener)\n    awaitClose { firebaseAuth.removeAuthStateListener(listener) }\n}",
      },
    ];
  }

  if (lower.includes("kmp") || lower.includes("kmm")) {
    return [
      {
        language: "kotlin",
        title: "KMP Expect/Actual Boundary",
        code: "expect class PlatformClock() {\n    fun nowMillis(): Long\n}\n\nclass SharedSyncUseCase(\n    private val clock: PlatformClock\n) {\n    fun shouldRefresh(lastSyncMillis: Long): Boolean =\n        clock.nowMillis() - lastSyncMillis > 15.minutes.inWholeMilliseconds\n}",
      },
    ];
  }

  if (lower.includes("security")) {
    return [
      {
        language: "kotlin",
        title: "Never Trust Local Entitlement State Alone",
        code: "suspend fun canAccessPremium(userId: String): Boolean {\n    val serverState = billingApi.verifyEntitlement(userId)\n    entitlementCache.save(serverState)\n    return serverState.isActive && serverState.signatureValid\n}",
      },
    ];
  }

  return [];
}

function mapPlaylistToExistingTopic(title) {
  const lower = title.toLowerCase();
  if (lower.includes("navigation")) return ["state-navigation", "Compose Navigation"];
  if (lower.includes("material") || lower.includes("ux") || lower.includes("compose") || lower.includes("pokédex")) {
    return ["ui-toolkit-views-jetpack-compose", "Jetpack Compose (Modern UI)"];
  }
  if (lower.includes("flow")) return ["kotlin-coroutines-flow", "Flow Advanced Patterns"];
  if (lower.includes("io essentials") || lower.includes("kotlin")) return ["kotlin-coroutines-flow", "Kotlin Essentials for Android"];
  if (lower.includes("kmp") || lower.includes("kmm")) return ["advanced-modern-android-topics", "KMP Fundamentals"];
  if (lower.includes("room")) return ["data-management-persistence", "Room Database"];
  if (lower.includes("storage")) return ["data-management-persistence", "File Storage"];
  if (lower.includes("security")) return ["security-privacy-app-integrity", "Code Security"];
  if (lower.includes("testing")) return ["testing-strategy", "Test Architecture"];
  if (lower.includes("git")) return ["build-release-ci-cd", "GitHub Actions for Android"];
  if (lower.includes("firebase")) return ["advanced-modern-android-topics", "Firebase Services"];
  if (lower.includes("ktor") || lower.includes("retrofit") || lower.includes("newsapp") || lower.includes("chat")) {
    return ["networking-apis", "API Response Handling"];
  }
  if (lower.includes("android basics")) return ["android-fundamentals-platform-basics", "Android Runtime, Process Model & App Startup"];
  if (lower.includes("camerax")) return ["jetpack-components-deep-dive", "Paging, Hilt, Security & Testing Components"];
  if (lower.includes("spring boot")) return ["system-design-for-mobile", "Common Design Scenarios"];
  if (lower.includes("news")) return ["resources-references", "Official Documentation"];
  return null;
}

function upsertContentSection(content, sectionIdToUpdate, topicTitle, heading, points) {
  const section = content.find((item) => item.id === sectionIdToUpdate);
  if (!section) return;

  const topic = (section.topics || []).find((item) => item.title === topicTitle);
  if (!topic) return;

  topic.content_sections = (topic.content_sections || []).filter((item) => item.heading !== heading);
  topic.content_sections.push({
    heading,
    points,
    subtopics: [],
  });
}

function parsePlaylistFeed(id, xml) {
  const title = textBetween(xml, "title") || id;
  const videos = [...xml.matchAll(/<entry>([\s\S]*?)<\/entry>/g)]
    .map((match) => {
      const entry = match[1];
      const videoId = textBetween(entry, "yt:videoId");
      const description = textBetween(entry, "media:description");
      return {
        title: textBetween(entry, "title"),
        videoId,
        url: `https://www.youtube.com/watch?v=${videoId}`,
        published: textBetween(entry, "published"),
        updated: textBetween(entry, "updated"),
        thumbnail: attrValue(entry, "media:thumbnail", "url"),
        views: attrValue(entry, "media:statistics", "views"),
        description,
        timestamps: extractTimestamps(description),
        codeLinks: extractCodeLinks(description),
      };
    })
    .filter((video) => video.title && video.videoId)
    .map((video) => ({ ...video, summary: summarizeVideo(video) }));

  return { id, title, category: playlistCategory(title), videos };
}

async function main() {
  let html = "";
  if (fs.existsSync(playlistsPagePath)) {
    html = fs.readFileSync(playlistsPagePath, "utf8");
  } else {
    html = await fetch(channelPlaylistsUrl).then((response) => response.text());
    fs.mkdirSync(path.dirname(playlistsPagePath), { recursive: true });
    fs.writeFileSync(playlistsPagePath, html);
  }

  const playlistIds = [...new Set([...html.matchAll(/playlist\?list=([A-Za-z0-9_-]+)/g)].map((match) => match[1]))];
  if (!playlistIds.length) throw new Error("No playlist IDs found.");

  const playlists = [];
  for (const id of playlistIds) {
    const url = `https://www.youtube.com/feeds/videos.xml?playlist_id=${id}`;
    const xml = await fetch(url).then((response) => {
      if (!response.ok) throw new Error(`Failed to fetch ${id}: ${response.status}`);
      return response.text();
    });
    const playlist = parsePlaylistFeed(id, xml);
    if (playlist.videos.length) playlists.push(playlist);
  }

  const content = JSON.parse(fs.readFileSync(contentPath, "utf8"));

  const groupedExistingPoints = new Map();
  for (const playlist of playlists) {
    const target = mapPlaylistToExistingTopic(playlist.title);
    if (!target) continue;

    const key = target.join("::");
    const current = groupedExistingPoints.get(key) || [];
    current.push(
      `${playlist.title}: ${playlist.category} playlist with ${playlist.videos.length} extracted videos. Start with: ${playlist.videos
        .slice(0, 3)
        .map((video) => video.title)
        .join("; ")}.`,
    );
    current.push(...playlist.videos.slice(0, 6).map(videoPoint));
    groupedExistingPoints.set(key, current);
  }

  for (const [key, points] of groupedExistingPoints) {
    const [targetSectionId, targetTopicTitle] = key.split("::");
    upsertContentSection(content, targetSectionId, targetTopicTitle, existingHeading, [
      "Playlist-derived points from Philipp Lackner's public YouTube playlist RSS feeds; use them as supplemental study notes next to the core roadmap.",
      ...points,
    ]);
  }

  const section = {
    id: sectionId,
    title: "Philipp Lackner Playlist Golden Data",
    description:
      "Playlist-level Android, Kotlin, Compose, KMP, testing, Firebase, persistence, networking, and tooling study data extracted from Philipp Lackner's public YouTube playlist RSS feeds.",
    topics: playlists.map((playlist) => ({
      title: playlist.title,
      icon: "",
      description: `${playlist.category} learning path extracted from ${playlist.videos.length} public playlist video entries.`,
      content_sections: [
        {
          heading: "Golden Takeaways",
          points: goldenPlaylistPoints(playlist),
          subtopics: [],
        },
        {
          heading: "Video-by-Video Points",
          points: playlist.videos.map(videoPoint),
          subtopics: playlist.videos.map((video) => ({
            title: video.title,
            description: [
              video.summary,
              `URL: ${video.url}`,
              video.timestamps.length ? `Timestamps: ${video.timestamps.join("; ")}` : "",
              video.codeLinks.length ? `Code links: ${video.codeLinks.join(", ")}` : "",
            ]
              .filter(Boolean)
              .join(" "),
          })),
        },
      ],
      code_blocks: codeBlocksForPlaylist(playlist.title),
    })),
  };

  const nextContent = content.filter((item) => item.id !== sectionId);
  nextContent.push(section);
  fs.writeFileSync(contentPath, `${JSON.stringify(nextContent, null, 2)}\n`);

  const videoCount = playlists.reduce((sum, playlist) => sum + playlist.videos.length, 0);
  console.log(`Injected ${playlists.length} playlists and ${videoCount} videos into ${contentPath}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
