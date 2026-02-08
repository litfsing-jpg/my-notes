import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "../types"
import { PageList } from "../PageList"
import { FullSlug } from "../../util/path"
import { byDateAndAlphabetical } from "../PageList"

export default (() => {
  const HomePage: QuartzComponent = ({ cfg, allFiles, fileData }: QuartzComponentProps) => {
    // Фильтруем только статьи (не index и не папки)
    const articles = allFiles.filter(file => {
      const slug = file.slug as FullSlug
      return !slug.endsWith("index") &&
             !slug.includes("SEO для инфобизнеса") && // Исключаем служебные папки
             file.slug !== "index" &&
             slug !== "" &&
             file.frontmatter?.title // Только файлы с заголовками
    })

    const listProps = {
      cfg,
      fileData,
      allFiles: articles,
      sort: byDateAndAlphabetical(cfg),
    }

    return (
      <div class="homepage">
        <article class="homepage-intro">
          <h1>Научный подход к здоровью</h1>
          <p class="homepage-description">
            Добро пожаловать в блог о здоровье, питании и нутрициологии.
            Здесь вы найдете научно обоснованные материалы о том, как улучшить
            качество жизни через правильное питание и здоровые привычки.
          </p>
        </article>

        <section class="homepage-section">
          <h2 class="section-title">Последние статьи</h2>
          <PageList {...listProps} />
        </section>
      </div>
    )
  }

  HomePage.css = `
    .homepage {
      max-width: 1200px;
      margin: 0 auto;
      padding: 2rem 1rem;
    }

    .homepage-intro {
      text-align: center;
      margin-bottom: 3rem;
      padding: 0 1rem;
    }

    .homepage-intro h1 {
      font-size: 2.5rem;
      margin-bottom: 1rem;
      color: #141414;
    }

    .homepage-description {
      font-size: 1.125rem;
      color: #4e4e4e;
      max-width: 700px;
      margin: 0 auto;
      line-height: 1.7;
    }

    .homepage-section {
      margin-top: 3rem;
    }

    .section-title {
      font-size: 1.75rem;
      font-weight: 600;
      color: #141414;
      margin-bottom: 2rem;
      padding-bottom: 0.75rem;
      border-bottom: 2px solid #53c257;
    }

    @media (max-width: 768px) {
      .homepage-intro h1 {
        font-size: 2rem;
      }

      .homepage-description {
        font-size: 1rem;
      }

      .section-title {
        font-size: 1.5rem;
      }
    }
  `

  return HomePage
}) satisfies QuartzComponentConstructor
