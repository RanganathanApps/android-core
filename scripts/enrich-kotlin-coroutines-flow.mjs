import fs from "node:fs";
import path from "node:path";

const contentPath = path.join(process.cwd(), "data", "content.json");
const content = JSON.parse(fs.readFileSync(contentPath, "utf8"));

const section = content.find((item) => item.id === "kotlin-coroutines-flow");
if (!section) throw new Error("Missing kotlin-coroutines-flow section");

function topic(title) {
  const item = (section.topics || []).find((candidate) => candidate.title === title);
  if (!item) throw new Error(`Missing topic: ${title}`);
  return item;
}

function upsertContentSection(targetTopic, heading, points, subtopics = []) {
  targetTopic.content_sections = (targetTopic.content_sections || []).filter((item) => item.heading !== heading);
  targetTopic.content_sections.push({ heading, points, subtopics });
}

function upsertCodeBlock(targetTopic, title, code) {
  targetTopic.code_blocks = (targetTopic.code_blocks || []).filter((item) => item.title !== title);
  targetTopic.code_blocks.push({ language: "kotlin", title, code });
}

const coroutines = topic("Coroutines Deep Dive");
const flow = topic("Flow Advanced Patterns");
const kotlin = topic("Kotlin Essentials for Android");

upsertContentSection(coroutines, "Production Coroutine Patterns", [
  "Structured concurrency is the default safety model: every launched coroutine should have an owner, a cancellation path, and a clear reason to outlive the caller.",
  "Use viewModelScope for UI-related work, lifecycleScope/repeatOnLifecycle for screen collection, and app-level scopes only for explicitly process-wide work such as sync managers.",
  "Use coroutineScope when sibling failure should cancel the whole operation; use supervisorScope when independent child work should fail in isolation.",
  "Dispatchers are a boundary decision: Main for UI, IO for blocking I/O, Default for CPU work, and limitedParallelism when a shared dispatcher needs backpressure.",
  "Never hide long-running fire-and-forget work inside repositories without documenting ownership; return suspend functions or Flow so the caller owns cancellation.",
  "Cancellation is cooperative: CPU loops need ensureActive/yield checks, suspend calls need correct propagation, and cleanup should be short even inside NonCancellable.",
  "In interviews, explain not only which dispatcher you use, but why the work is blocking, CPU-bound, UI-bound, or externally owned.",
]);

upsertContentSection(coroutines, "Failure, Timeout & Parallelism", [
  "Wrap only the boundary that can fail; a giant try/catch around the whole ViewModel often hides which dependency failed and makes retry behavior vague.",
  "Use withTimeout for user-visible deadlines and supervisorScope for partial results when some parallel requests can fail without invalidating the whole screen.",
  "Prefer async for true parallel decomposition, not as a default replacement for suspend calls; if you immediately await one async, it usually adds noise.",
  "CoroutineExceptionHandler only observes uncaught exceptions from root launch coroutines; async exceptions are delivered through await.",
  "Expose domain errors intentionally with Result, sealed error types, or UI state models instead of leaking transport exceptions directly to composables.",
  "For retry, combine retryWhen with error classification: retry transient network failures, do not retry validation errors, auth failures, or malformed server data forever.",
]);

upsertCodeBlock(
  coroutines,
  "Parallel Requests With Supervisor Scope",
  "suspend fun loadDashboard(userId: String): DashboardResult = supervisorScope {\n    val profile = async { profileRepository.getProfile(userId) }\n    val activity = async { activityRepository.getRecentActivity(userId) }\n    val recommendations = async { recommendationRepository.getRecommendations(userId) }\n\n    DashboardResult(\n        profile = runCatching { profile.await() }.getOrNull(),\n        activity = runCatching { activity.await() }.getOrDefault(emptyList()),\n        recommendations = runCatching { recommendations.await() }.getOrDefault(emptyList())\n    )\n}",
);

upsertCodeBlock(
  coroutines,
  "Dispatcher Injection for Testable Coroutines",
  "interface AppDispatchers {\n    val main: CoroutineDispatcher\n    val io: CoroutineDispatcher\n    val default: CoroutineDispatcher\n}\n\nclass UserRepository(\n    private val api: UserApi,\n    private val dispatchers: AppDispatchers\n) {\n    suspend fun loadUser(id: String): User = withContext(dispatchers.io) {\n        api.getUser(id).toDomain()\n    }\n}",
);

upsertContentSection(flow, "Cold vs Hot Flow Boundaries", [
  "Cold Flow starts work for each collector, which is ideal for declarative data pipelines but dangerous if every collector repeats expensive network or database work.",
  "StateFlow is a state holder: it always has a value, replays the latest value, and is the right default for screen UI state exposed by a ViewModel.",
  "SharedFlow is an event stream: configure replay and buffer policy deliberately, especially for navigation, snackbar, analytics, and one-off effects.",
  "Use stateIn to convert a cold repository stream into ViewModel state; use shareIn when multiple collectors should share upstream work without forcing a current-state model.",
  "Choose SharingStarted.WhileSubscribed for UI streams so upstream work stops after collectors disappear, usually with a short timeout to survive configuration changes.",
  "Avoid using SharedFlow as a hidden mutable event bus between unrelated modules; prefer explicit dependencies and typed contracts.",
]);

