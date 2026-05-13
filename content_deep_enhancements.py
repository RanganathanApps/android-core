"""Additional senior-level expansion blocks for the main Android guide.

The data shape appended here matches the existing guide structure:
section -> topics -> content_sections -> points/subtopics.
"""


SECTION_PROFILES = {
    "modern-architecture-patterns": {
        "lens": "architecture decision-making",
        "tradeoffs": "testability, module ownership, state consistency, build time, and team-scale maintainability",
        "failure_modes": "leaky boundaries, anemic use cases, duplicated models, circular dependencies, and navigation coupled to data layers",
        "signals": "explain why a pattern is chosen for a product constraint, not because it is fashionable",
    },
    "kotlin-coroutines-flow": {
        "lens": "structured asynchronous programming",
        "tradeoffs": "dispatcher choice, cancellation ownership, backpressure, error propagation, and lifecycle-aware collection",
        "failure_modes": "GlobalScope leaks, swallowed cancellation, unbounded flows, blocking calls on Main, and duplicate collectors after rotation",
        "signals": "trace coroutine lifetime and failure behavior from user action to repository and back to UI state",
    },
    "ui-toolkit-views-jetpack-compose": {
        "lens": "state-driven UI rendering",
        "tradeoffs": "recomposition cost, accessibility, adaptive layouts, animation meaning, and View/Compose interoperability",
        "failure_modes": "unstable parameters, excessive recomposition, lost state, nested scroll bugs, and accessibility regressions",
        "signals": "separate durable screen state from transient UI state and describe how the UI reacts to both",
    },
    "state-navigation": {
        "lens": "state restoration and destination ownership",
        "tradeoffs": "route type safety, SavedStateHandle usage, event delivery, deep-link validation, and back stack scoping",
        "failure_modes": "passing large objects through routes, re-triggered events, stale ViewModels, and inconsistent back behavior",
        "signals": "model navigation as a consequence of state and user intent rather than hidden UI side effects",
    },
    "dependency-injection": {
        "lens": "dependency ownership and object graph design",
        "tradeoffs": "scope lifetime, startup cost, test replacement, compile-time safety, and module boundaries",
        "failure_modes": "over-scoped mutable state, service locator drift, hidden dependencies, and DI modules that know too much",
        "signals": "justify scopes and bindings using lifecycle, ownership, and testability rather than personal preference",
    },
    "data-management-persistence": {
        "lens": "source-of-truth and durability",
        "tradeoffs": "cache freshness, migration safety, sync conflicts, transaction boundaries, and offline user experience",
        "failure_modes": "UI-owned caching rules, destructive migrations, main-thread storage, inconsistent local/remote state, and unbounded disk growth",
        "signals": "describe how data moves from network to disk to UI, including failure, retry, and process death",
    },
    "networking-apis": {
        "lens": "resilient client/server contracts",
        "tradeoffs": "timeouts, retries, idempotency, pagination, schema evolution, auth refresh, and observability",
        "failure_modes": "retry storms, token refresh races, brittle DTO mapping, missing cancellation, and poor error classification",
        "signals": "separate transport errors, protocol errors, domain failures, and recoverable user actions",
    },
    "concurrency-threading-background-work": {
        "lens": "work ownership under Android execution limits",
        "tradeoffs": "latency, reliability, user visibility, battery policy, constraints, and idempotency",
        "failure_modes": "duplicate jobs, foreground service misuse, blocking the main thread, lost progress, and non-idempotent retries",
        "signals": "choose between coroutine, WorkManager, foreground service, alarm, or server push based on the work contract",
    },
    "testing-strategy": {
        "lens": "confidence through layered verification",
        "tradeoffs": "test speed, determinism, fidelity, flakiness, fake boundaries, and regression coverage",
        "failure_modes": "over-mocked tests, UI-only coverage, unstable timing, shared state between tests, and missing migration checks",
        "signals": "explain what each test layer proves and which risks are intentionally left to another layer",
    },
    "performance-observability": {
        "lens": "measurement-driven quality",
        "tradeoffs": "startup, memory, frame time, battery, APK size, logging volume, and user-perceived latency",
        "failure_modes": "optimizing without traces, debug-only measurements, leaked contexts, excessive allocations, and noisy telemetry",
        "signals": "start with a reproducible metric, capture a trace, identify the bottleneck, then verify the fix",
    },
    "security-privacy-app-integrity": {
        "lens": "defense in depth for mobile clients",
        "tradeoffs": "local protection, server trust, user privacy, key management, abuse prevention, and recovery flows",
        "failure_modes": "secrets in APKs, exported component attacks, insecure WebView bridges, weak token storage, and over-trusting client signals",
        "signals": "treat the app as an untrusted client and explain which protections reduce risk rather than guarantee safety",
    },
    "build-release-ci-cd": {
        "lens": "repeatable delivery at scale",
        "tradeoffs": "build speed, reproducibility, cache correctness, signing security, rollout safety, and quality gates",
        "failure_modes": "non-hermetic builds, flaky CI, leaked signing keys, unversioned plugins, and release processes dependent on one person",
        "signals": "connect build choices to developer feedback time, release confidence, and incident recovery",
    },
    "advanced-modern-android-topics": {
        "lens": "emerging platform capability adoption",
        "tradeoffs": "device support, model size, privacy, battery, fallback behavior, and long-term maintenance",
        "failure_modes": "demo-only integrations, missing capability checks, inaccessible features, locale assumptions, and Play policy surprises",
        "signals": "explain rollout strategy, fallbacks, and measurement before adding an advanced platform feature",
    },
    "system-design-for-mobile": {
        "lens": "mobile constraints applied to distributed systems",
        "tradeoffs": "offline behavior, sync consistency, latency, bandwidth, battery, storage, observability, and failure recovery",
        "failure_modes": "server-only thinking, chatty APIs, no conflict model, weak pagination, and ignoring process death or network changes",
        "signals": "design from user journeys and failure modes, then map them to data, API, sync, and UI-state contracts",
    },
    "leadership-behavioral-questions": {
        "lens": "technical leadership under ambiguity",
        "tradeoffs": "speed, quality, alignment, mentorship, risk communication, and stakeholder trust",
        "failure_modes": "owning everything personally, hiding risk, vague feedback, architecture without adoption, and conflict avoidance",
        "signals": "tell stories with context, constraints, actions, measurable outcomes, and what changed afterward",
    },
    "interview-preparation-strategy": {
        "lens": "deliberate interview execution",
        "tradeoffs": "depth versus breadth, memorization versus reasoning, time management, communication, and practice feedback loops",
        "failure_modes": "reciting definitions, skipping clarifying questions, coding silently, ignoring edge cases, and weak project narratives",
        "signals": "make thinking visible, state assumptions, compare options, and tie answers back to product impact",
    },
    "resources-references": {
        "lens": "continuous learning and tool judgment",
        "tradeoffs": "official docs, source code, release notes, community knowledge, sample apps, and production constraints",
        "failure_modes": "copying outdated patterns, trusting snippets blindly, ignoring changelogs, and adding libraries without ownership",
        "signals": "explain how to evaluate a library, verify a pattern, and keep knowledge current as Android evolves",
    },
}


