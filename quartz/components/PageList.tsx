import { FullSlug, isFolderPath, resolveRelative } from "../util/path"
import { QuartzPluginData } from "../plugins/vfile"
import { Date, getDate } from "./Date"
import { QuartzComponent, QuartzComponentProps } from "./types"
import { GlobalConfiguration } from "../cfg"

export type SortFn = (f1: QuartzPluginData, f2: QuartzPluginData) => number

export function byDateAndAlphabetical(cfg: GlobalConfiguration): SortFn {
  return (f1, f2) => {
    // Sort by date/alphabetical
    if (f1.dates && f2.dates) {
      // sort descending
      return getDate(cfg, f2)!.getTime() - getDate(cfg, f1)!.getTime()
    } else if (f1.dates && !f2.dates) {
      // prioritize files with dates
      return -1
    } else if (!f1.dates && f2.dates) {
      return 1
    }

    // otherwise, sort lexographically by title
    const f1Title = f1.frontmatter?.title.toLowerCase() ?? ""
    const f2Title = f2.frontmatter?.title.toLowerCase() ?? ""
    return f1Title.localeCompare(f2Title)
  }
}

export function byDateAndAlphabeticalFolderFirst(cfg: GlobalConfiguration): SortFn {
  return (f1, f2) => {
    // Sort folders first
    const f1IsFolder = isFolderPath(f1.slug ?? "")
    const f2IsFolder = isFolderPath(f2.slug ?? "")
    if (f1IsFolder && !f2IsFolder) return -1
    if (!f1IsFolder && f2IsFolder) return 1

    // If both are folders or both are files, sort by date/alphabetical
    if (f1.dates && f2.dates) {
      // sort descending
      return getDate(cfg, f2)!.getTime() - getDate(cfg, f1)!.getTime()
    } else if (f1.dates && !f2.dates) {
      // prioritize files with dates
      return -1
    } else if (!f1.dates && f2.dates) {
      return 1
    }

    // otherwise, sort lexographically by title
    const f1Title = f1.frontmatter?.title.toLowerCase() ?? ""
    const f2Title = f2.frontmatter?.title.toLowerCase() ?? ""
    return f1Title.localeCompare(f2Title)
  }
}

type Props = {
  limit?: number
  sort?: SortFn
} & QuartzComponentProps

export const PageList: QuartzComponent = ({ cfg, fileData, allFiles, limit, sort }: Props) => {
  const sorter = sort ?? byDateAndAlphabeticalFolderFirst(cfg)
  // Фильтруем только статьи (убираем папки и служебные файлы)
  let list = allFiles
    .filter((file) => {
      const slug = file.slug || ""
      // Показываем только обычные статьи, исключаем папки и служебные файлы
      return !slug.includes("SEO для инфобизнеса") &&
             !slug.endsWith("/") && // не папки
             file.frontmatter?.title && // есть заголовок
             slug !== "index" // не index
    })
    .sort(sorter)

  if (limit) {
    list = list.slice(0, limit)
  }

  return (
    <div class="blog-cards-grid">
      {list.map((page) => {
        const title = page.frontmatter?.title
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
              {tags.length > 0 && (
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
  )
}

PageList.css = `
.section h3 {
  margin: 0;
}

.section > .tags {
  margin: 0;
}
`
