# Curated for senior modern Android interview preparation

from ast import literal_eval
from pathlib import Path

CONTENT = [
    {
        "id": "kotlin-coroutines-flow",
        "title": "Kotlin, Coroutines & Flow",
        "topics": [
            {
                "title": "Coroutines Deep Dive",
                "icon": "",
                "description": "Explains coroutine fundamentals and advanced interview-level "
                "concepts together, including dispatchers, scopes, structured "
                "concurrency, cancellation, and practical usage patterns in Android "
                "apps.",
                "content_sections": [
                    {
                        "heading": "Core Concepts",
                        "points": [
                            "Dispatchers determine which thread the coroutine "
                            "runs on: Main, IO, Default, or Unconfined",
                            "Structured concurrency ensures all coroutines are "
                            "cancelled when their scope is cancelled",
                            "SupervisorJob doesn't cancel siblings on failure - "
                            "useful for parallel operations",
                        ],
                    },
                    {
                        "heading": "When to Use Each Dispatcher",
                        "points": [],
                        "subtopics": [
                            {
                                "title": "Dispatchers.IO",
                                "description": "Network calls, database "
                                "operations, file I/O - "
                                "optimized for blocking tasks",
                            },
                            {
                                "title": "Dispatchers.Default",
                                "description": "CPU-intensive: JSON parsing, "
                                "image processing, sorting large "
                                "lists",
                            },
                            {
                                "title": "viewModelScope",
                                "description": "Automatically cancelled when "
                                "ViewModel is destroyed - use "
                                "for UI-related async",
                            },
                            {
                                "title": "lifecycleScope",
                                "description": "Tied to Activity/Fragment "
                                "lifecycle - auto-cancels when "
                                "lifecycle ends",
                            },
                        ],
                    },
                    {
                        "heading": "Dispatchers",
                        "points": [
                            "• Dispatchers.Main: UI operations",
                            "• Dispatchers.IO: Network, disk, database " "operations",
                            "• Dispatchers.Default: CPU-intensive work",
                            "• Dispatchers.Unconfined: Not recommended for "
                            "general use",
                        ],
                    },
                    {
                        "heading": "Coroutine Scopes",
                        "points": [
                            "• GlobalScope: app-wide (use sparingly)",
                            "• viewModelScope: tied to ViewModel lifecycle",
                            "• lifecycleScope: tied to Activity/Fragment " "lifecycle",
                            "• Custom CoroutineScope for specific components",
                        ],
                    },
                    {
                        "heading": "Coroutine Builders",
                        "points": [
                            "• launch: fire-and-forget",
                            "• async: returns Deferred<T>, use with await()",
                            "• runBlocking: blocks thread (tests only)",
                            "• withContext: switch dispatcher",
                        ],
                    },
                    {
                        "heading": "Exception Handling",
                        "points": [
                            "• try-catch in suspend functions",
                            "• CoroutineExceptionHandler for uncaught " "exceptions",
                            "• supervisorScope: child failure doesn't cancel "
                            "siblings",
                        ],
                    },
                    {
                        "heading": "Cancellation",
                        "points": [
                            "• Cooperative cancellation",
                            "• Check isActive before long operations",
                            "• ensureActive() throws if cancelled",
                            "• NonCancellable context for critical cleanup",
                        ],
                    },
                ],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: Proper Coroutine Scope Usage",
                        "code": "class UserViewModel(\n"
                        "    private val repository: UserRepository\n"
                        ") : ViewModel() {\n"
                        "\n"
                        "    // ViewModelScope - coroutines cancelled when "
                        "ViewModel is cleared\n"
                        "    fun loadUser(userId: String) {\n"
                        "        viewModelScope.launch {\n"
                        "            try {\n"
                        "                val user = repository.getUser(userId)\n"
                        "                _uiState.value = UiState.Success(user)\n"
                        "            } catch (e: Exception) {\n"
                        "                _uiState.value = UiState.Error(e.message)\n"
                        "            }\n"
                        "        }\n"
                        "    }\n"
                        "\n"
                        "    // Using withContext for thread switching\n"
                        "    suspend fun fetchAndProcess(): Result<Data> {\n"
                        "        val data = withContext(Dispatchers.IO) {\n"
                        "            api.fetchData()\n"
                        "        }\n"
                        "        val processed = withContext(Dispatchers.Default) "
                        "{\n"
                        "            processHeavy(data)\n"
                        "        }\n"
                        "        updateUI(processed)\n"
                        "    }\n"
                        "}",
                    }
                ],
            },
            {
                "title": "Flow Advanced Patterns",
                "icon": "",
                "description": "Combines practical Flow usage with interview-level reactive "
                "concepts, covering operators, builders, state streams, lifecycle "
                "collection, and how to model modern Android data flow.",
                "content_sections": [
                    {
                        "heading": "Key Flow Operators",
                        "points": [
                            "collectAsStateWithLifecycle - auto-cancels when "
                            "Activity stops, prevents leaks",
                            "flatMapLatest - cancels previous collection when "
                            "new value arrives (search debounce)",
                            "combine - merge multiple flows, re-emits when any "
                            "input changes",
                            "retryWhen - exponential backoff for network " "failures",
                        ],
                    },
                    {
                        "heading": "Flow Types Comparison",
                        "points": [],
                        "subtopics": [
                            {
                                "title": "StateFlow",
                                "description": "Holds single value, emits "
                                "current value to new collectors "
                                "- perfect for UI state",
                            },
                            {
                                "title": "SharedFlow",
                                "description": "Hot stream, emits to all new "
                                "collectors - ideal for one-time "
                                "events",
                            },
                            {
                                "title": "Flow",
                                "description": "Cold stream, produces values on "
                                "demand - use for data "
                                "transformations",
                            },
                            {
                                "title": "CallbackFlow",
                                "description": "Convert callbacks to Flow - "
                                "useful for legacy APIs and "
                                "event listeners",
                            },
                        ],
                    },
                    {
                        "heading": "Flow Builders",
                        "points": [
                            "• flow { ... }: basic flow builder",
                            "• flowOf(...): fixed set of values",
                            "• asFlow(): convert collections",
                            "• channelFlow: concurrent emissions",
                        ],
                    },
                    {
                        "heading": "Operators",
                        "points": [
                            "• Transformation: map, filter, transform",
                            "• Flattening: flatMapConcat, flatMapMerge, "
                            "flatMapLatest",
                            "• Combination: combine, zip, merge",
                            "• Terminal: collect, toList, first, reduce",
                        ],
                    },
                    {
                        "heading": "StateFlow vs SharedFlow",
                        "points": [
                            "• StateFlow: always has value, replays latest to "
                            "new collectors",
                            "• SharedFlow: configurable replay, can have no "
                            "initial value",
                            "• Use StateFlow for UI state",
                            "• Use SharedFlow for events",
                        ],
                    },
                ],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: StateFlow for UI State",
                        "code": "// StateFlow - holds single value, emits to new "
                        "collectors\n"
                        "private val _uiState = "
                        "MutableStateFlow<UiState>(UiState.Loading)\n"
                        "val uiState: StateFlow<UiState> = _uiState.asStateFlow()\n"
                        "\n"
                        "// SharedFlow - hot stream, emits to all new collectors\n"
                        "private val _events = MutableSharedFlow<Event>()\n"
                        "val events: SharedFlow<Event> = _events.asSharedFlow()\n"
                        "\n"
                        "// Collecting with lifecycle awareness\n"
                        "private fun observeUser() {\n"
                        "    viewModelScope.launch {\n"
                        "        viewModel.user.collectAsStateWithLifecycle { user "
                        "->\n"
                        "            updateUI(user)\n"
                        "        }\n"
                        "    }\n"
                        "}",
                    }
                ],
            },
            {
                "title": "Kotlin Language Features",
                "icon": "",
                "description": "Highlights the Kotlin features that most improve Android code "
                "quality, readability, and modeling of UI and domain state.",
                "content_sections": [
                    {
                        "heading": "Key Areas",
                        "subtopics": [
                            {
                                "title": "Sealed Classes",
                                "description": "Represent restricted "
                                "hierarchies - perfect for "
                                "UiState, Result, Event types",
                            },
                            {
                                "title": "Inline Functions",
                                "description": "reified enables runtime type "
                                "access: inline fun getType() = "
                                "T::class",
                            },
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Kotlin Essentials for Android",
                "icon": "",
                "description": "Reviews the Kotlin fundamentals senior Android engineers are "
                "expected to use fluently in everyday app development.",
                "content_sections": [
                    {
                        "heading": "Null Safety",
                        "points": [
                            "• Nullable types: String? vs String",
                            "• Safe call operator: obj?.method()",
                            "• Elvis operator: val name = user?.name ?: " '"Unknown"',
                            "• !! operator: forces non-null (use sparingly)",
                            "• let, run, with, apply, also scope functions",
                        ],
                    },
                    {
                        "heading": "Coroutines",
                        "points": [
                            "• Lightweight threads for asynchronous programming",
                            "• suspend functions: can be paused and resumed",
                            "• Dispatchers: Main, IO, Default, Unconfined",
                            "• CoroutineScope, viewModelScope, lifecycleScope",
                            "• Structured concurrency prevents memory leaks",
                            "• Example:",
                        ],
                    },
                    {
                        "heading": "Flow",
                        "points": [
                            "• Asynchronous data stream",
                            "• Cold stream: emits only when collected",
                            "• StateFlow: hot stream with state",
                            "• SharedFlow: hot stream for events",
                            "• Operators: map, filter, combine, flatMapLatest, " "etc.",
                            "• Preferred over LiveData in ViewModels",
                        ],
                    },
                    {
                        "heading": "Extension Functions",
                        "points": [
                            "• Add functions to existing classes without "
                            "inheritance",
                            '• fun String.toTitleCase() = this.split(" '
                            '").joinToString...',
                        ],
                    },
                    {
                        "heading": "Data Classes",
                        "points": [
                            "• Auto-generates equals(), hashCode(), toString(), "
                            "copy()",
                            "• data class User(val id: Int, val name: String)",
                            "• Ideal for models and DTOs",
                        ],
                    },
                    {
                        "heading": "Sealed Classes",
                        "points": [
                            "• Restricted class hierarchies",
                            "• Perfect for representing state:",
                        ],
                    },
                ],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Coroutines Example",
                        "code": "viewModelScope.launch {\n"
                        "    val result = withContext(Dispatchers.IO) {\n"
                        "        repository.fetchData()\n"
                        "    }\n"
                        "    _uiState.value = result\n"
                        "}",
                    },
                    {
                        "language": "kotlin",
                        "title": "Sealed Classes Example",
                        "code": "sealed class UiState {\n"
                        "    object Loading : UiState()\n"
                        "    data class Success(val data: List<Item>) : UiState()\n"
                        "    data class Error(val message: String) : UiState()\n"
                        "}",
                    },
                ],
            },
            {
                "title": "Java Key Concepts",
                "icon": "",
                "description": "Covers the Java foundations that still matter when working in mixed "
                "codebases, understanding older Android projects, or discussing "
                "runtime behavior.",
                "content_sections": [
                    {
                        "heading": "Garbage Collection",
                        "points": [
                            "• Automatic memory management",
                            "• Generational GC: Young, Old, Permanent " "generations",
                            "• Avoid memory leaks: static references, "
                            "listeners, handlers",
                        ],
                    },
                    {
                        "heading": "Concurrency (pre-Kotlin)",
                        "points": [
                            "• Thread, Runnable, Executor framework",
                            "• AsyncTask (deprecated - use Coroutines)",
                            "• Handler & Looper for thread communication",
                            "• synchronized keyword and locks",
                        ],
                    },
                    {
                        "heading": "Collections",
                        "points": [
                            "• List, Set, Map interfaces",
                            "• ArrayList, LinkedList, HashMap, TreeMap, HashSet",
                            "• Thread-safe: Vector, ConcurrentHashMap",
                        ],
                    },
                ],
                "code_blocks": [],
            },
        ],
        "description": "Covers Kotlin language fluency plus the coroutine and Flow patterns that power "
        "modern Android concurrency, state propagation, and reactive UI updates.",
    },
    {
        "id": "ui-toolkit-views-jetpack-compose",
        "title": "UI Toolkit: Views & Jetpack Compose",
        "topics": [
            {
                "title": "Compose Internals",
                "icon": "",
                "description": "Understanding recomposition is crucial for performance. Compose only "
                "recomposes what actually changed. Learning these internals helps "
                "avoid common performance pitfalls and build smooth UIs.",
                "content_sections": [
                    {
                        "heading": "Performance Optimization",
                        "points": [
                            "@Stable and @Immutable annotations tell Compose a "
                            "type won't change - enables optimization",
                            "derivedStateOf - prevents recomposition when only "
                            "derived data changes",
                            "rememberSaveable - survives configuration changes, "
                            "good for form state",
                            "key() modifier - helps Compose identify items in "
                            "lists for efficient updates",
                        ],
                    },
                    {
                        "heading": "Common Pitfalls",
                        "points": [],
                        "subtopics": [
                            {
                                "title": "Lambda Recreation",
                                "description": "Don't create new lambdas in "
                                "composable - use remember to "
                                "stabilize references",
                            },
                            {
                                "title": "Deep Composition",
                                "description": "Avoid deeply nested composables "
                                "- break into smaller "
                                "components",
                            },
                            {
                                "title": "Expensive Operations",
                                "description": "Never do heavy computation in "
                                "composable body - use remember "
                                "+ calculation",
                            },
                            {
                                "title": "Missing Keys",
                                "description": "Always provide stable keys in "
                                "LazyList - enables efficient "
                                "diffing",
                            },
                        ],
                    },
                ],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: Proper State Handling",
                        "code": "// WRONG - creates new lambda every recomposition\n"
                        "@Composable\n"
                        "fun BadExample(viewModel: VM) {\n"
                        "    // Don't do this - onClick recreated each recompose\n"
                        "    Button(onClick = { viewModel.doSomething() }) { }\n"
                        "}\n"
                        "\n"
                        "// RIGHT - stable lambda, use remember\n"
                        "@Composable\n"
                        "fun GoodExample(viewModel: VM) {\n"
                        "    val state by viewModel.state.collectAsState()\n"
                        "\n"
                        "    // Remember the callback - stable reference\n"
                        "    val onItemClick = remember(state.selectedId) {\n"
                        "        { id: String -> viewModel.selectItem(id) }\n"
                        "    }\n"
                        "\n"
                        "    LazyColumn {\n"
                        "        items(state.items, key = { it.id }) { item ->\n"
                        "            ItemRow(\n"
                        "                item = item,\n"
                        "                onClick = onItemClick\n"
                        "            )\n"
                        "        }\n"
                        "    }\n"
                        "}\n"
                        "\n"
                        "// DERIVED STATE - only recomputes when dependencies "
                        "change\n"
                        "val filteredItems = remember(query, items) {\n"
                        "    items.filter { it.name.contains(query) }\n"
                        "}",
                    }
                ],
            },
            {
                "title": "Compose UI Patterns",
                "icon": "",
                "description": "Master advanced Compose patterns for building complex, performant "
                "UIs. From custom layouts to canvas drawing, these patterns enable "
                "sophisticated visual experiences.",
                "content_sections": [
                    {
                        "heading": "Advanced UI Techniques",
                        "points": [],
                        "subtopics": [
                            {
                                "title": "Custom Layouts",
                                "description": "LayoutModifier, measurePolicy "
                                "for complex positioning - "
                                "carousel, calendar grids",
                            },
                            {
                                "title": "Canvas API",
                                "description": "drawCircle, drawPath, drawText "
                                "- custom charts, signatures, "
                                "animations",
                            },
                            {
                                "title": "LazyList Optimization",
                                "description": "key, contentType for efficient "
                                "updates, prefetchThreshold for "
                                "smooth scrolling",
                            },
                            {
                                "title": "Side Effects",
                                "description": "LaunchedEffect for async, "
                                "DisposableEffect for cleanup, "
                                "rememberCoroutineScope",
                            },
                        ],
                    }
                ],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: Canvas Custom Drawing",
                        "code": "@Composable\n"
                        "fun CircularProgressIndicator(\n"
                        "    progress: Float,\n"
                        "    modifier: Modifier = Modifier\n"
                        ") {\n"
                        "    Canvas(modifier = modifier.size(48.dp)) {\n"
                        "        val stroke = 4.dp.toPx()\n"
                        "        val radius = (size.minDimension - stroke) / 2\n"
                        "\n"
                        "        // Background circle\n"
                        "        drawCircle(\n"
                        "            color = Color.Gray.copy(alpha = 0.3f),\n"
                        "            radius = radius,\n"
                        "            style = Stroke(width = stroke)\n"
                        "        )\n"
                        "\n"
                        "        // Progress arc\n"
                        "        drawArc(\n"
                        "            color = Color.Blue,\n"
                        "            startAngle = -90f,\n"
                        "            sweepAngle = 360f * progress,\n"
                        "            useCenter = false,\n"
                        "            style = Stroke(width = stroke, cap = "
                        "StrokeCap.Round)\n"
                        "        )\n"
                        "    }\n"
                        "}",
                    }
                ],
            },
            {
                "title": "Animations in Compose",
                "icon": "",
                "description": "Compose provides a powerful animation system that's declarative and "
                "easy to use. Master these APIs to create smooth, engaging user "
                "experiences.",
                "content_sections": [
                    {
                        "heading": "Animation APIs Overview",
                        "points": [],
                        "subtopics": [
                            {
                                "title": "AnimatedVisibility",
                                "description": "Fade and slide animations for "
                                "showing/hiding content",
                            },
                            {
                                "title": "AnimatedContent",
                                "description": "Transition between different UI "
                                "states with custom animations",
                            },
                            {
                                "title": "animateXAsState",
                                "description": "Animate numeric values - color, "
                                "size, position, alpha",
                            },
                            {
                                "title": "Infinite Transition",
                                "description": "Looping animations for loading "
                                "indicators, pulsing effects",
                            },
                        ],
                    }
                ],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: Animated Visibility & Content",
                        "code": "// AnimatedVisibility - fade + slide\n"
                        "var expanded by remember { mutableStateOf(false) }\n"
                        "\n"
                        "AnimatedVisibility(\n"
                        "    visible = expanded,\n"
                        "    enter = fadeIn() + expandVertically(),\n"
                        "    exit = fadeOut() + shrinkVertically()\n"
                        ") {\n"
                        "    DetailContent()\n"
                        "}\n"
                        "\n"
                        "// AnimatedContent - transition between states\n"
                        "var state by remember { mutableStateOf(Loading) }\n"
                        "\n"
                        "AnimatedContent(\n"
                        "    targetState = state,\n"
                        "    transitionSpec = {\n"
                        "        fadeIn(tween(300)) togetherWith "
                        "fadeOut(tween(300))\n"
                        "    }\n"
                        ") { targetState ->\n"
                        "    when (targetState) {\n"
                        "        is Loading -> LoadingView()\n"
                        "        is Success -> SuccessView(targetState.data)\n"
                        "        is Error -> ErrorView(targetState.message)\n"
                        "    }\n"
                        "}",
                    }
                ],
            },
            {
                "title": "Traditional View System",
                "icon": "",
                "description": "Reviews the classic Android view toolkit that still appears in "
                "production apps and interview questions, especially around rendering "
                "and list performance.",
                "content_sections": [
                    {
                        "heading": "Layout Types",
                        "points": [
                            "• ConstraintLayout: Flat hierarchy, best " "performance",
                            "• LinearLayout: Vertical/horizontal arrangement",
                            "• FrameLayout: Stack views on top of each other",
                            "• RelativeLayout: Position relative to " "parent/siblings",
                            "• CoordinatorLayout: Complex scrolling behaviors",
                        ],
                    },
                    {
                        "heading": "RecyclerView",
                        "points": [
                            "• Efficient scrolling lists",
                            "• ViewHolder pattern for view recycling",
                            "• DiffUtil for efficient updates",
                            "• ListAdapter simplifies DiffUtil usage",
                            "• Multiple view types support",
                            "• ItemDecoration for spacing and dividers",
                        ],
                    },
                    {
                        "heading": "Custom Views",
                        "points": [
                            "• Extend View or ViewGroup",
                            "• Override onMeasure(), onLayout(), onDraw()",
                            "• Custom attributes via attrs.xml",
                            "• Canvas drawing with Paint",
                        ],
                    },
                ],
                "code_blocks": [],
            },
            {
                "title": "Jetpack Compose (Modern UI)",
                "icon": "",
                "description": "Covers the Compose mental model, state handling, layouts, and side "
                "effects that define modern Android UI development.",
                "content_sections": [
                    {
                        "heading": "Core Principles",
                        "points": [
                            "• Declarative UI: describe what UI should look " "like",
                            "• Composable functions: @Composable annotation",
                            "• Recomposition: UI updates when state changes",
                            "• State hoisting: move state to caller for " "reusability",
                        ],
                    },
                    {
                        "heading": "State Management",
                        "points": [
                            "• remember: preserves state across recompositions",
                            "• rememberSaveable: survives configuration changes",
                            "• mutableStateOf: observable state",
                            "• collectAsState(): observe Flow/StateFlow",
                            "• derivedStateOf: computed state",
                        ],
                    },
                    {
                        "heading": "Layouts",
                        "points": [
                            "• Column, Row, Box (fundamental layouts)",
                            "• LazyColumn, LazyRow (RecyclerView equivalent)",
                            "• Scaffold: top bar, bottom bar, fab, drawer",
                            "• Surface: container with elevation",
                        ],
                    },
                    {
                        "heading": "Navigation in Compose",
                        "points": [
                            "• NavHost and NavController",
                            "• Type-safe navigation with routes",
                            "• Passing arguments between screens",
                            "• BottomNavigation and NavigationRail",
                        ],
                    },
                    {
                        "heading": "Theming & Material Design",
                        "points": [
                            "• MaterialTheme: colors, typography, shapes",
                            "• Dynamic theming (Material You)",
                            "• Dark mode support",
                            "• Custom theme creation",
                        ],
                    },
                    {
                        "heading": "Side Effects",
                        "points": [
                            "• LaunchedEffect: coroutine tied to composable "
                            "lifecycle",
                            "• DisposableEffect: cleanup when composable leaves "
                            "composition",
                            "• SideEffect: sync Compose state to non-Compose " "code",
                            "• rememberCoroutineScope: manual coroutine " "launching",
                        ],
                    },
                ],
                "code_blocks": [],
            },
        ],
        "description": "Compares classic Android UI foundations with modern declarative Compose patterns "
        "so you can explain both legacy codebases and current best practices "
        "confidently.",
    },
    {
        "id": "state-navigation",
        "title": "State & Navigation",
        "topics": [
            {
                "title": "ViewModel & SavedStateHandle",
                "icon": "",
                "description": "Explains how screen state survives lifecycle changes and process "
                "recreation while keeping UI controllers lightweight.",
                "content_sections": [],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: ViewModel with SavedStateHandle",
                        "code": "@HiltViewModel\n"
                        "class FormViewModel @Inject constructor(\n"
                        "    private val savedStateHandle: SavedStateHandle,\n"
                        "    private val repository: FormRepository\n"
                        ") : ViewModel() {\n"
                        "\n"
                        "    // Restore state after process death\n"
                        "    var formData: FormData\n"
                        "        get() = FormData(\n"
                        '            name = savedStateHandle["name"] ?: "",\n'
                        '            email = savedStateHandle["email"] ?: "",\n'
                        '            age = savedStateHandle["age"] ?: 0\n'
                        "        )\n"
                        "        set(value) {\n"
                        '            savedStateHandle["name"] = value.name\n'
                        '            savedStateHandle["email"] = value.email\n'
                        '            savedStateHandle["age"] = value.age\n'
                        "        }\n"
                        "\n"
                        "    // Or use mutableStateOf with saveable\n"
                        "    var name by savedStateHandle.saveable {\n"
                        '        mutableStateOf("")\n'
                        "    }\n"
                        "}",
                    }
                ],
            },
            {
                "title": "Compose Navigation",
                "icon": "",
                "description": "Covers navigation patterns in Compose, including route modeling, "
                "argument passing, and state-safe screen transitions.",
                "content_sections": [
                    {
                        "heading": "Key Points",
                        "points": [
                            "Use sealed classes for routes - compile-time " "safety",
                            "NavBackStackEntry saves state when navigating - no "
                            "data loss on back",
                            "Use hiltNavGraph() for DI integration in " "navigation",
                        ],
                    }
                ],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: Type-Safe Navigation",
                        "code": "// Define navigation routes with arguments\n"
                        "sealed class Screen(val route: String) {\n"
                        '    object Home : Screen("home")\n'
                        '    object Detail : Screen("detail/{userId}") {\n'
                        "        fun createRoute(userId: String) = "
                        '"detail/$userId"\n'
                        "    }\n"
                        '    object Settings : Screen("settings")\n'
                        "}\n"
                        "\n"
                        "// NavHost setup\n"
                        "@Composable\n"
                        "AppNavHost(\n"
                        "    navController: NavHostController\n"
                        ") {\n"
                        "    NavHost(\n"
                        "        navController = navController,\n"
                        "        startDestination = Screen.Home.route\n"
                        "    ) {\n"
                        "        composable(Screen.Home.route) {\n"
                        "            HomeScreen(\n"
                        "                onUserClick = { userId ->\n"
                        "                    "
                        "navController.navigate(Screen.Detail.createRoute(userId))\n"
                        "                }\n"
                        "            )\n"
                        "        }\n"
                        "\n"
                        "        composable(\n"
                        "            route = Screen.Detail.route,\n"
                        "            arguments = listOf(\n"
                        '                navArgument("userId") { type = '
                        "NavType.StringType }\n"
                        "            )\n"
                        "        ) { backStackEntry ->\n"
                        "            val userId = "
                        'backStackEntry.arguments?.getString("userId")!!\n'
                        "            DetailScreen(userId = userId)\n"
                        "        }\n"
                        "    }\n"
                        "}\n"
                        "\n"
                        "// Deep linking\n"
                        "composable(\n"
                        "    route = Screen.Detail.route,\n"
                        "    deepLinks = listOf(\n"
                        '        deepLink { uriPattern("myapp://user/{userId}" },\n'
                        "        deepLink { action = Intent.ACTION_VIEW }\n"
                        "    )\n"
                        ") { ... }",
                    }
                ],
            },
            {
                "title": "Type-Safe Compose Navigation",
                "description": "The evolution from string-based routes to serializable Kotlin objects ensures compile-time safety across your app.",
                "content_sections": [
                    {
                        "heading": "Type-Safe Destinations",
                        "points": [
                            "Uses @Serializable data classes/objects to define routes instead of fragile strings.",
                            "Arguments are automatically serialized/deserialized via kotlinx.serialization.",
                            'Enables "Safe Args" functionality directly in Compose without Gradle plugins.',
                        ],
                    },
                    {
                        "heading": "Navigation 3 (The State-First Future)",
                        "points": [
                            "Removes the NavController in favor of direct backstack ownership (a simple List<Key>).",
                            "Allows storing navigation state in ViewModels, making it easier to test and share logic.",
                            'Native support for "Scenes" to handle adaptive layouts (multi-pane) on large screens.',
                        ],
                    },
                ],
            },
            {
                "title": "Cross-Platform & KMP Solutions",
                "description": "Navigation logic is increasingly moved to shared code to support Android, iOS, and Desktop simultaneously.",
                "content_sections": [
                    {
                        "heading": "Voyager",
                        "points": [
                            'A pragmatic, screen-centric library popular for its "multi-stack" support (e.g., BottomTabs).',
                            "Built-in support for transitions and lifecycle-aware state management.",
                            "Easier onboarding for teams moving from traditional Android navigation.",
                        ],
                    },
                    {
                        "heading": "Decompose",
                        "points": [
                            'The "Power User" choice for Kotlin Multiplatform (KMP).',
                            "Decouples navigation logic from UI entirely using a component-tree architecture.",
                            "Handles complex lifecycles and process death natively across all platforms.",
                        ],
                    },
                ],
            },
        ],
        "description": "Focuses on app-level architecture decisions, state ownership, modular "
        "boundaries, and navigation structure rather than repeating lower-level platform "
        "fundamentals.",
    },
    {
        "id": "dependency-injection",
        "title": "Dependency Injection",
        "topics": [
            {
                "title": "Dependency Injection (DI) - Hilt vs Koin in 2026",
                "description": "DI is the glue that connects your layers. The choice depends on your platform targets.",
                "content_sections": [
                    {
                        "heading": "Hilt (The Android Standard)",
                        "points": [
                            "Built on top of Dagger. Provides compile-time safety.",
                            "Best for Android-only apps due to its deep integration with ViewModels and WorkManager.",
                            "Uses KSP (Kotlin Symbol Processing) in 2026 for 2x faster build times than old kapt.",
                        ],
                    },
                    {
                        "heading": "Koin (The KMP Favorite)",
                        "points": [
                            "A lightweight, runtime DI (no code generation).",
                            "Highly preferred for Kotlin Multiplatform because it works natively on iOS and Web.",
                            "Very easy to set up with almost zero boilerplate.",
                        ],
                    },
                ],
            },
            {
                "title": "Hilt Deep Dive",
                "icon": "",
                "description": "Covers the Android-focused dependency injection stack with Hilt and "
                "Dagger concepts, including scopes, qualifiers, generated components, "
                "and production-ready module design.",
                "content_sections": [
                    {
                        "heading": "Scope Types",
                        "points": [
                            "@Singleton - one instance for entire app "
                            "(Application, OkHttp, Retrofit)",
                            "@ActivityScoped - same instance within one "
                            "Activity lifecycle",
                            "@ViewModelScoped - one instance per ViewModel "
                            "(automatic with @HiltViewModel)",
                            "@EntryPoint - for non-Hilt classes that need "
                            "dependencies (ContentProvider, Worker)",
                            "@FragmentScoped - same instance within one "
                            "Fragment lifecycle",
                        ],
                    },
                    {
                        "heading": "Key Concepts",
                        "points": [],
                        "subtopics": [
                            {
                                "title": "Component Hierarchy",
                                "description": "SingletonComponent → "
                                "ActivityComponent → "
                                "FragmentComponent → "
                                "ViewModelComponent",
                            },
                            {
                                "title": "Scope Inheritance",
                                "description": "@Singleton can inject into "
                                "@ActivityScoped, but not vice "
                                "versa",
                            },
                            {
                                "title": "Qualifiers",
                                "description": "@Named or custom @Qualifier for "
                                "multiple implementations of "
                                "same interface",
                            },
                            {
                                "title": "Binds vs Provides",
                                "description": "@Binds for interface "
                                "implementations (faster), "
                                "@Provides for concrete "
                                "classes",
                            },
                        ],
                    },
                    {
                        "heading": "Hilt (Recommended for Android)",
                        "points": [
                            "• Built on top of Dagger",
                            "• Reduces Dagger boilerplate for Android",
                            "• Standard components and scopes",
                            "• @HiltAndroidApp: Application class",
                            "• @AndroidEntryPoint: Activities, Fragments, "
                            "Views, Services",
                            "• @Inject: constructor injection",
                            "• @Module: provides dependencies",
                            "• @InstallIn: defines component lifecycle",
                        ],
                    },
                    {
                        "heading": "Scopes in Hilt",
                        "points": [
                            "• @Singleton: app lifecycle",
                            "• @ActivityScoped: activity lifecycle",
                            "• @ViewModelScoped: ViewModel lifecycle",
                            "• @FragmentScoped: fragment lifecycle",
                        ],
                    },
                    {
                        "heading": "Qualifiers",
                        "points": [
                            "• Multiple implementations of same interface",
                            '• @Named("qualifier")',
                            "• Custom qualifiers with @Qualifier annotation",
                        ],
                    },
                ],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: Hilt Modules & Scopes",
                        "code": "// Network Module\n"
                        "@Module\n"
                        "@InstallIn(SingletonComponent::class)\n"
                        "object NetworkModule {\n"
                        "\n"
                        "    @Provides\n"
                        "    @Singleton\n"
                        "    fun provideOkHttpClient(\n"
                        "        loggingInterceptor: LoggingInterceptor\n"
                        "    ): OkHttpClient {\n"
                        "        return OkHttpClient.Builder()\n"
                        "            .addInterceptor(loggingInterceptor)\n"
                        "            .connectTimeout(30, TimeUnit.SECONDS)\n"
                        "            .build()\n"
                        "    }\n"
                        "\n"
                        "    @Provides\n"
                        "    @Singleton\n"
                        "    fun provideRetrofit(okHttp: OkHttpClient): Retrofit {\n"
                        "        return Retrofit.Builder()\n"
                        '            .baseUrl("https://api.example.com/")\n'
                        "            .client(okHttp)\n"
                        "            "
                        ".addConverterFactory(GsonConverterFactory.create())\n"
                        "            .build()\n"
                        "    }\n"
                        "}\n"
                        "\n"
                        "// Activity Scope - same instance within an Activity\n"
                        "@Module\n"
                        "@InstallIn(ActivityComponent::class)\n"
                        "object ActivityModule {\n"
                        "    @ActivityScoped\n"
                        "    @Provides\n"
                        "    fun provideActivityNavigator(\n"
                        "        activity: Activity\n"
                        "    ): ActivityNavigator = ActivityNavigator(activity)\n"
                        "}\n"
                        "\n"
                        "// ViewModel Factory with AssistedInject\n"
                        "@HiltViewModel\n"
                        "class UserViewModel @Inject constructor(\n"
                        "    private val getUserUseCase: GetUserUseCase,\n"
                        "    private val savedStateHandle: SavedStateHandle\n"
                        ") : ViewModel() {\n"
                        "\n"
                        "    private val userId: String = "
                        'savedStateHandle["userId"] ?: ""\n'
                        "\n"
                        "    init { loadUser() }\n"
                        "}",
                    }
                ],
            },
            {
                "title": "Koin",
                "icon": "",
                "description": "Introduces Koin as a simpler runtime DI alternative and frames when "
                "that tradeoff is helpful versus heavier compile-time solutions.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Lightweight, Kotlin-first DI framework • No code "
                            "generation, pure Kotlin DSL • Easy to learn and "
                            "set up • module { ... }: define dependencies • "
                            "single { ... }: singleton • factory { ... }: new "
                            "instance each time • by viewModel(): inject "
                            "ViewModel • Good for small to medium projects"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Manual Dependency Injection",
                "icon": "",
                "description": "Shows how explicit wiring can still be useful for small modules, "
                "tests, and understanding DI fundamentals without a framework.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Service locator pattern • Constructor injection "
                            "manually • Simple for small projects • No external "
                            "dependencies • Full control over object "
                            "creation"
                        ],
                    }
                ],
                "code_blocks": [],
            },
        ],
        "description": "Organizes dependency management around one clear Android DI section, covering "
        "Hilt deeply while still preserving the comparison points with alternative "
        "approaches.",
    },
    {
        "id": "data-management-persistence",
        "title": "Data Management & Persistence",
        "topics": [
            {
                "title": "Room Database",
                "icon": "",
                "description": "Explains Room as the standard structured persistence layer for "
                "Android apps, including schema modeling, DAOs, and reactive reads.",
                "content_sections": [
                    {
                        "heading": "Key Points",
                        "points": [
                            "Use @Transaction for operations that need to be " "atomic",
                            "Return Flow for reactive data - Room auto-updates "
                            "when DB changes",
                            "Migration strategy: always preserve user data, "
                            "test thoroughly",
                            "Use FTS (Full-Text Search) for search " "functionality",
                        ],
                    },
                    {
                        "heading": "Components",
                        "points": [
                            "• Entity: Table definition with @Entity",
                            "• DAO (Data Access Object): Database operations "
                            "with @Dao",
                            "• Database: Abstract class with @Database",
                        ],
                    },
                    {
                        "heading": "Relationships",
                        "points": [
                            "• One-to-One: @Embedded or @Relation",
                            "• One-to-Many: @Relation with parentColumn and "
                            "entityColumn",
                            "• Many-to-Many: Junction table with @Entity",
                        ],
                    },
                    {
                        "heading": "Migrations",
                        "points": [
                            "• Database schema changes",
                            "• Migration class with migrate() method",
                            "• fallbackToDestructiveMigration() for development",
                            "• Test migrations thoroughly",
                        ],
                    },
                    {
                        "heading": "Advanced Features",
                        "points": [
                            "• Full-text search with @Fts4",
                            "• Database views with @DatabaseView",
                            "• Type converters for custom types",
                            "• Pre-populated databases",
                        ],
                    },
                ],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: Complete Room Setup",
                        "code": "// Entity with relations\n"
                        '@Entity(tableName = "users")\n'
                        "data class UserEntity(\n"
                        "    @PrimaryKey val id: String,\n"
                        "    val name: String,\n"
                        "    val email: String,\n"
                        "    val avatarUrl: String?,\n"
                        "    val createdAt: Long = System.currentTimeMillis()\n"
                        ")\n"
                        "\n"
                        '@Entity(tableName = "posts", foreignKeys = [\n'
                        "    ForeignKey(\n"
                        "        entity = UserEntity::class,\n"
                        '        parentColumns = ["id"],\n'
                        '        childColumns = ["userId"],\n'
                        "        onDelete = ForeignKey.CASCADE\n"
                        "    )\n"
                        "])\n"
                        "data class PostEntity(\n"
                        "    @PrimaryKey val id: String,\n"
                        "    val userId: String,\n"
                        "    val title: String,\n"
                        "    val content: String,\n"
                        "    val publishedAt: Long\n"
                        ")\n"
                        "\n"
                        "// Relation class\n"
                        "data class UserWithPosts(\n"
                        "    @Relation(\n"
                        '        parentColumn = "id",\n'
                        '        entityColumn = "userId"\n'
                        "    )\n"
                        "    val posts: List<PostEntity>,\n"
                        "    val user: UserEntity\n"
                        ")\n"
                        "\n"
                        "// DAO with complex queries\n"
                        "@Dao\n"
                        "interface UserDao {\n"
                        "\n"
                        '    @Query("SELECT * FROM users WHERE id = :userId")\n'
                        "    suspend fun getUserById(userId: String): UserEntity?\n"
                        "\n"
                        "    @Transaction\n"
                        '    @Query("SELECT * FROM users WHERE id = :userId")\n'
                        "    suspend fun getUserWithPosts(userId: String): "
                        "UserWithPosts?\n"
                        "\n"
                        "    @Query(\"SELECT * FROM users WHERE name LIKE '%' || "
                        ":query || '%'\")\n"
                        "    fun searchUsers(query: String): "
                        "Flow<List<UserEntity>>\n"
                        "\n"
                        "    @Insert(onConflict = OnConflictStrategy.REPLACE)\n"
                        "    suspend fun insertUser(user: UserEntity)\n"
                        "\n"
                        "    @Insert(onConflict = OnConflictStrategy.REPLACE)\n"
                        "    suspend fun insertUsers(users: List<UserEntity>)\n"
                        "\n"
                        "    @Delete\n"
                        "    suspend fun deleteUser(user: UserEntity)\n"
                        "\n"
                        '    @Query("DELETE FROM users")\n'
                        "    suspend fun deleteAllUsers()\n"
                        "}\n"
                        "\n"
                        "// Database with migrations\n"
                        "@Database(\n"
                        "    entities = [UserEntity::class, PostEntity::class],\n"
                        "    version = 2,\n"
                        "    exportSchema = true\n"
                        ")\n"
                        "abstract class AppDatabase : RoomDatabase() {\n"
                        "    abstract fun userDao(): UserDao\n"
                        "\n"
                        "    companion object {\n"
                        "        val MIGRATION_1_2 = object : Migration(1, 2) {\n"
                        "            override fun migrate(database: "
                        "SupportSQLiteDatabase) {\n"
                        '                database.execSQL("ALTER TABLE users ADD '
                        'COLUMN avatarUrl TEXT")\n'
                        "            }\n"
                        "        }\n"
                        "    }\n"
                        "}",
                    }
                ],
            },
            {
                "title": "DataStore",
                "icon": "",
                "description": "Introduces DataStore as the modern replacement for many "
                "SharedPreferences use cases, especially when consistency and async "
                "access matter.",
                "content_sections": [],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: DataStore Preferences",
                        "code": "// Preferences DataStore\n"
                        "class SettingsRepository(\n"
                        "    private val dataStore: DataStore<Preferences>\n"
                        ") {\n"
                        "    private object PreferencesKeys {\n"
                        "        val DARK_MODE = "
                        'booleanPreferencesKey("dark_mode")\n'
                        "        val NOTIFICATIONS = "
                        'booleanPreferencesKey("notifications")\n'
                        "        val SELECTED_LANGUAGE = "
                        'stringPreferencesKey("language")\n'
                        "    }\n"
                        "\n"
                        "    val darkMode: Flow<Boolean> = dataStore.data\n"
                        "        .map { it[PreferencesKeys.DARK_MODE] ?: false }\n"
                        "\n"
                        "    suspend fun setDarkMode(enabled: Boolean) {\n"
                        "        dataStore.edit { it[PreferencesKeys.DARK_MODE] = "
                        "enabled }\n"
                        "    }\n"
                        "}\n"
                        "\n"
                        "// Proto DataStore (type-safe)\n"
                        "// 1. Define schema in proto/settings.proto\n"
                        "// 2. Generate serializer\n"
                        'val protoDataStore = dataStore.file("settings.pb", '
                        "SettingsSerializer)",
                    }
                ],
            },
            {
                "title": "SharedPreferences",
                "icon": "",
                "description": "Covers simple key-value persistence, typical limitations, and when "
                "legacy preference storage still appears in Android projects.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Key-value storage for simple data • Stores "
                            "primitives: Boolean, Int, Long, Float, String • "
                            "DataStore preferred (modern alternative): - "
                            "Preferences DataStore (key-value) - Proto "
                            "DataStore (typed objects) - Asynchronous with Flow "
                            "- Type-safe and transactional"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "File Storage",
                "icon": "",
                "description": "Reviews file-based persistence options and the tradeoffs around "
                "private storage, media files, and scoped storage behavior.",
                "content_sections": [
                    {
                        "heading": "Internal Storage",
                        "points": [
                            "• Private to app, deleted on uninstall",
                            "• context.filesDir for files",
                            "• context.cacheDir for temporary files",
                        ],
                    },
                    {
                        "heading": "External Storage",
                        "points": [
                            "• Scoped Storage (Android 10+)",
                            "• MediaStore API for media files",
                            "• Storage Access Framework (SAF) for documents",
                            "• App-specific directory (no permissions " "needed)",
                        ],
                    },
                ],
                "code_blocks": [],
            },
            {
                "title": "Repository Pattern",
                "icon": "",
                "description": "Explains how repositories coordinate local and remote data sources "
                "while presenting a cleaner API to the domain or UI layer.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Single source of truth for data • Abstracts data "
                            "sources (network, database, cache) • Handles data "
                            "caching and sync logic • ViewModel depends on "
                            "Repository, not data sources directly"
                        ],
                    }
                ],
                "code_blocks": [],
            },
        ],
        "description": "Covers local persistence, preference storage, repository boundaries, and how "
        "Android apps model data flow between disk, network, and UI.",
    },
    {
        "id": "networking-apis",
        "title": "Networking & APIs",
        "topics": [
            {
                "title": "Retrofit & OkHttp",
                "icon": "",
                "description": "Combines the core Android HTTP client stack with Retrofit interface "
                "design, coroutine support, interceptors, serialization, and "
                "production networking patterns.",
                "content_sections": [
                    {
                        "heading": "Setup",
                        "points": [
                            "• Define API interface with annotations",
                            "• @GET, @POST, @PUT, @DELETE, @PATCH",
                            "• @Path, @Query, @Body, @Header",
                            "• Converter factories: Gson, Moshi, Kotlinx "
                            "Serialization",
                        ],
                    },
                    {
                        "heading": "Coroutines Integration",
                        "points": [
                            "• suspend functions for API calls",
                            "• Response<T> for access to headers and status " "codes",
                            "• Exception handling with try-catch",
                        ],
                    },
                    {
                        "heading": "Interceptors (OkHttp)",
                        "points": [
                            "• Logging: HttpLoggingInterceptor",
                            "• Authentication: Add tokens to requests",
                            "• Retry logic",
                            "• Caching strategies",
                        ],
                    },
                ],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: Complete Network Setup",
                        "code": "// API Interface with full configuration\n"
                        "interface UserApi {\n"
                        "\n"
                        '    @GET("users/{id}")\n'
                        "    suspend fun getUser(\n"
                        '        @Path("id") userId: String,\n'
                        '        @Query("include") include: String = '
                        '"posts,photos"\n'
                        "    ): Response<UserDto>\n"
                        "\n"
                        '    @POST("users")\n'
                        "    suspend fun createUser(\n"
                        "        @Body user: CreateUserRequest\n"
                        "    ): Response<UserDto>\n"
                        "\n"
                        "    @Multipart\n"
                        '    @POST("upload")\n'
                        "    suspend fun uploadImage(\n"
                        "        @Part image: MultipartBody.Part\n"
                        "    ): Response<UploadResponse>\n"
                        "}\n"
                        "\n"
                        "// OkHttp Interceptors for auth, logging, retry\n"
                        "class AuthInterceptor : Interceptor {\n"
                        "    override fun intercept(chain: Interceptor.Chain): "
                        "Response {\n"
                        "        val original = chain.request()\n"
                        "        val token = getAuthToken()\n"
                        "\n"
                        "        val newRequest = original.newBuilder()\n"
                        '            .header("Authorization", "Bearer $token")\n'
                        '            .header("Accept", "application/json")\n'
                        "            .build()\n"
                        "\n"
                        "        return chain.proceed(newRequest)\n"
                        "    }\n"
                        "}\n"
                        "\n"
                        "// Retry Interceptor with exponential backoff\n"
                        "class RetryInterceptor(val maxRetries: Int = 3) : "
                        "Interceptor {\n"
                        "    override fun intercept(chain: Interceptor.Chain): "
                        "Response {\n"
                        "        val request = chain.request()\n"
                        "        var response: Response? = null\n"
                        "        var exception: IOException? = null\n"
                        "        var retryCount = 0\n"
                        "\n"
                        "        while (retryCount < maxRetries) {\n"
                        "            try {\n"
                        "                response?.close()\n"
                        "                response = chain.proceed(request)\n"
                        "                if (response.isSuccessful) return "
                        "response\n"
                        "            } catch (e: IOException) {\n"
                        "                exception = e\n"
                        "                retryCount++\n"
                        "                Thread.sleep(1000L * retryCount) // "
                        "Exponential backoff\n"
                        "            }\n"
                        "        }\n"
                        "\n"
                        '        throw exception ?: IOException("Unknown error")\n'
                        "    }\n"
                        "}",
                    }
                ],
            },
            {
                "title": "GraphQL with Apollo",
                "icon": "",
                "description": "Covers Apollo-based GraphQL integration on Android, including "
                "schema-driven requests, caching, query design, and how it differs "
                "from REST-based networking.",
                "content_sections": [
                    {
                        "heading": "Key Points",
                        "points": [
                            "Apollo caches responses automatically - configure "
                            "cache policies",
                            "Fragments reduce duplication across queries",
                            "Subscriptions for real-time data (WebSocket)",
                        ],
                    },
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Query specific fields needed • Single endpoint "
                            "vs multiple REST endpoints • Type-safe code "
                            "generation • Real-time data with subscriptions • "
                            "Normalized caching"
                        ],
                    },
                ],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: Apollo Client Setup",
                        "code": "// Apollo Client with caching\n"
                        "val apolloClient = ApolloClient.Builder()\n"
                        "    "
                        '.httpLink(HttpLink("https://api.example.com/graphql"))\n'
                        "    "
                        ".cache(NormalizedCacheFactory(LruNormalizedCacheFactory(10_000_000)))\n"
                        "    .addInterceptor(AuthorizationInterceptor())\n"
                        "    .build()\n"
                        "\n"
                        "// Query with fragments\n"
                        "class GetUserQuery(val userId: String) : "
                        "Query<GetUserQuery.Data, GetUserQuery.Variables> {\n"
                        "    override fun queryDocument() = DOCUMENT\n"
                        "    override fun variables() = Variables(userId)\n"
                        "\n"
                        "    data class Data(val user: User)\n"
                        "    data class Variables(val userId: String)\n"
                        "}\n"
                        "\n"
                        "// Usage with Flow\n"
                        "suspend fun getUser(id: String): User {\n"
                        "    return apolloClient.query(GetUserQuery(id))\n"
                        "        .execute()\n"
                        "        .data\n"
                        "        .user\n"
                        "}",
                    }
                ],
            },
            {
                "title": "Certificate Pinning",
                "icon": "",
                "description": "Explains transport hardening by restricting trust to expected "
                "certificates or public keys for sensitive network paths.",
                "content_sections": [],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: Certificate Pinning",
                        "code": "val certificatePinner = CertificatePinner.Builder()\n"
                        '    .add("api.example.com", '
                        '"sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")\n'
                        '    .add("api.example.com", '
                        '"sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=")\n'
                        "    .build()\n"
                        "\n"
                        "val client = OkHttpClient.Builder()\n"
                        "    .certificatePinner(certificatePinner)\n"
                        "    .build()",
                    }
                ],
            },
            {
                "title": "WebSockets",
                "icon": "",
                "description": "Explains persistent two-way communication for real-time features "
                "such as chat, live updates, or collaborative state sync.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Full-duplex communication • OkHttp WebSocket "
                            "support • Real-time chat, live updates, gaming • "
                            "Connection management and reconnection logic"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "API Response Handling",
                "icon": "",
                "description": "Focuses on mapping, validation, error handling, and resilience "
                "strategies when turning raw API responses into usable app state.",
                "content_sections": [
                    {"heading": "Result/Resource Pattern", "points": []},
                    {
                        "heading": "Error Handling",
                        "points": [
                            "• Network errors (no connectivity)",
                            "• HTTP errors (4xx, 5xx)",
                            "• Parsing errors",
                            "• Timeout errors",
                            "• Retry strategies with exponential backoff",
                        ],
                    },
                ],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Result/Resource Pattern Example",
                        "code": "sealed class Result<out T> {\n"
                        "    data class Success<T>(val data: T) : Result<T>()\n"
                        "    data class Error(val exception: Exception) : "
                        "Result<Nothing>()\n"
                        "    object Loading : Result<Nothing>()\n"
                        "}",
                    }
                ],
            },
        ],
        "description": "Consolidates the Android networking stack into clearer REST and GraphQL topics, "
        "plus the resilience and security concerns expected in senior interviews.",
    },
    {
        "id": "concurrency-threading-background-work",
        "title": "Concurrency, Threading & Background Work",
        "topics": [
            {
                "title": "WorkManager: Core Mechanisms & Reliability",
                "description": "WorkManager manages the complexity of background execution by abstracting system-level APIs based on device conditions and API levels.Explains the recommended API for deferrable and reliable background "
                "execution under Android power-management constraints.",
                "content_sections": [
                    {
                        "heading": "Guaranteed Persistence",
                        "points": [
                            "Uses an internal SQLite database to track tasks, ensuring they survive app crashes and reboots.",
                            "Intelligently picks between JobScheduler (API 23+) and a combination of AlarmManager + BroadcastReceiver for older versions.",
                            "Adheres to modern system health standards like Doze mode and App Standby to optimize battery life.",
                        ],
                    },
                    {
                        "heading": "Constraint-Based Triggers",
                        "points": [
                            "Network: Run only when connected to Wi-Fi or an unmetered network to save data.",
                            "Power: Schedule work to only occur while the device is charging or has a sufficient battery level.",
                            "Storage & Idle: Trigger maintenance tasks when storage is not low or the device is in an idle state.",
                        ],
                    },
                    {
                        "heading": "Work Types",
                        "points": [
                            "One-Time Work: Execute a task once, with optional delay and constraints.",
                            "Periodic Work: Schedule recurring tasks at defined intervals (e.g., sync every 12 hours).",
                            "Chained Work: Create complex sequences of dependent tasks that run in order.",
                        ],
                    },
                    {
                        "heading": "Key Points",
                        "points": [
                            "WorkManager handles device restart, battery "
                            "optimization, API level differences",
                            "Use setExpedited() for urgent tasks (requires "
                            "override to be async)",
                            "Chain work with beginWith() then() for " "dependencies",
                        ],
                    },
                ],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: WorkManager for Background Tasks",
                        "code": "// Periodic Work - sync data every 6 hours\n"
                        "val syncRequest = PeriodicWorkRequestBuilder<SyncWorker>(\n"
                        "    6, TimeUnit.HOURS,\n"
                        "    15, TimeUnit.MINUTES // flex interval\n"
                        ")\n"
                        "    .setConstraints(\n"
                        "        Constraints.Builder()\n"
                        "            "
                        ".setRequiredNetworkType(NetworkType.CONNECTED)\n"
                        "            .setRequiresBatteryNotLow(true)\n"
                        "            .build()\n"
                        "    )\n"
                        '    .addTag("sync")\n'
                        "    .build()\n"
                        "\n"
                        "WorkManager.getInstance(context)\n"
                        "    .enqueueUniquePeriodicWork(\n"
                        '        "data_sync",\n'
                        "        ExistingPeriodicWorkPolicy.KEEP,\n"
                        "        syncRequest\n"
                        "    )\n"
                        "\n"
                        "// One-time Work with input/output\n"
                        "val uploadRequest = "
                        "OneTimeWorkRequestBuilder<UploadWorker>()\n"
                        '    .setInputData(workDataOf("file_uri" to fileUri))\n'
                        "    .setConstraints(\n"
                        "        Constraints.Builder()\n"
                        "            "
                        ".setRequiredNetworkType(NetworkType.UNMETERED)\n"
                        "            .build()\n"
                        "    )\n"
                        "    .build()\n"
                        "\n"
                        "// Worker implementation\n"
                        "class SyncWorker(\n"
                        "    context: Context,\n"
                        "    params: WorkerParameters\n"
                        ") : CoroutineWorker(context, params) {\n"
                        "\n"
                        "    override suspend fun doWork: Result {\n"
                        "        return runCatching {\n"
                        "            val remoteData = api.fetchData()\n"
                        "            database.insertAll(remoteData)\n"
                        "            Result.success()\n"
                        "        }.getOrElse {\n"
                        "            if (runAttemptCount < 3) Result.retry()\n"
                        "            else Result.failure()\n"
                        "        }\n"
                        "    }\n"
                        "}",
                    }
                ],
            },
            {
                "title": "WorkManager: Primary Use-Cases",
                "description": "WorkManager is best for non-immediate tasks that must complete reliably over time.",
                "content_sections": [
                    {
                        "heading": "Data Synchronization",
                        "points": [
                            "Uploading logs or analytics to backend servers periodically without blocking the UI.",
                            "Syncing local database changes with a remote server (e.g., email or message drafts).",
                        ],
                    },
                    {
                        "heading": "Media & File Processing",
                        "points": [
                            "Applying filters to images or transcoding videos after they are captured.",
                            "Large file uploads (e.g., 100+ images) that should continue even if the user leaves the app.",
                        ],
                    },
                    {
                        "heading": "System Maintenance",
                        "points": [
                            "Daily database cleanup or old cache removal to keep the app performing smoothly.",
                            "Periodic content updates (e.g., pre-fetching news or assets) so data is ready when the user opens the app.",
                        ],
                    },
                ],
            },
            {
                        "title": "Expedited Work for Urgent Tasks",
                        "description": "Expedited work is for tasks that must run immediately, even if the system is under memory pressure or the app is in the background.",
                        "content_sections": [
                            {
                                "heading": "Setting up Expedited Work",
                                "points": [
                                    "Override the `getForegroundInfo()` method in your Worker to handle notifications for older Android versions.",
                                    "Use `setExpedited(OutOfQuotaPolicy.RUN_AS_NON_EXPEDITED_WORK_REQUEST)` to define behavior when your quota is hit.",
                                    "Ideal for user-initiated actions like sending a chat message or processing an immediate upload.",
                                ],
                                "code_blocks": [
                                    """val request = OneTimeWorkRequestBuilder<UploadWorker>()
    .setExpedited(OutOfQuotaPolicy.RUN_AS_NON_EXPEDITED_WORK_REQUEST)
    .build()

WorkManager.getInstance(context).enqueue(request)"""
                                ],
                            }
                        ],
                    },
                    {
                        "title": "Work Chaining & Data Flow",
                        "description": "Chaining allows you to orchestrate complex background pipelines where tasks depend on the successful completion of previous ones.",
                        "content_sections": [
                            {
                                "heading": "Sequential Execution",
                                "points": [
                                    "Use `beginWith()` followed by `then()` to create a linear execution path.",
                                    "Workers pass data using `Data` objects; the output of the first becomes the input of the second.",
                                    "If a worker fails, the entire chain stops by default, preventing corrupted data states.",
                                ],
                                "code_blocks": [
                                    """WorkManager.getInstance(context)
    .beginWith(filterWorker) // Task 1: Image Filtering
    .then(compressWorker)    // Task 2: Compression (runs after filtering)
    .then(uploadWorker)      // Task 3: Upload (runs after compression)
    .enqueue()"""
                                ],
                            },
                            {
                                "heading": "Parallel Branching (Combine)",
                                "points": [
                                    "You can run multiple chains in parallel and join them together before a final task.",
                                    "Use `WorkContinuation.combine()` to merge separate branches.",
                                ],
                                "code_blocks": [
                                    """val chain1 = WorkManager.getInstance(context).beginWith(workA)
val chain2 = WorkManager.getInstance(context).beginWith(workB)

WorkContinuation.combine(listOf(chain1, chain2))
    .then(finalReportWorker)
    .enqueue()"""
                                ],
                            },
                        ],
                    },
            
            {
                "title": "Foreground Services",
                "icon": "",
                "description": "Reviews when foreground services are appropriate, what policies "
                "apply, and how to justify long-running visible work.",
                "content_sections": [],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: Foreground Service for Music",
                        "code": "class MusicService : Service() {\n"
                        "\n"
                        "    override fun onCreate() {\n"
                        "        startForeground(NOTIFICATION_ID, "
                        "createNotification())\n"
                        "    }\n"
                        "\n"
                        "    private fun createNotification(): Notification {\n"
                        "        return NotificationCompat.Builder(this, "
                        "CHANNEL_ID)\n"
                        '            .setContentTitle("Playing")\n'
                        "            .setContentText(songTitle)\n"
                        "            .setSmallIcon(R.drawable.ic_play)\n"
                        "            .addAction(prevAction)\n"
                        "            .addAction(playPauseAction)\n"
                        "            .addAction(nextAction)\n"
                        "            .setStyle(MediaStyle()\n"
                        "                .setShowActionsInCompactView(0, 1, 2))\n"
                        "            .build()\n"
                        "    }\n"
                        "}\n"
                        "\n"
                        "// Starting foreground service from Activity\n"
                        "val intent = Intent(this, MusicService::class.class)\n"
                        "startForegroundService(intent)",
                    }
                ],
            },
            {
                "title": "Thread Safety",
                "icon": "",
                "description": "Covers race conditions, shared mutable state, and the "
                "synchronization patterns senior engineers should understand beyond "
                "coroutine basics.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• @Volatile annotation for visibility • Atomic "
                            "operations: AtomicInteger, AtomicBoolean • Mutex "
                            "for mutual exclusion in coroutines • Thread-safe "
                            "collections: ConcurrentHashMap • Immutable data "
                            "structures preferred"
                        ],
                    }
                ],
                "code_blocks": [],
            },
        ],
        "description": "Focuses on background execution models, safe threading, and long-running work "
        "patterns that keep apps responsive while respecting platform constraints.",
    },
    {
        "id": "testing-strategy",
        "title": "Testing Strategy",
        "topics": [
            {
                "title": "Unit Testing",
                "icon": "",
                "description": "Covers the fastest feedback layer for verifying business logic, "
                "mapping, and isolated component behavior in Android apps.",
                "content_sections": [
                    {
                        "heading": "JUnit & Mockito",
                        "points": [
                            "• JUnit 4 or JUnit 5 (Jupiter)",
                            "• @Test, @Before, @After annotations",
                            "• Assertions: assertEquals, assertTrue, " "assertNotNull",
                            "• Mockito for mocking dependencies",
                            "• mock(), when(), verify()",
                        ],
                    },
                    {
                        "heading": "MockK (Kotlin)",
                        "points": [
                            "• Kotlin-first mocking library",
                            "• mockk<T>(): create mock",
                            "• every { ... } returns ...: stub behavior",
                            "• verify { ... }: verify calls",
                            "• Supports suspend functions and coroutines",
                        ],
                    },
                    {
                        "heading": "Coroutine Testing",
                        "points": [
                            "• kotlinx-coroutines-test library",
                            "• runTest: test coroutines",
                            "• TestDispatcher for controlling virtual time",
                            "• advanceTimeBy(), advanceUntilIdle()",
                        ],
                    },
                ],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: Testing ViewModels with MockK",
                        "code": "@ExtendWith(InstantTaskExecutorExtension::class)\n"
                        "class UserViewModelTest {\n"
                        "\n"
                        "    @InjectMockKs\n"
                        "    lateinit var viewModel: UserViewModel\n"
                        "\n"
                        "    @Mock\n"
                        "    lateinit var getUserUseCase: GetUserUseCase\n"
                        "\n"
                        "    @BeforeEach\n"
                        "    fun setup() {\n"
                        "        clearAllMocks()\n"
                        "    }\n"
                        "\n"
                        "    @Test\n"
                        "    fun loadUser_success() = runTest {\n"
                        "        // Given\n"
                        '        val user = User("1", "John")\n'
                        '        coEvery { getUserUseCase("1") } returns '
                        "Result.success(user)\n"
                        "\n"
                        "        // When\n"
                        '        viewModel.loadUser("1")\n'
                        "\n"
                        "        // Then\n"
                        "        assertEquals(UserUiState.Success(user), "
                        "viewModel.uiState.value)\n"
                        "    }\n"
                        "\n"
                        "    @Test\n"
                        "    fun loadUser_failure() = runTest {\n"
                        "        // Given\n"
                        '        coEvery { getUserUseCase("1") } returns\n'
                        "            Result.failure(NetworkException())\n"
                        "\n"
                        "        // When\n"
                        '        viewModel.loadUser("1")\n'
                        "\n"
                        "        // Then\n"
                        "        val state = viewModel.uiState.value as "
                        "UserUiState.Error\n"
                        '        assertTrue(state.message.contains("Network"))\n'
                        "    }\n"
                        "}",
                    }
                ],
            },
            {
                "title": "Compose UI Testing",
                "icon": "",
                "description": "Focuses on testing declarative Compose UIs with semantics, "
                "recomposition-aware assertions, state-driven checks, and practical "
                "Android UI verification patterns.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• createComposeRule(): test setup • "
                            "onNodeWithText(), onNodeWithTag() • "
                            "performClick(), performTextInput() • "
                            "assertIsDisplayed(), assertTextEquals() • "
                            "Semantics for accessibility and testing"
                        ],
                    }
                ],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: Compose UI Tests",
                        "code": "@RunWith(AndroidJUnit4::class)\n"
                        "class LoginScreenTest {\n"
                        "\n"
                        "    @get:Rule\n"
                        "    val composeTestRule = createComposeRule()\n"
                        "\n"
                        "    @Test\n"
                        "    fun login_success() {\n"
                        "        // Set content\n"
                        "        composeTestRule.setContent {\n"
                        "            LoginScreen(\n"
                        "                onLogin = { mock() }\n"
                        "            )\n"
                        "        }\n"
                        "\n"
                        "        // Find and perform actions\n"
                        '        composeTestRule.onNodeWithText("Email")\n'
                        '            .performTextInput("test@example.com")\n'
                        "\n"
                        '        composeTestRule.onNodeWithText("Password")\n'
                        '            .performTextInput("password123")\n'
                        "\n"
                        '        composeTestRule.onNodeWithText("Login")\n'
                        "            .performClick()\n"
                        "\n"
                        "        // Verify\n"
                        '        composeTestRule.onNodeWithText("Welcome")\n'
                        "            .assertIsDisplayed()\n"
                        "    }\n"
                        "\n"
                        "    @Test\n"
                        "    fun login_validation_error() {\n"
                        "        composeTestRule.setContent { LoginScreen(...) }\n"
                        "\n"
                        "        // Tap login without input\n"
                        '        composeTestRule.onNodeWithText("Login")\n'
                        "            .performClick()\n"
                        "\n"
                        "        // Verify error message\n"
                        '        composeTestRule.onNodeWithText("Email is '
                        'required")\n'
                        "            .assertIsDisplayed()\n"
                        "    }\n"
                        "}",
                    }
                ],
            },
            {
                "title": "Integration & E2E Testing",
                "icon": "",
                "description": "Explains broader test slices that validate system behavior across "
                "multiple layers and more realistic app flows.",
                "content_sections": [
                    {
                        "heading": "Key Areas",
                        "subtopics": [
                            {
                                "title": "Room Testing",
                                "description": "Use "
                                "Room.inMemoryDatabaseBuilder "
                                "for fast tests without file "
                                "I/O",
                            },
                            {
                                "title": "MockWebServer",
                                "description": "Mock HTTP responses for API "
                                "testing - control status codes, "
                                "delays, errors",
                            },
                            {
                                "title": "Hilt Test",
                                "description": "@HiltAndroidTest creates test "
                                "component with test modules",
                            },
                            {
                                "title": "Screenshot Testing",
                                "description": "Paparazzi for Compose, Shot for "
                                "View-based - catch visual "
                                "regressions",
                            },
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Instrumentation Testing",
                "icon": "",
                "description": "Reviews on-device or emulator-based testing and the tradeoffs "
                "between realism, cost, and maintenance overhead.",
                "content_sections": [
                    {
                        "heading": "Espresso (UI Testing)",
                        "points": [
                            "• onView(): find view",
                            "• perform(): perform action (click, typeText, " "swipe)",
                            "• check(): verify view state",
                            "• IdlingResource for async operations",
                            "• RecyclerView actions and assertions",
                        ],
                    },
                    {
                        "heading": "UI Automator",
                        "points": [
                            "• Cross-app interactions",
                            "• System UI testing",
                            "• UiDevice, UiObject, UiSelector",
                        ],
                    },
                    {
                        "heading": "Room Testing",
                        "points": [
                            "• In-memory database for tests",
                            "• Room.inMemoryDatabaseBuilder()",
                            "• Test migrations",
                        ],
                    },
                ],
                "code_blocks": [],
            },
            {
                "title": "Test Architecture",
                "icon": "",
                "description": "Explains how to structure tests, fakes, fixtures, and environment "
                "boundaries so Android code stays testable as complexity grows.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Test Pyramid: More unit tests, fewer UI tests • "
                            "Given-When-Then pattern • Test doubles: Mock, "
                            "Stub, Fake, Spy • Repository pattern enables easy "
                            "testing • Dependency injection makes mocking "
                            "easier • Code coverage tools: JaCoCo"
                        ],
                    }
                ],
                "code_blocks": [],
            },
        ],
        "description": "Keeps the testing section focused on distinct testing layers so Compose-specific "
        "testing is covered once, clearly, and in the right place.",
    },
    {
        "id": "performance-observability",
        "title": "Performance & Observability",
        "topics": [
            {
                "title": "App Startup Optimization",
                "icon": "",
                "description": "Covers startup performance from measurement to optimization, "
                "including critical-path reduction, deferred initialization, and "
                "launch-time diagnostics.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• App Startup library for initialization • Lazy "
                            "initialization with by lazy • ContentProvider "
                            "initialization overhead • Baseline Profiles for "
                            "faster startup • Strict Mode for detecting main "
                            "thread violations"
                        ],
                    }
                ],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: App Startup Library",
                        "code": "// Initializer for expensive initialization\n"
                        "class AnalyticsInitializer : Initializer<Analytics> {\n"
                        "    override fun create(context: Context): Analytics {\n"
                        "        return Analytics().apply {\n"
                        "            initialize(context)\n"
                        "        }\n"
                        "    }\n"
                        "\n"
                        "    override fun dependencies(): List<Class<out "
                        "Initializer<*>>> {\n"
                        "        // No dependencies\n"
                        "        return emptyList()\n"
                        "    }\n"
                        "}\n"
                        "\n"
                        "// Register in AndroidManifest.xml\n"
                        "<provider\n"
                        "    "
                        'android:name="androidx.startup.InitializationProvider"\n'
                        "    "
                        'android:authorities="${applicationId}.androidx-startup"\n'
                        '    android:exported="false">\n'
                        "    <meta-data\n"
                        '        android:name="com.example.AnalyticsInitializer"\n'
                        '        android:value="androidx.startup" />\n'
                        "</provider>",
                    }
                ],
            },
            {
                "title": "Observability",
                "icon": "",
                "description": "Brings together crash reporting, analytics, logging, and performance "
                "monitoring so Android teams can understand product health and "
                "diagnose real-world issues quickly.",
                "content_sections": [
                    {
                        "heading": "Key Areas",
                        "subtopics": [
                            {
                                "title": "Firebase Crashlytics",
                                "description": "Production crash reporting with "
                                "breadcrumbs and analytics",
                            },
                            {
                                "title": "Firebase Performance",
                                "description": "Automatic performance "
                                "monitoring - startup, network, "
                                "screen rendering",
                            },
                            {
                                "title": "Firebase Analytics",
                                "description": "User events, funnels, cohorts - "
                                "understand user behavior",
                            },
                            {
                                "title": "Remote Config",
                                "description": "Feature flags, A/B testing, "
                                "dynamic values without app "
                                "update",
                            },
                        ],
                    },
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Firebase Crashlytics • Firebase Analytics • "
                            "Custom event tracking • Performance monitoring • "
                            "Network request logging • User session recording "
                            "(where privacy permits)"
                        ],
                    },
                ],
                "code_blocks": [],
            },
            {
                "title": "Modern Android Summary",
                "icon": "",
                "description": "Explains modern android summary in the context of performance & "
                "observability, with focus on key points and the practical decisions "
                "behind patterns such as Kotlin + Coroutines + Flow for async - "
                "modern standard.",
                "content_sections": [
                    {
                        "heading": "Key Points",
                        "points": [
                            "Kotlin + Coroutines + Flow for async - modern " "standard",
                            "Jetpack Compose for UI - declarative, less code, "
                            "better performance",
                            "Hilt for DI - compile-time safety, automatic " "cleanup",
                            "Clean Architecture + MVI - testable, maintainable, "
                            "scalable",
                            "Room + DataStore - modern local persistence",
                            "WorkManager - reliable background work",
                            "CI/CD with GitHub Actions - automated testing and "
                            "builds",
                            "KMP for code sharing - future-proof your business "
                            "logic",
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Memory Management",
                "icon": "",
                "description": "Covers heap behavior, leak detection, and object-lifecycle awareness "
                "needed to keep Android apps stable over time.",
                "content_sections": [
                    {
                        "heading": "Memory Leaks",
                        "points": [
                            "• Common causes:",
                            "- Static references to Activities/Fragments",
                            "- Non-static inner classes holding Activity " "reference",
                            "- Unregistered listeners and callbacks",
                            "- Handler with Activity reference",
                            "• Detection: LeakCanary library",
                            "• Prevention: WeakReference, proper lifecycle " "handling",
                        ],
                    },
                    {
                        "heading": "Memory Optimization",
                        "points": [
                            "• Bitmap management: inSampleSize, recycle()",
                            "• Image loading libraries: Glide, Coil",
                            "• Avoid object churn in loops",
                            "• Use SparseArray instead of HashMap for int keys",
                            "• onTrimMemory() callback for memory pressure",
                        ],
                    },
                ],
                "code_blocks": [],
            },
            {
                "title": "UI Performance",
                "icon": "",
                "description": "Reviews rendering performance concerns such as layout cost, "
                "recomposition, scrolling smoothness, and overdraw.",
                "content_sections": [
                    {
                        "heading": "Layout Performance",
                        "points": [
                            "• Flatten view hierarchy with ConstraintLayout",
                            "• Avoid nested LinearLayouts with weights",
                            "• ViewStub for lazy inflation",
                            "• Merge tag to reduce hierarchy",
                            "• Include tag for reusable layouts",
                        ],
                    },
                    {
                        "heading": "Rendering Performance",
                        "points": [
                            "• 16ms per frame for 60fps (jank threshold)",
                            "• Systrace for performance profiling",
                            "• GPU overdraw: minimize overlapping draws",
                            "• Hardware acceleration",
                            "• RecyclerView optimization: setHasFixedSize(), "
                            "setItemViewCacheSize()",
                        ],
                    },
                    {
                        "heading": "Compose Performance",
                        "points": [
                            "• Minimize recomposition scope",
                            "• Use derivedStateOf for computed state",
                            "• key() for stable item identity in lists",
                            "• Avoid unstable parameters in Composables",
                            "• LazyColumn performance best practices",
                        ],
                    },
                ],
                "code_blocks": [],
            },
            {
                "title": "Battery Optimization",
                "icon": "",
                "description": "Explains how background behavior, networking, wakeups, and "
                "scheduling choices affect battery usage and system limits.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Doze mode and App Standby • Battery Historian "
                            "tool • WorkManager for battery-efficient "
                            "background work • Reduce network calls, batch "
                            "requests • Use JobScheduler constraints • Wake "
                            "locks: use carefully, release properly"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "APK Size Optimization",
                "icon": "",
                "description": "Covers strategies for reducing binary size, modularizing delivery, "
                "and shipping only what each device actually needs.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• ProGuard/R8 for code shrinking • Resource "
                            "shrinking: shrinkResources true • Vector drawables "
                            "instead of PNGs • WebP format for images • Android "
                            "App Bundle (AAB) for dynamic delivery • Remove "
                            "unused libraries and resources"
                        ],
                    }
                ],
                "code_blocks": [],
            },
        ],
        "description": "Combines performance tuning and production observability into non-overlapping "
        "topics that reflect how senior engineers reason about quality in real apps.",
    },
    {
        "id": "security-privacy-app-integrity",
        "title": "Security, Privacy & App Integrity",
        "topics": [
            {
                "title": "Secure Storage",
                "icon": "",
                "description": "Explains secure local storage options for secrets and sensitive user "
                "data on Android devices.",
                "content_sections": [],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: Encrypted SharedPreferences",
                        "code": "val masterKey = MasterKey.Builder(context)\n"
                        "    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)\n"
                        "    .build()\n"
                        "\n"
                        "val encryptedPrefs = EncryptedSharedPreferences.create(\n"
                        "    context,\n"
                        '    "secure_prefs",\n'
                        "    masterKey,\n"
                        "    "
                        "EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,\n"
                        "    "
                        "EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM\n"
                        ")\n"
                        "\n"
                        "// Usage\n"
                        'encryptedPrefs.edit().putString("token", '
                        "authToken).apply()\n"
                        "\n"
                        "// Encrypted File\n"
                        'val file = File(context.filesDir, "secure.dat")\n'
                        "val encryptedFile = EncryptedFile.Builder(\n"
                        "    context,\n"
                        "    file,\n"
                        "    masterKey,\n"
                        "    "
                        "EncryptedFile.FileEncryptionScheme.AES256_GCM_HKDF_4KB\n"
                        ").build()",
                    }
                ],
            },
            {
                "title": "Biometric Authentication",
                "icon": "",
                "description": "Reviews biometric flows and the user experience, security, and "
                "fallback patterns expected in sensitive Android features.",
                "content_sections": [],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: BiometricPrompt",
                        "code": "val executor = ContextCompat.getMainExecutor(context)\n"
                        "\n"
                        "val biometricPrompt = BiometricPrompt(\n"
                        "    activity,\n"
                        "    executor,\n"
                        "    object : BiometricPrompt.AuthenticationCallback() {\n"
                        "        override fun onAuthenticationSucceeded(result: "
                        "BiometricPrompt.AuthenticationResult) {\n"
                        "            unlockSensitiveData()\n"
                        "        }\n"
                        "\n"
                        "        override fun onAuthenticationError(errorCode: Int, "
                        "errString: CharSequence) {\n"
                        "            showError(errString)\n"
                        "        }\n"
                        "    }\n"
                        ")\n"
                        "\n"
                        "val promptInfo = BiometricPrompt.PromptInfo.Builder()\n"
                        '    .setTitle("Authenticate")\n'
                        '    .setSubtitle("Use your fingerprint")\n'
                        '    .setNegativeButtonText("Use password")\n'
                        "    .setAllowedAuthenticators(\n"
                        "        BiometricManager.Authenticators.BIOMETRIC_STRONG "
                        "or\n"
                        "        BiometricManager.Authenticators.DEVICE_CREDENTIAL\n"
                        "    )\n"
                        "    .build()\n"
                        "\n"
                        "biometricPrompt.authenticate(promptInfo)",
                    }
                ],
            },
            {
                "title": "Play Integrity API",
                "icon": "",
                "description": "Introduces device and app integrity signals that can help protect "
                "sensitive flows against tampering and abuse.",
                "content_sections": [],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: Play Integrity Check",
                        "code": "val integrityManager = IntegrityManager.create(context)\n"
                        "val tokenRequest = IntegrityTokenRequest.builder()\n"
                        "    .setNonce(generateNonce())\n"
                        "    .requestVerification()\n"
                        "    .build()\n"
                        "\n"
                        "integrityManager.requestIntegrityToken(tokenRequest)\n"
                        "    .addOnSuccessListener { response ->\n"
                        "        val token = response.token()\n"
                        "        verifyOnServer(token)\n"
                        "    }\n"
                        "    .addOnFailureListener { e ->\n"
                        "        handleError(e)\n"
                        "    }",
                    }
                ],
            },
            {
                "title": "Data Security",
                "icon": "",
                "description": "Covers the broad data-protection mindset expected in Android apps, "
                "from storage and transport to least-privilege access.",
                "content_sections": [
                    {
                        "heading": "Encrypted Storage",
                        "points": [
                            "• EncryptedSharedPreferences for sensitive "
                            "key-value data",
                            "• SQLCipher for database encryption",
                            "• Android Keystore for cryptographic keys",
                            "• BiometricPrompt for user authentication",
                        ],
                    },
                    {
                        "heading": "Network Security",
                        "points": [
                            "• HTTPS only, no HTTP",
                            "• Certificate pinning for critical APIs",
                            "• Network Security Configuration (XML)",
                            "• Validate SSL certificates",
                            "• Don't trust user input",
                        ],
                    },
                ],
                "code_blocks": [],
            },
            {
                "title": "Code Security",
                "icon": "",
                "description": "Reviews hardening practices aimed at reducing reverse engineering, "
                "insecure defaults, and avoidable attack surface.",
                "content_sections": [
                    {
                        "heading": "ProGuard/R8",
                        "points": [
                            "• Code obfuscation",
                            "• Makes reverse engineering harder",
                            "• Keep rules for reflection and serialization",
                        ],
                    },
                    {
                        "heading": "SafetyNet/Play Integrity API",
                        "points": [
                            "• Device attestation",
                            "• Detect rooted devices",
                            "• Verify app integrity",
                        ],
                    },
                    {
                        "heading": "Input Validation",
                        "points": [
                            "• Sanitize all user inputs",
                            "• SQL injection prevention with Room",
                            "• Avoid eval() or dynamic code execution",
                        ],
                    },
                ],
                "code_blocks": [],
            },
            {
                "title": "Authentication & Authorization",
                "icon": "",
                "description": "Explains identity verification and access-control concepts as they "
                "appear in mobile app flows and backend integration.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• OAuth 2.0 / OpenID Connect • JWT tokens with "
                            "proper expiration • Refresh token strategy • Never "
                            "store passwords in plain text • Biometric "
                            "authentication where appropriate"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Permissions",
                "icon": "",
                "description": "Covers the Android permission model, runtime request strategy, and "
                "how to minimize friction while respecting privacy.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Request minimum permissions needed • Runtime "
                            "permissions (Android 6.0+) • Handle permission "
                            "denial gracefully • Location permissions: precise "
                            "vs approximate • Background location: additional "
                            "justification needed"
                        ],
                    }
                ],
                "code_blocks": [],
            },
        ],
        "description": "Collects the security foundations required for modern Android apps, including "
        "storage hardening, authentication flows, permissions, and tamper protection.",
    },
    {
        "id": "build-release-ci-cd",
        "title": "Modern Build Systems, Release & CI/CD",
        "topics": [
            {
                "title": "GitHub Actions for Android",
                "icon": "",
                "description": "Shows how Android teams automate validation, builds, and artifact "
                "generation within a modern CI workflow.",
                "content_sections": [],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: CI Pipeline",
                        "code": "# .github/workflows/ci.yml\n"
                        "name: CI\n"
                        "\n"
                        "on:\n"
                        "  push:\n"
                        "    branches: [main]\n"
                        "  pull_request:\n"
                        "    branches: [main]\n"
                        "\n"
                        "jobs:\n"
                        "  build:\n"
                        "    runs-on: ubuntu-latest\n"
                        "\n"
                        "    steps:\n"
                        "      - uses: actions/checkout@v4\n"
                        "\n"
                        "      - name: Set up JDK\n"
                        "        uses: actions/setup-java@v4\n"
                        "        with:\n"
                        "          java-version: '17'\n"
                        "          distribution: 'temurin'\n"
                        "\n"
                        "      - name: Cache Gradle\n"
                        "        uses: actions/cache@v3\n"
                        "        with:\n"
                        "          path: ~/.gradle/caches\n"
                        "          key: ${{ runner.os }}-gradle-${{ "
                        "hashFiles('**/*.gradle*') }}\n"
                        "\n"
                        "      - name: Run tests\n"
                        "        run: ./gradlew test\n"
                        "\n"
                        "      - name: Run lint\n"
                        "        run: ./gradlew lintDebug\n"
                        "\n"
                        "      - name: Build debug APK\n"
                        "        run: ./gradlew assembleDebug\n"
                        "\n"
                        "      - name: Upload APK\n"
                        "        uses: actions/upload-artifact@v3\n"
                        "        with:\n"
                        "          name: app-debug\n"
                        "          path: "
                        "app/build/outputs/apk/debug/app-debug.apk",
                    }
                ],
            },
            {
                "title": "Code Quality Gates",
                "icon": "",
                "description": "Explains the automated checks that protect maintainability and keep "
                "regressions from reaching shared branches or releases.",
                "content_sections": [
                    {
                        "heading": "Key Areas",
                        "subtopics": [
                            {
                                "title": "Detekt",
                                "description": "Kotlin-specific static analysis "
                                "- complexity, code smells, "
                                "style",
                            },
                            {
                                "title": "ktlint",
                                "description": "Code style enforcement - "
                                "consistent formatting across "
                                "team",
                            },
                            {
                                "title": "Kover",
                                "description": "Kotlin code coverage - track "
                                "test coverage in CI",
                            },
                            {
                                "title": "Danger",
                                "description": "Automated code review comments "
                                "on PRs",
                            },
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Gradle & Build System",
                "icon": "",
                "description": "Combines Android build-system fundamentals with modern Gradle "
                "practices such as version catalogs, dependency modeling, plugin "
                "setup, and build optimization.",
                "content_sections": [
                    {
                        "heading": "Build Configuration",
                        "points": [
                            "• build.gradle (project level)",
                            "• build.gradle (module level)",
                            "• gradle.properties for project-wide settings",
                            "• Build types: debug, release",
                            "• Product flavors for app variants",
                            "• Build variants: combination of type and flavor",
                        ],
                    },
                    {
                        "heading": "Dependencies",
                        "points": [
                            "• implementation: compile time only",
                            "• api: transitive dependencies",
                            "• testImplementation: unit tests",
                            "• androidTestImplementation: instrumentation tests",
                            "• Version catalogs for centralized dependency "
                            "management",
                        ],
                    },
                    {
                        "heading": "Optimization",
                        "points": [
                            "• Gradle daemon",
                            "• Parallel execution",
                            "• Configuration cache",
                            "• Build cache",
                            "• Incremental compilation",
                        ],
                    },
                ],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: Version Catalogs (libs.versions.toml)",
                        "code": "# gradle/libs.versions.toml\n"
                        "[versions]\n"
                        'kotlin = "1.9.22"\n'
                        'compose = "1.5.8"\n'
                        'hilt = "2.50"\n'
                        'room = "2.6.1"\n'
                        "\n"
                        "[libraries]\n"
                        'kotlin-stdlib = { group = "org.jetbrains.kotlin", name = '
                        '"kotlin-stdlib" }\n'
                        'compose-ui = { group = "androidx.compose.ui", name = "ui" '
                        "}\n"
                        'hilt-android = { group = "com.google.dagger", name = '
                        '"hilt-android" }\n'
                        'room-runtime = { group = "androidx.room", name = '
                        '"room-runtime" }\n'
                        "\n"
                        "[plugins]\n"
                        'kotlin-android = { id = "org.jetbrains.kotlin.android", '
                        'version.ref = "kotlin" }\n'
                        'hilt = { id = "com.google.dagger.hilt.android", '
                        'version.ref = "hilt" }\n'
                        "\n"
                        "# app/build.gradle.kts\n"
                        "plugins {\n"
                        "    alias(libs.plugins.kotlin.android)\n"
                        "    alias(libs.plugins.hilt)\n"
                        "}\n"
                        "\n"
                        "dependencies {\n"
                        "    implementation(libs.compose.ui)\n"
                        "    implementation(libs.hilt.android)\n"
                        "}",
                    }
                ],
            },
            {
                "title": "The Shift to Kotlin DSL & Gradle 8+",
                "description": "Modern Android builds have moved from Groovy to type-safe Kotlin scripting, making build logic as maintainable as app code.",
                "content_sections": [
                    {
                        "heading": "Kotlin DSL (.gradle.kts)",
                        "points": [
                            "Full IDE support with auto-completion, refactoring, and source-code navigation.",
                            'Compile-time error checking, eliminating "guesswork" when configuring complex build logic.',
                            "Standardized syntax (double quotes, explicit assignments) ensures consistency across team members.",
                        ],
                    },
                    {
                        "heading": "Version Catalogs (TOML)",
                        "points": [
                            "Centralizes all dependencies and versions in a single `libs.versions.toml` file.",
                            'Eliminates "magic strings" and manual version syncing across multi-module projects.',
                            "Enables type-safe accessors in build scripts (e.g., alias(libs.androidx.compose)).",
                        ],
                    },
                    {
                        "heading": "Convention Plugins",
                        "points": [
                            'Replaces massive "common.gradle" files with reusable Kotlin logic in the `buildSrc` or `composite builds`.',
                            'Allows teams to define "Standard Android Library" or "Compose UI" configurations once.',
                            "Significantly reduces boilerplate in module-level build files.",
                        ],
                    },
                ],
            },
            {
                "title": "Kotlin DSL & Gradle Evolution",
                "description": "The modern Android build system leverages Kotlin DSL and advanced Gradle features to provide a type-safe, performant developer experience.",
                "content_sections": [
                    {
                        "heading": "Core Benefits of Kotlin DSL",
                        "points": [
                            "Type Safety: Catch errors at compile-time instead of runtime during builds.",
                            "IDE Support: Full auto-completion, syntax highlighting, and refactoring in Android Studio.",
                            "Unified Language: Use Kotlin for both app logic and build configuration for better consistency.",
                            'Maintainability: Stricter syntax (double quotes, explicit "=" assignments) makes scripts predictable.',
                        ],
                    },
                    {
                        "heading": "Modern Configuration Components",
                        "points": [
                            "settings.gradle.kts: Defines project-level repositories and module structure.",
                            "Root build.gradle.kts: Manages global plugin versions and common build logic.",
                            "Module build.gradle.kts: Configures SDK versions, build types, and specific dependencies.",
                            "Version Catalogs (TOML): Centralizes dependency management in libs.versions.toml for multi-module consistency.",
                        ],
                    },
                    {
                        "heading": "Advanced Build Features",
                        "points": [
                            "Declarative Plugins: Use the plugins {} block for type-safe accessors over old apply syntax.",
                            "Build Variants: Manage productFlavors and buildTypes natively within Kotlin scripts.",
                            "KSP Integration: Using Kotlin Symbol Processing (KSP) instead of kapt for significantly faster build speeds.",
                        ],
                    },
                ],
            },
            {
                "title": "Continuous Integration",
                "icon": "",
                "description": "Explains CI as the feedback loop that continuously validates changes "
                "through build, test, and static-analysis steps.",
                "content_sections": [
                    {
                        "heading": "CI Platforms",
                        "points": [
                            "• GitHub Actions",
                            "• GitLab CI",
                            "• Jenkins",
                            "• CircleCI",
                            "• Bitrise",
                        ],
                    },
                    {
                        "heading": "Pipeline Stages",
                        "points": [
                            "• Code checkout",
                            "• Build",
                            "• Unit tests",
                            "• Instrumentation tests (on emulator/device)",
                            "• Lint checks",
                            "• Static analysis (Detekt, ktlint)",
                            "• Code coverage reports",
                            "• APK/AAB generation",
                            "• Signing",
                            "• Upload to distribution (Firebase App "
                            "Distribution, TestFlight)",
                        ],
                    },
                ],
                "code_blocks": [],
            },
            {
                "title": "Continuous Deployment",
                "icon": "",
                "description": "Covers the release automation path from tested artifacts to "
                "controlled rollout across testing and production tracks.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Fastlane for automation • Google Play Console "
                            "API • Internal testing track • Closed testing "
                            "(alpha/beta) • Open testing • Production release "
                            "with staged rollout • Release management and "
                            "versioning"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "App Signing",
                "icon": "",
                "description": "Explains how Android signing works, why key management matters, and "
                "how signing fits into release workflows.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Debug keystore for development • Release "
                            "keystore for production • Google Play App Signing "
                            "• Keep upload key secure • Signing configurations "
                            "in Gradle"
                        ],
                    }
                ],
                "code_blocks": [],
            },
        ],
        "description": "Covers the Android delivery lifecycle cleanly, from local build logic and Gradle "
        "structure to CI pipelines, release automation, and signing.",
    },
    {
        "id": "advanced-modern-android-topics",
        "title": "Advanced Modern Android Topics",
        "topics": [
            {
                "title": "ML Kit",
                "icon": "",
                "description": "Summarizes ml kit as part of the broader advanced modern android "
                "topics study area for senior Android interview preparation.",
                "content_sections": [],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: Text Recognition",
                        "code": "// Text Recognition\n"
                        "val recognizer = "
                        "TextRecognition.getClient(TextRecognizerOptions.DEFAULT_OPTIONS)\n"
                        "\n"
                        "val image = InputImage.fromBitmap(bitmap, 0)\n"
                        "recognizer.process(image)\n"
                        "    .addOnSuccessListener { text ->\n"
                        "        for (block in text.textBlocks) {\n"
                        '            Log.d("OCR", block.text)\n'
                        "        }\n"
                        "    }\n"
                        "    .addOnFailureListener { e ->\n"
                        '        Log.e("OCR", e.message)\n'
                        "    }\n"
                        "\n"
                        "// Face Detection\n"
                        "val faceDetector = FaceDetection.getClient(\n"
                        "    FaceDetectorOptions.Builder()\n"
                        "        "
                        ".setPerformanceMode(FaceDetectorOptions.PERFORMANCE_MODE_ACCURATE)\n"
                        "        "
                        ".setLandmarkMode(FaceDetectorOptions.LANDMARK_MODE_ALL)\n"
                        "        .build()\n"
                        ")",
                    }
                ],
            },
            {
                "title": "TensorFlow Lite",
                "icon": "",
                "description": "Summarizes tensorflow lite as part of the broader advanced modern "
                "android topics study area for senior Android interview preparation.",
                "content_sections": [],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: TFLite Inference",
                        "code": "// Load and run TFLite model\n"
                        'val model = TFLite.loadModelFromAssets("model.tflite")\n'
                        "val interpreter = Interpreter(model)\n"
                        "\n"
                        "val input = Array(1) { FloatArray(224 * 224 * 3) }\n"
                        "val output = Array(1) { FloatArray(1000) }\n"
                        "\n"
                        "interpreter.run(input, output)\n"
                        "\n"
                        "// With GPU delegate for acceleration\n"
                        "val gpuDelegate = GpuDelegate()\n"
                        "val options = "
                        "Interpreter.Options().addDelegate(gpuDelegate)\n"
                        "val interpreter = Interpreter(model, options)",
                    }
                ],
            },
            {
                "title": "LLM Integration",
                "icon": "",
                "description": "Summarizes llm integration as part of the broader advanced modern "
                "android topics study area for senior Android interview preparation.",
                "content_sections": [],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: Gemini API Integration",
                        "code": "// Using Gemini API\n"
                        "val generativeModel = GenerativeModel(\n"
                        '    modelName = "gemini-pro",\n'
                        "    apiKey = BuildConfig.GEMINI_API_KEY\n"
                        ")\n"
                        "\n"
                        "suspend fun generateResponse(prompt: String): String {\n"
                        "    val response = "
                        "generativeModel.generateContent(prompt)\n"
                        "    return response.text\n"
                        "}\n"
                        "\n"
                        "// Streaming response\n"
                        "fun generateStream(prompt: String): Flow<String> = flow {\n"
                        "    generativeModel.generateContentStream(prompt)\n"
                        "        .collect { chunk ->\n"
                        '            emit(chunk.text ?: "")\n'
                        "        }\n"
                        "}",
                    }
                ],
            },
            {
                "title": "KMP Fundamentals",
                "icon": "",
                "description": "Explains kmp fundamentals in the context of advanced modern android "
                "topics, with focus on key points and the practical decisions behind "
                "patterns such as expect/actual pattern for platform-specific "
                "implementations.",
                "content_sections": [
                    {
                        "heading": "Key Points",
                        "points": [
                            "expect/actual pattern for platform-specific "
                            "implementations",
                            "Ktor for multiplatform HTTP, SQLDelight for " "database",
                            "Compose Multiplatform for shared UI (evolving)",
                        ],
                    }
                ],
                "code_blocks": [
                    {
                        "language": "kotlin",
                        "title": "Example: Shared Code Structure",
                        "code": "// commonMain/kotlin/Repository.kt\n"
                        "expect class HttpClient() {\n"
                        "    suspend fun get(url: String): String\n"
                        "    suspend fun post(url: String, body: String): String\n"
                        "}\n"
                        "\n"
                        "// androidMain/kotlin/HttpClient.kt\n"
                        "actual class HttpClient actual constructor() {\n"
                        "    private val client = OkHttpClient()\n"
                        "\n"
                        "    actual suspend fun get(url: String): String {\n"
                        "        return "
                        "client.newCall(Request.Builder().url(url).build())\n"
                        '            .execute().body?.string ?: ""\n'
                        "    }\n"
                        "\n"
                        "    actual suspend fun post(url: String, body: String): "
                        "String { ... }\n"
                        "}\n"
                        "\n"
                        "// iosMain/kotlin/HttpClient.kt\n"
                        "actual class HttpClient actual constructor() {\n"
                        "    // NSURLSession implementation\n"
                        "}",
                    }
                ],
            },
            {
                "title": "Modern Android Development",
                "icon": "",
                "description": "Highlights broader modern Android trends and platform shifts that "
                "often come up in senior-level discussions.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Kotlin Multiplatform Mobile (KMM) • Jetpack "
                            "Compose for Desktop • Material Design 3 (Material "
                            "You) • Baseline profiles for improved performance "
                            "• Android 13+ features: predictive back gesture, "
                            "notification permissions • Privacy Sandbox on "
                            "Android"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Firebase Services",
                "icon": "",
                "description": "Summarizes the Firebase tools most often used to add messaging, "
                "analytics, remote config, and distribution capabilities to Android "
                "apps.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Firebase Cloud Messaging (FCM) • Firebase Remote "
                            "Config • Firebase Authentication • Cloud Firestore "
                            "• Firebase Analytics • Firebase Crashlytics • "
                            "Firebase Performance Monitoring • Firebase App "
                            "Distribution"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Android App Links & Deep Linking",
                "icon": "",
                "description": "Covers how Android apps participate in URL routing, verified links, "
                "and in-app navigation entry points.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Intent filters for custom schemes • Android App "
                            "Links (verified HTTPS links) • assetlinks.json for "
                            "domain verification • Navigation deeplinks • "
                            "Dynamic links (Firebase)"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Accessibility",
                "icon": "",
                "description": "Reviews the accessibility expectations of well-built Android apps, "
                "from semantics and touch targets to assistive-tech testing.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Content descriptions for screen readers • "
                            "Minimum touch target size (48dp) • Color contrast "
                            "ratios • Focus order and keyboard navigation • "
                            "Accessibility scanner tool • TalkBack testing"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Localization & Internationalization",
                "icon": "",
                "description": "Explains how Android apps adapt content, layout, and formatting for "
                "multiple locales and writing directions.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• strings.xml for different locales • RTL "
                            "(Right-to-Left) layout support • Date, time, and "
                            "number formatting • Plurals and quantity strings • "
                            "Locale-specific resources"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Google Play Store",
                "icon": "",
                "description": "Covers the release-surface concerns beyond code, including listing "
                "quality, policy requirements, and monetization setup.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• App listing optimization (ASO) • Screenshot and "
                            "video requirements • Privacy policy requirements • "
                            "Data safety section • In-app purchases and "
                            "subscriptions • Play Billing Library • Store "
                            "listing experiments (A/B testing)"
                        ],
                    }
                ],
                "code_blocks": [],
            },
        ],
        "description": "Brings together newer areas that often differentiate senior candidates, such as "
        "KMP, ML features, Firebase tooling, accessibility, and store-readiness topics.",
    },
    {
        "id": "system-design-for-mobile",
        "title": "System Design for Mobile",
        "topics": [
            {
                "title": "Mobile System Design Principles",
                "icon": "",
                "description": "Introduces the system-design principles that matter most on mobile, "
                "especially around connectivity, storage, and resource constraints.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Offline-first architecture • Local database as "
                            "single source of truth • Background sync "
                            "strategies • Handling intermittent connectivity • "
                            "Data consistency and conflict resolution • Battery "
                            "and bandwidth optimization"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Common Design Scenarios",
                "icon": "",
                "description": "Walks through common product patterns senior Android engineers are "
                "expected to reason about in system-design rounds.",
                "content_sections": [
                    {
                        "heading": "News Feed App",
                        "points": [
                            "• Pagination with paging 3 library",
                            "• Pull-to-refresh",
                            "• Image caching strategy",
                            "• Push notifications for new content",
                            "• Room database for offline access",
                            "• Sync strategy: periodic WorkManager",
                        ],
                    },
                    {
                        "heading": "Chat Application",
                        "points": [
                            "• WebSocket for real-time messaging",
                            "• Message queue for offline messages",
                            "• Local database for message history",
                            "• Delivery and read receipts",
                            "• Push notifications with FCM",
                            "• Media upload/download with progress",
                        ],
                    },
                    {
                        "heading": "E-commerce App",
                        "points": [
                            "• Product catalog with search and filters",
                            "• Shopping cart management",
                            "• Payment gateway integration",
                            "• Order tracking",
                            "• Wishlist sync across devices",
                            "• Product recommendations engine",
                        ],
                    },
                    {
                        "heading": "Ride-sharing App",
                        "points": [
                            "• Real-time location tracking",
                            "• Map integration (Google Maps SDK)",
                            "• Driver-rider matching algorithm",
                            "• ETA calculation",
                            "• WebSocket for live updates",
                            "• Background location updates",
                        ],
                    },
                ],
                "code_blocks": [],
            },
            {
                "title": "Scalability Considerations",
                "icon": "",
                "description": "Highlights the scale-related concerns that influence mobile "
                "architecture over time, from rollout safety to compatibility and "
                "caching.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• API versioning strategy • Backward compatibility "
                            "• Feature flags for gradual rollout • A/B testing "
                            "infrastructure • Analytics and crash reporting • "
                            "CDN for static assets • Distributed caching"
                        ],
                    }
                ],
                "code_blocks": [],
            },
        ],
        "description": "Frames mobile system design from an Android perspective, including offline-first "
        "thinking, sync strategy, scalability, and platform-aware tradeoffs.",
    },
    {
        "id": "leadership-behavioral-questions",
        "title": "Leadership & Behavioral Questions",
        "topics": [
            {
                "title": "Technical Leadership",
                "icon": "",
                "description": "Frames the leadership conversations that assess mentoring, code "
                "quality influence, and technical decision-making maturity.",
                "content_sections": [
                    {
                        "heading": "Common Questions",
                        "points": [
                            "• How do you mentor junior developers?",
                            "• Describe your code review process",
                            "• How do you make architectural decisions?",
                            "• Tell me about a time you had to refactor a large "
                            "codebase",
                            "• How do you handle technical debt?",
                            "• Describe a complex technical problem you " "solved",
                        ],
                    },
                    {
                        "heading": "Key Points to Cover",
                        "points": [
                            "• Collaboration with product and design teams",
                            "• Setting coding standards",
                            "• Knowledge sharing (tech talks, documentation)",
                            "• Balancing speed and quality",
                            "• Technology evaluation and adoption",
                        ],
                    },
                ],
                "code_blocks": [],
            },
            {
                "title": "Project Management",
                "icon": "",
                "description": "Covers delivery-oriented questions around estimation, "
                "prioritization, planning, and handling shifting constraints.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• How do you estimate tasks? • Tell me about a "
                            "project that went off track • How do you "
                            "prioritize features? • Describe your sprint "
                            "planning process • How do you handle changing "
                            "requirements? • Working with distributed teams"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Problem-Solving Approach",
                "icon": "",
                "description": "Focuses on how senior engineers investigate issues, make tradeoffs, "
                "and communicate through ambiguity or production pressure.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Describe your debugging process • How do you "
                            "approach performance issues? • Tell me about a "
                            "production incident you handled • How do you stay "
                            "updated with Android development? • Describe a "
                            "time you disagreed with a team decision"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "STAR Method for Behavioral Questions",
                "icon": "",
                "description": "Provides a concise structure for answering behavioral questions with "
                "enough context, ownership, and measurable outcome.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "S - Situation: Set the context T - Task: Describe "
                            "your responsibility A - Action: Explain what you "
                            "did R - Result: Share the outcome and learnings"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Cultural Fit Questions",
                "icon": "",
                "description": "Summarizes the reflective questions used to understand motivation, "
                "self-awareness, and alignment with team culture.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Why do you want to work for our company? • What "
                            "excites you about Android development? • Where do "
                            "you see yourself in 5 years? • What are your "
                            "strengths and weaknesses? • How do you handle "
                            "criticism? • What motivates you?"
                        ],
                    }
                ],
                "code_blocks": [],
            },
        ],
        "description": "Prepares for the senior-level interview rounds that assess mentoring, "
        "decision-making, delivery ownership, and cross-functional influence.",
    },
    {
        "id": "interview-preparation-strategy",
        "title": "Interview Preparation Strategy",
        "topics": [
            {
                "title": "Before the Interview",
                "icon": "",
                "description": "Outlines the preparation work that most improves confidence and "
                "recall before a senior Android interview loop begins.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Research the company's Android apps • Review "
                            "their tech stack (job description, tech blogs) • "
                            "Practice coding on whiteboard or online editors • "
                            "Prepare questions to ask the interviewer • Review "
                            "your own projects and be ready to discuss • Update "
                            "your portfolio/GitHub with recent work"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "During the Interview",
                "icon": "",
                "description": "Covers the communication habits and problem-solving behaviors that "
                "make your technical reasoning easier for interviewers to follow.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Think aloud - explain your reasoning • Ask "
                            "clarifying questions before coding • Consider edge "
                            "cases and error handling • Discuss trade-offs in "
                            "your solutions • Be honest about what you don't "
                            "know • Show enthusiasm for learning"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Common Coding Questions",
                "icon": "",
                "description": "Summarizes the implementation-style problems that commonly appear in "
                "senior Android interview rounds.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Implement a custom View • Create a simple cache "
                            "with LRU eviction • Design a ViewModel for a "
                            "specific screen • Implement pagination for a list "
                            "• Handle configuration changes properly • "
                            "Implement a simple dependency injection container "
                            "• Debug a memory leak scenario"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Questions to Ask Interviewer",
                "icon": "",
                "description": "Helps you finish interviews strongly by asking questions that reveal "
                "team maturity, technical depth, and growth opportunities.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• What does your typical sprint look like? • How "
                            "do you handle technical debt? • What's your code "
                            "review process? • How do you support career "
                            "growth? • What are the biggest technical "
                            "challenges? • How is the Android team structured? "
                            "• What metrics do you track for app quality?"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Overview",
                "icon": "",
                "description": "Wraps the guide into a final revision summary that reinforces the "
                "main themes senior Android candidates should keep top of mind.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "This comprehensive guide covers the essential "
                            "topics for Android interviews at product-based "
                            "MNCs for candidates with 10+ years of experience. "
                            "Key focus areas: 1. Demonstrate deep understanding "
                            "of Android fundamentals 2. Show expertise in "
                            "modern tools: Kotlin, Coroutines, Flow, Compose 3. "
                            "Emphasize architectural thinking and design "
                            "patterns 4. Highlight testing, CI/CD, and quality "
                            "practices 5. Showcase leadership experience and "
                            "mentoring abilities 6. Be prepared for system "
                            "design discussions Remember: Senior roles value "
                            "breadth and depth of knowledge, along with the "
                            "ability to make informed decisions, mentor others, "
                            "and drive technical excellence. Good luck with "
                            "your interviews! --- Prepared: April 2026 For: "
                            "Ranganathan | 10+ Years Experience"
                        ],
                    }
                ],
                "code_blocks": [],
            },
        ],
        "description": "Turns the guide into a practical revision plan with preparation tactics, "
        "question framing, and final-round interview habits.",
    },
    {
        "id": "resources-references",
        "title": "Resources & References",
        "topics": [
            {
                "title": "Official Documentation",
                "icon": "",
                "description": "Points to the most authoritative product and language documentation "
                "for accurate Android learning and interview refreshers.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• developer.android.com - Official Android "
                            "documentation • kotlinlang.org - Kotlin official "
                            "site • developer.android.com/jetpack/compose - "
                            "Compose docs • Android Developers YouTube "
                            "channel"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Learning Platforms",
                "icon": "",
                "description": "Highlights structured learning sources that are useful when you want "
                "guided refreshers or targeted practice on Android topics.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Android Developers Codelabs • Udacity Android "
                            "courses • Coursera Android specializations • Ray "
                            "Wenderlich tutorials • Medium articles and "
                            "publications"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Communities",
                "icon": "",
                "description": "Lists the communities where Android engineers share solutions, "
                "trends, release notes, and practical troubleshooting advice.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Stack Overflow • Reddit: r/androiddev • Android "
                            "Dev Discord servers • LinkedIn Android groups • "
                            "Local Android meetups and conferences"
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Recommended Books",
                "icon": "",
                "description": "Collects high-value books that deepen Android fundamentals, software "
                "craftsmanship, and architectural thinking.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            '• "Android Programming: The Big Nerd Ranch Guide" '
                            '• "Kotlin Coroutines by Tutorials" • "Effective '
                            'Java" by Joshua Bloch • "Clean Code" by Robert C. '
                            'Martin • "Design Patterns" - Gang of Four'
                        ],
                    }
                ],
                "code_blocks": [],
            },
            {
                "title": "Tools & Libraries to Know",
                "icon": "",
                "description": "Summarizes the tools senior Android engineers should recognize for "
                "debugging, API work, performance analysis, and daily delivery.",
                "content_sections": [
                    {
                        "heading": "Highlights",
                        "points": [
                            "• Android Studio (IDE) • Postman (API testing) • "
                            "Charles Proxy (network debugging) • Stetho (debug "
                            "bridge) • LeakCanary (memory leak detection) • "
                            "Flipper (debugging platform)"
                        ],
                    }
                ],
                "code_blocks": [],
            },
        ],
        "description": "Lists the documentation, communities, tools, and learning sources that are most "
        "useful for continued Android interview preparation and day-to-day growth.",
    },
]


