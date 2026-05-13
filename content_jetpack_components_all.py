[
  {
    "id": "android-fundamentals-platform-basics",
    "title": "Android Fundamentals & Platform Basics",
    "description": "Covers the Android runtime model, app building blocks, process behavior, resources, permissions, storage, threading, and lifecycle rules that every senior Android engineer should be able to reason about without relying on framework magic.",
    "topics": [
      {
        "title": "Android Runtime, Process Model & App Startup",
        "icon": "",
        "description": "Explains what happens before the first screen appears: how Android installs, launches, isolates, and may later kill an app process.",
        "content_sections": [
          {
            "heading": "Runtime Model",
            "points": [
              "Android apps run in isolated Linux processes with a unique UID by default, which gives each app a private sandbox for files, memory, and permissions.",
              "ART (Android Runtime) executes app bytecode and combines ahead-of-time, just-in-time, and profile-guided compilation to balance startup, memory, and steady-state performance.",
              "The framework calls app components through Binder IPC and the main thread message loop; application code does not own the process entry point like a normal JVM main method.",
              "Process death can happen while the task remains in Recents, so state restoration must not assume that ViewModels, singletons, repositories, or in-memory caches are still alive."
            ]
          },
          {
            "heading": "Startup Flow",
            "points": [
              "Launcher selection resolves an intent with ACTION_MAIN and CATEGORY_LAUNCHER to the configured Activity.",
              "The system creates the process if needed, initializes the Application object, then creates the target Activity and drives it through lifecycle callbacks.",
              "Cold start includes process creation and class loading; warm start reuses an existing process; hot start brings an already-created Activity back to the foreground.",
              "Heavy initialization should be deferred, lazy, or moved behind App Startup / dependency boundaries because Application.onCreate runs before the first frame."
            ]
          },
          {
            "heading": "Senior Interview Focus",
            "points": [
              "Be able to explain why static singletons are not reliable persistence and why SavedStateHandle, Room, DataStore, or disk-backed caches are needed for process death.",
              "Know how to identify startup work using logcat, Perfetto, Startup Timing metrics, Baseline Profiles, and Android Studio profiling tools.",
              "Understand the difference between task, back stack, process, Activity instance, and app data; these concepts are often mixed up in interviews."
            ]
          }
        ],
        "code_blocks": [
          {
            "language": "kotlin",
            "title": "Application Startup Guard",
            "code": "class App : Application() {\n    override fun onCreate() {\n        super.onCreate()\n        // Keep this thin: initialize only process-wide essentials.\n        // Defer analytics, remote config, and heavy SDK work until needed.\n    }\n}"
          }
        ]
      },
      {
        "title": "Android Application Components",
        "icon": "",
        "description": "Details the core component types and the contracts the operating system uses to create, stop, restore, and communicate with them.",
        "content_sections": [
          {
            "heading": "Activities",
            "points": [
              "An Activity is a single focused UI entry point that owns a window, participates in the task back stack, and receives lifecycle callbacks from the system.",
              "Activity lifecycle is not just linear; configuration changes, multi-window mode, permission dialogs, process death, and back navigation can all change the path.",
              "Use onCreate for one-time UI setup, onStart/onStop for visible resource ownership, and onResume/onPause for foreground-only interactions such as sensors or camera preview.",
              "Avoid treating an Activity as a business-logic container; it should coordinate UI, lifecycle, navigation, and permission/result APIs."
            ]
          },
          {
            "heading": "Fragments",
            "points": [
              "A Fragment is a reusable portion of UI and behavior hosted by an Activity, with separate fragment and view lifecycles.",
              "The view lifecycle can be destroyed while the Fragment instance remains, so view bindings, collectors, and adapters should be scoped to viewLifecycleOwner.",
              "Fragment transactions are asynchronous by default and participate in a FragmentManager back stack that is distinct from the Activity task back stack.",
              "Modern Fragment apps usually pair FragmentManager with Navigation, Safe Args, shared ViewModels, and lifecycle-aware collection."
            ]
          },
          {
            "heading": "Services",
            "points": [
              "A Service performs work without a direct UI, but it still runs on the main thread unless the app explicitly moves work to another dispatcher, thread, or scheduler.",
              "Started services are for app-requested work, bound services expose an IPC-style interface, and foreground services require a visible notification and valid foreground service type.",
              "Long-running background work is heavily restricted; prefer WorkManager for deferrable guaranteed work and foreground services only for user-visible active operations.",
              "A service is not a magic background process keeper; the system can still kill the process under memory pressure or policy constraints."
            ]
          },
          {
            "heading": "Broadcast Receivers & Content Providers",
            "points": [
              "BroadcastReceivers react to system or app-wide events and must finish quickly because they run under strict execution limits.",
              "Manifest receivers are useful for explicit, policy-allowed broadcasts; dynamic receivers are better for lifecycle-scoped app behavior.",
              "Content Providers expose structured data across process boundaries using URIs, MIME types, permissions, and query/update/delete contracts.",
              "Providers are initialized early, so avoid expensive startup work inside ContentProvider.onCreate unless the provider truly owns that initialization."
            ]
          }
        ],
        "code_blocks": []
      },
      {
        "title": "Lifecycle, State & Configuration Changes",
        "icon": "",
        "description": "Focuses on the practical rules for keeping UI correct when screens rotate, processes die, windows resize, and users navigate away and back.",
        "content_sections": [
          {
            "heading": "Lifecycle Ownership",
            "points": [
              "LifecycleOwner exposes state transitions so observers can start and stop work safely instead of leaking Activities, Fragments, or Views.",
              "Activity, Fragment, Fragment view, NavBackStackEntry, and ProcessLifecycleOwner are different lifecycle scopes; choosing the wrong one creates stale UI or leaked work.",
              "repeatOnLifecycle is the preferred pattern for collecting flows from UI because it cancels and restarts collection as visibility changes.",
              "Compose has its own composition lifecycle, so remember, rememberSaveable, LaunchedEffect, DisposableEffect, and ViewModel scopes must be chosen deliberately."
            ]
          },
          {
            "heading": "State Categories",
            "points": [
              "Ephemeral UI state is temporary screen state such as expanded rows, selected tabs, text input, or scroll position.",
              "Screen UI state is derived from domain/data layers and should normally live in a ViewModel as immutable state exposed through StateFlow.",
              "Persistent state must survive process death and app restarts, so it belongs in Room, DataStore, files, or a remote source of truth.",
              "Saved instance state is for small restoration values, not large objects, repositories, bitmaps, database results, or network responses."
            ]
          },
          {
            "heading": "Configuration Changes",
            "points": [
              "Configuration changes can recreate Activities for rotation, locale, font scale, night mode, screen size, keyboard availability, and other resource-affecting changes.",
              "Do not opt out with configChanges as a default fix; it shifts responsibility for resource reloading and layout updates onto the app.",
              "ViewModel survives configuration changes but not final process death, so combine it with SavedStateHandle and persistent storage when restoration matters.",
              "Design UI state as a pure model that can be recreated from saved arguments plus repository data."
            ]
          }
        ],
        "code_blocks": [
          {
            "language": "kotlin",
            "title": "Lifecycle-Aware Flow Collection",
            "code": "viewLifecycleOwner.lifecycleScope.launch {\n    viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {\n        viewModel.uiState.collect { state ->\n            render(state)\n        }\n    }\n}"
          }
        ]
      },
      {
        "title": "Intents, Navigation & Inter-App Communication",
        "icon": "",
        "description": "Covers how Android components request actions, pass data, cross app boundaries, and preserve predictable navigation behavior.",
        "content_sections": [
          {
            "heading": "Intent Fundamentals",
            "points": [
              "Explicit intents target a known component and are preferred for in-app navigation or service calls.",
              "Implicit intents describe an action and data type, letting the system resolve a capable app or show a chooser.",
              "Intent extras should be small, typed, and stable; large payloads should be passed through a shared repository, database, file URI, or content provider.",
              "PendingIntent lets another process perform a future action as your app identity, so mutability flags and request-code uniqueness matter for security."
            ]
          },
          {
            "heading": "Task & Back Stack Rules",
            "points": [
              "A task is a user-facing stack of Activities, while a process is an OS execution container; one process can contain multiple Activities and one task can involve multiple apps.",
              "launchMode, taskAffinity, intent flags, document mode, and deep links can change how Activities are reused or placed in tasks.",
              "Predictive back and OnBackPressedDispatcher require apps to model back behavior explicitly instead of overriding legacy back key methods everywhere.",
              "Deep links should validate inputs, define a clear destination, and restore enough state for the target screen to render independently."
            ]
          }
        ],
        "code_blocks": [
          {
            "language": "kotlin",
            "title": "Safe Activity Result Pattern",
            "code": "private val pickImage = registerForActivityResult(\n    ActivityResultContracts.PickVisualMedia()\n) { uri: Uri? ->\n    if (uri != null) viewModel.onImageSelected(uri)\n}\n\nfun openPicker() {\n    pickImage.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))\n}"
          }
        ]
      },
      {
        "title": "Resources, Manifest, Permissions & App Compatibility",
        "icon": "",
        "description": "Explains how Android adapts one APK or app bundle to many devices, locales, densities, versions, and permission states.",
        "content_sections": [
          {
            "heading": "Resources & Qualifiers",
            "points": [
              "Resources are selected at runtime using qualifiers such as locale, density, night mode, smallest width, orientation, layout direction, and API level.",
              "Use density-independent units for layout, scalable pixels for text, vector drawables where appropriate, and resource aliases to avoid duplicated assets.",
              "Configuration-specific resources should express device adaptation, not business branching; app logic should not depend on which XML file was selected.",
              "Large screens, foldables, tablets, and desktop modes require adaptive layouts rather than phone-only assumptions."
            ]
          },
          {
            "heading": "Manifest Responsibilities",
            "points": [
              "The manifest declares app identity, components, permissions, features, exported boundaries, intent filters, backup behavior, foreground service types, and metadata.",
              "android:exported must be explicit for components with intent filters, and exported components should be treated as public attack surface.",
              "uses-feature controls Play Store filtering while runtime capability checks protect behavior on devices that technically install but lack hardware support.",
              "Manifest placeholders and build variants should be used carefully because they can change authorities, deep links, and app identity across environments."
            ]
          },
          {
            "heading": "Permissions & Privacy",
            "points": [
              "Dangerous permissions require runtime consent, and the app must handle denial, one-time grants, approximate location, auto-reset, and settings changes.",
              "Request permission at the moment of user intent and explain value through UI context rather than front-loading permission prompts at startup.",
              "Prefer privacy-preserving platform APIs such as Photo Picker, Credential Manager, and scoped storage instead of broad file or account access.",
              "Security-sensitive flows should validate caller identity, input URIs, exported components, WebView bridges, and PendingIntent mutability."
            ]
          }
        ],
        "code_blocks": []
      },
      {
        "title": "Storage, Threading & Performance Basics",
        "icon": "",
        "description": "Connects platform fundamentals to practical app quality: where data lives, where work runs, and how to avoid jank or ANRs.",
        "content_sections": [
          {
            "heading": "Storage Choices",
            "points": [
              "Use Room for structured relational data that needs queries, transactions, constraints, and observable invalidation.",
              "Use DataStore for small key-value or typed preference state, especially when SharedPreferences synchronization or main-thread blocking is a risk.",
              "Use app-specific files for private blobs and MediaStore or Photo Picker for user-owned media that should survive outside the app sandbox.",
              "Use the Storage Access Framework when the user intentionally grants document-level access across providers."
            ]
          },
          {
            "heading": "Threading Rules",
            "points": [
              "The main thread owns UI work and lifecycle callbacks; blocking it with disk, network, database, decoding, or heavy JSON parsing risks ANRs and jank.",
              "Coroutines do not automatically make work background; dispatch CPU work to Default and blocking IO to IO, while keeping UI updates on Main.",
              "Structured concurrency means child work should be tied to a scope that represents real ownership, such as viewModelScope, lifecycleScope, or an application-level scope.",
              "Cancellation must be cooperative, especially around loops, callbacks, database work, and network requests."
            ]
          },
          {
            "heading": "Performance Basics",
            "points": [
              "Jank happens when frames miss deadlines, often from main-thread work, excessive recomposition/layout, bitmap decoding, synchronization, or expensive RecyclerView binding.",
              "ANRs happen when the main thread is blocked too long during input, broadcast handling, service startup, or content provider operations.",
              "Memory leaks commonly come from keeping references to Activity, Fragment views, Context, callbacks, adapters, dialogs, or long-lived coroutine scopes.",
              "Measure before optimizing: use Layout Inspector, Memory Profiler, CPU Profiler, Perfetto, Macrobenchmark, and baseline profile reports."
            ]
          }
        ],
        "code_blocks": [
          {
            "language": "kotlin",
            "title": "Dispatcher Ownership",
            "code": "class UserRepository(\n    private val api: UserApi,\n    private val ioDispatcher: CoroutineDispatcher = Dispatchers.IO\n) {\n    suspend fun refreshUser(id: String): User = withContext(ioDispatcher) {\n        api.fetchUser(id)\n    }\n}"
          }
        ]
      }
    ]
  },
  {
    "id": "jetpack-components-deep-dive",
    "title": "Jetpack Components Deep Dive",
    "description": "Splits Jetpack into its own study section and covers lifecycle-aware architecture, persistence, background work, navigation, UI, security, testing, and performance components used in production Android apps.",
    "topics": [
      {
        "title": "Lifecycle, ViewModel & State Management",
        "icon": "",
        "description": "Covers the Jetpack architecture primitives that keep UI state predictable across lifecycle changes, configuration changes, and process recreation.",
        "content_sections": [
          {
            "heading": "ViewModel Responsibilities",
            "points": [
              "ViewModel owns screen state and UI-facing business logic, but it should not hold Activity, Fragment, View, or lifecycle-bound references.",
              "Expose immutable UI state, commonly with StateFlow, and keep MutableStateFlow private to prevent external mutation.",
              "Use SavedStateHandle for navigation arguments and small restoration keys that must survive process death.",
              "Model loading, content, empty, partial, and error states explicitly instead of scattering booleans across the UI."
            ]
          },
          {
            "heading": "LiveData, Flow & StateFlow",
            "points": [
              "LiveData is lifecycle-aware and still appears in legacy code, but Flow and StateFlow are preferred for coroutine-first data pipelines.",
              "StateFlow represents current state and always has a value; SharedFlow represents events or broadcasts when replay and buffering are configured intentionally.",
              "One-time UI events such as navigation, snackbar messages, and permission prompts should be modeled carefully to avoid re-delivery after rotation.",
              "Use collectAsStateWithLifecycle in Compose and repeatOnLifecycle in Views/Fragments to avoid collecting while the UI is stopped."
            ]
          },
          {
            "heading": "Unidirectional Data Flow",
            "points": [
              "UI sends intents or actions to the ViewModel, the ViewModel updates state, and the UI renders that state as the single source of truth.",
              "Reducers make state transitions explicit and easier to test, especially for complex screens with filters, pagination, offline mode, or optimistic updates.",
              "Avoid two-way hidden mutation between UI widgets and repositories; it makes lifecycle and process-death bugs harder to reproduce.",
              "Derive UI state from domain models at the boundary so composables/fragments stay focused on rendering."
            ]
          }
        ],
        "code_blocks": [
          {
            "language": "kotlin",
            "title": "StateFlow ViewModel Pattern",
            "code": "data class ProfileUiState(\n    val isLoading: Boolean = false,\n    val name: String = \"\",\n    val errorMessage: String? = null\n)\n\nclass ProfileViewModel(\n    private val repository: ProfileRepository,\n    savedStateHandle: SavedStateHandle\n) : ViewModel() {\n    private val userId: String = checkNotNull(savedStateHandle[\"userId\"])\n\n    private val _uiState = MutableStateFlow(ProfileUiState(isLoading = true))\n    val uiState: StateFlow<ProfileUiState> = _uiState.asStateFlow()\n\n    fun refresh() = viewModelScope.launch {\n        _uiState.update { it.copy(isLoading = true, errorMessage = null) }\n        runCatching { repository.loadProfile(userId) }\n            .onSuccess { profile -> _uiState.value = ProfileUiState(name = profile.name) }\n            .onFailure { error -> _uiState.update { it.copy(isLoading = false, errorMessage = error.message) } }\n    }\n}"
          }
        ]
      },
      {
        "title": "Room, DataStore & Offline-First Data",
        "icon": "",
        "description": "Explains how Jetpack persistence components support local-first screens, observable data, migrations, and durable user preferences.",
        "content_sections": [
          {
            "heading": "Room Database",
            "points": [
              "Room provides a typed abstraction over SQLite with compile-time query validation, schema export, migrations, transactions, and observable query invalidation.",
              "Entities model tables, DAOs model database operations, and Database classes define versioning, type converters, callbacks, and migrations.",
              "Use transactions for multi-step writes that must remain consistent, especially when replacing cached network data or updating relational tables.",
              "Export schemas and test migrations because broken migrations are production data-loss bugs, not just compile-time mistakes."
            ]
          },
          {
            "heading": "DataStore",
            "points": [
              "Preferences DataStore is useful for simple key-value settings; Proto DataStore is better for typed, schema-driven settings.",
              "DataStore is asynchronous, Flow-based, and avoids many main-thread and consistency issues associated with SharedPreferences.",
              "Keep DataStore small; it is not a replacement for Room, large documents, search indexes, or cache tables.",
              "Handle corruption, default values, and migration from SharedPreferences explicitly."
            ]
          },
          {
            "heading": "Offline-First Strategy",
            "points": [
              "A common pattern is network-bound resource: read local data first, refresh from network, write results to Room, and let observable queries update UI.",
              "Repositories should define the source-of-truth policy so UI code does not decide when cached data is valid.",
              "Sync systems need conflict strategy, retry policy, idempotent writes, tombstones or deletion markers, and clear user feedback for pending changes.",
              "Paging 3 with RemoteMediator connects local database paging to network pagination for scalable feeds."
            ]
          }
        ],
        "code_blocks": [
          {
            "language": "kotlin",
            "title": "Room DAO With Observable Query",
            "code": "@Dao\ninterface ArticleDao {\n    @Query(\"SELECT * FROM articles ORDER BY updatedAt DESC\")\n    fun observeArticles(): Flow<List<ArticleEntity>>\n\n    @Insert(onConflict = OnConflictStrategy.REPLACE)\n    suspend fun upsertAll(articles: List<ArticleEntity>)\n\n    @Query(\"DELETE FROM articles\")\n    suspend fun clear()\n}"
          }
        ]
      },
      {
        "title": "Navigation, Activity Result APIs & Modular Screens",
        "icon": "",
        "description": "Covers Jetpack Navigation and related APIs used to pass arguments, handle results, support deep links, and keep feature modules loosely coupled.",
        "content_sections": [
          {
            "heading": "Navigation Component",
            "points": [
              "Navigation centralizes destinations, arguments, actions, deep links, and back stack behavior for Fragment or Compose applications.",
              "Type-safe navigation reduces stringly-typed route bugs and makes destination contracts easier to refactor.",
              "Nested graphs help model feature flows such as onboarding, checkout, login, and settings without flattening every screen into one global graph.",
              "NavBackStackEntry provides lifecycle, SavedStateHandle, and ViewModelStore ownership for destination-scoped state."
            ]
          },
          {
            "heading": "Deep Links & Results",
            "points": [
              "Deep links should map external inputs into validated internal destinations, not directly trust arbitrary URI parameters.",
              "For Fragment navigation results, SavedStateHandle on the previous back stack entry can pass small result values back to the caller.",
              "Activity Result APIs replace request-code based startActivityForResult and permission callbacks with lifecycle-aware contracts.",
              "Navigation should be state-driven where possible so tests can verify destination decisions without launching full UI stacks."
            ]
          },
          {
            "heading": "Modular Navigation",
            "points": [
              "Feature modules should expose destination contracts rather than forcing other modules to know internal screen classes.",
              "Dynamic feature navigation requires graceful handling when a module is not installed yet.",
              "Avoid passing repository objects, ViewModels, or complex graphs through navigation arguments; pass stable IDs and load data at the destination.",
              "Keep app-level navigation orchestration separate from feature-level screen state."
            ]
          }
        ],
        "code_blocks": []
      },
      {
        "title": "WorkManager, Background Work & App Startup",
        "icon": "",
        "description": "Explains Jetpack APIs for reliable deferred work, dependency-aware startup, constraints, retries, and background execution limits.",
        "content_sections": [
          {
            "heading": "WorkManager Core Mechanisms",
            "points": [
              "WorkManager is for deferrable, guaranteed work that should eventually run even if the app process exits.",
              "OneTimeWorkRequest, PeriodicWorkRequest, constraints, input/output Data, tags, unique work names, and chaining define the execution contract.",
              "Workers must be idempotent because retries, process death, and scheduler handoff can cause work to run again.",
              "Use CoroutineWorker for suspend APIs and keep long-running foreground work explicit with foreground info when policy requires user visibility."
            ]
          },
          {
            "heading": "Reliability Patterns",
            "points": [
              "Use unique work policies to prevent duplicate sync jobs, upload storms, or multiple cleanup tasks.",
              "Backoff criteria should match failure type; retry transient network/server errors and fail fast for validation or authorization errors.",
              "Persist enough work input to resume after process death, but avoid stuffing large payloads into WorkManager Data.",
              "Observe work state for user-visible operations and expose progress when the user expects feedback."
            ]
          },
          {
            "heading": "App Startup",
            "points": [
              "Jetpack App Startup lets libraries and apps define initializers with dependencies instead of hiding work in ContentProviders.",
              "Disable automatic initialization for expensive SDKs when they are not needed before first screen.",
              "Startup should be measured with realistic builds because debug builds and emulators can hide or exaggerate bottlenecks.",
              "Baseline Profiles complement startup work reduction by precompiling hot paths for launch and common interactions."
            ]
          }
        ],
        "code_blocks": [
          {
            "language": "kotlin",
            "title": "Unique Sync Work",
            "code": "val request = OneTimeWorkRequestBuilder<SyncWorker>()\n    .setConstraints(\n        Constraints.Builder()\n            .setRequiredNetworkType(NetworkType.CONNECTED)\n            .build()\n    )\n    .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 30, TimeUnit.SECONDS)\n    .build()\n\nWorkManager.getInstance(context).enqueueUniqueWork(\n    \"account-sync\",\n    ExistingWorkPolicy.KEEP,\n    request\n)"
          }
        ]
      },
      {
        "title": "Compose, UI Toolkit & View Interoperability",
        "icon": "",
        "description": "Covers Jetpack UI components and the bridge between modern Compose screens and existing View-based applications.",
        "content_sections": [
          {
            "heading": "Compose Runtime Basics",
            "points": [
              "Compose renders UI from state, and recomposition updates only affected parts of the composition when observable state changes.",
              "remember keeps values across recompositions, rememberSaveable preserves small values across Activity recreation, and ViewModel owns screen-level state.",
              "Stable parameters, immutable UI models, keys in lazy lists, and derivedStateOf help avoid unnecessary recomposition or incorrect item reuse.",
              "Side effects belong in LaunchedEffect, DisposableEffect, SideEffect, rememberCoroutineScope, or produceState depending on ownership and cancellation rules."
            ]
          },
          {
            "heading": "Material, Windowing & Adaptive UI",
            "points": [
              "Material 3 provides design tokens, components, typography, color schemes, dynamic color, and accessibility defaults.",
              "Window size classes and adaptive layouts help support phones, tablets, foldables, ChromeOS, desktop mode, and split-screen.",
              "Compose semantics, content descriptions, focus order, contrast, font scaling, and touch targets are required for accessible production UI.",
              "Animation APIs should support meaning and continuity without hiding state changes or blocking interaction."
            ]
          },
          {
            "heading": "View Interop",
            "points": [
              "ComposeView lets existing Fragment or Activity screens host Compose while AndroidView lets Compose host legacy Views.",
              "Interop requires lifecycle and state ownership discipline because View disposal and composition disposal are not the same thing.",
              "Mixed apps should define clear boundaries: Compose for new surfaces, Views for stable legacy surfaces, and shared ViewModels/repositories for state.",
              "Testing strategy may need both Compose UI tests and Espresso when screens mix frameworks."
            ]
          }
        ],
        "code_blocks": []
      },
      {
        "title": "Paging, Hilt, Security & Testing Components",
        "icon": "",
        "description": "Groups production-scale Jetpack support libraries that senior engineers use to keep large Android apps maintainable, secure, and testable.",
        "content_sections": [
          {
            "heading": "Paging 3",
            "points": [
              "PagingSource loads chunks of data from a source, Pager exposes PagingData, and UI adapters or Compose lazy items render load states.",
              "RemoteMediator coordinates network and Room so feeds can load from local cache while fetching additional pages from a backend.",
              "Paging requires stable keys, sensible page sizes, refresh behavior, placeholders strategy, and user-friendly error/retry states.",
              "Do not mix manual pagination state with PagingData without a clear boundary; duplicate loading logic causes race conditions."
            ]
          },
          {
            "heading": "Hilt & Dependency Injection",
            "points": [
              "Hilt standardizes Dagger setup for Android classes and provides components scoped to Singleton, ActivityRetained, ViewModel, Activity, Fragment, View, and Service lifetimes.",
              "Constructor injection should be preferred for app classes while modules provide interfaces, builders, external SDKs, and objects the app cannot construct directly.",
              "Scope dependencies only when shared lifetime is required; over-scoping causes stale state and hidden memory retention.",
              "Testing with Hilt should replace bindings at the boundary and keep tests focused on observable behavior."
            ]
          },
          {
            "heading": "Security, Credentials & Biometrics",
            "points": [
              "Credential Manager unifies passkeys, passwords, and federated sign-in flows behind a modern Android identity API.",
              "BiometricPrompt provides a lifecycle-aware biometric authentication surface and should be paired with clear fallback and lockout handling.",
              "Encrypted local storage should use platform-backed keys where appropriate, but encryption does not replace access control, server validation, or threat modeling.",
              "Sensitive values should not be logged, placed in intents, stored in screenshots, or exposed through exported components."
            ]
          },
          {
            "heading": "Testing Libraries",
            "points": [
              "Use androidx.test for instrumentation, ActivityScenario for lifecycle control, FragmentScenario for isolated Fragment tests, and core-testing for architecture component rules.",
              "Compose UI tests verify semantics and user flows; Espresso remains useful for View-based screens and interop.",
              "Room can be tested with in-memory databases, migration tests, and DAO integration tests.",
              "WorkManager TestInitHelper and test drivers let tests control constraints, delays, and execution timing."
            ]
          }
        ],
        "code_blocks": [
          {
            "language": "kotlin",
            "title": "Hilt ViewModel Injection",
            "code": "@HiltViewModel\nclass FeedViewModel @Inject constructor(\n    private val repository: FeedRepository,\n    savedStateHandle: SavedStateHandle\n) : ViewModel() {\n    val feed = repository.observeFeed()\n        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())\n}"
          }
        ]
      }
    ]
  }
]
