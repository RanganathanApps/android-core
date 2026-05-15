import fs from "node:fs";
import path from "node:path";

const contentPath = path.join(process.cwd(), "data", "content.json");
const content = JSON.parse(fs.readFileSync(contentPath, "utf8"));

const boostHeading = "Focused Senior Boost";

const topicBoosts = {
  "performance-observability::Modern Android Summary": [
    "Use this topic as a synthesis checkpoint: connect architecture, UI, concurrency, persistence, testing, performance, and release practices into one production story.",
    "Senior Android answers should explain how choices interact: Compose state affects performance, persistence affects offline behavior, CI affects release confidence, and observability affects debugging.",
    "A modern stack is not a checklist; it is a set of boundaries that make change safer: UDF, modularization, DI, repository contracts, typed state, tests, and metrics.",
    "When reviewing an app, look for missing feedback loops: no startup metrics, no crash segmentation, no test gates, no release rollback, or no ownership of background work.",
    "Practice by describing one feature end-to-end from user action to API/database, UI state, tests, metrics, and rollout.",
  ],
  "state-navigation::ViewModel & SavedStateHandle": [
    "ViewModel owns screen-level state and work that survives configuration change, but it does not survive process death unless paired with SavedStateHandle or persistence.",
    "SavedStateHandle should store small restoration keys or primitives, not large domain objects or cached API payloads.",
    "Use repository/database state as the durable source of truth, and use SavedStateHandle for route arguments, selected tabs, draft IDs, and restoration hints.",
    "Do not leak Activity, Fragment, View, or NavController into ViewModel; expose state and events instead.",
    "Interview framing: explain what happens during rotation, process death, back stack restore, and logout.",
  ],
  "state-navigation::Compose Navigation": [
    "Compose Navigation works best when routes are small contracts and destinations load their own data from stable IDs.",
    "Keep navigation execution in the app/navigation layer; ViewModels can emit navigation intents, but should not own NavController.",
    "Use nested graphs for feature flows, auth gates, onboarding, and bottom-tab sections.",
    "Test navigation by asserting visible destinations and state restoration rather than internal route strings where possible.",
    "Senior trade-off: simple apps can use direct route strings, but larger apps benefit from typed routes and feature-owned route contracts.",
  ],
  "data-management-persistence::DataStore": [
    "Use Preferences DataStore for simple key-value preferences and Proto DataStore for typed settings with schema evolution.",
    "DataStore is asynchronous and coroutine/Flow-friendly, making it safer than SharedPreferences for modern Android.",
    "Keep DataStore for small settings, not relational data, large documents, caches, or frequently queried collections.",
    "Model defaults explicitly so first launch, migration, and corrupt data behavior are predictable.",
    "Expose settings as Flow and map them into UI state through ViewModel rather than reading synchronously from UI.",
  ],
  "networking-apis::Certificate Pinning": [
    "Certificate pinning protects against certain man-in-the-middle attacks, but it also creates operational risk when certificates rotate unexpectedly.",
    "Pin public keys or intermediate CA strategy carefully; avoid brittle leaf-only pinning unless there is a controlled rotation plan.",
    "Always define a recovery story: app update, backup pins, remote config limitations, monitoring, and customer support impact.",
    "Do not use pinning as a replacement for proper TLS, auth, secure storage, or backend authorization.",
    "Interview framing: explain both the security benefit and the outage risk.",
  ],
  "concurrency-threading-background-work::Foreground Services": [
    "Use foreground services only for immediate, user-visible work that must continue while the app is backgrounded.",
    "Show a meaningful notification and choose the correct foreground service type to satisfy modern Android policy.",
    "Prefer WorkManager for deferrable guaranteed work; do not use foreground services as a general background escape hatch.",
    "Handle cancellation from the notification, process death, permission changes, and OS restrictions.",
    "Examples: active navigation, media playback, fitness tracking, ongoing upload with visible user value.",
  ],
  "security-privacy-app-integrity::Secure Storage": [
    "Secure storage is for reducing local extraction risk, not for making client-side secrets impossible to obtain.",
    "Use EncryptedSharedPreferences or encrypted files for sensitive local data, but avoid storing secrets that can be server-derived or short-lived.",
    "Protect refresh tokens more carefully than access tokens and clear them on logout, account removal, or suspicious auth state.",
    "Never log secrets, decrypted payloads, auth headers, or personally identifiable data.",
    "Senior framing: explain threat model, storage choice, key invalidation, backup behavior, and logout behavior.",
  ],
  "security-privacy-app-integrity::Biometric Authentication": [
    "Biometrics are a local re-authentication and convenience layer; they do not replace server-side authorization.",
    "Use BiometricPrompt and CryptoObject when the action truly requires cryptographic gating.",
    "Plan fallback behavior for device credential, biometric enrollment changes, lockout, and unsupported devices.",
    "Do not gate critical account recovery solely behind biometrics.",
    "Interview framing: distinguish identity proof, device unlock, local secret release, and server authorization.",
  ],
  "security-privacy-app-integrity::Play Integrity API": [
    "Play Integrity helps assess app/device integrity signals, but the server must make the final trust decision.",
    "Treat verdicts as risk signals, not absolute truth; combine with account, transaction, and abuse signals.",
    "Never place enforcement logic only in the Android client because the client can be modified.",
    "Design graceful degradation for false negatives and network failures.",
    "Use it for abuse-sensitive flows such as payments, premium entitlement, anti-cheat, and high-risk API access.",
  ],
  "build-release-ci-cd::GitHub Actions for Android": [
    "A good Android workflow caches Gradle safely, sets up JDK/Android SDK consistently, runs deterministic checks, and publishes reports.",
    "Split fast PR checks from slower release or nightly jobs to keep developer feedback quick.",
    "Store signing keys and Play credentials as protected secrets with least privilege and branch/environment rules.",
    "Upload artifacts, test reports, lint reports, and mapping files so failures and crashes are actionable.",
    "Keep CI commands close to local Gradle commands so developers can reproduce failures.",
  ],
  "advanced-modern-android-topics::ML Kit": [
    "ML Kit is strongest for common on-device ML tasks such as barcode scanning, text recognition, face detection, translation, and smart replies.",
    "Evaluate latency, offline need, privacy, model size, and device support before adding ML features.",
    "Keep ML behind a feature boundary so permissions, camera lifecycle, threading, and fallback UI are testable.",
    "Measure real device performance because emulator and flagship-device results can hide latency or memory issues.",
    "Senior framing: explain why on-device ML is better than backend inference for this specific use case.",
  ],
  "advanced-modern-android-topics::TensorFlow Lite": [
    "TensorFlow Lite is useful when you need custom on-device inference beyond ML Kit's packaged APIs.",
    "Plan model delivery, versioning, quantization, delegate support, warm-up, memory use, and fallback behavior.",
    "Move inference off the main thread and treat model loading as a performance-sensitive resource boundary.",
    "Validate accuracy and latency on representative low-end devices, not only development hardware.",
    "Senior framing: include model lifecycle, observability, privacy, and rollback strategy.",
  ],
};

