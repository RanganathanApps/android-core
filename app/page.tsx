import RoadmapApp from "@/components/RoadmapApp";
import content from "@/data/content.json";
import type { RoadmapSection } from "@/lib/content";

export default function Home() {
  return <RoadmapApp initialContent={content as RoadmapSection[]} />;
}
