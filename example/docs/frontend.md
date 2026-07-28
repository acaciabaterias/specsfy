# Frontend e design system

<!-- specsfy:documentator:start -->
## Views, páginas e componentes

| Tipo | Nome | Fonte |
| --- | --- | --- |
| View | app | `resources/views/app.blade.php` |
| Página | layout | `resources/js/layouts/settings/layout.tsx` |
| Página | confirm-password | `resources/js/pages/auth/confirm-password.tsx` |
| Página | forgot-password | `resources/js/pages/auth/forgot-password.tsx` |
| Página | login | `resources/js/pages/auth/login.tsx` |
| Página | register | `resources/js/pages/auth/register.tsx` |
| Página | reset-password | `resources/js/pages/auth/reset-password.tsx` |
| Página | two-factor-challenge | `resources/js/pages/auth/two-factor-challenge.tsx` |
| Página | dashboard | `resources/js/pages/dashboard.tsx` |
| Página | index | `resources/js/pages/directory/teams/index.tsx` |
| Página | show | `resources/js/pages/directory/teams/show.tsx` |
| Página | index | `resources/js/pages/directory/users/index.tsx` |
| Página | show | `resources/js/pages/directory/users/show.tsx` |
| Página | appearance | `resources/js/pages/settings/appearance.tsx` |
| Página | profile | `resources/js/pages/settings/profile.tsx` |
| Página | security | `resources/js/pages/settings/security.tsx` |
| Página | edit | `resources/js/pages/teams/edit.tsx` |
| Página | index | `resources/js/pages/teams/index.tsx` |
| Página | welcome | `resources/js/pages/welcome.tsx` |
| Componente | alert-error | `resources/js/components/alert-error.tsx` |
| Componente | app-content | `resources/js/components/app-content.tsx` |
| Componente | app-header | `resources/js/components/app-header.tsx` |
| Componente | app-logo-icon | `resources/js/components/app-logo-icon.tsx` |
| Componente | app-logo | `resources/js/components/app-logo.tsx` |
| Componente | app-shell | `resources/js/components/app-shell.tsx` |
| Componente | app-sidebar-header | `resources/js/components/app-sidebar-header.tsx` |
| Componente | app-sidebar | `resources/js/components/app-sidebar.tsx` |
| Componente | appearance-tabs | `resources/js/components/appearance-tabs.tsx` |
| Componente | breadcrumbs | `resources/js/components/breadcrumbs.tsx` |
| Componente | cancel-invitation-modal | `resources/js/components/cancel-invitation-modal.tsx` |
| Componente | create-team-modal | `resources/js/components/create-team-modal.tsx` |
| Componente | delete-team-modal | `resources/js/components/delete-team-modal.tsx` |
| Componente | delete-user | `resources/js/components/delete-user.tsx` |
| Componente | heading | `resources/js/components/heading.tsx` |
| Componente | input-error | `resources/js/components/input-error.tsx` |
| Componente | invite-member-modal | `resources/js/components/invite-member-modal.tsx` |
| Componente | leave-team-modal | `resources/js/components/leave-team-modal.tsx` |
| Componente | manage-passkeys | `resources/js/components/manage-passkeys.tsx` |
| Componente | manage-two-factor | `resources/js/components/manage-two-factor.tsx` |
| Componente | nav-footer | `resources/js/components/nav-footer.tsx` |
| Componente | nav-main | `resources/js/components/nav-main.tsx` |
| Componente | nav-user | `resources/js/components/nav-user.tsx` |
| Componente | passkey-item | `resources/js/components/passkey-item.tsx` |
| Componente | passkey-register | `resources/js/components/passkey-register.tsx` |
| Componente | passkey-verify | `resources/js/components/passkey-verify.tsx` |
| Componente | password-input | `resources/js/components/password-input.tsx` |
| Componente | pending-invitations-modal | `resources/js/components/pending-invitations-modal.tsx` |
| Componente | remove-member-modal | `resources/js/components/remove-member-modal.tsx` |
| Componente | team-invitation-alert | `resources/js/components/team-invitation-alert.tsx` |
| Componente | team-switcher | `resources/js/components/team-switcher.tsx` |
| Componente | text-link | `resources/js/components/text-link.tsx` |
| Componente | two-factor-recovery-codes | `resources/js/components/two-factor-recovery-codes.tsx` |
| Componente | two-factor-setup-modal | `resources/js/components/two-factor-setup-modal.tsx` |
| Componente | alert | `resources/js/components/ui/alert.tsx` |
| Componente | avatar | `resources/js/components/ui/avatar.tsx` |
| Componente | badge | `resources/js/components/ui/badge.tsx` |
| Componente | breadcrumb | `resources/js/components/ui/breadcrumb.tsx` |
| Componente | button | `resources/js/components/ui/button.tsx` |
| Componente | card | `resources/js/components/ui/card.tsx` |
| Componente | checkbox | `resources/js/components/ui/checkbox.tsx` |
| Componente | collapsible | `resources/js/components/ui/collapsible.tsx` |
| Componente | dialog | `resources/js/components/ui/dialog.tsx` |
| Componente | dropdown-menu | `resources/js/components/ui/dropdown-menu.tsx` |
| Componente | icon | `resources/js/components/ui/icon.tsx` |
| Componente | input-otp | `resources/js/components/ui/input-otp.tsx` |
| Componente | input | `resources/js/components/ui/input.tsx` |
| Componente | label | `resources/js/components/ui/label.tsx` |
| Componente | navigation-menu | `resources/js/components/ui/navigation-menu.tsx` |
| Componente | placeholder-pattern | `resources/js/components/ui/placeholder-pattern.tsx` |
| Componente | select | `resources/js/components/ui/select.tsx` |
| Componente | separator | `resources/js/components/ui/separator.tsx` |
| Componente | sheet | `resources/js/components/ui/sheet.tsx` |
| Componente | sidebar | `resources/js/components/ui/sidebar.tsx` |
| Componente | skeleton | `resources/js/components/ui/skeleton.tsx` |
| Componente | sonner | `resources/js/components/ui/sonner.tsx` |
| Componente | spinner | `resources/js/components/ui/spinner.tsx` |
| Componente | toggle-group | `resources/js/components/ui/toggle-group.tsx` |
| Componente | toggle | `resources/js/components/ui/toggle.tsx` |
| Componente | tooltip | `resources/js/components/ui/tooltip.tsx` |
| Componente | user-info | `resources/js/components/user-info.tsx` |
| Componente | user-menu-content | `resources/js/components/user-menu-content.tsx` |

