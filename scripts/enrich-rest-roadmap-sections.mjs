import fs from "node:fs";
import path from "node:path";

const contentPath = path.join(process.cwd(), "data", "content.json");
const content = JSON.parse(fs.readFileSync(contentPath, "utf8"));
const heading = "Senior Deep Dive Expansion";

function getTopic(sectionId, topicTitle) {
  const section = content.find((item) => item.id === sectionId);
  if (!section) throw new Error(`Missing section ${sectionId}`);
  const topic = (section.topics || []).find((item) => item.title === topicTitle);
  if (!topic) throw new Error(`Missing topic ${sectionId} / ${topicTitle}`);
  return topic;
}

function upsertContentSection(topic, points, subtopics = []) {
  topic.content_sections = (topic.content_sections || []).filter((item) => item.heading !== heading);
  topic.content_sections.push({ heading, points, subtopics });
}

function upsertCodeBlocks(topic, codeBlocks = []) {
  topic.code_blocks = topic.code_blocks || [];
  for (const block of codeBlocks) {
    topic.code_blocks = topic.code_blocks.filter((item) => item.title !== block.title);
    topic.code_blocks.push({ language: "kotlin", ...block });
  }
}

const enrichments = [
  {
    sectionId: "android-fundamentals-platform-basics",
    topicTitle: "Lifecycle, State & Configuration Changes",
    points: [
      "Senior Android lifecycle knowledge is mostly about state ownership: what belongs in remember, rememberSaveable, ViewModel, SavedStateHandle, database, or backend.",
      "Configuration change is not the same as process death; configuration change preserves ViewModel, while process death requires explicit persistence or saved state restoration.",
      "Do not treat Activity lifecycle callbacks as a linear script. Dialogs, split-screen, PiP, permission prompts, predictive back, and task restoration create non-obvious paths.",
      "For user input, keep ephemeral UI state close to the screen but promote business-critical state to a ViewModel or persistence boundary.",
      "For interviews, explain how you would test lifecycle behavior: rotate, enable Don't keep activities, kill process from Recents/developer tools, and verify state recovery.",
      "Avoid storing Context, View, Activity, Fragment, or long-lived callbacks inside ViewModels; these are common leak and lifecycle bugs.",
    ],
    codeBlocks: [
      {
        title: "SavedStateHandle Restoration Boundary",
        code: "class DetailsViewModel(\n    savedStateHandle: SavedStateHandle,\n    private val repository: ItemRepository\n) : ViewModel() {\n    private val itemId: String = checkNotNull(savedStateHandle[\"itemId\"])\n\n    val uiState: StateFlow<DetailsUiState> = repository.observeItem(itemId)\n        .map { item -> DetailsUiState.Content(item) }\n        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), DetailsUiState.Loading)\n}",
      },
    ],
  },
  {
    sectionId: "jetpack-components-deep-dive",
    topicTitle: "WorkManager, Background Work & App Startup",
    points: [
      "Use WorkManager for deferrable, guaranteed work, not for immediate user-visible operations or long-running foreground interactions.",
      "Model workers as idempotent units because the system can retry them after process death, constraint changes, or app/device restart.",
      "Pass small inputs through Data and store larger payloads in a database or file, then pass stable IDs to the worker.",
      "Use unique work names to prevent duplicate sync jobs and define ExistingWorkPolicy intentionally: KEEP for de-dupe, REPLACE for newest intent, APPEND for ordered pipelines.",
      "Observe work state from the UI only as a progress signal; the source of truth should usually remain repository/database state.",
      "App Startup should initialize only the dependencies required before first frame; move analytics, remote config, and optional SDKs behind lazy boundaries.",
    ],
    codeBlocks: [
      {
        title: "Idempotent Sync Worker",
        code: "class SyncWorker(\n    context: Context,\n    params: WorkerParameters,\n    private val syncRepository: SyncRepository\n) : CoroutineWorker(context, params) {\n    override suspend fun doWork(): Result = runCatching {\n        syncRepository.syncPendingChanges()\n        Result.success()\n    }.getOrElse { error ->\n        if (error is IOException) Result.retry() else Result.failure()\n    }\n}",
      },
    ],
  },
  {
    sectionId: "modern-architecture-patterns",
    topicTitle: "The 3-Layer Clean Architecture",
    points: [
      "Clean Architecture is useful when dependency direction protects business rules from framework churn; it is harmful when it creates ceremony without independent domain decisions.",
      "Keep domain models free from Retrofit, Room, Compose, Android resource, and Parcelable concerns unless the app is intentionally small and the trade-off is explicit.",
      "Use cases should express business actions, not become one-line pass-through wrappers over repositories.",
      "Repository interfaces belong where the dependency direction needs them; in many Android apps, domain owns interfaces and data owns implementations.",
      "Mapping is not busywork when it isolates API instability, database migrations, nullability differences, and presentation formatting.",
      "Senior answers should explain where they would bend the architecture for speed and where they would enforce it for long-term maintainability.",
    ],
    codeBlocks: [
      {
        title: "Domain Use Case Boundary",
        code: "class RefreshFeedUseCase(\n    private val feedRepository: FeedRepository,\n    private val clock: Clock\n) {\n    suspend operator fun invoke(force: Boolean): RefreshResult {\n        val lastSync = feedRepository.lastSuccessfulSync()\n        if (!force && !lastSync.isStale(clock.now())) return RefreshResult.Skipped\n\n        return feedRepository.refreshFeed()\n    }\n}",
      },
    ],
  },
  {
    sectionId: "ui-toolkit-views-jetpack-compose",
    topicTitle: "Compose Internals",
    points: [
      "Compose performance starts with stability and invalidation boundaries: avoid forcing broad recomposition when only one row or one derived value changes.",
      "Hoist state when multiple composables need to read/write it; keep local state when the state is purely visual and has no business meaning.",
      "Use derivedStateOf for expensive values derived from frequently changing state, and rememberUpdatedState for latest lambdas captured by long-lived effects.",
      "LaunchedEffect should be keyed by the identity of the job you want to restart; unstable keys can create accidental loops or stale work.",
      "Lazy lists need stable keys for item identity, especially with animations, paging, selection, and item-local remembered state.",
      "Senior Compose interviews often test whether you understand recomposition is normal; the bug is unnecessary work or incorrect side effects during recomposition.",
    ],
    codeBlocks: [
      {
        title: "Stable LazyColumn State",
        code: "@Composable\nfun MessagesList(messages: List<Message>, onOpen: (String) -> Unit) {\n    LazyColumn {\n        items(\n            items = messages,\n            key = { message -> message.id }\n        ) { message ->\n            MessageRow(\n                message = message,\n                onClick = { onOpen(message.id) }\n            )\n        }\n    }\n}",
      },
    ],
  },
  {
    sectionId: "state-navigation",
    topicTitle: "Type-Safe Compose Navigation",
    points: [
      "Type-safe navigation reduces stringly typed route bugs, but it does not remove the need to decide ownership of state, deep links, and back stack behavior.",
      "Pass stable identifiers through routes, not large objects; load the real data from repository/database in the destination ViewModel.",
      "Treat navigation as an event produced by UI logic and executed by the navigation host, not as a repository or domain concern.",
      "For result passing, prefer explicit saved-state or shared ViewModel patterns only when the lifecycle and ownership are clear.",
      "Deep links should be validated like external input: parse, authorize, handle missing records, and recover gracefully.",
      "In modular apps, features should expose route contracts or navigation entry points without depending on the app shell implementation.",
    ],
    codeBlocks: [
      {
        title: "Route With Stable ID Only",
        code: "@Serializable\ndata class ArticleRoute(val articleId: String)\n\n@Composable\nfun ArticleRouteScreen(\n    route: ArticleRoute,\n    viewModel: ArticleViewModel = hiltViewModel()\n) {\n    val state by viewModel.observe(route.articleId).collectAsStateWithLifecycle()\n    ArticleScreen(state = state)\n}",
      },
    ],
  },
  {
    sectionId: "dependency-injection",
    topicTitle: "Hilt Deep Dive",
    points: [
      "Hilt scopes are lifecycle contracts: SingletonComponent for process-wide dependencies, ActivityRetained for ViewModel-adjacent state, ViewModelComponent for ViewModel-owned dependencies.",
      "Avoid injecting short-lived Android objects into longer-lived scopes; this is a common source of leaks and stale references.",
      "Use qualifiers when two bindings share a type but represent different policies, such as auth vs public OkHttp clients.",
      "Prefer constructor injection for app-owned classes; use modules for third-party builders, interfaces, framework objects, and assisted factories.",
      "Test replacement modules should preserve behavior contracts, not just return mocks that bypass important threading, error, or cache behavior.",
      "In interviews, compare Hilt and manual DI through team scale, generated code, test setup, startup cost, and explicitness.",
    ],
    codeBlocks: [
      {
        title: "Qualified Network Bindings",
        code: "@Qualifier\nannotation class AuthenticatedClient\n\n@Module\n@InstallIn(SingletonComponent::class)\nobject NetworkModule {\n    @Provides\n    @Singleton\n    @AuthenticatedClient\n    fun provideAuthenticatedClient(authInterceptor: AuthInterceptor): OkHttpClient =\n        OkHttpClient.Builder()\n            .addInterceptor(authInterceptor)\n            .build()\n}",
      },
    ],
  },
  {
    sectionId: "data-management-persistence",
    topicTitle: "Repository Pattern",
    points: [
      "A repository is a consistency boundary, not just a folder name. It decides cache policy, source priority, sync behavior, and error mapping.",
      "Offline-first repositories usually expose database-backed Flow and perform network refresh as a side effect that updates local storage.",
      "Do not expose DTOs or Entity objects to UI unless you intentionally accept API/database coupling in that feature.",
      "Use transactions when multiple tables must change together, especially for parent-child replacement and sync checkpoints.",
      "Model stale data explicitly: lastSyncedAt, dirty flags, pending operations, and conflict states beat hidden boolean flags.",
      "Senior interviews often expect you to explain read path and write path separately, including what happens when the network fails halfway.",
    ],
    codeBlocks: [
      {
        title: "Offline-First Repository",
        code: "class ArticleRepository(\n    private val api: ArticleApi,\n    private val dao: ArticleDao\n) {\n    fun observeArticles(): Flow<List<Article>> =\n        dao.observeArticles().map { entities -> entities.map { it.toDomain() } }\n\n    suspend fun refresh() {\n        val remote = api.getArticles().map { it.toEntity() }\n        dao.replaceAll(remote)\n    }\n}",
      },
    ],
  },
  {
    sectionId: "networking-apis",
    topicTitle: "API Response Handling",
    points: [
      "Response handling should separate transport errors, protocol errors, parsing errors, auth errors, validation errors, and domain-empty states.",
      "Use an error model that UI can act on: retryable, requires login, no connection, forbidden, rate-limited, invalid input, or unknown.",
      "Do not let every screen invent its own Retrofit try/catch mapping; centralize policy near the API/repository boundary.",
      "Retries should be conservative and classified. Retry timeouts and 5xx with backoff; do not blindly retry 400, 401, 403, or validation failures.",
      "For pagination, treat next keys, empty pages, refresh, append errors, and invalidation as separate states.",
      "Senior system design answers should include API contracts for idempotency, pagination, versioning, rate limits, and auth refresh.",
    ],
    codeBlocks: [
      {
        title: "Typed API Error Mapping",
        code: "sealed interface NetworkError {\n    data object NoConnection : NetworkError\n    data object Unauthorized : NetworkError\n    data object RateLimited : NetworkError\n    data class Server(val code: Int) : NetworkError\n    data class Unknown(val cause: Throwable) : NetworkError\n}\n\nsuspend fun <T> safeApiCall(block: suspend () -> T): Result<T> =\n    runCatching { block() }",
      },
    ],
  },
  {
    sectionId: "concurrency-threading-background-work",
    topicTitle: "Thread Safety",
    points: [
      "Thread safety in Android is mostly about shared mutable state: caches, repositories, singletons, database transactions, and UI state reducers.",
      "Prefer immutability and single-writer models before reaching for locks.",
      "Mutex is useful for suspending critical sections; synchronized is blocking and should be used carefully around coroutines.",
      "StateFlow updates should use update when the new value depends on the previous value.",
      "Room transactions protect database consistency, but they do not automatically protect in-memory caches around the database.",
      "Senior-level debugging includes looking for double clicks, repeated collectors, duplicate workers, and race conditions after rotation/process recreation.",
    ],
    codeBlocks: [
      {
        title: "Atomic StateFlow Update",
        code: "private val _state = MutableStateFlow(CartState())\nval state: StateFlow<CartState> = _state.asStateFlow()\n\nfun addItem(item: CartItem) {\n    _state.update { current ->\n        current.copy(items = current.items + item)\n    }\n}",
      },
    ],
  },
  {
    sectionId: "testing-strategy",
    topicTitle: "Test Architecture",
    points: [
      "A strong test strategy mirrors architecture boundaries: pure unit tests for domain, fake-backed ViewModel tests for presentation, integration tests for repositories, and UI tests for critical flows.",
      "Prefer fakes over mocks when behavior matters, especially for repositories, data sources, and clock/dispatcher abstractions.",
      "Test state transitions and side effects, not private methods. Private method tests usually indicate the unit boundary is wrong.",
      "Compose tests should use semantic nodes and user-visible behavior instead of fragile implementation details.",
      "Instrumented tests are expensive; reserve them for framework integration, database migrations, navigation, permissions, and top business flows.",
      "Senior engineers should know how to make tests deterministic: injected dispatchers, fake clocks, controlled flows, seeded data, and no real network.",
    ],
    codeBlocks: [
      {
        title: "ViewModel Test With Fake Repository",
        code: "@Test\nfun `refresh exposes content`() = runTest {\n    val repository = FakeArticleRepository()\n    repository.articles.value = listOf(Article(\"1\", \"Testing\"))\n\n    val viewModel = ArticlesViewModel(repository)\n\n    assertEquals(\n        ArticlesUiState.Content(listOf(ArticleUiModel(\"Testing\"))),\n        viewModel.uiState.value\n    )\n}",
      },
    ],
  },
  {
    sectionId: "performance-observability",
    topicTitle: "App Startup Optimization",
    points: [
      "Startup optimization starts with measurement: cold/warm/hot startup, time to first draw, first interactive state, and slow frame attribution.",
      "Move non-critical SDK initialization out of Application.onCreate and behind lazy, background, or first-use boundaries.",
      "Baseline Profiles improve startup and hot paths by guiding ART compilation, but they must cover real user journeys.",
      "Avoid synchronous disk, network, database, reflection-heavy DI, and large JSON parsing before first frame.",
      "Use Android Studio profilers, Perfetto, Macrobenchmark, startup timing logs, and Play Console vitals to connect local findings to production impact.",
      "Senior answers should include trade-offs: faster startup may defer work, but deferred work still needs scheduling, failure handling, and user-visible readiness.",
    ],
    codeBlocks: [
      {
        title: "Macrobenchmark Startup Skeleton",
        code: "@Test\nfun startup() = benchmarkRule.measureRepeated(\n    packageName = \"com.example.app\",\n    metrics = listOf(StartupTimingMetric()),\n    iterations = 10,\n    startupMode = StartupMode.COLD,\n    setupBlock = { pressHome() }\n) {\n    startActivityAndWait()\n}",
      },
    ],
  },
  {
    sectionId: "security-privacy-app-integrity",
    topicTitle: "Authentication & Authorization",
    points: [
      "Authentication proves identity; authorization decides allowed actions. Android clients should enforce UX-level gates but servers must enforce real authorization.",
      "Token refresh should be centralized, synchronized, and safe under concurrent API calls to avoid refresh storms.",
      "Store refresh tokens more carefully than access tokens, prefer encrypted storage where appropriate, and consider biometric-gated access only when the product needs it.",
      "Never log tokens, PII, auth headers, one-time codes, or decrypted secrets.",
      "Handle auth failure as a state transition: clear protected caches if required, navigate intentionally, and preserve non-sensitive local data.",
      "For interviews, discuss threat model: rooted devices, reverse engineering, replay, MITM, local storage extraction, and compromised sessions.",
    ],
    codeBlocks: [
      {
        title: "Single-Flight Token Refresh",
        code: "class TokenRefresher(\n    private val authApi: AuthApi\n) {\n    private val mutex = Mutex()\n\n    suspend fun refresh(current: Tokens): Tokens = mutex.withLock {\n        if (!current.isExpiredSoon()) return current\n        authApi.refresh(current.refreshToken)\n    }\n}",
      },
    ],
  },
  {
    sectionId: "build-release-ci-cd",
    topicTitle: "Code Quality Gates",
    points: [
      "Quality gates should be fast locally and strict in CI: format, lint, unit tests, dependency checks, build, and targeted instrumentation where risk warrants it.",
      "Failing gates should produce actionable output, not just red builds; publish reports for lint, tests, coverage, and static analysis.",
      "Keep CI workflows close to local commands so developers can reproduce failures without guessing hidden build-server behavior.",
      "Use Gradle build cache and configuration cache carefully, then monitor flakes separately from real failures.",
      "Gate release branches with versioning, signing, changelog, Play Console track upload, smoke tests, and rollback notes.",
      "Senior engineers should treat CI as product infrastructure: owned, measured, maintained, and improved with the same seriousness as app code.",
    ],
    codeBlocks: [
      {
        title: "Quality Gate Gradle Task Group",
        code: "tasks.register(\"qualityCheck\") {\n    group = \"verification\"\n    dependsOn(\n        \"ktlintCheck\",\n        \"detekt\",\n        \"lintDebug\",\n        \"testDebugUnitTest\"\n    )\n}",
      },
    ],
  },
  {
    sectionId: "advanced-modern-android-topics",
    topicTitle: "KMP Fundamentals",
    points: [
      "KMP is strongest when sharing business logic, data models, validation, networking, persistence policy, and domain rules, while keeping platform UI native where needed.",
      "Expect/actual should be reserved for genuine platform differences, not used to hide every dependency behind a custom abstraction.",
      "Shared modules need the same engineering discipline as Android modules: tests, API boundaries, dependency hygiene, binary compatibility, and release strategy.",
      "Coroutines and Flow are natural shared primitives, but lifecycle collection and UI state adaptation remain platform-specific.",
      "KMP adoption should start with low-risk shared logic before moving persistence, networking, or complex platform integrations.",
      "Senior answers should cover team costs: iOS collaboration, debugging, build time, dependency maturity, and ownership of shared code.",
    ],
    codeBlocks: [
      {
        title: "Shared Repository Contract",
        code: "interface SettingsRepository {\n    val settings: Flow<AppSettings>\n    suspend fun updateTheme(theme: ThemeMode)\n}\n\nclass ObserveSettingsUseCase(\n    private val repository: SettingsRepository\n) {\n    operator fun invoke(): Flow<AppSettings> = repository.settings\n}",
      },
    ],
  },
  {
    sectionId: "system-design-for-mobile",
    topicTitle: "Scalability Considerations",
    points: [
      "Mobile scalability is not only backend QPS; it includes offline behavior, sync conflicts, battery cost, payload size, cold start, observability, and release safety.",
      "Design read paths and write paths separately: cached reads can be fast and offline, while writes need idempotency, retries, conflict resolution, and user feedback.",
      "Use pagination, delta sync, compression, and field selection to control data transfer and memory pressure.",
      "Plan for feature flags and backward-compatible APIs because old app versions remain in the wild after backend changes.",
      "Observability must include client version, network type, endpoint, latency, error category, and user journey so production issues can be segmented.",
      "Senior system design answers should explicitly state what happens during airplane mode, auth expiry, server outage, app upgrade, and partial sync failure.",
    ],
    codeBlocks: [
      {
        title: "Idempotent Sync Command",
        code: "data class PendingCommand(\n    val idempotencyKey: String,\n    val type: CommandType,\n    val payload: String,\n    val createdAt: Instant\n)\n\nsuspend fun flushPendingCommands() {\n    pendingCommandDao.oldestFirst().forEach { command ->\n        api.sendCommand(command.idempotencyKey, command.payload)\n        pendingCommandDao.delete(command.idempotencyKey)\n    }\n}",
      },
    ],
  },
  {
    sectionId: "leadership-behavioral-questions",
    topicTitle: "Technical Leadership",
    points: [
      "Senior technical leadership is about increasing team decision quality, not being the person who writes the cleverest code.",
      "Good architecture proposals include context, constraints, options, trade-offs, migration plan, risk, validation, and rollback.",
      "Mentorship should create independence: pair on reasoning, review patterns, ask design questions, and document principles.",
      "When disagreeing, separate goals from solutions. Align on user/business constraints before debating implementation details.",
      "Use RFCs or lightweight ADRs for decisions that affect multiple teams, long-lived contracts, or release risk.",
      "Strong behavioral stories include measurable outcomes: build time reduced, crash rate lowered, review time improved, onboarding shortened, or incident recurrence prevented.",
    ],
    codeBlocks: [],
  },
  {
    sectionId: "interview-preparation-strategy",
    topicTitle: "During the Interview",
    points: [
      "For senior interviews, answer in layers: clarify requirements, state assumptions, propose a simple design, identify risks, then deepen into trade-offs.",
      "When asked a coding question, narrate invariants and edge cases before optimizing; correctness and communication beat silent speed.",
      "For architecture questions, name what you would measure: startup, jank, crash-free users, latency, battery, build time, or test flake rate.",
      "Use production language: rollout, migration, observability, failure mode, backward compatibility, privacy, and rollback.",
      "If you do not know a detail, say how you would verify it using docs, source, experiments, or profiling rather than bluffing.",
      "Close answers by explaining what would change at larger scale or with different constraints.",
    ],
    codeBlocks: [],
  },
  {
    sectionId: "resources-references",
    topicTitle: "Official Documentation",
    points: [
      "Use official docs as the source of truth for platform behavior, especially permissions, background limits, target SDK changes, Play policies, and security APIs.",
      "Check publication/update dates for blog posts and tutorials because Android guidance ages quickly.",
      "Validate third-party advice against AndroidX release notes, Kotlin release notes, official samples, issue trackers, and source when behavior is subtle.",
      "For new APIs, create a small spike project before committing an app-wide architecture direction.",
      "Keep a team knowledge base with decisions, migration notes, gotchas, and links to the exact docs that justified the choice.",
      "A senior engineer should know where to look faster than they can memorize every API.",
    ],
    codeBlocks: [],
  },
];

for (const item of enrichments) {
  const targetTopic = getTopic(item.sectionId, item.topicTitle);
  upsertContentSection(targetTopic, item.points, item.subtopics || []);
  upsertCodeBlocks(targetTopic, item.codeBlocks || []);
}

fs.writeFileSync(contentPath, `${JSON.stringify(content, null, 2)}\n`);
console.log(`Enriched ${enrichments.length} roadmap topics outside Kotlin Coroutines & Flow`);
