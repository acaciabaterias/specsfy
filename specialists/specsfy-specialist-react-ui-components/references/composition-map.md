# Mapa de Composicao

Use este mapa, junto de `$specsfy-specialist-ui-design`, para decidir quais
famílias de `assets/components/` consultar e em qual ordem. Os nomes `ui-*`
abaixo são rótulos de família herdados pelas composições; consulte a
correspondência em [catalog.md](catalog.md).

## Landing Page SaaS

Sequencia comum:

1. `ui-hero`: primeira dobra com navbar e prova visual.
2. `ui-marketing-features`: feature section ou grid de beneficios.
3. `ui-marketing-proof`: stats, testimonials ou logos para prova.
4. `ui-marketing-conversion` ou `ui-marketing-content`: pricing, FAQ ou CTA final.
5. `ui-layout-navigation`: footer.

Boas combinacoes:

- `hero-with-navbar-screenshot` + `feature-grid-with-screenshot` + `testimonial-masonry-grid` + `pricing-three-tier-frequency-toggle` + `faq-disclosure-list` + `footer-newsletter-row`.
- `hero-with-navbar-screenshot` + `feature-grid-three-column` + `logo-cloud-trusted-teams` + `pricing-two-tier-card-highlight` + `footer-newsletter-row`.
- `ui-layout-navigation/navbar-marketing-mega-menu` + `hero-with-navbar-screenshot` + `feature-grid-inline-icons` + `testimonial-masonry-grid` + `footer-newsletter-row`.
- `ui-layout-navigation/navbar-marketing-mega-menu-full-width` + `hero-with-background-image-navbar` + `feature-grid-with-screenshot` + `pricing-two-tier-card-highlight` + `footer-newsletter-row`.
- `ui-layout-navigation/navbar-marketing-dual-popover` + `hero-with-navbar-screenshot` + `content-mission-stats` + `team-image-social-grid` + `footer-multi-column-social`.
- `ui-layout-navigation/navbar-marketing-dual-popover-sticky-mobile-cta` + `hero-with-code-panel` + `feature-grid-with-screenshot` + `cta-dark-centered` + `footer-newsletter-row`.
- `ui-layout-navigation/navbar-marketing-popover-overlay` + `hero-with-navbar-screenshot` + `feature-grid-with-screenshot` + `logo-cloud-trusted-teams` + `footer-newsletter-row`.
- `ui-layout-navigation/navbar-marketing-popover-enterprise` + `hero-with-code-panel` + `pricing-two-tier-card-highlight` + `stats-trust-grid` + `footer-newsletter-row`.
- `ui-layout-navigation/navbar-marketing-popover-enterprise-split-nav` + `hero-with-code-panel` + `feature-grid-with-screenshot` + `pricing-two-tier-card-highlight` + `footer-newsletter-row`.
- `ui-layout-navigation/navbar-marketing-popover-editorial-blog` + `hero-with-navbar-screenshot` + `blog-featured-list.tsx` + `cta-dark-centered.tsx` + `footer-newsletter-row`.
- `ui-layout-navigation/navbar-marketing-simple` + `hero-with-code-panel` + `feature-grid-three-column` + `logo-cloud-trusted-teams` + `footer-centered-links-social`.
- `ui-layout-navigation/navbar-marketing-centered-logo` + `hero-with-navbar-image-collage` + `content-mission-stats` + `footer-centered-links-social`.
- `ui-layout-navigation/navbar-marketing-simple-full-bleed` + `hero-with-navbar-image-collage` + `content-mission-stats` + `footer-centered-links-social`.
- `ui-layout-navigation/navbar-marketing-simple-inline-login` + `hero-with-navbar-screenshot` + `feature-grid-three-column` + `footer-centered-links-social`.
- `ui-layout-navigation/navbar-marketing-simple-left-grouped` + `hero-with-navbar-image-collage` + `content-mission-stats` + `footer-multi-column-social`.
- `ui-layout-navigation/navbar-marketing-simple-signup-cta` + `hero-with-code-panel` + `pricing-two-tier-card-highlight` + `cta-dark-centered` + `footer-newsletter-row`.
- `ui-layout-navigation/navbar-marketing-simple-indigo` + `hero-with-background-image-navbar` + `stats-trust-grid` + `cta-dark-centered` + `footer-social-simple`.
- `ui-layout-navigation/navbar-marketing-indigo-stacked-mobile-links` + `hero-with-background-image-navbar` + `logo-cloud-trusted-teams` + `cta-dark-centered` + `footer-social-simple`.
- `hero-with-code-panel` + `feature-grid-inline-icons` + `stats-trust-grid` + `cta-dark-centered` + `footer-social-simple`.
- `support-contact-split-form` + `ui-forms/input` + `ui-forms/textarea`.
- `contact-project-brief-form` + `support-contact-cards-background` + `ui-forms/input`.
- `contact-work-together-form` + `ui-forms/radio` + `ui-forms/input`.
- `contact-info-form-panel` + `ui-forms/input` + `ui-forms/textarea`.
- `contact-side-info-form` + `ui-forms/input` + `ui-forms/textarea`.
- `contact-info-form-panel` + `ui-forms/input` + `ui-forms/textarea`.

