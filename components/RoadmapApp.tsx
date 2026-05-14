"use client";

import { useEffect, useMemo, useState } from "react";
import type { Dispatch, SetStateAction } from "react";
import {
  estimateSectionDuration,
  getPriorityLabel,
  getSectionPriority,
  getTopicKey,
  normalizeSearchText,
  topicMatchesSearch,
  type Priority,
  type RoadmapSection,
  type RoadmapTopic,
} from "@/lib/content";

type Filter = Priority | "all";

type RoadmapAppProps = {
  initialContent: RoadmapSection[];
};

const progressStorageKey = "modern-android-roadmap-progress";
const themeStorageKey = "modern-android-roadmap-theme";

const themes = {
  light: "theme-light bg-white text-zinc-950",
  dark: "theme-dark bg-[#10211f] text-zinc-950",
};

type Theme = keyof typeof themes;

const filters: { id: Filter; label: string }[] = [
  { id: "all", label: "All Sections" },
  { id: "must-know", label: "Must Know" },
  { id: "important", label: "Important" },
  { id: "advanced", label: "Advanced" },
];

function cx(...classes: Array<string | false | null | undefined>) {
  return classes.filter(Boolean).join(" ");
}

function getCodeLanguage(language?: string) {
  return language || "text";
}

export default function RoadmapApp({ initialContent }: RoadmapAppProps) {
  const [isHydrated, setIsHydrated] = useState(false);
  const [searchInput, setSearchInput] = useState("");
  const searchTerm = normalizeSearchText(searchInput);
  const [activeFilter, setActiveFilter] = useState<Filter>("all");
  const [completedTopics, setCompletedTopics] = useState<Set<string>>(() => new Set());
  const [expandedSections, setExpandedSections] = useState<Set<string>>(
    () => new Set(initialContent.map((_, index) => getSectionId(index))),
  );
  const [expandedTopics, setExpandedTopics] = useState<Set<string>>(() => new Set());
  const [expandedCodeBlocks, setExpandedCodeBlocks] = useState<Set<string>>(() => new Set());
  const [theme, setTheme] = useState<Theme>("light");

  useEffect(() => {
    setIsHydrated(true);

    let storedProgress: string | null = null;
    let storedTheme: string | null = null;

    try {
      storedProgress = window.localStorage.getItem(progressStorageKey);
      storedTheme = window.localStorage.getItem(themeStorageKey);
    } catch {
      storedProgress = null;
      storedTheme = null;
    }

    if (storedProgress) {
      try {
        setCompletedTopics(new Set(JSON.parse(storedProgress) as string[]));
      } catch {
        setCompletedTopics(new Set());
      }
    }

    if (storedTheme) {
      setTheme(normalizeStoredTheme(storedTheme));
    }
  }, []);

  useEffect(() => {
    if (!isHydrated) return;

    try {
      window.localStorage.setItem(progressStorageKey, JSON.stringify([...completedTopics]));
    } catch {
      // Progress still works for the current session if browser storage is blocked.
    }
  }, [completedTopics, isHydrated]);

  useEffect(() => {
    if (!isHydrated) return;

    try {
      window.localStorage.setItem(themeStorageKey, theme);
    } catch {
      // Theme still works for the current session if browser storage is blocked.
    }
  }, [isHydrated, theme]);

  useEffect(() => {
    if (!searchTerm) return;

    const nextSections = new Set<string>();
    const nextTopics = new Set<string>();

    initialContent.forEach((section, sectionIndex) => {
      const sectionId = getSectionId(sectionIndex);
      let sectionHasMatch = false;

      (section.topics || []).forEach((topic, topicIndex) => {
        const topicNumber = `${sectionIndex + 1}.${topicIndex + 1}`;
        if (topicMatchesSearch(section.title || "", topic, topicNumber, searchTerm)) {
          sectionHasMatch = true;
          nextTopics.add(getTopicKey(section, topic, sectionIndex, topicIndex));
        }
      });

      if (sectionHasMatch) {
        nextSections.add(sectionId);
      }
    });

    setExpandedSections(nextSections);
    setExpandedTopics(nextTopics);
  }, [initialContent, searchTerm]);

  const visibleSections = useMemo(() => {
    return initialContent
      .map((section, sectionIndex) => {
        const priority = getSectionPriority(section.title);
        if (activeFilter !== "all" && priority !== activeFilter) return null;

        const visibleTopics = (section.topics || [])
          .map((topic, topicIndex) => ({ topic, topicIndex }))
          .filter(({ topic, topicIndex }) => {
            const topicNumber = `${sectionIndex + 1}.${topicIndex + 1}`;
            return topicMatchesSearch(section.title || "", topic, topicNumber, searchTerm);
          });

        if (visibleTopics.length === 0) return null;
        return { section, sectionIndex, priority, visibleTopics };
      })
      .filter(Boolean);
  }, [activeFilter, initialContent, searchTerm]);

  const totalTopics = initialContent.reduce((sum, section) => sum + (section.topics?.length || 0), 0);
  const totalSections = initialContent.length;
  const progressPercent = totalTopics ? Math.round((completedTopics.size / totalTopics) * 100) : 0;

  function toggleSetValue(setter: Dispatch<SetStateAction<Set<string>>>, value: string) {
    setter((current) => {
      const next = new Set(current);
      if (next.has(value)) {
        next.delete(value);
      } else {
        next.add(value);
      }
      return next;
    });
  }

  function toggleTopicCompletion(topicKey: string) {
    toggleSetValue(setCompletedTopics, topicKey);
  }

  function toggleSection(sectionId: string) {
    toggleSetValue(setExpandedSections, sectionId);
  }

  function expandAllSections() {
    setExpandedSections(new Set(initialContent.map((_, index) => getSectionId(index))));
  }

  function collapseAllTopics() {
    setExpandedTopics(new Set());
  }

  function expandAllTopics() {
    const next = new Set<string>();
    initialContent.forEach((section, sectionIndex) => {
      (section.topics || []).forEach((topic, topicIndex) => {
        next.add(getTopicKey(section, topic, sectionIndex, topicIndex));
      });
    });
    setExpandedTopics(next);
  }

  return (
    <main className={cx("min-h-screen", themes[theme])}>
      <div className="grid w-full gap-6">
        <header className="landing-header flex min-h-screen flex-col overflow-hidden">
          <div className="mx-auto flex w-full max-w-7xl flex-wrap items-center justify-between gap-4 px-4 py-5 sm:px-6 lg:px-8">
            <div className="flex items-center gap-3">
              <div className="landing-mark flex h-11 w-11 items-center justify-center rounded-full bg-teal-300 text-sm font-semibold">
                AS
              </div>
              <div>
                <div className="landing-display landing-brand text-base font-semibold">Android Study Roadmap</div>
                <div className="landing-muted text-xs font-medium uppercase">Senior interview preparation</div>
              </div>
            </div>
            <div className="landing-muted flex flex-wrap justify-end gap-2 text-xs font-medium">
              <span
                className={cx(
                  "rounded-full border px-3 py-2",
                  isHydrated
                    ? "border-emerald-200/30 bg-emerald-200/10 text-emerald-100"
                    : "border-amber-200/30 bg-amber-200/10 text-amber-100",
                )}
              >
                {isHydrated ? "Interactive" : "Loading interactivity"}
              </span>
              <span className="rounded-full border border-white/10 bg-black/20 px-3 py-2">{totalSections} sections</span>
              <span className="rounded-full border border-white/10 bg-black/20 px-3 py-2">{totalTopics} topics</span>
              <span className="rounded-full border border-teal-200/30 bg-teal-200/10 px-3 py-2 text-teal-100">
                {progressPercent}% complete
              </span>
            </div>
          </div>

          <div className="mx-auto grid w-full max-w-7xl flex-1 items-center gap-10 px-4 pb-10 pt-8 sm:px-6 lg:grid-cols-[minmax(0,1fr)_430px] lg:px-8">
            <div className="grid max-w-4xl gap-7">
              <div className="flex flex-wrap items-center gap-3">
                <div className="landing-accent w-fit rounded-full border border-teal-200/20 bg-teal-200/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em]">
                  Senior Android Guide
                </div>
                <span className="landing-muted rounded-full border border-white/10 bg-black/20 px-4 py-2 text-xs font-medium uppercase tracking-[0.12em]">
                  Structured practice plan
                </span>
              </div>
              <div className="grid gap-5">
                <h1 className="landing-display hero-gradient-text max-w-3xl text-3xl font-semibold leading-[1.08] text-white sm:text-5xl lg:text-6xl">
                  Prepare for senior Android interviews with a clear roadmap
                </h1>
                <p className="landing-body max-w-2xl text-base font-light leading-7">
                  Move through the topics that matter most: architecture, Kotlin, Compose, testing, performance, and production readiness.
                </p>
              </div>
              <div className="landing-focus max-w-2xl border-l border-white/20 py-1 pl-5">
                <p className="landing-accent text-[11px] font-semibold uppercase tracking-[0.18em]">How to use it</p>
                <p className="landing-body mt-2 text-sm font-light leading-6">
                  Search for a concept, open the details, study the examples, and mark topics complete as you progress.
                </p>
              </div>
              <div className="flex flex-wrap gap-3">
                <a
                  href="#section-1"
                  className="landing-primary-action rounded-full bg-teal-300 px-6 py-3 text-sm font-semibold shadow-[0_18px_40px_rgba(45,212,191,0.18)] transition hover:-translate-y-0.5 hover:bg-teal-200"
                >
                  Start roadmap
                </a>
                <button
                  type="button"
                  onClick={expandAllTopics}
                  className="landing-secondary-action rounded-full border border-white/10 bg-white/[0.05] px-6 py-3 text-sm font-medium transition hover:-translate-y-0.5 hover:border-teal-200/70"
                >
                  Expand topics
                </button>
              </div>
              <div className="landing-muted grid max-w-3xl gap-3 border-t border-white/10 pt-5 text-xs font-medium uppercase tracking-[0.14em] sm:grid-cols-3">
                <span>Architecture</span>
                <span>Compose</span>
                <span>Production</span>
              </div>
            </div>

            <section className="landing-panel grid gap-5 border-l border-white/20 pl-5 sm:pl-6">
              <div className="flex items-center justify-between gap-3">
                <span className="landing-muted text-sm font-medium uppercase tracking-[0.12em]">Your progress</span>
                <span className="landing-accent landing-display text-lg font-semibold">
                  {completedTopics.size} / {totalTopics}
                </span>
              </div>
              <div className="h-3 overflow-hidden rounded-full bg-slate-900 ring-1 ring-white/10">
                <div className="h-full bg-teal-300 transition-all" style={{ width: `${progressPercent}%` }} />
              </div>
              <div className="landing-brand landing-display text-5xl font-semibold leading-none sm:text-6xl">{progressPercent}%</div>
              <p className="landing-body max-w-sm text-sm font-light leading-6">
                Track what you have completed and keep the next section easy to find.
              </p>
              <div className="grid gap-3 border-y border-white/10 py-4">
                <div className="flex items-center justify-between gap-3 text-sm">
                  <span className="landing-body font-light">Visible now</span>
                  <span className="landing-brand font-semibold">{visibleSections.length}</span>
                </div>
                <div className="flex items-center justify-between gap-3 text-sm">
                  <span className="landing-body font-light">Sections</span>
                  <span className="landing-brand font-semibold">{totalSections}</span>
                </div>
                <div className="flex items-center justify-between gap-3 text-sm">
                  <span className="landing-body font-light">Topics</span>
                  <span className="landing-brand font-semibold">{totalTopics}</span>
                </div>
                <div className="flex items-center justify-between gap-3 text-sm">
                  <span className="landing-body font-light">Mode</span>
                  <span className="landing-brand font-semibold capitalize">{theme}</span>
                </div>
              </div>
              <div className="landing-muted grid gap-2 text-xs font-medium uppercase tracking-[0.14em]">
                <span>Clean architecture</span>
                <span>Jetpack Compose</span>
                <span>Testing and performance</span>
              </div>
            </section>
          </div>
        </header>

        <section className="mx-4 grid max-w-7xl gap-3 rounded-lg border border-white/10 bg-black/20 p-4 sm:mx-6 lg:mx-auto lg:w-full lg:grid-cols-[minmax(240px,1fr)_auto_auto] lg:items-center">
          <input
            value={searchInput}
            onChange={(event) => setSearchInput(event.target.value)}
            placeholder="Search topics, code, concepts..."
            className="h-11 rounded-lg border border-white/10 bg-slate-950/70 px-4 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-teal-300"
          />

          <div className="flex flex-wrap gap-2">
            {filters.map((filter) => (
              <button
                key={filter.id}
                type="button"
                onClick={() => setActiveFilter(filter.id)}
                className={cx(
                  "h-10 rounded-lg border px-3 text-sm font-semibold transition",
                  activeFilter === filter.id
                    ? "border-teal-300 bg-teal-300 text-slate-950"
                    : "border-white/10 bg-white/[0.04] text-slate-200 hover:border-teal-200/70",
                )}
              >
                {filter.label}
              </button>
            ))}
          </div>

          <select
            value={theme}
            onChange={(event) => setTheme(event.target.value as Theme)}
            className="h-10 rounded-lg border border-white/10 bg-slate-950 px-3 text-sm text-white outline-none focus:border-teal-300"
          >
            <option value="light">Light</option>
            <option value="dark">Dark</option>
          </select>
        </section>

        <section className="mx-auto grid w-full max-w-7xl gap-4 px-4 pb-6 sm:px-6 lg:grid-cols-[300px_minmax(0,1fr)] lg:items-start lg:px-8">
          <aside className="grid gap-3 rounded-lg border border-white/10 bg-white/[0.035] p-4 lg:sticky lg:top-4">
            <div className="flex items-center justify-between">
              <h2 className="text-base font-bold text-white">Study Roadmap</h2>
              <span className="text-xs font-semibold text-slate-400">{visibleSections.length} sections</span>
            </div>
            <div className="grid max-h-[70vh] gap-2 overflow-auto pr-1">
              {visibleSections.map((item) => {
                if (!item) return null;
                const { section, sectionIndex, priority } = item;

                return (
                  <a
                    key={getSectionId(sectionIndex)}
                    href={`#section-${sectionIndex + 1}`}
                    className="rounded-lg border border-white/10 bg-slate-950/45 p-3 text-sm transition hover:border-teal-200/70"
                  >
                    <div className="mb-2 flex items-center justify-between gap-2">
                      <span className="font-bold text-teal-200">{sectionIndex + 1}</span>
                      <span className="text-xs text-slate-400">{estimateSectionDuration(section, priority)}</span>
                    </div>
                    <div className="font-semibold text-slate-100">{section.title || "Untitled Section"}</div>
                    <div className="mt-2 text-xs text-slate-500">{getPriorityLabel(priority)}</div>
                  </a>
                );
              })}
            </div>
          </aside>

          <div className="grid gap-4">
            <div className="flex flex-wrap gap-2">
              <button className="rounded-lg border border-white/10 bg-white/[0.05] px-3 py-2 text-sm font-semibold text-slate-200 hover:border-teal-200/70" onClick={expandAllSections} type="button">
                Expand Sections
              </button>
              <button className="rounded-lg border border-white/10 bg-white/[0.05] px-3 py-2 text-sm font-semibold text-slate-200 hover:border-teal-200/70" onClick={expandAllTopics} type="button">
                Expand Topics
              </button>
              <button className="rounded-lg border border-white/10 bg-white/[0.05] px-3 py-2 text-sm font-semibold text-slate-200 hover:border-teal-200/70" onClick={collapseAllTopics} type="button">
                Collapse Topics
              </button>
            </div>

            {visibleSections.length === 0 ? (
              <div className="rounded-lg border border-white/10 bg-white/[0.04] p-8 text-center text-slate-300">
                No topics matched your current search or filter.
              </div>
            ) : (
              visibleSections.map((item) => {
                if (!item) return null;
                const { section, sectionIndex, priority, visibleTopics } = item;
                const sectionId = getSectionId(sectionIndex);
                const sectionExpanded = expandedSections.has(sectionId);

                return (
                  <section
                    key={sectionId}
                    id={`section-${sectionIndex + 1}`}
                    onClick={(event) => {
                      if (event.target !== event.currentTarget) return;
                      toggleSection(sectionId);
                    }}
                    className="cursor-pointer rounded-lg border border-white/10 bg-white/[0.045] shadow-2xl shadow-black/20"
                  >
                    <button
                      type="button"
                      onClick={() => toggleSection(sectionId)}
                      className="grid w-full gap-3 rounded-lg p-4 text-left transition hover:bg-white/[0.04] sm:grid-cols-[auto_minmax(0,1fr)_auto] sm:items-start"
                      aria-expanded={sectionExpanded}
                    >
                      <span className="inline-flex h-9 min-w-9 items-center justify-center rounded-lg bg-teal-300 px-2 text-sm font-black text-slate-950">
                        {sectionIndex + 1}
                      </span>
                      <span className="grid gap-1">
                        <span className="text-xl font-black text-white">{section.title || "Untitled Section"}</span>
                        <span className="text-sm leading-6 text-slate-300">
                          {section.description ? `${section.description} ` : ""}
                          {visibleTopics.length} topic{visibleTopics.length === 1 ? "" : "s"} in this section.
                        </span>
                      </span>
                      <span className="flex items-center gap-2">
                        <span className={cx("rounded-lg border px-2 py-1 text-xs font-bold", priorityClass(priority))}>
                          {getPriorityLabel(priority)}
                        </span>
                        <span className="text-lg text-slate-300">{sectionExpanded ? "v" : ">"}</span>
                      </span>
                    </button>

                    {sectionExpanded ? (
                      <div className="grid gap-0 px-4 pb-4">
                        {visibleTopics.map(({ topic, topicIndex }) => (
                          <TopicCard
                            key={getTopicKey(section, topic, sectionIndex, topicIndex)}
                            topic={topic}
                            topicIndex={topicIndex}
                            section={section}
                            sectionIndex={sectionIndex}
                            completedTopics={completedTopics}
                            expandedTopics={expandedTopics}
                            expandedCodeBlocks={expandedCodeBlocks}
                            toggleSetValue={toggleSetValue}
                            toggleTopicCompletion={toggleTopicCompletion}
                            setExpandedTopics={setExpandedTopics}
                            setExpandedCodeBlocks={setExpandedCodeBlocks}
                          />
                        ))}
                      </div>
                    ) : null}
                  </section>
                );
              })
            )}
          </div>
        </section>
      </div>
    </main>
  );
}

