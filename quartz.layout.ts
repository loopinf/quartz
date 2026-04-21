import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

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
      useSavedState: true,
      filterFn: (node) => {
        if (node.isFolder) return true
        const keep = new Set([
          "market-intel/MARKET_INTEL_RECENT_CHANGES",
          "market-intel/market-intel-progress-big-picture",
          "market-intel/daily/2026-04-21_evening-briefing-input",
          "market-intel/daily/2026-04-20_top30_recap",
          "market-intel/daily/2026-04-20_next-session-prep",
          "market-intel/research/prediction-workspace",
          "market-intel/research/portfolio-pilot-review-dashboard",
          "market-intel/workflows/predictive-replay-and-review-system",
        ])
        return keep.has(node.slug)
      },
      mapFn: (node) => {
        const labels = {
          "market-intel": "Market Intel Home",
          "daily": "Daily",
          "research": "Prediction / Research",
          "workflows": "Workflows",
          "events": "Events",
          "entities": "Stocks",
          "MARKET_INTEL_RECENT_CHANGES": "최근 변경 로그",
          "market-intel-progress-big-picture": "큰그림",
          "2026-04-21_evening-briefing-input": "오늘 input",
          "2026-04-20_top30_recap": "최신 validated recap",
          "2026-04-20_next-session-prep": "내일 대응 준비",
          "prediction-workspace": "Prediction Workspace",
          "portfolio-pilot-review-dashboard": "예측 후보 대시보드",
          "predictive-replay-and-review-system": "Predictive Replay",
        }
        if (labels[node.slugSegment]) node.displayName = labels[node.slugSegment]
      },
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
      title: "섹션",
      folderDefaultState: "collapsed",
      useSavedState: false,
      filterFn: (node) => {
        if (node.isFolder) return true
        const keep = new Set([
          "market-intel/MARKET_INTEL_RECENT_CHANGES",
          "market-intel/market-intel-progress-big-picture",
          "market-intel/daily/2026-04-21_evening-briefing-input",
          "market-intel/daily/2026-04-20_top30_recap",
          "market-intel/daily/2026-04-20_next-session-prep",
          "market-intel/research/prediction-workspace",
          "market-intel/research/portfolio-pilot-review-dashboard",
          "market-intel/workflows/predictive-replay-and-review-system",
        ])
        return keep.has(node.slug)
      },
      mapFn: (node) => {
        const labels = {
          "market-intel": "Market Intel Home",
          "daily": "Daily",
          "research": "Prediction / Research",
          "workflows": "Workflows",
          "events": "Events",
          "entities": "Stocks",
          "MARKET_INTEL_RECENT_CHANGES": "최근 변경 로그",
          "market-intel-progress-big-picture": "큰그림",
          "2026-04-21_evening-briefing-input": "오늘 input",
          "2026-04-20_top30_recap": "최신 validated recap",
          "2026-04-20_next-session-prep": "내일 대응 준비",
          "prediction-workspace": "Prediction Workspace",
          "portfolio-pilot-review-dashboard": "예측 후보 대시보드",
          "predictive-replay-and-review-system": "Predictive Replay",
        }
        if (labels[node.slugSegment]) node.displayName = labels[node.slugSegment]
      },
    }),
  ],
  right: [],
}
