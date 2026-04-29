import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"
import {
  MARKET_INTEL_EXPLORER_KEEP_ENTRIES,
  MARKET_INTEL_EXPLORER_LABELS,
} from "./market-intel-current"

const marketIntelExplorerFilterFn = new Function(
  "node",
  `const keep = new Set(${JSON.stringify(MARKET_INTEL_EXPLORER_KEEP_ENTRIES)});
   const slug = node.slug ?? "";
   if (node.isFolder) {
     return slug === "" || slug === "market-intel" || slug.startsWith("market-intel/");
   }
   if (slug === "index") return true;
   if (keep.has(slug)) return true;
   if (!slug.startsWith("market-intel/")) return false;
   const parts = slug.split("/");
   if (parts.length <= 2) return true;
   if (parts.length === 3 && parts[2] === "index") return true;
   return false;`,
) as (node: { isFolder: boolean; slug?: string }) => boolean

const marketIntelExplorerMapFn = new Function(
  "node",
  `const labels = ${JSON.stringify(MARKET_INTEL_EXPLORER_LABELS)}; const label = labels[node.slugSegment]; if (label) node.displayName = label;`,
) as (node: { slugSegment: string; displayName: string }) => void

// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({
    links: {
      GitHub: "https://github.com/jackyzha0/quartz",
      "Discord Community": "https://discord.gg/cRFFHYye7t",
    },
  }),
}

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.ConditionalRender({
      component: Component.HermesTrigger(),
      condition: (page) => {
        const entityType = page.fileData.frontmatter?.entity_type
        const slug = page.fileData.slug ?? ""
        return Boolean(entityType && slug.startsWith("market-intel/entities/"))
      },
    }),
    Component.TagList(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
        { Component: Component.ReaderMode() },
      ],
    }),
    Component.Explorer({
      title: "workspace",
      folderDefaultState: "collapsed",
      folderClickBehavior: "link",
      useSavedState: true,
      filterFn: marketIntelExplorerFilterFn,
      mapFn: marketIntelExplorerMapFn,
    }),
  ],
  right: [
    Component.ConditionalRender({
      component: Component.Graph(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ConditionalRender({
      component: Component.DesktopOnly(Component.TableOfContents()),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ConditionalRender({
      component: Component.Backlinks(),
      condition: (page) => page.fileData.slug !== "index",
    }),
  ],
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
      ],
    }),
    Component.Explorer({
      title: "workspace",
      folderDefaultState: "collapsed",
      folderClickBehavior: "link",
      useSavedState: true,
      filterFn: marketIntelExplorerFilterFn,
      mapFn: marketIntelExplorerMapFn,
    }),
  ],
  right: [],
}
