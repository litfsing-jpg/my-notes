import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 *
 * See https://quartz.jzhao.xyz/configuration for more information.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "Здоровье и Нутрициология",
    pageTitleSuffix: " - Научный подход к питанию",
    enableSPA: true,
    enablePopovers: true,
    analytics: {
      provider: "plausible",
    },
    locale: "ru-RU",
    baseUrl: "quartz.jzhao.xyz",
    ignorePatterns: ["private", "templates", ".obsidian", "SEO для инфобизнеса актуальность, возможности, инструменты/разговор с нейронкой", "SEO для инфобизнеса актуальность, возможности, инструменты/РОЛИ_ЭКСПЕРТОВ", "SEO для инфобизнеса актуальность, возможности, инструменты/SEO_РАБОТА"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Inter",
        body: "Georgia",
        code: "JetBrains Mono",
      },
      colors: {
        lightMode: {
          light: "#ffffff",
          lightgray: "#f5f5f5",
          gray: "#9ca3af",
          darkgray: "#374151",
          dark: "#141414",
          secondary: "#53c257",
          tertiary: "#2f9e35",
          highlight: "rgba(83, 194, 87, 0.1)",
          textHighlight: "#fbbf2488",
        },
        darkMode: {
          light: "#0f172a",
          lightgray: "#1e293b",
          gray: "#64748b",
          darkgray: "#cbd5e1",
          dark: "#f1f5f9",
          secondary: "#53c257",
          tertiary: "#2f9e35",
          highlight: "rgba(83, 194, 87, 0.15)",
          textHighlight: "#fbbf2488",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      // Comment out CustomOgImages to speed up build time
      Plugin.CustomOgImages(),
    ],
  },
}

export default config
