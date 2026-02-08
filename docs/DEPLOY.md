# Инструкция по деплою

Руководство по развертыванию блога на собственном домене.

---

## 🚀 Быстрый старт

### Вариант 1: GitHub Pages (рекомендуется)

1. **Настройка репозитория:**
   ```bash
   # Убедитесь, что изменения запушены
   git push origin v4
   ```

2. **Включить GitHub Pages:**
   - Перейдите в Settings репозитория
   - Pages → Source → GitHub Actions

3. **Создать workflow файл:**
   Создайте `.github/workflows/deploy.yml`:
   ```yaml
   name: Deploy Quartz site to Pages

   on:
     push:
       branches: ["v4"]
     workflow_dispatch:

   permissions:
     contents: read
     pages: write
     id-token: write

   concurrency:
     group: "pages"
     cancel-in-progress: false

   jobs:
     build:
       runs-on: ubuntu-22.04
       steps:
         - uses: actions/checkout@v4
           with:
             fetch-depth: 0

         - uses: actions/setup-node@v4
           with:
             node-version: 18

         - name: Install Dependencies
           run: npm ci

         - name: Build Quartz
           run: npx quartz build

         - name: Upload artifact
           uses: actions/upload-pages-artifact@v3
           with:
             path: ./public

     deploy:
       environment:
         name: github-pages
         url: ${{ steps.deployment.outputs.page_url }}
       runs-on: ubuntu-22.04
       needs: build
       steps:
         - name: Deploy to GitHub Pages
           id: deployment
           uses: actions/deploy-pages@v4
   ```

4. **Настроить кастомный домен:**
   - В настройках Pages добавьте свой домен
   - Настройте DNS записи у регистратора:
     ```
     Type: CNAME
     Name: www (или @)
     Value: <username>.github.io
     ```
   - Подождите распространения DNS (5-30 минут)
   - Включите "Enforce HTTPS"

---

### Вариант 2: Cloudflare Pages

1. **Подключить репозиторий:**
   - Войдите в Cloudflare Dashboard
   - Pages → Create a project → Connect to Git
   - Выберите ваш репозиторий

2. **Настройки сборки:**
   ```
   Framework preset: None
   Build command: npx quartz build
   Build output directory: public
   Root directory: /
   ```

3. **Environment variables:**
   ```
   NODE_VERSION=18
   ```

4. **Кастомный домен:**
   - Custom domains → Add a domain
   - Следуйте инструкциям для настройки DNS

---

### Вариант 3: Vercel

1. **Импорт проекта:**
   - Войдите в Vercel
   - Add New → Project
   - Import Git Repository

2. **Настройки:**
   ```
   Build Command: npx quartz build
   Output Directory: public
   Install Command: npm install
   ```

3. **Кастомный домен:**
   - Settings → Domains → Add
   - Следуйте инструкциям

---

### Вариант 4: Netlify

1. **Создать `netlify.toml` в корне:**
   ```toml
   [build]
     command = "npx quartz build"
     publish = "public"

   [[redirects]]
     from = "/*"
     to = "/index.html"
     status = 200
   ```

2. **Деплой:**
   - Войдите в Netlify
   - Add new site → Import existing project
   - Выберите репозиторий

3. **Домен:**
   - Domain settings → Add custom domain

---

## 🔧 Настройка перед деплоем

### 1. Обновить baseUrl в quartz.config.ts:

```typescript
const config: QuartzConfig = {
  configuration: {
    pageTitle: "Здоровье и Нутрициология",
    baseUrl: "your-domain.com", // ← Изменить на ваш домен
    // ...
  },
}
```

### 2. Проверить ignorePatterns:

```typescript
ignorePatterns: [
  "private",
  "templates",
  ".obsidian",
  "docs", // Добавьте, если не хотите публиковать документацию
],
```

### 3. Включить аналитику (опционально):

```typescript
analytics: {
  provider: "plausible",
  // или
  provider: "google",
  tagId: "G-XXXXXXXXXX",
},
```

---

## ✅ Checklist перед первым деплоем

- [ ] `baseUrl` настроен в `quartz.config.ts`
- [ ] Все изменения закоммичены и запушены
- [ ] Проект собирается локально без ошибок (`npx quartz build`)
- [ ] Проверены все страницы на localhost
- [ ] Подготовлен кастомный домен (если нужен)
- [ ] Выбрана платформа для хостинга
- [ ] Настроены DNS записи
- [ ] Включен HTTPS

---

## 🔄 Автоматический деплой

После настройки любого из вариантов выше:

1. Внесите изменения в контент
2. Закоммитьте: `git commit -m "Добавлена новая статья"`
3. Запушьте: `git push origin v4`
4. Сайт автоматически пересоберется и обновится (1-3 минуты)

---

## 📊 После деплоя

### Проверка:
- [ ] Сайт открывается по домену
- [ ] Все страницы загружаются
- [ ] Изображения отображаются
- [ ] Стили применены
- [ ] Навигация работает
- [ ] HTTPS включен
- [ ] Mobile версия работает

### Оптимизация:
- [ ] Проверить Lighthouse score
- [ ] Настроить кэширование
- [ ] Подключить CDN (если не Cloudflare)
- [ ] Добавить в Google Search Console
- [ ] Создать robots.txt
- [ ] Проверить sitemap.xml

---

## 🐛 Проблемы и решения

### Сайт не обновляется после push

1. Проверьте статус workflow в GitHub Actions
2. Очистите кэш CDN
3. Проверьте, что push был в правильную ветку

### 404 на всех страницах кроме главной

1. Проверьте настройки redirects
2. Убедитесь, что SPA режим включен в `quartz.config.ts`
3. Настройте fallback на index.html

### Broken styles or assets

1. Проверьте `baseUrl` в конфиге
2. Убедитесь, что `public` папка правильно публикуется
3. Проверьте пути к ресурсам (должны быть относительные)

---

## 📚 Дополнительные ресурсы

- [Quartz Documentation](https://quartz.jzhao.xyz/)
- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages/)
- [Vercel Docs](https://vercel.com/docs)
- [Netlify Docs](https://docs.netlify.com/)

---

*Последнее обновление: 2026-02-08*