## Tailwind CSS

| Configuração | Fonte |
| --- | --- |
| Tailwind | `resources/css/app.css` |

### Tokens observados

`--accent`, `--accent-foreground`, `--background`, `--border`, `--card`, `--card-foreground`, `--chart-1`, `--chart-2`, `--chart-3`, `--chart-4`, `--chart-5`, `--color-accent`, `--color-accent-foreground`, `--color-background`, `--color-border`, `--color-card`, `--color-card-foreground`, `--color-chart-1`, `--color-chart-2`, `--color-chart-3`, `--color-chart-4`, `--color-chart-5`, `--color-destructive`, `--color-destructive-foreground`, `--color-foreground`, `--color-input`, `--color-muted`, `--color-muted-foreground`, `--color-popover`, `--color-popover-foreground`, `--color-primary`, `--color-primary-foreground`, `--color-ring`, `--color-secondary`, `--color-secondary-foreground`, `--color-sidebar`, `--color-sidebar-accent`, `--color-sidebar-accent-foreground`, `--color-sidebar-border`, `--color-sidebar-foreground`, `--color-sidebar-primary`, `--color-sidebar-primary-foreground`, `--color-sidebar-ring`, `--destructive`, `--destructive-foreground`, `--font-sans`, `--foreground`, `--input`, `--muted`, `--muted-foreground`, `--normal-bg`, `--normal-border`, `--normal-text`, `--popover`, `--popover-foreground`, `--primary`, `--primary-foreground`, `--radius`, `--radius-lg`, `--radius-md`, `--radius-sm`, `--radix-dropdown-menu-trigger-width`, `--radix-navigation-menu-viewport-height`, `--radix-navigation-menu-viewport-width`, `--radix-select-content-available-height`, `--radix-select-content-transform-origin`, `--radix-select-trigger-height`, `--radix-select-trigger-width`, `--ring`, `--secondary`, `--secondary-foreground`, `--sidebar`, `--sidebar-accent`, `--sidebar-accent-foreground`, `--sidebar-border`, `--sidebar-foreground`, `--sidebar-primary`, `--sidebar-primary-foreground`, `--sidebar-ring`, `--sidebar-width`, `--sidebar-width-icon`, `--skeleton-width`, `--spacing`, `--stroke-color`

### Padrões utilitários mais usados

| Classe | Ocorrências |
| --- | --- |
| flex | 125 |
| items-center | 82 |
| w-full | 54 |
| text-sm | 50 |
| text-muted-foreground | 50 |
| gap-2 | 49 |
| flex-col | 47 |
| font-medium | 45 |
| grid | 40 |
| border | 31 |
| px-4 | 29 |
| relative | 29 |
| justify-center | 27 |
| gap-4 | 25 |
| rounded-lg | 24 |
| space-y-6 | 22 |
| py-3 | 22 |
| sr-only | 19 |
| absolute | 18 |
| text-center | 18 |
| h-full | 15 |
| h-4 | 15 |
| mt-1 | 15 |
| justify-between | 14 |
| overflow-hidden | 14 |
| size-4 | 14 |
| p-4 | 13 |
| w-4 | 13 |
| flex-1 | 12 |
| block | 11 |

## Convenções de leitura

- Blade vive normalmente em `resources/views/`.
- React é mapeado por componentes JSX/TSX e suas páginas consumidoras.
- Tailwind é derivado de configuração, imports, tokens e classes observadas;
  este mapa não inventa design tokens ausentes.
<!-- specsfy:documentator:end -->
