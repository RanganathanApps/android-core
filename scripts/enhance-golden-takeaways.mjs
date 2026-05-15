import fs from "node:fs";
import path from "node:path";

const contentPath = path.join(process.cwd(), "data", "content.json");
const content = JSON.parse(fs.readFileSync(contentPath, "utf8"));

const sectionTakeaways = {
  "android-fundamentals-platform-basics": {
    title: "Android Fundamentals Golden Takeaways",
    description: "The senior-level essence of Android fundamentals: process, lifecycle, components, state, permissions, resources, storage, and startup behavior.",
    master: [
      "Explain process death, task/back stack, Activity recreation, and state restoration without mixing them together.",
      "Know which app state belongs in memory, SavedStateHandle, DataStore, Room, files, or backend storage.",
      "Understand framework entry points: Application, Activity, Service, BroadcastReceiver, ContentProvider, Binder, and main thread message loop.",
    ],
    tradeoffs: [
      "Thin Application startup improves first frame but requires lazy initialization and clear dependency boundaries.",
      "Persisting more state improves resilience but increases schema, migration, privacy, and consistency responsibilities.",
      "Using platform components directly is powerful, but lifecycle and background limits must shape the design.",
    ],
    interview: "When asked a fundamentals question, draw the lifecycle/state boundary first, then explain what happens during configuration change, process death, and task restoration.",
    practice: "Take one screen in your app and document exactly what survives rotation, process death, logout, and app upgrade.",
  },
  "jetpack-components-deep-dive": {
    title: "Jetpack Components Golden Takeaways",
    description: "The practical role of Jetpack components in building lifecycle-aware, offline-capable, background-safe Android apps.",
    master: [
      "Use ViewModel, Room, DataStore, WorkManager, Paging, Navigation, and Activity Result APIs as lifecycle-aware contracts, not isolated libraries.",
      "Understand where each Jetpack component stores state, what owns cancellation, and what survives process death.",
      "Know the failure modes: duplicate workers, stale paging sources, migration crashes, lost activity results, and lifecycle-unsafe collection.",
    ],
    tradeoffs: [
      "Jetpack components reduce boilerplate, but they can hide important ownership and threading decisions if used mechanically.",
      "WorkManager reliability is valuable for deferrable work, but it is not a replacement for immediate foreground execution.",
      "Room and DataStore improve correctness, but schema/versioning and migration discipline become part of delivery.",
    ],
    interview: "Tie each component to the problem it solves: lifecycle, persistence, background reliability, navigation, paging, dependency boundaries, or testing.",
    practice: "Trace a feature from UI event to ViewModel, repository, persistence, background work, and UI refresh; name every Jetpack component involved.",
  },
  "kotlin-coroutines-flow": {
    title: "Kotlin Coroutines & Flow Golden Takeaways",
    description: "The core senior-level mental model for asynchronous Kotlin: ownership, cancellation, dispatchers, hot/cold streams, and reactive UI state.",
    master: [
      "Coroutines are about structured concurrency: every async task needs an owner, scope, dispatcher, and cancellation path.",
      "Flow is about data over time: know cold Flow, StateFlow, SharedFlow, callbackFlow, stateIn, shareIn, and lifecycle collection.",
      "Operator choice matters: combine, zip, merge, flatMapLatest, debounce, retryWhen, catch, and flowOn all encode different behavior.",
    ],
    tradeoffs: [
      "StateFlow is excellent for UI state, but it can hide stale state if refresh and error models are not explicit.",
      "SharedFlow is useful for events, but overuse becomes an event bus with unclear ownership.",
      "Parallel async work improves latency but complicates partial failure, cancellation, and error reporting.",
    ],
    interview: "Answer coroutine questions by naming the scope, dispatcher, cancellation behavior, failure propagation, and test strategy.",
    practice: "Build a search flow with debounce, flatMapLatest, loading/error/content states, and a deterministic unit test.",
  },
  "modern-architecture-patterns": {
    title: "Architecture Golden Takeaways",
    description: "The decision-making core behind UDF, Clean Architecture, modularization, repositories, use cases, and dependency direction.",
    master: [
      "Architecture is a set of trade-offs that protects change boundaries: UI, domain, data, platform, and feature modules.",
      "UDF makes state predictable when reducers, events, effects, and state ownership are explicit.",
      "Modularization should improve ownership, build speed, testability, and feature isolation, not just create more Gradle projects.",
    ],
    tradeoffs: [
      "Strict Clean Architecture improves long-term resilience but can slow small features if every pass-through layer is ceremonial.",
      "Feature modules scale teams well, but shared contracts and dependency rules must be enforced.",
      "Repositories simplify callers but can become god objects if sync, cache, mapping, and policy are not split thoughtfully.",
    ],
    interview: "Explain the architecture by walking a user action end-to-end, then point out where you would test, mock, cache, and handle failure.",
    practice: "Draw one feature as UI -> state holder -> use case -> repository -> data sources, including module ownership and dependency arrows.",
  },
  "ui-toolkit-views-jetpack-compose": {
    title: "UI & Compose Golden Takeaways",
    description: "The senior UI perspective: state-driven rendering, recomposition, design systems, accessibility, performance, and interoperability.",
    master: [
      "Compose is declarative: UI is a function of state, and side effects must be isolated in the right effect APIs.",
      "Know recomposition, stability, remember, rememberSaveable, derivedStateOf, Lazy list keys, and snapshot state.",
      "Design systems need reusable tokens, components, accessibility semantics, previews, and dark/light behavior.",
    ],
    tradeoffs: [
      "Hoisting state improves control but can make APIs noisy; local state is fine for purely visual behavior.",
      "Custom composables improve consistency, but over-abstraction can hide simple layout intent.",
      "Interoperability with Views is practical during migration, but ownership and lifecycle boundaries must stay explicit.",
    ],
    interview: "For Compose questions, separate rendering, state ownership, side effects, and performance instead of jumping straight to APIs.",
    practice: "Take a complex screen and list which state is UI-only, screen state, domain state, saved state, and persisted state.",
  },
  "state-navigation": {
    title: "State & Navigation Golden Takeaways",
    description: "The high-signal rules for UI state, saved state, navigation events, deep links, and modular navigation contracts.",
    master: [
      "Navigation should pass stable route arguments and IDs, not large mutable objects.",
      "State restoration depends on the layer: rememberSaveable, SavedStateHandle, ViewModel, Room, DataStore, or backend.",
      "Deep links are external input and need parsing, validation, authorization, and graceful missing-data behavior.",
    ],
    tradeoffs: [
      "Type-safe navigation reduces route bugs but still requires clear back stack and state ownership decisions.",
      "Shared ViewModels can simplify sibling screens but become hidden coupling if scope is unclear.",
      "Single-activity navigation is clean for Compose, but complex apps still need modular route boundaries.",
    ],
    interview: "Describe navigation as route contracts plus state ownership; then explain back behavior, deep links, and process death.",
    practice: "Design a profile -> edit -> result flow and specify how the result returns, what survives rotation, and what survives process death.",
  },
  "dependency-injection": {
    title: "Dependency Injection Golden Takeaways",
    description: "The senior DI view: object graph ownership, lifecycle scope, test replacement, qualifiers, and architecture boundaries.",
    master: [
      "DI is about controlling construction and lifetimes, not just avoiding new keywords.",
      "Know Hilt components/scopes, constructor injection, modules, qualifiers, assisted injection, and test bindings.",
      "Long-lived dependencies must not capture short-lived Android objects such as Activity, View, or Fragment references.",
    ],
    tradeoffs: [
      "Hilt standardizes large Android graphs but adds generated code, build complexity, and framework coupling.",
      "Manual DI is explicit and lightweight but can become repetitive as the app grows.",
      "Koin is flexible and multiplatform-friendly but trades compile-time guarantees for runtime resolution.",
    ],
    interview: "Answer DI questions by naming lifetime, ownership, construction boundary, test replacement, and failure mode.",
    practice: "Pick one dependency and identify who owns it, how long it lives, how it is tested, and what it must never reference.",
  },
  "data-management-persistence": {
    title: "Data & Persistence Golden Takeaways",
    description: "The core decisions behind offline-first data, repositories, Room, DataStore, files, sync, migrations, and cache policy.",
    master: [
      "Data architecture is read path plus write path: observe local truth, refresh from network, persist changes, and sync pending writes.",
      "Room is for structured relational data; DataStore is for small key-value/proto preferences; files are for blobs and external payloads.",
      "Repositories should define cache policy, source priority, error mapping, stale data, and conflict behavior.",
    ],
    tradeoffs: [
      "Offline-first improves UX but requires conflict resolution, sync status, retry policy, and user-visible stale state.",
      "Normalizing data improves consistency but increases mapping and query complexity.",
      "Aggressive caching improves speed but can serve stale or unauthorized data if invalidation is weak.",
    ],
    interview: "For persistence questions, explain schema, migration, transactions, offline behavior, sync retry, and data ownership.",
    practice: "Design an offline edit flow: pending write table, sync worker, conflict state, retry policy, and UI feedback.",
  },
  "networking-apis": {
    title: "Networking & APIs Golden Takeaways",
    description: "The production API mindset: contracts, auth, error models, retries, pagination, observability, and secure transport.",
    master: [
      "Separate transport, protocol, parsing, auth, validation, and domain errors.",
      "Understand Retrofit, OkHttp interceptors, TLS, certificate pinning, WebSockets, GraphQL, pagination, and response mapping.",
      "Design API models around versioning, idempotency, rate limits, auth refresh, and backward compatibility.",
    ],
    tradeoffs: [
      "Retries improve resilience but can amplify outages or duplicate writes without idempotency.",
      "GraphQL reduces overfetching but adds schema/codegen/cache complexity.",
      "Certificate pinning improves MITM resistance but creates operational risk during cert rotation.",
    ],
    interview: "Map a network request from UI action through auth, cache, API, error mapping, retry, and observability.",
    practice: "Write a network error model and map five failures: no internet, 401, 403, 429, and malformed JSON.",
  },
  "concurrency-threading-background-work": {
    title: "Concurrency & Background Work Golden Takeaways",
    description: "The practical rules for thread safety, WorkManager, foreground services, expedited work, and reliable background execution.",
    master: [
      "Use WorkManager for deferrable guaranteed work, foreground services for immediate user-visible long-running work, and coroutines for in-process async.",
      "Thread safety starts with reducing shared mutable state; use single-writer state, immutability, transactions, Mutex, and atomic updates.",
      "Background limits, battery policy, network constraints, and process death shape every background design.",
    ],
    tradeoffs: [
      "Expedited work improves urgency but is quota-limited and should not become the default path.",
      "Foreground services are powerful but user-visible and policy-sensitive.",
      "Chained workers clarify pipelines but require careful data passing, idempotency, and failure handling.",
    ],
    interview: "Classify the work first: immediate vs deferrable, user-visible vs invisible, guaranteed vs best effort, one-time vs periodic.",
    practice: "Design a photo upload pipeline with local queue, compression, network constraint, retry, notification, and cancellation.",
  },
  "testing-strategy": {
    title: "Testing Golden Takeaways",
    description: "The senior testing strategy: deterministic boundaries, meaningful fakes, CI gates, UI confidence, and migration safety.",
    master: [
      "Use unit tests for pure logic, ViewModel tests for state transitions, repository tests for data policy, and UI tests for critical user flows.",
      "Prefer fakes when behavior matters; use mocks sparingly for interaction verification.",
      "Inject dispatchers, clocks, random generators, and data sources so tests are deterministic.",
    ],
    tradeoffs: [
      "More UI tests increase confidence but can slow CI and create flakes.",
      "High coverage is less useful than coverage over risky decisions, edge cases, and regressions.",
      "End-to-end tests catch integration bugs but are expensive to debug without good logs and test data control.",
    ],
    interview: "Explain your test pyramid by risk and feedback speed, then give examples of bugs each layer catches.",
    practice: "For one feature, write a test plan covering reducer/domain, ViewModel, repository, Room migration, and Compose UI behavior.",
  },
  "performance-observability": {
    title: "Performance & Observability Golden Takeaways",
    description: "The production lens for startup, jank, memory, battery, APK size, logging, tracing, metrics, and incident response.",
    master: [
      "Measure before optimizing: startup timing, frame metrics, memory, network latency, battery, ANR, crash-free users, and conversion impact.",
      "Know tools: Perfetto, Macrobenchmark, Baseline Profiles, Android Studio profilers, LeakCanary, Play Console vitals, and crash analytics.",
      "Observability should classify failures and performance by app version, device, OS, network, feature, and user journey.",
    ],
    tradeoffs: [
      "Deferring startup work improves first frame but can shift latency into the first interaction.",
      "More logs help diagnosis but can expose privacy risk, cost money, and add noise.",
      "Shrinking and obfuscation reduce size and attack surface but require mapping files and crash decoding discipline.",
    ],
    interview: "Tie every performance answer to measurement, user impact, root cause, fix, and regression guard.",
    practice: "Pick one slow flow and define metrics, profiling plan, suspected causes, fix options, and CI/perf guardrail.",
  },
  "security-privacy-app-integrity": {
    title: "Security & Privacy Golden Takeaways",
    description: "The senior security baseline: threat modeling, secure storage, auth, permissions, app integrity, privacy, and payment hardening.",
    master: [
      "Never trust the client for authorization, entitlement, or tamper-proof business decisions.",
      "Understand secure storage, token lifecycle, biometric gating, Play Integrity, certificate pinning, obfuscation, and permission minimization.",
      "Privacy is architecture: collect less, store less, log less, encrypt where needed, and explain data use clearly.",
    ],
    tradeoffs: [
      "Biometrics improve local access control but do not replace server authorization.",
      "Certificate pinning improves security but adds operational cert-rotation risk.",
      "Obfuscation raises reverse-engineering cost but does not make local secrets safe.",
    ],
    interview: "Start with threat model, then explain mitigations, residual risk, monitoring, and incident response.",
    practice: "Threat-model login, token refresh, premium entitlement, local cache, logs, and network transport for one app.",
  },
  "build-release-ci-cd": {
    title: "Build, Release & CI/CD Golden Takeaways",
    description: "The delivery backbone: Gradle, CI quality gates, signing, release tracks, versioning, rollback, and build performance.",
    master: [
      "Know Gradle basics, Kotlin DSL, version catalogs, build variants, signing configs, caching, configuration cache, and CI reproducibility.",
      "CI should run fast checks early and expensive checks only where risk justifies them.",
      "Release engineering includes changelog, signing, Play tracks, staged rollout, monitoring, rollback, and mapping files.",
    ],
    tradeoffs: [
      "Strict CI improves quality but can slow teams if flakes and poor reports are ignored.",
      "More modular builds can improve parallelism but increase dependency management complexity.",
      "Automated deployment reduces manual mistakes but requires strong secrets, approvals, and rollback strategy.",
    ],
    interview: "Explain the pipeline from PR to production, including gates, artifacts, signing, release notes, rollout, and post-release monitoring.",
    practice: "Design a CI pipeline for a modular Android app with unit tests, lint, Compose tests, release build, and Play internal upload.",
  },
  "advanced-modern-android-topics": {
    title: "Advanced Android Golden Takeaways",
    description: "The differentiators: KMP, ML/AI, Firebase, app links, accessibility, localization, Play readiness, and modern platform shifts.",
    master: [
      "Advanced topics should connect to product value, not novelty: shared code, ML features, accessibility, app discovery, and production readiness.",
      "KMP is best for shared domain/data logic; ML Kit/TFLite are best when latency, privacy, or offline inference matter.",
      "Accessibility, localization, deep links, and Play policies are senior topics because they affect real users and release success.",
    ],
    tradeoffs: [
      "KMP reduces duplicated logic but adds tooling, dependency, debugging, and cross-team coordination cost.",
      "On-device ML improves privacy and latency but increases model size, device variability, and update complexity.",
      "Firebase accelerates features but can increase vendor coupling and architecture shortcuts.",
    ],
    interview: "For advanced topics, explain when you would adopt the technology, when you would avoid it, and how you would validate the decision.",
    practice: "Choose one advanced feature and write an adoption memo: value, risk, architecture, rollout, metrics, and fallback.",
  },
  "system-design-for-mobile": {
    title: "Mobile System Design Golden Takeaways",
    description: "The senior mobile design frame: requirements, client/backend split, offline-first, sync, scale, observability, and failure modes.",
    master: [
      "Mobile system design starts with product requirements, constraints, user journeys, and failure modes before diagrams.",
      "Separate client state, local persistence, API contracts, backend responsibilities, sync, auth, push, analytics, and rollout.",
      "Always discuss offline behavior, old app versions, network variability, battery, privacy, and observability.",
    ],
    tradeoffs: [
      "Client-side caching improves UX but requires invalidation and consistency strategy.",
      "Backend-driven UI enables flexibility but can reduce native polish and increase contract complexity.",
      "Real-time sync improves collaboration but costs battery, bandwidth, conflict handling, and backend complexity.",
    ],
    interview: "Structure answers as requirements -> high-level design -> data model -> APIs -> offline/sync -> failure modes -> observability -> trade-offs.",
    practice: "Design a mobile notes app that supports offline editing, multi-device sync, conflict resolution, sharing, and push notifications.",
  },
  "leadership-behavioral-questions": {
    title: "Leadership Golden Takeaways",
    description: "The senior behavioral core: technical judgment, influence, mentoring, delivery, conflict, ownership, and measurable outcomes.",
    master: [
      "Senior leadership is creating better decisions and stronger engineers, not merely owning the hardest tickets.",
      "Use RFCs, ADRs, design reviews, pairing, and postmortems to turn individual judgment into team learning.",
      "Great stories include context, constraint, action, trade-off, result, and what changed afterward.",
    ],
    tradeoffs: [
      "Consensus improves buy-in but can slow urgent decisions; know when to decide and when to facilitate.",
      "Mentoring takes time but pays back through reduced review load, fewer repeated mistakes, and stronger ownership.",
      "Technical debt negotiation requires business framing, not only engineering frustration.",
    ],
    interview: "Use STAR, but make the technical decision and measurable impact clear: reliability, speed, quality, cost, team health, or user outcome.",
    practice: "Prepare five stories: conflict, failure, mentoring, architecture decision, and production incident.",
  },
  "interview-preparation-strategy": {
    title: "Interview Strategy Golden Takeaways",
    description: "How to convert broad Android knowledge into clear senior interview performance.",
    master: [
      "Senior interviews reward structured reasoning, trade-offs, production examples, and communication under ambiguity.",
      "Prepare reusable stories for architecture, performance, testing, incidents, mentoring, and difficult trade-offs.",
      "Practice explaining one topic at three depths: 60-second summary, 5-minute design answer, and deep implementation details.",
    ],
    tradeoffs: [
      "Memorizing APIs helps less than explaining why and when you would choose them.",
      "Over-answering can obscure clarity; start concise, then invite deeper follow-up.",
      "Admitting uncertainty is fine when paired with a credible verification path.",
    ],
    interview: "Use a repeatable answer shape: clarify, propose, trade off, validate, monitor, and evolve.",
    practice: "Record yourself answering one architecture question and one behavioral question, then remove vague claims and add concrete evidence.",
  },
  "resources-references": {
    title: "Learning Resources Golden Takeaways",
    description: "How to keep Android knowledge current without drowning in outdated tutorials or tool churn.",
    master: [
      "Official docs, release notes, samples, issue trackers, and source code are the most reliable references for changing platform behavior.",
      "Tutorials are useful for speed, but production adoption needs verification against current APIs, target SDK behavior, and team constraints.",
      "A senior learning system turns resources into decisions, experiments, notes, and reusable team guidance.",
    ],
    tradeoffs: [
      "Following trends keeps skills current but can distract from fundamentals if not tied to real problems.",
      "Books build deep judgment but may lag behind modern Android APIs.",
      "Community answers are useful, but they need date/context validation before production use.",
    ],
    interview: "When asked how you stay current, mention your validation loop: read, experiment, compare docs, test, measure, and share.",
    practice: "Pick a new Android API and create a one-page adoption note with source links, constraints, sample code, and migration risk.",
  },
};

function makeTopic(data) {
  return {
    title: data.title,
    icon: "",
    description: data.description,
    content_sections: [
      {
        heading: "What To Master",
        points: data.master,
        subtopics: [],
      },
      {
        heading: "Senior Trade-Offs",
        points: data.tradeoffs,
        subtopics: [],
      },
      {
        heading: "Interview Framing",
        points: [data.interview],
        subtopics: [],
      },
      {
        heading: "Practice Prompt",
        points: [data.practice],
        subtopics: [],
      },
    ],
    code_blocks: [],
  };
}

for (const section of content) {
  const data = sectionTakeaways[section.id];
  if (!data) continue;

  section.topics = (section.topics || []).filter((topic) => topic.title !== data.title);
  section.topics.unshift(makeTopic(data));
}

fs.writeFileSync(contentPath, `${JSON.stringify(content, null, 2)}\n`);
console.log(`Enhanced golden takeaways for ${Object.keys(sectionTakeaways).length} sections`);