## Site Institucional

Sequencia comum:

1. `ui-hero`: imagem editorial, colagem ou split image.
2. `ui-marketing-content` ou `ui-marketing-proof`: about/content, mission, stats.
3. `ui-marketing-company`: team, offices, careers ou contact.
4. `ui-layout-navigation`: footer multi-coluna.

Boas combinacoes:

- `hero-with-background-image-navbar` + `content-mission-stats` + `team-image-social-grid` + `offices-simple-grid` + `footer-multi-column-social`.
- `hero-with-navbar-image-collage` + `careers-job-openings` + `team-avatar-dense-grid` + `footer-centered-links-social`.

## Produto Mobile

Sequencia comum:

1. `ui-hero`: mobile app em device frame.
2. `ui-marketing-features`: features compactas.
3. `ui-marketing-proof`: testimonials ou stats.
4. `ui-marketing-conversion`: CTA/newsletter.

Use `ui-forms` se houver waitlist, email capture ou early access.

## App Autenticado

Sequencia comum:

1. `ui-layout-navigation`: `sidebar-layout` ou `stacked-layout`.
2. `ui-data-display`: tabela, badges, avatares, details.
3. `ui-forms`: filtros, busca, edicao.
4. `ui-actions-feedback`: dropdowns, dialogs, alerts, empty states.
5. `ui-typography`: heading, description, dividers.

Evite `ui-hero` e secoes de marketing dentro de dashboard, salvo telas publicas ou onboarding.

## Formulario Publico

Sequencia comum:

1. `ui-marketing-company` ou `ui-marketing-features` para contexto da secao, se for landing/contact section.
2. `ui-forms` para campos e controles.
3. `ui-actions-feedback` para submit, erro, sucesso e confirmacao.
4. `ui-typography` para labels, helper text e policy copy.

Boas combinacoes:

- `contact-sales-form-gradient` + `ui-forms/input` + `ui-forms/select` + `ui-forms/textarea` + `ui-forms/switch`.

## Pagina de Conteudo/Artigo

Sequencia comum:

1. `ui-marketing-content` para article/content section.
2. `ui-typography` para hierarquia de texto.
3. `ui-marketing-content` ou `ui-marketing-conversion` para related posts, FAQ ou CTA final.
4. `ui-layout-navigation` para footer.

## Componente Isolado

Escolha a skill pelo papel do componente:

- botao/menu/dialog/alerta -> `ui-actions-feedback`;
- input/select/radio/switch -> `ui-forms`;
- tabela/avatar/badge/detail -> `ui-data-display`;
- heading/link/divider/text -> `ui-typography`;
- footer/navbar/sidebar/pagination -> `ui-layout-navigation`.