const highlightReplacements = {
  "dependency-injection::Koin": [
    "Koin is a lightweight, Kotlin-first DI framework that uses a DSL instead of generated code.",
    "Use single for singleton-like dependencies, factory for new instances, and viewModel for ViewModel bindings.",
    "Koin can be quick to adopt and friendly for KMP, but runtime resolution errors need test coverage and discipline.",
    "For larger teams, compare Koin against Hilt in terms of compile-time guarantees, Android integration, startup cost, and graph visibility.",
  ],
  "data-management-persistence::SharedPreferences": [
    "SharedPreferences is legacy key-value storage for small primitive values.",
    "Prefer DataStore for modern async preference storage because it avoids synchronous disk reads and has Flow support.",
    "Avoid SharedPreferences for structured data, lists, caches, secrets, or values that need transactional consistency.",
    "When migrating, define default values, migration behavior, and cleanup of old keys.",
  ],
  "testing-strategy::Compose UI Testing": [
    "Use createComposeRule or AndroidComposeTestRule depending on whether the test needs an Activity.",
    "Prefer semantics-based selectors such as text, content description, or test tags for stable tests.",
    "Test user behavior: click, input, scroll, assert visible state, and verify accessibility semantics.",
    "Avoid asserting implementation details that change during refactors, such as internal composable structure.",
  ],
  "performance-observability::Battery Optimization": [
    "Batch network work, use constraints, and avoid unnecessary wakeups to reduce battery drain.",
    "Use WorkManager for deferrable work and foreground services only for active user-visible operations.",
    "Understand Doze, App Standby, exact alarm restrictions, background location limits, and wake lock risk.",
    "Measure with Battery Historian, Perfetto, Play Console vitals, and targeted field metrics.",
  ],
  "performance-observability::APK Size Optimization": [
    "Use R8 shrinking, resource shrinking, Android App Bundles, vector drawables, WebP/AVIF where appropriate, and dependency hygiene.",
    "Inspect APK/AAB contents before optimizing blindly; large native libraries, images, ML models, and unused dependencies are common offenders.",
    "Keep mapping files for crash decoding and test release builds because shrinking can reveal reflection/serialization issues.",
    "Use dynamic delivery only when the product and architecture can tolerate deferred feature install.",
  ],
  "security-privacy-app-integrity::Permissions": [
    "Request the minimum permission at the moment the user understands why it is needed.",
    "Handle denial, don't-ask-again, approximate location, background location, notification permission, and partial photo access gracefully.",
    "Keep permission state in UI state and explain blocked flows with recovery actions.",
    "Avoid permissions entirely when system pickers or scoped APIs solve the use case.",
  ],
  "advanced-modern-android-topics::Firebase Services": [
    "Firebase can accelerate auth, messaging, analytics, crash reporting, remote config, Firestore, storage, and distribution.",
    "Use Firebase behind repositories/service boundaries so product code is not tightly coupled to vendor SDKs.",
    "Define privacy, retention, offline behavior, indexing, security rules, and cost monitoring before relying on Firebase in production.",
    "Treat Remote Config and feature flags as release infrastructure with ownership and rollback rules.",
  ],
  "advanced-modern-android-topics::Accessibility": [
    "Accessibility is core product quality: screen readers, touch targets, contrast, focus order, dynamic type, captions, and reduced motion.",
    "Compose and Views both need meaningful semantics/content descriptions, especially for custom components.",
    "Test with TalkBack, keyboard navigation, font scaling, color contrast tools, and Accessibility Scanner.",
    "A senior engineer should include accessibility acceptance criteria in design review and QA, not as a late polish task.",
  ],
  "advanced-modern-android-topics::Google Play Store": [
    "Play readiness includes signing, target SDK, data safety, privacy policy, store listing, screenshots, release notes, and policy compliance.",
    "Use staged rollout, internal/closed testing, crash monitoring, vitals, and rollback planning to reduce release risk.",
    "Billing, subscriptions, and premium access need server-side verification and clear entitlement handling.",
    "Store experiments can improve conversion, but product analytics should distinguish acquisition, activation, retention, and revenue impact.",
  ],
};