upsertContentSection(flow, "Operator Decision Guide", [
  "map transforms each emission; transform can emit zero, one, or many values; onEach is for side effects and should not change the value.",
  "flatMapLatest is correct for search, filters, and selected IDs because new input cancels stale work.",
  "flatMapMerge is for concurrent inner streams when order is less important than throughput; cap concurrency if upstream can emit quickly.",
  "flatMapConcat preserves order and waits for each inner flow, which is safer for sequential workflows but slower for independent work.",
  "combine emits whenever any input changes after all inputs have emitted; zip pairs emissions one-to-one and can stall if one side is slow.",
  "debounce reduces noisy input; distinctUntilChanged prevents redundant recomposition or duplicate queries; sample is useful for periodic snapshots.",
  "catch handles upstream exceptions only; place it before or after operators depending on which part of the pipeline you intend to protect.",
  "flowOn changes upstream execution context only; it does not move downstream collection or UI updates off Main.",
]);

upsertContentSection(flow, "Flow Testing & Debugging", [
  "Test Flow with runTest and deterministic dispatchers so delays, debounce windows, and timeout behavior are controlled.",
  "Assert the sequence of states, not just the final value, for loading-content-error flows.",
  "When testing StateFlow, set up the collector before triggering the action if intermediate states matter.",
  "For hot flows, explicitly handle replay and buffer behavior in tests so a passing test does not depend on timing accidents.",
  "Use fake repositories exposing MutableStateFlow or channel-backed flows; avoid sleeping in tests to wait for emissions.",
  "For production debugging, log at boundaries: upstream source, transformation failures, retry attempts, and UI collection lifecycle.",
]);

upsertCodeBlock(
  flow,
  "Search Flow With Cancellation",
  "val results: StateFlow<SearchUiState> = searchQuery\n    .debounce(300)\n    .map { it.trim() }\n    .distinctUntilChanged()\n    .flatMapLatest { query ->\n        if (query.length < 2) {\n            flowOf(SearchUiState.Idle)\n        } else {\n            repository.search(query)\n                .map<SearchResult, SearchUiState> { SearchUiState.Content(it.items) }\n                .onStart { emit(SearchUiState.Loading) }\n                .catch { emit(SearchUiState.Error) }\n        }\n    }\n    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), SearchUiState.Idle)",
);

upsertCodeBlock(
  flow,
  "Combining Offline Data With Sync State",
  "val uiState: StateFlow<ArticlesUiState> = combine(\n    articleDao.observeArticles(),\n    syncManager.syncState,\n    networkMonitor.isOnline\n) { articles, syncState, isOnline ->\n    ArticlesUiState(\n        articles = articles.map { it.toUiModel() },\n        isRefreshing = syncState is SyncState.Running,\n        showOfflineBanner = !isOnline\n    )\n}.stateIn(\n    scope = viewModelScope,\n    started = SharingStarted.WhileSubscribed(5_000),\n    initialValue = ArticlesUiState()\n)",
);

upsertCodeBlock(
  flow,
  "Testing StateFlow Emissions",
  "@Test\nfun `search emits loading then content`() = runTest {\n    repository.result = flowOf(SearchResult(listOf(Item(\"Flow\"))))\n    val viewModel = SearchViewModel(repository, testDispatcher)\n\n    val states = mutableListOf<SearchUiState>()\n    val job = launch { viewModel.results.take(3).toList(states) }\n\n    viewModel.onQueryChanged(\"flow\")\n    advanceUntilIdle()\n\n    assertEquals(SearchUiState.Idle, states[0])\n    assertEquals(SearchUiState.Loading, states[1])\n    assertEquals(SearchUiState.Content(listOf(Item(\"Flow\"))), states[2])\n    job.cancel()\n}",
);

upsertContentSection(kotlin, "Kotlin IO & Backend-Aware Android Notes", [
  "Kotlin IO essentials matter for Android when working with files, streams, uploads, downloads, caches, and large payloads; avoid reading large files fully into memory.",
  "Prefer buffered reads/writes for stream-heavy work and move blocking file operations to Dispatchers.IO.",
  "Close streams with use so file descriptors are released even when parsing or network upload fails.",
  "Backend-aware Android engineers should understand HTTP status codes, request validation, environment configuration, and server-side persistence because mobile system design depends on those contracts.",
  "When consuming Kotlin/Spring or Ktor backends from Android, align DTO validation, error response shape, pagination, auth refresh, and retry behavior across client and server.",
]);

upsertCodeBlock(
  kotlin,
  "Buffered File Copy on Dispatchers.IO",
  "suspend fun copyToCache(\n    input: InputStream,\n    outputFile: File,\n    dispatchers: AppDispatchers\n): File = withContext(dispatchers.io) {\n    outputFile.outputStream().buffered().use { output ->\n        input.buffered().use { source ->\n            source.copyTo(output)\n        }\n    }\n    outputFile\n}",
);

fs.writeFileSync(contentPath, `${JSON.stringify(content, null, 2)}\n`);
console.log("Enriched Kotlin, Coroutines & Flow section");
