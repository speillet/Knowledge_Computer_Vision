# Reading the vault on GitHub Pages

## Acceptance criteria

- Use Hugo and Blowfish, following the navigation, typography, light/dark
  appearance and expandable answers of
  [Knowledge_AI_Engineering](https://github.com/speillet/Knowledge_AI_Engineering/tree/d1686b7383d11fcfd8523b0dd73dbf342ebd60fe/website).
- Generate the website from `vault/` and `scripts/vault_sections.json`, with
  all fourteen domains, flashcards, reference notes and learning guides.
- Keep questions, recall objectives, complete answers, sources and stable card
  anchors. Support opening a linked card and showing or hiding all answers.
- Preserve equations, diagrams, images and links between cards and references.
  Search must include the text of questions and answers.
- Leave vault files, pedagogical IDs, Anki identities and export behavior intact.
- Build and check the site on pull requests; deploy `main` through GitHub Pages.
  Check generated internal links, assets and anchors before deployment.

## Structure

The requested reference site determines the presentation and build structure:
`website/config/_default/`, `website/assets/`, `website/layouts/`, a pinned
Blowfish submodule in `website/themes/blowfish`, generated Hugo content in
`website/content/`, and static output in `site/`. Both generated trees are
ignored by Git. New and revised website text is English, as in the vault.

`scripts/prepare_site.py` reads the existing card parser and generates the
reading view. Each question has an expandable answer; reference notes remain
separate, linked pages. The numbered domain order comes from the section
manifest. Guides, the curriculum and the inventory retain their links.

The site uses the same Hugo extended release (0.169.0) and Blowfish 3.10.0 commit
(`3e4b25c4dc74d4da0e83ce5b6b3ac3850de40072`) as the reference repository.
The workflow verifies the Hugo download against its published SHA-256 checksum.
Configuration was checked against the official
[Hugo mathematics documentation](https://gohugo.io/content-management/mathematics/)
and [Blowfish documentation](https://blowfish.page/docs/), using Context7.

## Build and preview

Install Hugo extended 0.169.0, Python 3.9+ and Git. No Python dependencies are
needed for the website.

```sh
git submodule update --init --depth 1 website/themes/blowfish
make site
make site-serve
```

`make site` regenerates content, builds with warnings treated as errors, then
checks internal links, anchors, local assets and the search index. The output
is `site/`. `make site-serve` previews at `http://127.0.0.1:1313/`; rerun it
after changing vault sources, because Hugo watches the generated content.

## GitHub Pages

GitHub Pages was enabled on 16 November 2026 with **GitHub Actions** as the
build and deployment source (`build_type: workflow`, confirmed through the
GitHub API). For another clone or repository, select that source in
**Settings → Pages**. After merging the website files into `main`, the
`Documentation site` workflow builds, validates and deploys to:

<https://speillet.github.io/Knowledge_Computer_Vision/>

Pull requests build and validate an artifact without deploying. A manual
workflow dispatch on `main` can rebuild the published site. The first remote
deployment must be verified separately from a successful local build.

## Local validation, 16 November 2026

- Hugo extended 0.169.0 built the complete site with warnings treated as errors.
- The generated HTML link check found no broken internal pages, assets or
  anchors across 159 pages. The search index contains full answer text.
- All nine website tests passed: content and source identity preservation,
  equations and quoted questions, links and media, stale-page replacement,
  invalid input, project subpaths, missing builds and search targets.
- The full Python suite ran 71 tests: 69 passed and two package tests were
  skipped because `genanki` was unavailable. Website generation needs no
  `genanki`; the Anki exporter was not changed by this work.
- Browser checks used Google Chrome through the existing Playwright 1.57.0
  installation. Home navigation, folded answers, show/hide controls, direct
  card links, KaTeX, Mermaid, search and a 390 px mobile view in dark mode passed
  without JavaScript errors or failed resource requests.
- All 50 Mermaid diagrams passed parsing with the pinned theme's renderer.

These are website and local repository checks. They do not validate learner
recall, scientific coverage, Obsidian behavior or Anki device rendering.

## Visual refinement acceptance criteria

- Replace the eye symbol with an original violet shard built from flat SVG
  facets, drawing on the visual direction of Obsidian's crystal mark. Use the
  same asset for the header and the fingerprinted favicon.
- Give the home page a clear typographic hierarchy, a prominent entry into
  the cards, compact collection counts and an ordered domain directory.
- Use neutral text, restrained violet accents, square corners and visible
  rules. Keep the reading view spacious, with clear question/answer boundaries.
- Preserve navigation, search, card anchors, complete learning content and
  keyboard access. Verify desktop and narrow mobile layouts in both appearances.

Visual refinement checks on 16 November 2026: the complete build and all 159
pages passed the link check. Chrome checks passed at 320, 390, 768, 900, 1024
and 1440 px in light and dark appearances, including menu switching, mobile
menu navigation, keyboard-operated cards, square borders and the new SVG
favicon. Search, answer controls, card links, equations and Mermaid rendering
also passed without JavaScript errors or failed resource requests.