function key(sectionId, topicTitle) {
  return `${sectionId}::${topicTitle}`;
}

function findTopic(sectionId, topicTitle) {
  const section = content.find((item) => item.id === sectionId);
  return (section?.topics || []).find((topic) => topic.title === topicTitle);
}

function upsertSection(topic, heading, points) {
  topic.content_sections = (topic.content_sections || []).filter((section) => section.heading !== heading);
  topic.content_sections.push({ heading, points, subtopics: [] });
}

for (const [topicKey, points] of Object.entries(topicBoosts)) {
  const [sectionId, topicTitle] = topicKey.split("::");
  const topic = findTopic(sectionId, topicTitle);
  if (topic) upsertSection(topic, boostHeading, points);
}

for (const [topicKey, points] of Object.entries(highlightReplacements)) {
  const [sectionId, topicTitle] = topicKey.split("::");
  const topic = findTopic(sectionId, topicTitle);
  if (!topic) continue;

  for (const contentSection of topic.content_sections || []) {
    if (contentSection.heading === "Key Points") {
      contentSection.points = (contentSection.points || []).filter((point) => !point.startsWith("Highlights:"));
    }
  }

  upsertSection(topic, "Structured Highlights", points);
}

let thinBoosted = 0;
for (const section of content) {
  if (section.id?.startsWith("philipp-")) continue;

  for (const topic of section.topics || []) {
    if (topic.title?.includes("Golden Takeaways")) continue;
    if (topic.title === "11+ Years Interview Questions") continue;

    const count =
      (topic.content_sections || []).reduce((total, contentSection) => total + (contentSection.points || []).length + (contentSection.subtopics || []).length, 0) +
      (topic.code_blocks || []).length;

    if (count >= 5) continue;
    const existing = (topic.content_sections || []).some((contentSection) => contentSection.heading === boostHeading);
    if (existing) continue;

    upsertSection(topic, boostHeading, [
      `${topic.title} should be explained through purpose, lifecycle/ownership, failure modes, and production trade-offs rather than as a memorized API list.`,
      `For senior interviews, connect ${topic.title} to user impact, testability, observability, rollout risk, and long-term maintainability.`,
      `Know when to use ${topic.title}, when to avoid it, and what simpler alternative would work for a small app or prototype.`,
      `Practice prompt: describe a production bug involving ${topic.title}, how you would diagnose it, and what guardrail would prevent recurrence.`,
    ]);
    thinBoosted += 1;
  }
}

fs.writeFileSync(contentPath, `${JSON.stringify(content, null, 2)}\n`);
console.log(
  `Boosted ${Object.keys(topicBoosts).length} targeted thin topics, cleaned ${Object.keys(highlightReplacements).length} highlight groups, generically boosted ${thinBoosted} additional topics.`,
);