SECTION_ORDER = [
    "android-fundamentals-platform-basics",
    "jetpack-components-deep-dive",
    "kotlin-coroutines-flow",
    "modern-architecture-patterns",
    "ui-toolkit-views-jetpack-compose",
    "state-navigation",
    "dependency-injection",
    "data-management-persistence",
    "networking-apis",
    "concurrency-threading-background-work",
    "testing-strategy",
    "performance-observability",
    "security-privacy-app-integrity",
    "build-release-ci-cd",
    "advanced-modern-android-topics",
    "system-design-for-mobile",
    "leadership-behavioral-questions",
    "interview-preparation-strategy",
    "resources-references",
]


INTERVIEW_QA = {
    "android-fundamentals-platform-basics": [
        {
            "title": "An app returns from Recents with a blank screen after being killed in the background. How do you debug and fix it?",
            "description": "I would treat it as process death, not just a lifecycle bug. I would verify whether Activity arguments, SavedStateHandle, persisted screen state, and repository data are enough to recreate the screen. The fix is usually to persist durable state in Room/DataStore or reload it from a stable ID, keep only small restoration keys in saved state, and make the UI render loading, restored, and error states explicitly.",
        },
        {
            "title": "How do Activity, task, process, and back stack differ?",
            "description": "An Activity is a UI component instance, a task is the user-visible stack of Activities, a process is the OS execution container, and the back stack is the navigation history inside a task or navigation graph. Senior-level bugs often come from mixing these concepts, especially with deep links, launch modes, process death, and multi-window behavior.",
        },
        {
            "title": "When would you use a foreground service instead of WorkManager?",
            "description": "I would use WorkManager for deferrable guaranteed work and a foreground service only for active, user-visible work that must continue immediately, such as navigation, recording, or an ongoing upload with visible progress. I would also check Android background limits, foreground service type requirements, notification UX, cancellation, and battery impact.",
        },
        {
            "title": "How do you design for configuration changes without hiding problems using configChanges?",
            "description": "I keep UI state in a ViewModel, persist durable state outside memory, use SavedStateHandle for small restoration values, and make the UI render from state. I avoid configChanges unless there is a specific reason, because it makes the app responsible for resource reloading, layout adaptation, locale changes, night mode, and screen-size updates.",
        },
    ],
    "jetpack-components-deep-dive": [
        {
            "title": "How would you design a ViewModel for a complex screen with loading, pagination, filters, and errors?",
            "description": "I would expose one immutable UiState through StateFlow, keep MutableStateFlow private, model user actions as explicit events, and keep business rules in use cases or repositories. Pagination and filters should be part of state, errors should be recoverable, and one-time effects like navigation should not be stored as permanent screen state.",
        },
        {
            "title": "Room, DataStore, or files: how do you choose the right persistence API?",
            "description": "Room is for structured relational data, queries, transactions, migrations, and observable invalidation. DataStore is for small preference or typed settings. Files are for blobs or app-specific documents. I would avoid using DataStore as a database, avoid SharedPreferences for new async state, and test Room migrations as production-critical behavior.",
        },
        {
            "title": "What makes WorkManager reliable, and what can still go wrong?",
            "description": "WorkManager persists work specs and delegates execution through platform schedulers, so it is good for deferrable guaranteed work. It can still fail if work is not idempotent, inputs are too large, constraints are wrong, retries are unbounded, or unique work policies allow duplicate jobs. I design workers to resume safely and report observable state.",
        },
        {
            "title": "How do you prevent Navigation from becoming tightly coupled across modules?",
            "description": "I define destination contracts with stable arguments, pass IDs instead of objects, keep feature internals private, and let app-level navigation compose feature graphs. For results I use scoped SavedStateHandle or explicit callbacks at boundaries. Deep links must validate inputs before routing into feature screens.",
        },
    ],
    "kotlin-coroutines-flow": [
        {
            "title": "A coroutine keeps running after the screen closes. What do you check first?",
            "description": "I check which scope launched it. UI work should usually be in viewModelScope or lifecycle-aware collection, not GlobalScope or an unmanaged custom scope. I also check whether the suspend work is cooperative with cancellation and whether callbacks, flows, or blocking IO ignore cancellation.",
        },
        {
            "title": "How do StateFlow, SharedFlow, and Channel differ in Android UI?",
            "description": "StateFlow represents current state and always has a latest value. SharedFlow is useful for broadcast-style events when replay and buffering are chosen intentionally. Channel is point-to-point and can be useful internally, but UI events need careful lifecycle handling to avoid lost or repeated delivery.",
        },
        {
            "title": "When do you use Dispatchers.IO vs Default?",
            "description": "IO is for blocking network, file, and database calls. Default is for CPU work like parsing, sorting, diffing, and transformations. The important part is not to block Main and not to assume coroutines automatically make work background. Dispatcher ownership should be injectable for tests.",
        },
        {
            "title": "How do you test coroutine and Flow code deterministically?",
            "description": "I use runTest, a TestDispatcher, controlled virtual time, and Turbine or explicit collection for flows. I avoid real delays, avoid relying on thread timing, inject dispatchers, and assert both emitted states and cancellation/error behavior.",
        },
    ],
    "modern-architecture-patterns": [
        {
            "title": "How do you decide between MVVM and MVI for a production screen?",
            "description": "I use pragmatic MVVM for straightforward screens where state transitions are simple. I move toward MVI or reducer-style state when the screen has complex interactions, optimistic updates, undo, filters, pagination, or multiple async sources. The decision should reduce bugs and improve testability, not add ceremony.",
        },
        {
            "title": "What belongs in the domain layer in Clean Architecture?",
            "description": "The domain layer should hold business rules, use cases, and domain models that should not depend on Android UI or data frameworks. I keep it thin when rules are simple and stronger when logic is shared, test-heavy, or reused across features. I avoid creating empty use cases just to satisfy a diagram.",
        },
        {
            "title": "How do you prevent modularization from slowing the team down?",
            "description": "I define clear module ownership, dependency direction, public APIs, and build boundaries. I avoid tiny modules with no ownership value and large shared modules that become dumping grounds. The goal is faster builds, parallel work, clear contracts, and safer feature changes.",
        },
        {
            "title": "How do you review architecture decisions as a senior engineer?",
            "description": "I ask what problem the architecture solves, what alternatives were considered, how state and errors flow, how it will be tested, and what future change it makes easier or harder. I prefer decisions tied to product and team constraints over pattern-driven design.",
        },
    ],
    "ui-toolkit-views-jetpack-compose": [
        {
            "title": "A Compose screen is janky. How do you investigate?",
            "description": "I check recomposition counts, unstable parameters, expensive work in composition, lazy list keys, layout nesting, image loading, and main-thread work. I use Layout Inspector, traces, and macrobenchmarks where needed. The fix is usually to move work out of composition, stabilize models, and make state reads more focused.",
        },
        {
            "title": "How do you manage state in Compose?",
            "description": "I keep screen state in a ViewModel, expose immutable StateFlow, collect with lifecycle awareness, and use remember for local transient values. I use rememberSaveable only for small UI restoration and avoid duplicating domain state inside composables.",
        },
        {
            "title": "How do you migrate a large View-based app to Compose safely?",
            "description": "I start with isolated new screens or leaf components, keep shared ViewModels and repositories stable, use ComposeView or AndroidView at clear boundaries, and maintain existing tests while adding Compose UI tests. I avoid mixing frameworks randomly inside the same ownership boundary.",
        },
        {
            "title": "What accessibility issues do you look for in Android UI reviews?",
            "description": "I check semantic labels, touch target size, focus order, contrast, font scaling, TalkBack behavior, dynamic type, error announcements, and non-color-only status. Accessibility should be part of component design, not a final QA pass.",
        },
    ],
    "state-navigation": [
        {
            "title": "How do you handle one-time events like navigation or snackbars?",
            "description": "I avoid storing one-time events as permanent state that replays after rotation. Depending on the app, I use a SharedFlow with intentional buffering, an event wrapper, or state that is consumed through an explicit acknowledgement. The key is to test rotation and process recreation behavior.",
        },
        {
            "title": "What should be passed through navigation arguments?",
            "description": "I pass stable, small values such as IDs, filters, or route parameters. I do not pass repositories, ViewModels, large objects, bitmaps, or complex mutable state. The destination should load or derive data from its own stable contract.",
        },
        {
            "title": "How do you make deep links safe?",
            "description": "I validate the URI, required parameters, auth state, feature availability, and destination ownership before navigating. I also define fallback screens for invalid or expired links and test links from cold start, warm start, and logged-out states.",
        },
        {
            "title": "How do you scope ViewModels in nested navigation graphs?",
            "description": "I scope ViewModels to the smallest owner that matches the state lifetime: destination, graph, Activity, or shared parent. Graph-scoped state is useful for multi-step flows, but over-sharing can create stale state and accidental coupling.",
        },
    ],
    "dependency-injection": [
        {
            "title": "How do you choose DI scopes in Hilt?",
            "description": "I scope objects based on real lifetime and sharing needs. Stateless services often do not need a scope. Expensive app-wide dependencies can be Singleton. Screen state belongs in ViewModel scope. Over-scoping mutable objects is a common source of stale state and memory retention.",
        },
        {
            "title": "When would you avoid using a DI framework?",
            "description": "For very small apps, libraries, or simple object graphs, manual DI can be clearer and faster. I avoid forcing a framework where constructor injection and explicit factories are enough. The tradeoff is boilerplate versus compile-time safety, test replacement, and team consistency.",
        },
        {
            "title": "How do you keep DI modules from becoming dumping grounds?",
            "description": "I organize modules by ownership and dependency type, prefer constructor injection, expose interfaces at feature boundaries, and keep provider methods small. If a module knows too much about many layers, it is usually hiding architectural coupling.",
        },
        {
            "title": "How do you test code that uses Hilt?",
            "description": "I replace bindings at the boundary with fakes, keep tests focused on behavior, and avoid mocking every internal class. For ViewModels I test the class directly when possible; for integration tests I use Hilt test modules or uninstall modules carefully.",
        },
    ],
    "data-management-persistence": [
        {
            "title": "How do you design an offline-first repository?",
            "description": "I make local storage the source of truth, expose observable local data, refresh from network, write network results into Room inside transactions, and let UI update from database invalidation. Sync state, conflicts, retries, and user-visible pending changes must be explicit.",
        },
        {
            "title": "How do you handle Room migrations safely?",
            "description": "I export schemas, write migration tests, avoid destructive migrations for user data, and review defaults, nullability, indexes, and foreign keys. Migrations are production data transformations, so they need the same care as backend schema changes.",
        },
        {
            "title": "When is DataStore the wrong tool?",
            "description": "DataStore is wrong for large datasets, relational queries, search, paginated content, or frequently changing cache tables. It is best for small preferences or typed settings. For structured app data, Room is usually the better choice.",
        },
        {
            "title": "How do you prevent repositories from becoming god classes?",
            "description": "I keep repositories focused on data coordination for one domain, move business decisions into use cases when they grow, separate local/remote data sources, and expose clear models. A repository should not own UI state, navigation, or unrelated feature logic.",
        },
    ],
    "networking-apis": [
        {
            "title": "How do you design robust API error handling?",
            "description": "I separate transport errors, HTTP/protocol errors, serialization errors, auth failures, and domain-level failures. UI should receive a meaningful domain result, not raw exceptions everywhere. Retry should be limited to safe, transient, idempotent operations.",
        },
        {
            "title": "How do you handle token refresh races?",
            "description": "I centralize auth refresh in an OkHttp authenticator or a synchronized token manager, ensure only one refresh happens at a time, update persisted credentials atomically, and fail gracefully when refresh is rejected. I avoid each request trying to refresh independently.",
        },
        {
            "title": "When would you use GraphQL instead of REST on Android?",
            "description": "GraphQL is useful when clients need flexible shape selection, fewer round trips, and typed schemas. REST can be simpler for cacheable resource-oriented APIs. On Android I also consider generated models, normalized cache, schema evolution, pagination, and team backend maturity.",
        },
        {
            "title": "How do you make networking observable in production?",
            "description": "I track latency, status codes, failure categories, retry counts, payload size, timeout rates, and user-impacting flows. Logs must avoid sensitive data. Good observability lets the team distinguish client bugs, backend regressions, network conditions, and release-specific issues.",
        },
    ],
    "concurrency-threading-background-work": [
        {
            "title": "How do you choose between coroutines, WorkManager, foreground service, and alarms?",
            "description": "Coroutines are for in-process async work tied to a scope. WorkManager is for deferrable guaranteed work. Foreground services are for immediate user-visible ongoing work. Alarms are for time-based triggers with platform limits. The choice depends on urgency, reliability, visibility, and battery policy.",
        },
        {
            "title": "What makes a Worker production-safe?",
            "description": "A Worker should be idempotent, use stable inputs, respect constraints, classify retryable versus permanent failures, report progress when user-visible, and avoid large Data payloads. It should survive process death and not assume in-memory state.",
        },
        {
            "title": "How do you debug an ANR?",
            "description": "I inspect traces to see what blocked the main thread, correlate with logs and user action, check disk/network/database work on Main, lock contention, broadcast/service timeouts, and expensive rendering. The fix must be verified with traces, not just code inspection.",
        },
        {
            "title": "How do you prevent race conditions in shared state?",
            "description": "I reduce shared mutable state, use immutable models, confine mutation to one owner, and use Mutex, actors, database transactions, or atomic types when needed. I also test concurrent paths and cancellation because many races only appear under timing pressure.",
        },
    ],
    "testing-strategy": [
        {
            "title": "What should be covered by unit tests versus instrumentation tests?",
            "description": "Unit tests should cover business logic, reducers, mappers, use cases, and ViewModel state transitions quickly and deterministically. Instrumentation tests should cover framework behavior, navigation, Room integration, UI interactions, and device-specific behavior. I avoid pushing everything into slow UI tests.",
        },
        {
            "title": "How do you reduce flaky Android tests?",
            "description": "I remove real sleeps, control dispatchers and clocks, use idling resources or Compose test synchronization, isolate test data, avoid shared global state, and run tests on stable environments. Flakiness is usually a product issue in the test architecture, not just bad luck.",
        },
        {
            "title": "How do you test a ViewModel using StateFlow?",
            "description": "I inject fake repositories and test dispatchers, use runTest, collect emissions with Turbine or explicit collection, trigger user actions, and assert ordered UI states. I also test loading, success, empty, error, retry, and cancellation paths.",
        },
        {
            "title": "What is your test strategy for Room?",
            "description": "I use DAO tests with in-memory databases for query behavior, migration tests with exported schemas for version upgrades, and repository tests for transaction/source-of-truth behavior. Migration tests are especially important because failures can destroy real user data.",
        },
    ],
    "performance-observability": [
        {
            "title": "How do you approach app startup optimization?",
            "description": "I measure cold, warm, and hot start separately, inspect startup traces, defer non-critical SDK initialization, use App Startup intentionally, reduce main-thread work, and add Baseline Profiles for hot paths. I verify with release-like builds, not only debug builds.",
        },
        {
            "title": "How do you diagnose memory leaks?",
            "description": "I use LeakCanary and heap analysis to identify retained Activities, Fragment views, adapters, callbacks, dialogs, or coroutine scopes. Then I trace ownership and lifecycle cleanup. The fix is usually to scope references correctly and clear view-bound objects at the right lifecycle point.",
        },
        {
            "title": "What metrics matter for UI performance?",
            "description": "I look at frame time, jank percentage, slow/frozen frames, recomposition/layout cost, list binding time, image decode cost, and main-thread work. The useful metric is the one tied to a user journey, such as opening feed, scrolling search results, or checkout.",
        },
        {
            "title": "How do you use observability without leaking sensitive data?",
            "description": "I log structured events, error categories, and performance timings while redacting tokens, PII, payloads, and user-generated sensitive content. Good observability should explain impact and failure mode without becoming a privacy or security risk.",
        },
    ],
    "security-privacy-app-integrity": [
        {
            "title": "How do you store tokens securely on Android?",
            "description": "I avoid hardcoding secrets, store tokens using platform-backed encryption when appropriate, minimize token lifetime, and rely on server-side validation. Secure storage reduces local risk, but the mobile client is still not fully trusted, so backend controls remain essential.",
        },
        {
            "title": "What are common exported component risks?",
            "description": "Exported Activities, Services, Receivers, and Providers can be called by other apps. I validate inputs, require permissions where needed, avoid exposing sensitive data, check caller identity for privileged flows, and keep exported surfaces intentionally small.",
        },
        {
            "title": "How do you use Play Integrity correctly?",
            "description": "I treat Play Integrity as one risk signal, not a guarantee. The server should evaluate the verdict with account, device, behavioral, and transaction signals. The app should handle failures gracefully and avoid putting security decisions only on the client.",
        },
        {
            "title": "How do you review a WebView for security?",
            "description": "I check JavaScript bridges, allowed origins, file access, mixed content, URL loading, token exposure, downloads, and navigation interception. JavaScript interfaces should be minimal, origin-validated, and never expose privileged app operations blindly.",
        },
    ],
    "build-release-ci-cd": [
        {
            "title": "What does a healthy Android CI pipeline include?",
            "description": "It should run formatting/lint, unit tests, selected instrumentation or screenshot tests, build checks, dependency checks, and artifact generation. It should cache safely, fail fast, publish useful reports, and keep secrets isolated from logs and forks.",
        },
        {
            "title": "How do you manage Gradle build performance?",
            "description": "I use version catalogs, convention plugins, configuration cache where compatible, build cache, modular boundaries, and profiling. I avoid heavy logic in build scripts and track build scan data so optimization is based on evidence.",
        },
        {
            "title": "How do you release safely to the Play Store?",
            "description": "I use signed artifacts, staged rollout, internal testing tracks, release notes, crash monitoring, feature flags, and rollback/disable plans. A senior release plan includes observability and ownership after the button is clicked.",
        },
        {
            "title": "How do you protect signing keys and release secrets?",
            "description": "I use Play App Signing, restricted CI secrets, least-privilege service accounts, protected branches, audit logs, and no secrets in repo or build logs. Release access should be operationally convenient but not dependent on one person's laptop.",
        },
    ],
    "advanced-modern-android-topics": [
        {
            "title": "How do you decide whether to add ML Kit or on-device AI?",
            "description": "I start with the product value, latency, privacy, device support, offline needs, and fallback behavior. I also consider model size, battery impact, confidence thresholds, abuse cases, and whether the feature can be measured and improved after release.",
        },
        {
            "title": "How do you roll out an advanced feature safely?",
            "description": "I use capability checks, feature flags, staged rollout, metrics, crash monitoring, and server-side disablement where possible. I provide fallback UX and avoid blocking core flows on optional device-specific capabilities.",
        },
        {
            "title": "What are KMP adoption risks?",
            "description": "KMP works best for shared business logic, networking, validation, and persistence where teams agree on boundaries. Risks include tooling maturity, platform-specific UX needs, debugging complexity, dependency support, and forcing shared abstractions where native code is clearer.",
        },
        {
            "title": "How do you evaluate a Firebase integration?",
            "description": "I look at product need, data ownership, privacy, offline behavior, pricing, vendor lock-in, observability, and failure modes. Firebase can speed delivery, but the architecture should still isolate SDK calls behind app-owned interfaces.",
        },
    ],
    "system-design-for-mobile": [
        {
            "title": "How do you design an offline-first chat app?",
            "description": "I use local storage as the source of truth, optimistic sends with pending status, server acknowledgements, retry queues, conflict handling, pagination, push notifications, and sync after reconnect. UI should clearly show sent, pending, failed, and delivered states.",
        },
        {
            "title": "How do mobile constraints change system design?",
            "description": "Mobile adds intermittent network, limited battery, process death, storage limits, background restrictions, app upgrades, and varied devices. I design APIs and sync protocols to reduce round trips, support retries, and render useful local state.",
        },
        {
            "title": "How would you design a scalable feed?",
            "description": "I combine paginated APIs, local caching, stable item IDs, diffing, image prefetching, offline support, load states, and telemetry for scroll performance and freshness. I avoid pulling entire feeds and make refresh, pagination, and invalidation explicit.",
        },
        {
            "title": "How do you handle conflicts in mobile sync?",
            "description": "I first decide whether conflicts are possible and user-visible. Strategies include server wins, client wins, timestamp/version checks, merge rules, or user resolution. The important part is to preserve intent and avoid silent data loss.",
        },
    ],
    "leadership-behavioral-questions": [
        {
            "title": "Tell me about a time you changed an architecture direction.",
            "description": "I would describe the context, the pain, the options considered, how I got buy-in, and the measurable result. For an 11+ years role, the important part is not that I was right alone, but that I aligned the team and made the change adoptable.",
        },
        {
            "title": "How do you mentor mid-level Android engineers?",
            "description": "I give them ownership with guardrails, review tradeoffs instead of only code style, pair on debugging, and help them connect implementation choices to product outcomes. I also create reusable examples and encourage them to lead smaller design discussions.",
        },
        {
            "title": "How do you handle disagreement with product or backend teams?",
            "description": "I clarify the user impact, constraints, risks, and options. I avoid framing it as engineering versus product. The goal is a decision everyone understands, with explicit tradeoffs, owners, and follow-up metrics.",
        },
        {
            "title": "How do you communicate technical risk to leadership?",
            "description": "I translate risk into impact, probability, timeline, and options. Instead of saying something is bad, I explain what may happen, what mitigation costs, and what decision is needed. Clear tradeoffs build trust.",
        },
    ],
    "interview-preparation-strategy": [
        {
            "title": "How should an 11+ years Android engineer introduce themselves?",
            "description": "The answer should connect years of experience to scope: architecture, delivery, mentoring, debugging production issues, and cross-team influence. I would keep it concise and anchor it in two or three high-impact examples.",
        },
        {
            "title": "How do you answer when you do not know a detail?",
            "description": "I state what I know, identify the uncertain part, reason from fundamentals, and explain how I would verify it. Senior interviewers usually value clear reasoning and honesty more than pretending to remember every API detail.",
        },
        {
            "title": "How do you approach coding rounds at senior level?",
            "description": "I clarify requirements, discuss constraints, choose simple data structures, code incrementally, test edge cases, and narrate tradeoffs. Senior signal comes from correctness, communication, and ability to simplify under pressure.",
        },
        {
            "title": "What questions should you ask the interviewer?",
            "description": "I ask about architecture ownership, release quality, incident process, team collaboration, technical debt decisions, roadmap pressure, and how senior engineers are expected to influence beyond their tickets.",
        },
    ],
    "resources-references": [
        {
            "title": "How do you keep Android knowledge current?",
            "description": "I follow official Android docs, release notes, AndroidX changes, Kotlin updates, talks, issue trackers, and source samples. I validate new patterns through small experiments before recommending them to a team.",
        },
        {
            "title": "How do you evaluate a third-party library?",
            "description": "I check maintenance activity, API stability, transitive dependencies, binary size, security posture, license, testability, platform compatibility, and escape plan. A library should reduce owned complexity more than it adds operational risk.",
        },
        {
            "title": "How do you avoid outdated Android advice?",
            "description": "I compare advice against current docs, release dates, AndroidX recommendations, target SDK behavior, and production constraints. Android changes quickly, so I avoid copying snippets without checking lifecycle, permission, and background execution rules.",
        },
        {
            "title": "Which tools should a senior Android engineer be fluent with?",
            "description": "I expect fluency with Android Studio profilers, Layout Inspector, logcat, Gradle build scans, Perfetto, LeakCanary, lint, baseline profiles, Play Console, crash reporting, and CI reports. Tools matter because they turn opinions into evidence.",
        },
    ],
}