def _load_extra_content(filename, default_description):
    extra_path = Path(__file__).with_name(filename)
    if not extra_path.exists():
        return []

    raw_items = literal_eval(extra_path.read_text(encoding="utf-8"))
    cleaned_items = []

    for item in raw_items:
        cleaned = dict(item)
        title = str(cleaned.get("title", "")).strip()
        cleaned["title"] = title.split(". ", 1)[1] if ". " in title else title
        cleaned.setdefault("description", default_description)
        cleaned_items.append(cleaned)

    return cleaned_items


_merged_content = (
    _load_extra_content(
        "content_jetpack_components_all.py",
        "Covers Jetpack-focused Android areas with a more forward-looking, 2026-style deep dive so these platform capabilities stay prominent in the study path.",
    )
    + _load_extra_content(
        "content_architecture.py",
        "Expands the architecture portion of the guide with modern Android design patterns, clean layering, modularization, and DI tradeoffs that are especially useful in senior interviews.",
    )
    + CONTENT
)

CONTENT = []
_seen_ids = set()
_seen_titles = set()
for _section in _merged_content:
    _section_id = _section.get("id") or _section.get("title")
    _section_title = " ".join(str(_section.get("title", "")).lower().split())
    if _section_id in _seen_ids or _section_title in _seen_titles:
        continue
    _seen_ids.add(_section_id)
    _seen_titles.add(_section_title)
    CONTENT.append(_section)
