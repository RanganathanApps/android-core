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


def _key_points_section(section_id, topic_title):
    profile = _profile_for(section_id)
    return {
        "heading": "Key Points",
        "points": [
            f"{topic_title} should be understood through {profile['lens']}, with clear ownership boundaries and lifecycle behavior.",
            f"Know the production tradeoffs around {profile['tradeoffs']} as they apply specifically to {topic_title}.",
            f"Be ready to discuss common mistakes in {topic_title}, especially {profile['failure_modes']}.",
            f"Interview-ready answer: define the concept, explain when to use it, compare alternatives, and connect it to a measurable app-quality outcome.",
        ],
    }


def _deep_dive_section(section_id, topic_title):
    profile = _profile_for(section_id)

    return {
        "heading": "Senior-Level Deep Dive",
        "points": [
            f"Know why {topic_title} matters in real Android apps, not just which API to call.",
            f"Be able to explain the main tradeoffs: {profile['tradeoffs']}.",
            f"Watch for common issues: {profile['failure_modes']}.",
            f"Strong answer: {profile['signals']}.",
        ],
        "subtopics": [
            {
                "title": "Design Review Prompt",
                "description": f"For a feature using {topic_title}, explain the owner, lifecycle, failure path, and how you would measure success.",
            },
            {
                "title": "Debugging Prompt",
                "description": f"If {topic_title} breaks, state a hypothesis, check logs/traces/tests, isolate the boundary, and verify the fix.",
            },
        ],
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

        for topic in section.get("topics", []):
            content_sections = topic.setdefault("content_sections", [])

            has_key_points = any(
                block.get("heading") in {"Key Points", "Core Concepts"}
                for block in content_sections
            )
            if not has_key_points:
                content_sections.insert(
                    0,
                    _key_points_section(section_id, topic.get("title", "This topic")),
                )

            topic["content_sections"] = [
                block
                for block in content_sections
                if block.get("heading") != "Senior-Level Deep Dive"
            ]
            content_sections = topic["content_sections"]

            deep_dive = _deep_dive_section(section_id, topic.get("title", "this topic"))
            if deep_dive:
                content_sections.append(deep_dive)

            _dedupe_topic_content(topic)

    return content