DEFAULT_PROFILE = {
    "lens": "Android engineering fundamentals",
    "tradeoffs": "lifecycle ownership, state restoration, compatibility, user experience, and operational reliability",
    "failure_modes": "unclear ownership, lifecycle leaks, process-death bugs, untested edge cases, and behavior that only works on the happy path",
    "signals": "connect the concept to a real production failure mode and explain how you would prevent or debug it",
}


def _profile_for(section_id):
    return SECTION_PROFILES.get(section_id, DEFAULT_PROFILE)


def _normalize_text(value):
    return " ".join(str(value or "").split())


def _dedupe_list(items, key_func):
    seen = set()
    deduped = []
    for item in items:
        key = key_func(item)
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def _dedupe_topic_content(topic):
    merged_sections = []
    section_by_heading = {}

    for content_section in topic.get("content_sections", []):
        heading = _normalize_text(content_section.get("heading"))
        if not heading:
            merged_sections.append(content_section)
            continue

        existing = section_by_heading.get(heading.lower())
        if existing is None:
            section_by_heading[heading.lower()] = content_section
            merged_sections.append(content_section)
            continue

        existing.setdefault("points", []).extend(content_section.get("points", []))
        existing.setdefault("subtopics", []).extend(content_section.get("subtopics", []))

    for content_section in merged_sections:
        content_section["points"] = _dedupe_list(
            content_section.get("points", []),
            lambda point: _normalize_text(point).lower(),
        )
        content_section["subtopics"] = _dedupe_list(
            content_section.get("subtopics", []),
            lambda subtopic: (
                _normalize_text(subtopic.get("title")).lower(),
                _normalize_text(subtopic.get("description")).lower(),
            ),
        )

    topic["content_sections"] = merged_sections


