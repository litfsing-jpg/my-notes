import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { FullSlug, SimpleSlug, resolveRelative } from "../util/path"
import { QuartzPluginData } from "../plugins/vfile"
import { byDateAndAlphabetical } from "./PageList"
import style from "./styles/recentNotes.scss"
import { Date, getDate } from "./Date"
import { GlobalConfiguration } from "../cfg"
import { i18n } from "../i18n"
import { classNames } from "../util/lang"

interface Options {
  title?: string
  limit: number
  linkToMore: SimpleSlug | false
  showTags: boolean
  filter: (f: QuartzPluginData) => boolean
  sort: (f1: QuartzPluginData, f2: QuartzPluginData) => number
}

const defaultOptions = (cfg: GlobalConfiguration): Options => ({
  limit: 3,
  linkToMore: false,
  showTags: true,
  filter: () => true,
  sort: byDateAndAlphabetical(cfg),
})

export default ((userOpts?: Partial<Options>) => {
  const RecentNotes: QuartzComponent = ({
    allFiles,
    fileData,
    displayClass,
    cfg,
  }: QuartzComponentProps) => {
    const opts = { ...defaultOptions(cfg), ...userOpts }
    const pages = allFiles.filter(opts.filter).sort(opts.sort)
    const remaining = Math.max(0, pages.length - opts.limit)
    return (
      <div class={classNames(displayClass, "recent-notes")}>
        <h2 class="section-title">{opts.title ?? i18n(cfg.locale).components.recentNotes.title}</h2>
        <div class="blog-cards-grid">
          {pages.slice(0, opts.limit).map((page) => {
            const title = page.frontmatter?.title ?? i18n(cfg.locale).propertyDefaults.title
            const tags = page.frontmatter?.tags ?? []
            const description = page.description
            const image = page.frontmatter?.image || page.frontmatter?.cover

            return (
              <a href={resolveRelative(fileData.slug!, page.slug!)} class="blog-card">
                {image && (
                  <div class="blog-card-image">
                    <img src={image} alt={title} loading="lazy" />
                  </div>
                )}
                <div class="blog-card-content">
                  <h3 class="blog-card-title">{title}</h3>
                  {description && (
                    <p class="blog-card-description">{description}</p>
                  )}
                  {opts.showTags && tags.length > 0 && (
                    <div class="blog-card-tags">
                      {tags.map((tag) => (
                        <span class="blog-card-tag">{tag}</span>
                      ))}
                    </div>
                  )}
                </div>
              </a>
            )
          })}
        </div>
        {opts.linkToMore && remaining > 0 && (
          <p>
            <a href={resolveRelative(fileData.slug!, opts.linkToMore)}>
              {i18n(cfg.locale).components.recentNotes.seeRemainingMore({ remaining })}
            </a>
          </p>
        )}
      </div>
    )
  }

  RecentNotes.css = style
  return RecentNotes
}) satisfies QuartzComponentConstructor