function TopicCard({
  topic,
  topicIndex,
  section,
  sectionIndex,
  completedTopics,
  expandedTopics,
  expandedCodeBlocks,
  toggleSetValue,
  toggleTopicCompletion,
  setExpandedTopics,
  setExpandedCodeBlocks,
}: {
  topic: RoadmapTopic;
  topicIndex: number;
  section: RoadmapSection;
  sectionIndex: number;
  completedTopics: Set<string>;
  expandedTopics: Set<string>;
  expandedCodeBlocks: Set<string>;
  toggleSetValue: (setter: Dispatch<SetStateAction<Set<string>>>, value: string) => void;
  toggleTopicCompletion: (topicKey: string) => void;
  setExpandedTopics: Dispatch<SetStateAction<Set<string>>>;
  setExpandedCodeBlocks: Dispatch<SetStateAction<Set<string>>>;
}) {
  const topicNumber = `${sectionIndex + 1}.${topicIndex + 1}`;
  const topicKey = getTopicKey(section, topic, sectionIndex, topicIndex);
  const topicExpanded = expandedTopics.has(topicKey);
  const isComplete = completedTopics.has(topicKey);

  return (
    <article className={cx("border-t border-white/10 py-4 first:border-t-0", isComplete && "opacity-70")}>
      <div className="grid grid-cols-[minmax(0,1fr)_auto] items-center gap-2">
        <button
          type="button"
          aria-expanded={topicExpanded}
          onClick={() => toggleSetValue(setExpandedTopics, topicKey)}
          className="grid min-h-12 grid-cols-[auto_minmax(0,1fr)_auto] items-center gap-3 rounded-lg p-2 text-left outline-none transition hover:bg-white/[0.04] focus-visible:ring-2 focus-visible:ring-teal-300/70"
        >
          <span className="rounded-lg border border-teal-200/20 bg-teal-200/10 px-2 py-1 text-xs font-black text-teal-200">
            {topicNumber}
          </span>
          <span className="min-w-0 text-base font-bold text-slate-100">{topic.title || "Untitled Topic"}</span>
          <span className="flex h-9 w-9 items-center justify-center rounded-lg border border-white/10 text-lg text-slate-200">
            {topicExpanded ? "v" : ">"}
          </span>
        </button>

        <label className="flex h-10 w-10 items-center justify-center rounded-lg border border-white/10 hover:border-teal-200/70">
          <input
            type="checkbox"
            checked={isComplete}
            onChange={() => toggleTopicCompletion(topicKey)}
            className="h-4 w-4 accent-teal-300"
            aria-label={`Mark ${topic.title || "topic"} complete`}
          />
        </label>
      </div>

      {topicExpanded ? (
        <div className="grid gap-4 px-2 pb-2 pt-3">
          {topic.description ? <p className="m-0 text-sm leading-6 text-slate-300">{topic.description}</p> : null}

          {(topic.content_sections || []).map((contentSection, index) => (
            <section key={`${topicKey}-content-${index}`} className="grid gap-3 rounded-lg border border-white/10 bg-slate-950/35 p-4">
              {contentSection.heading ? <h4 className="text-sm font-black text-white">{contentSection.heading}</h4> : null}
              {contentSection.points?.length ? (
                <div className="grid gap-2">
                  {contentSection.points.map((point, pointIndex) => (
                    <div key={`${topicKey}-point-${pointIndex}`} className="grid grid-cols-[10px_minmax(0,1fr)] gap-3 rounded-lg border border-white/10 bg-white/[0.03] p-3 text-sm leading-6 text-slate-300">
                      <span className="mt-2 h-2 w-2 rounded-full bg-teal-300" />
                      <span>{point}</span>
                    </div>
                  ))}
                </div>
              ) : null}
              {contentSection.subtopics?.length ? (
                <div className="grid gap-2 sm:grid-cols-2">
                  {contentSection.subtopics.map((subtopic, subtopicIndex) => (
                    <div key={`${topicKey}-subtopic-${subtopicIndex}`} className="rounded-lg border border-white/10 bg-black/20 p-3">
                      <div className="text-sm font-bold text-slate-100">{subtopic.title}</div>
                      {subtopic.description ? <div className="mt-1 text-sm leading-6 text-slate-400">{subtopic.description}</div> : null}
                    </div>
                  ))}
                </div>
              ) : null}
            </section>
          ))}

          {(topic.code_blocks || []).map((block, codeIndex) => {
            const codeKey = `${topicKey}:code:${codeIndex}`;
            const expanded = expandedCodeBlocks.has(codeKey);

            return (
              <section key={codeKey} className="overflow-hidden rounded-lg border border-white/10 bg-slate-950">
                <button
                  type="button"
                  onClick={() => toggleSetValue(setExpandedCodeBlocks, codeKey)}
                  className="flex w-full items-center justify-between gap-3 border-b border-white/10 px-4 py-3 text-left hover:bg-white/[0.04]"
                  aria-expanded={expanded}
                >
                  <span className="min-w-0 font-semibold text-slate-100">{block.title || "Code Example"}</span>
                  <span className="shrink-0 rounded-lg bg-teal-200/10 px-2 py-1 text-xs font-bold text-teal-200">
                    {getCodeLanguage(block.language)}
                  </span>
                </button>
                {expanded ? (
                  <pre className="overflow-auto p-4 text-sm leading-6 text-slate-200">
                    <code>{block.code || ""}</code>
                  </pre>
                ) : null}
              </section>
            );
          })}
        </div>
      ) : null}
    </article>
  );
}

function getSectionId(sectionIndex: number) {
  return `section-${sectionIndex + 1}`;
}

function normalizeStoredTheme(value: string): Theme {
  if (value === "light" || value === "dark") return value;
  return "dark";
}

function priorityClass(priority: Priority) {
  if (priority === "must-know") return "border-teal-200/30 bg-teal-200/10 text-teal-100";
  if (priority === "important") return "border-amber-200/30 bg-amber-200/10 text-amber-100";
  return "border-sky-200/30 bg-sky-200/10 text-sky-100";
}