def _simplify_point(point):
    text = _normalize_text(point)
    if not text:
        return ""

    prefixes = (
        "Know why ",
        "Understand the main tradeoffs: ",
        "Watch for common issues: ",
        "Strong answer: ",
    )
    if any(text.startswith(prefix) for prefix in prefixes):
        return ""

    return text


def _takeaway_from_section(content_section):
    heading = _normalize_text(content_section.get("heading"))
    points = [
        _simplify_point(point)
        for point in content_section.get("points", [])
    ]
    points = [point for point in points if point]

    if points:
        selected = []
        for point in points:
            selected.append(point.rstrip("."))
            if len(" ".join(selected)) >= 90 or len(selected) == 3:
                break
        first = "; ".join(selected)
        if heading:
            return f"{heading}: {first}."
        return first + "."

    subtopics = content_section.get("subtopics", [])
    if subtopics:
        subtopic = subtopics[0]
        title = _normalize_text(subtopic.get("title"))
        description = _normalize_text(subtopic.get("description")).rstrip(".")
        if title and description:
            return f"{title}: {description}."
        if title:
            return title + "."
        if description:
            return description + "."

    return ""


def _build_key_points(topic):
    takeaways = []
    for content_section in topic.get("content_sections", []):
        heading = content_section.get("heading")
        if heading in {"Key Points", "Senior-Level Deep Dive"}:
            continue

        takeaway = _takeaway_from_section(content_section)
        if takeaway:
            takeaways.append(takeaway)

    takeaways = _dedupe_list(takeaways, lambda point: _normalize_text(point).lower())

    if len(takeaways) >= 4:
        return takeaways[:4]

    description = _normalize_text(topic.get("description"))
    if description:
        takeaways.insert(0, description.rstrip(".") + ".")

    title = _normalize_text(topic.get("title") or "This topic")
    while len(takeaways) < 3:
        fallback = f"{title}: understand the purpose, correct usage, and main production tradeoffs."
        if fallback in takeaways:
            break
        takeaways.append(fallback)

    return _dedupe_list(takeaways[:4], lambda point: _normalize_text(point).lower())


