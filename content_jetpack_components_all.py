[
    {'id': 'android-fundamentals-platform-architecture',
  'title': 'Android Fundamentals & Jetpack Components',
  'topics': [{'title': 'Android Application Components',
              'icon': '',
              'description': 'Introduces the primary Android building blocks and the '
                             'responsibilities, lifecycle behavior, and platform constraints '
                             'associated with each one.',
              'content_sections': [{'heading': 'Activities',
                                    'points': ['Single screen with user interface',
                                               'Lifecycle: onCreate() → onStart() → onResume() → '
                                               'onPause() → onStop() → onDestroy()',
                                               'Configuration changes (rotation) destroy and '
                                               'recreate activity',
                                               'Use ViewModel to survive configuration changes']},
                                   {'heading': 'Fragments',
                                    'points': ['Reusable UI components within Activities',
                                               'Lifecycle tied to hosting Activity but with '
                                               'additional callbacks',
                                               'FragmentManager handles fragment transactions',
                                               'Navigation Component for modern fragment '
                                               'navigation']},
                                   {'heading': 'Services',
                                    'points': ['Background operations without UI',
                                               'Started Service: runs until stopped',
                                               'Bound Service: client-server interface',
                                               'Foreground Service: visible to user '
                                               '(notification required)',
                                               'WorkManager preferred for deferrable background '
                                               'work']},
                                   {'heading': 'Broadcast Receivers',
                                    'points': ['Listen for system-wide broadcast announcements',
                                               'Can be registered in manifest or dynamically',
                                               'Android 8.0+ restricts implicit broadcasts']},
                                   {'heading': 'Content Providers',
                                    'points': ['Manage shared app data',
                                               'Standard interface for data access across '
                                               'processes',
                                               'Uses URI scheme for data access']}],
              'code_blocks': []},
             {'title': 'Android Architecture Patterns',
              'icon': '',
              'description': 'Compares the most common Android architecture styles and explains '
                             'how they affect separation of concerns, scalability, and testing.',
              'content_sections': [{'heading': 'MVC (Model-View-Controller)',
                                    'points': ['Model: Data layer',
                                               'View: UI (Activity/Fragment)',
                                               'Controller: Logic (Activity handles both View '
                                               'and Controller - tight coupling)']},
                                   {'heading': 'MVP (Model-View-Presenter)',
                                    'points': ['Presenter separates business logic from View',
                                               "View is passive - doesn't directly interact with "
                                               'Model',
                                               'Better testability than MVC',
                                               'Challenge: Presenter can grow large']},
                                   {'heading': 'MVVM (Model-View-ViewModel) - RECOMMENDED',
                                    'points': ['ViewModel holds UI state and business logic',
                                               'View observes ViewModel (LiveData/StateFlow)',
                                               'ViewModel survives configuration changes',
                                               'Clean separation of concerns',
                                               'Google recommended architecture']},
                                   {'heading': 'MVI (Model-View-Intent)',
                                    'points': ['Unidirectional data flow',
                                               'Intent: User actions',
                                               'Model: Immutable state',
                                               'View: Renders state',
                                               'Excellent for complex UI state management']}],
              'code_blocks': []},
             {'title': 'Android Jetpack Architecture Components',
              'icon': '',
              'description': 'Summarizes the Jetpack components most frequently used to structure '
                             'modern Android apps around lifecycle awareness and predictable state '
                             'handling.Architecture focuses on robust, testable logic and state-driven UI flow. In 2026, the shift is toward high-consistency UDF (Unidirectional Data Flow) and KMP-ready logic.',
              'content_sections': [{'heading': 'ViewModel',
                                    'points': ['Stores and manages UI-related data',
                                               'Lifecycle-aware: survives configuration changes',
                                               'Should not hold references to '
                                               'Activities/Fragments/Views',
                                               'Use ViewModelFactory for dependency injection']},
                                   {'heading': 'LiveData',
                                    'points': ['Observable data holder',
                                               'Lifecycle-aware: only updates active observers',
                                               'No memory leaks - automatically cleans up',
                                               'Alternative: Kotlin Flow (more powerful)']},
                                   {'heading': 'Room Database',
                                    'points': ['SQLite abstraction layer',
                                               'Compile-time SQL query verification',
                                               '@Entity, @Dao, @Database annotations',
                                               'Supports Flow, LiveData, RxJava']},
                                   {'heading': 'Navigation Component',
                                    'points': ['Handles fragment transactions and back stack',
                                               'Type-safe argument passing with Safe Args',
                                               'Deep linking support',
                                               'Navigation graph visualization']},
                                               {
                        'heading': 'ViewModel & StateFlow Strategies',
                        'points': [
                            'Utilizing StateFlow for UI state to ensure "at-least-once" delivery and persistence during configuration changes.',
                            'Handling "Single-Live Events" via SharedFlow to prevent event re-triggering (e.g., Snackbars, Nav events).',
                            'SavedStateHandle integration for 2026 process-death resilience in a modularized environment.'
                        ]
                    },
                    {
                        'heading': 'Navigation 3 Paradigm',
                        'subtopics': [
                            {
                                'title': 'Type-Safe Navigation',
                                'description': 'Moving away from String routes to Kotlin DSL and Serializable objects for compile-time safety.'
                            },
                            {
                                'title': 'Navigation as State',
                                'description': 'The backstack is treated as a state object (SceneState), making navigation 100% unit-testable without UI.'
                            }
                        ]
                    },
                                   {'heading': 'WorkManager',
                                    'points': ['Deferrable, guaranteed background work',
                                               'Respects battery optimization',
                                               'Constraints: network, charging, idle',
                                               'Chaining and parallel work support']},
                                               {
                        'heading': 'Core Data & Logic',
                        'points': [
                            'Paging 3.4: Handles massive datasets with built-in support for separators, headers, and state headers. Works seamlessly with Room and Retrofit/Ktor.',
                            'Room: The SQLite abstraction layer. In 2026, focus on its Kotlin Multiplatform (KMP) capabilities for sharing DAOs across platforms.',
                            'ViewModel & LiveData/StateFlow: Managing UI-related data in a lifecycle-conscious way. (Note: LiveData is largely replaced by StateFlow in 2026).',
                            'Navigation 3: The newest type-safe, state-driven navigation framework for Compose.'
                        ]
                    }
                    ],
              'code_blocks': [
                  {
                        'language': 'kotlin',
                        'title': 'MVI State Update Pattern',
                        'code': 'private val _uiState = MutableStateFlow(UiState())\nval uiState = _uiState.asStateFlow()\n\nfun onIntent(intent: UserIntent) {\n    when(intent) {\n        is UserIntent.Refresh -> _uiState.update { it.copy(isLoading = true) }\n    }\n}'
                    }
              ]},
              {
                'title': 'Foundation Components & Security',
                'description': 'Foundation components provide the underlying cross-platform support and modern security protocols like Passkeys.undation components provide low-level capabilities, backward compatibility, and the testing infrastructure',
                'content_sections': [
                    {
                        'heading': 'Security & Identity',
                        'points': [
                            'Credentials Manager: The unified API for Passkeys, Biometrics, and Google Identity.',
                            'DataStore-Tink: Using hardware-backed encryption for all local preferences and small data blocks.',
                            'Android KTX: Leveraging Kotlin-first extensions for cleaner, idiomatic system interaction.'
                        ]
                    },
                    {
                        'heading': 'The Basics',
                        'points': [
                            'AppCompat: Providing backward compatibility for UI and system features.',
                            'Android KTX: Kotlin extensions that turn complex Java-style APIs into concise Kotlin code.',
                            'Multidex: Support for apps with over 64k methods (standardized but still a foundation component).',
                            'Test: Comprehensive libraries for JUnit 5 and Espresso/Compose UI testing.'
                        ]
                    }
                ],
                'code_blocks': [
                    {
                        'language': 'kotlin',
                        'title': 'Credential Manager Implementation',
                        'code': 'val request = GetCredentialRequest.Builder()\n    .addCredentialOption(GetPasswordOption())\n    .addCredentialOption(GetPublicKeyCredentialOption(requestJson))\n    .build()\n\ncredentialManager.getCredential(context, request)'
                    }
                ]
            },
            
            {
                'title': 'Behavior Components & Agentic AI',
                'description': 'These manage how the app behaves within the Android ecosystem, including permissions, notifications, and background work. Behavioral components manage how your app interacts with the OS, including background execution and the new AppFunctions AI protocol.',
                'content_sections': [
                    {
                        'heading': 'Efficiency',
                        'points': [
                            'AppFunctions: Defining @AppFunction endpoints for Gemini and system AI agents to trigger app logic.',
                            'Baseline Profiles: Crucial for optimizing JIT/AOT compilation paths to ensure 60/120 FPS UI performance.'
                        ]
                    },
                    {
                        'heading': 'User & System Interaction',
                        'points': [
                            'Permissions: Modern handling via Activity Result APIs. In 2026, focus on "Approximate Location" and "Photo Picker" integrations.',
                            'WorkManager: The standard for deferrable, guaranteed background execution.',
                            'Notifications: Handling channels, bubbles, and high-priority messaging.',
                            'Sharing: The ShareTarget and Sharing shortcuts for deep system integration.',
                            'AppFunctions: The 2026 way to let AI agents trigger your app actions.'
                        ]
                    }
                ],
                'code_blocks': [
                    {
                        'language': 'kotlin',
                        'title': 'AI-Ready AppFunction',
                        'code': '@AppFunction\nsuspend fun executeInternalTask(input: String): TaskResult {\n    // This function is now discoverable by On-Device AI agents\n    return repository.process(input)\n}'
                    },
                    {
                        'language': 'kotlin',
                        'title': 'Modern Permission Request',
                        'code': 'val requestPermissionLauncher = registerForActivityResult(\n    ActivityResultContracts.RequestPermission()\n) { isGranted ->\n    if (isGranted) { /* Access granted */ }\n}'
                    }
                ]
            },
            {
                'title': 'UI components, Visuals & Theming',
                'description': 'These components focus on the user-facing layer, from the modern Compose framework to utility libraries like Palette.',
                'content_sections': [
                    {
                        'heading': 'Graphics & Color',
                        'points': [
                            'Palette: Extracts prominent colors from images to dynamically theme UI elements. Critical for "Music Player" style UIs.',
                            'Compose Material 3: The standard for Material You and Dynamic Color.',
                            'Emoji2: Ensures your app can render modern emojis even on older Android versions.',
                            'Animations: Shared element transitions and the Motion subsystem for fluid UX.'
                        ]
                    },
                    {
                        'heading': 'Legacy & Integration',
                        'points': [
                            'Fragments & Views: Still important for maintaining older codebases or using specific View-based libraries.',
                            'Slices: (Legacy Alert) While still in the docs, Slices are largely deprecated in favor of AppFunctions and Widgets in 2026.'
                        ]
                    }
                ],
                'code_blocks': [
                    {
                        'language': 'kotlin',
                        'title': 'Extracting Palette Colors',
                        'code': 'Palette.from(bitmap).generate { palette ->\n    val dominantColor = palette?.getDominantColor(defaultColor)\n    // Update UI background to match image\n}'
                    }
                ]
            }
            ],
  'description': 'Covers the platform building blocks, lifecycle model, and core Jetpack '
                 'architecture pieces that senior Android engineers are expected to understand '
                 'deeply before discussing higher-level design tradeoffs.'},
    
    
   
    
   
    
]