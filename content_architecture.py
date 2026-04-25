[
    {
        'id': 'modern-architecture-patterns',
        'title': 'Modern Patterns and Modular Architectures',
        'topics': [
            {
                'title': 'The Unidirectional Data Flow (UDF) Standard',
                'description': 'By 2026, UDF is the mandatory standard for Compose apps. Both MVVM+ and MVI rely on a single source of truth for UI state.',
                'content_sections': [
                    {
                        'heading': 'MVVM+ (The Pragmatic Choice)',
                        'points': [
                            'ViewModel exposes multiple StateFlows or a single UiState object.',
                            'Business logic resides in UseCases to keep ViewModels lean.',
                            'Best for standard CRUD apps where state transitions are straightforward.'
                        ]
                    },
                    {
                        'heading': 'MVI (The State Machine)',
                        'description': 'MVI (Model-View-Intent) provides unidirectional data flow: Intent → '
                             'Model → View. This pattern ensures predictable state management and '
                             'makes debugging easier through explicit state transitions.',
                        'points': [
                            'Model: A single, immutable State object representing the entire screen.',
                            'Intent: A sealed class of user actions (e.g., ClickLogin, ChangeUsername).',
                            'Reducer: A pure function that takes the current State + Intent and returns a New State.',
                            'Best for complex UIs (Chat, Payments, Media Players) where state consistency is critical.'
                        ],
                        'subtopics': [{'title': 'State',
                                                   'description': 'Single immutable data class '
                                                                  'representing entire UI state'},
                                                  {'title': 'Intent',
                                                   'description': 'User actions or events that '
                                                                  'trigger state changes'},
                                                  {'title': 'Effect',
                                                   'description': 'One-time events like '
                                                                  'navigation, snackbars, dialogs'},
                                                  {'title': 'Reducer',
                                                   'description': 'Pure function that transforms '
                                                                  'state based on intents'}]
                    }
                ],
                'code_blocks': [
                    {
                        'language': 'kotlin',
                        'title': 'MVI Reducer Example (2026)',
                        'code': 'data class ScreenState(val items: List<String> = emptyList(), val isLoading: Boolean = false)\n\nsealed class UiIntent { object LoadData : UiIntent() }\n\n// The Reducer ensures state transitions are predictable\nfun reduce(oldState: ScreenState, intent: UiIntent): ScreenState = when(intent) {\n    is UiIntent.LoadData -> oldState.copy(isLoading = true)\n}'
                    },
                    {'language': 'kotlin',
                               'title': 'Example: Complete MVI Implementation',
                               'code': '// 1. UI STATE - single source of truth\n'
                                       'data class UserListState(\n'
                                       '    val isLoading: Boolean = false,\n'
                                       '    val users: List<User> = emptyList(),\n'
                                       '    val error: String? = null,\n'
                                       '    val searchQuery: String = ""\n'
                                       ')\n'
                                       '\n'
                                       '// 2. INTENT - user actions\n'
                                       'sealed class UserListIntent {\n'
                                       '    data class Search(val query: String) : '
                                       'UserListIntent()\n'
                                       '    data class LoadMore() : UserListIntent()\n'
                                       '    data class DeleteUser(val userId: String) : '
                                       'UserListIntent()\n'
                                       '    object Refresh : UserListIntent()\n'
                                       '}\n'
                                       '\n'
                                       '// 3. EFFECT - one-time events (navigation, snackbars)\n'
                                       'sealed class UserListEffect {\n'
                                       '    data class ShowError(val message: String) : '
                                       'UserListEffect()\n'
                                       '    data class NavigateToDetail(val userId: String) : '
                                       'UserListEffect()\n'
                                       '    data class ShowSnackbar(val message: String) : '
                                       'UserListEffect()\n'
                                       '}\n'
                                       '\n'
                                       '// 4. VIEWMODEL - processes intents, emits state\n'
                                       'class UserListViewModel(\n'
                                       '    private val getUsersUseCase: GetUsersUseCase\n'
                                       ') : ViewModel() {\n'
                                       '\n'
                                       '    private val _state = '
                                       'MutableStateFlow(UserListState())\n'
                                       '    val state: StateFlow<UserListState> = '
                                       '_state.asStateFlow()\n'
                                       '\n'
                                       '    private val _effect = '
                                       'MutableSharedFlow<UserListEffect>()\n'
                                       '    val effect: SharedFlow<UserListEffect> = '
                                       '_effect.asSharedFlow()\n'
                                       '\n'
                                       '    fun processIntent(intent: UserListIntent) {\n'
                                       '        when (intent) {\n'
                                       '            is UserListIntent.Search -> '
                                       'handleSearch(intent.query)\n'
                                       '            is UserListIntent.LoadMore -> '
                                       'handleLoadMore()\n'
                                       '            is UserListIntent.DeleteUser -> '
                                       'handleDelete(intent.userId)\n'
                                       '            UserListIntent.Refresh -> handleRefresh()\n'
                                       '        }\n'
                                       '    }\n'
                                       '\n'
                                       '    private fun handleSearch(query: String) {\n'
                                       '        _state.update { it.copy(searchQuery = query, '
                                       'isLoading = true) }\n'
                                       '        viewModelScope.launch {\n'
                                       '            getUsersUseCase(query).onSuccess { users ->\n'
                                       '                _state.update { it.copy(users = users, '
                                       'isLoading = false) }\n'
                                       '            }.onFailure { e ->\n'
                                       '                _state.update { it.copy(error = e.message, '
                                       'isLoading = false) }\n'
                                       '                '
                                       '_effect.emit(UserListEffect.ShowError(e.message ?: '
                                       '"Error"))\n'
                                       '            }\n'
                                       '        }\n'
                                       '    }\n'
                                       '}'}
                ]
            },
        
            
            {
                'title': 'The 3-Layer Clean Architecture',
              'icon': '',
              'description': 'Clean Architecture separates the code into three distinct layers to ensure that business logic is independent of the UI and database. Clean Architecture separates code into layers with strict dependency '
                             'rules - inner layers know nothing about outer layers. This creates '
                             'testable, maintainable, and scalable codebases.',
              'content_sections': [
                                               {
                        'heading': '1. Presentation Layer (UI/ViewModel)',
                        'points': [
                            'Purely handles how data is displayed and user interaction.',
                            'Contains Composables and ViewModels.',
                            'Depends only on the Domain Layer.'
                        ]
                    },
                    {
                        'heading': '2. Domain Layer (The Brain)',
                        'points': [
                            'The most stable layer. Contains Entities and UseCases.',
                            'In 2026, this layer is usually written in pure Kotlin (no Android dependencies) to be used in KMP.',
                            'Defines Repository Interfaces that the Data layer must implement.'
                        ]
                    },
                    {
                        'heading': '3. Data Layer (The Source)',
                        'points': [
                            'Implements Repository Interfaces.',
                            'Coordinates between Network (Ktor/Retrofit) and Local Database (Room).',
                            'Handles Data Mapping (converting API models to Domain entities).'
                        ]
                    },
                    {'heading': 'Layer Responsibilities',
                                    'points': ['Domain layer has NO Android dependencies - '
                                               'testable without Robolectric',
                                               'Use cases encapsulate single business logic - '
                                               'easier to test and maintain',
                                               'Repository defines contract, implementation is in '
                                               'data layer',
                                               'Dependency direction always points inward - domain '
                                               "doesn't know data sources"]},
                                   {'heading': 'Architecture Layers',
                                    'points': [],
                                    'subtopics': [{'title': 'Domain Layer',
                                                   'description': 'Use cases, entities, repository '
                                                                  'interfaces - pure Kotlin, no '
                                                                  'Android deps'},
                                                  {'title': 'Data Layer',
                                                   'description': 'Repository implementations, '
                                                                  'data sources (local/remote), '
                                                                  'mappers'},
                                                  {'title': 'Presentation Layer',
                                                   'description': 'ViewModels, Composables, UI '
                                                                  'state - Android-specific UI '
                                                                  'code'},
                                                  {'title': 'DI Layer',
                                                   'description': 'Hilt modules, dependency '
                                                                  'provision - connects all '
                                                                  'layers'}]}],
              'code_blocks': [{'language': 'kotlin',
                               'title': 'Example: Clean Architecture Layers',
                               'code': '// DOMAIN LAYER - Business logic, pure Kotlin\n'
                                       'class GetUserUseCase(\n'
                                       '    private val repository: UserRepository\n'
                                       ') {\n'
                                       '    suspend operator fun invoke(userId: String): '
                                       'Result<User> {\n'
                                       '        return runCatching {\n'
                                       '            // Business rules here\n'
                                       '            val user = repository.getUser(userId)\n'
                                       '            if (user.isActive) user\n'
                                       '            else throw UserInactiveException()\n'
                                       '        }\n'
                                       '    }\n'
                                       '}\n'
                                       '\n'
                                       '// DATA LAYER - Repository implementations, data sources\n'
                                       'class UserRepositoryImpl(\n'
                                       '    private val localDataSource: UserLocalDataSource,\n'
                                       '    private val remoteDataSource: UserRemoteDataSource\n'
                                       ') : UserRepository {\n'
                                       '\n'
                                       '    override suspend fun getUser(id: String): User {\n'
                                       '        // Single source of truth logic\n'
                                       '        return localDataSource.getUser(id)\n'
                                       '            ?: remoteDataSource.fetchUser(id).also {\n'
                                       '                localDataSource.saveUser(it)\n'
                                       '            }\n'
                                       '    }\n'
                                       '}\n'
                                       '\n'
                                       '// PRESENTATION LAYER - UI, ViewModels\n'
                                       'class UserViewModel(\n'
                                       '    private val getUserUseCase: GetUserUseCase\n'
                                       ') : ViewModel() { ... }'
                                       }]
         },
            {
                'title': 'Modularization: Feature-Based - Scalability & Build Speed',
                'description': 'Modularization improves build times, enables parallel development, '
                             'and provides better code organization. Strategic module boundaries '
                             'are crucial for maintainability. Modern apps are no longer monolithic. They are broken into independent Gradle modules.',
                'content_sections': [
                    {
                        'heading': 'Module Types',
                        'points': [
                            'Feature Modules: (e.g., :feature:login, :feature:dashboard) Contains UI and ViewModels for a specific flow.',
                            'Core Modules: (e.g., :core:network, :core:database, :core:ui-kit) Reusable utilities used across features.',
                            'Domain Modules: Often a single :domain module or split per feature to allow sharing logic via KMP.'
                        ]
                    },
                    {
                        'heading': 'Benefits',
                        'points': [
                            'Faster Build Times: Gradle only recompiles the changed module.',
                            'Code Ownership: Different teams can own different modules without merge conflicts.',
                            'Dynamic Delivery: Allows downloading features on-demand to keep the initial APK size small.'
                        ]
                    },
                    {'heading': 'Module Types',
                                    'points': [],
                                    'subtopics': [{'title': 'Feature Modules',
                                                   'description': 'Each feature = separate module '
                                                                  '- auth, profile, settings. '
                                                                  'Independent builds'},
                                                  {'title': 'Library Modules',
                                                   'description': 'Common code: ui-components, '
                                                                  'utils, network, database. '
                                                                  'Shared across features'},
                                                  {'title': 'App Module',
                                                   'description': 'Entry point, wires '
                                                                  'dependencies, applies '
                                                                  'configurations'},
                                                  {'title': 'Dynamic Delivery',
                                                   'description': 'Play Feature Delivery - '
                                                                  'on-demand module loading for '
                                                                  'large apps'}]}
                ],
                'code_blocks': [{'language': 'kotlin',
                               'title': 'Example: Module Dependencies',
                               'code': '// settings/build.gradle.kts\n'
                                       'plugins {\n'
                                       '    id("com.android.library")\n'
                                       '    id("org.jetbrains.kotlin.android")\n'
                                       '    id("com.google.dagger.hilt.android")\n'
                                       '}\n'
                                       '\n'
                                       'dependencies {\n'
                                       '    implementation(project(":core:ui"))\n'
                                       '    implementation(project(":core:domain"))\n'
                                       '    implementation(project(":core:network"))\n'
                                       '\n'
                                       '    // Feature module only depends on core modules\n'
                                       '    // No direct dependency on other feature modules!\n'
                                       '}'}]
            }
        ]
    }
]