def _key_points_section_from_topic(topic):
    return {
        "heading": "Key Points",
        "points": _build_key_points(topic),
    }


def _interview_topic(section):
    section_title = _normalize_text(section.get("title") or "This section")

    qa_items = INTERVIEW_QA.get(section.get("id"))
    if qa_items is None:
        return None

    return {
        "title": "11+ Years Interview Questions",
        "icon": "",
        "description": f"Senior Android interview questions for {section_title}, written for engineers with around 11 years of production Android experience.",
        "content_sections": [
            {
                "heading": "Questions & Model Answers",
                "points": [],
                "subtopics": qa_items,
            }
        ],
        "code_blocks": [],
    }


def apply_deep_enhancements(content):
    """Clean, order, and enrich the merged guide content."""
    order_index = {section_id: index for index, section_id in enumerate(SECTION_ORDER)}
    content.sort(
        key=lambda section: (
            order_index.get(section.get("id"), len(SECTION_ORDER)),
            _normalize_text(section.get("title")).lower(),
        )
    )

    for section in content:
        section_id = section.get("id")
        section["topics"] = [
            topic
            for topic in section.get("topics", [])
            if _normalize_text(topic.get("title")) != "11+ Years Interview Questions"
        ]

        for topic in section.get("topics", []):
            content_sections = topic.setdefault("content_sections", [])

            topic["content_sections"] = [
                block
                for block in content_sections
                if block.get("heading") not in {"Key Points", "Senior-Level Deep Dive"}
            ]
            content_sections = topic["content_sections"]

            content_sections.insert(
                0,
                _key_points_section_from_topic(topic),
            )

            _dedupe_topic_content(topic)

        interview_topic = _interview_topic(section)
        if interview_topic:
            section.setdefault("topics", []).append(interview_topic)

    return content
