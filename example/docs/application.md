# Aplicação e implementações

<!-- specsfy:documentator:start -->
## Inventário implementado

O inventário inclui código anterior à adoção do Specsfy e mudanças recentes.
Nomes representam símbolos ou arquivos observados, não responsabilidades
inventadas.

| Tipo | Implementação | Fonte |
| --- | --- | --- |
| Controllers | Controller | `app/Http/Controllers/Controller.php` |
| Controllers | DashboardController | `app/Http/Controllers/DashboardController.php` |
| Controllers | TeamDirectoryController | `app/Http/Controllers/Directory/TeamDirectoryController.php` |
| Controllers | UserDirectoryController | `app/Http/Controllers/Directory/UserDirectoryController.php` |
| Controllers | ProfileController | `app/Http/Controllers/Settings/ProfileController.php` |
| Controllers | SecurityController | `app/Http/Controllers/Settings/SecurityController.php` |
| Controllers | TeamController | `app/Http/Controllers/Teams/TeamController.php` |
| Controllers | TeamInvitationController | `app/Http/Controllers/Teams/TeamInvitationController.php` |
| Controllers | TeamMemberController | `app/Http/Controllers/Teams/TeamMemberController.php` |
| Controllers | DashboardController | `resources/js/actions/App/Http/Controllers/DashboardController.ts` |
| Controllers | TeamDirectoryController | `resources/js/actions/App/Http/Controllers/Directory/TeamDirectoryController.ts` |
| Controllers | UserDirectoryController | `resources/js/actions/App/Http/Controllers/Directory/UserDirectoryController.ts` |
| Controllers | index | `resources/js/actions/App/Http/Controllers/Directory/index.ts` |
| Controllers | ProfileController | `resources/js/actions/App/Http/Controllers/Settings/ProfileController.ts` |
| Controllers | SecurityController | `resources/js/actions/App/Http/Controllers/Settings/SecurityController.ts` |
| Controllers | index | `resources/js/actions/App/Http/Controllers/Settings/index.ts` |
| Controllers | TeamController | `resources/js/actions/App/Http/Controllers/Teams/TeamController.ts` |
| Controllers | TeamInvitationController | `resources/js/actions/App/Http/Controllers/Teams/TeamInvitationController.ts` |
| Controllers | TeamMemberController | `resources/js/actions/App/Http/Controllers/Teams/TeamMemberController.ts` |
| Controllers | index | `resources/js/actions/App/Http/Controllers/Teams/index.ts` |
| Controllers | index | `resources/js/actions/App/Http/Controllers/index.ts` |
| Controllers | AuthenticatedSessionController | `resources/js/actions/Laravel/Fortify/Http/Controllers/AuthenticatedSessionController.ts` |
| Controllers | ConfirmablePasswordController | `resources/js/actions/Laravel/Fortify/Http/Controllers/ConfirmablePasswordController.ts` |
| Controllers | ConfirmedPasswordStatusController | `resources/js/actions/Laravel/Fortify/Http/Controllers/ConfirmedPasswordStatusController.ts` |
| Controllers | ConfirmedTwoFactorAuthenticationController | `resources/js/actions/Laravel/Fortify/Http/Controllers/ConfirmedTwoFactorAuthenticationController.ts` |
| Controllers | NewPasswordController | `resources/js/actions/Laravel/Fortify/Http/Controllers/NewPasswordController.ts` |
| Controllers | PasswordResetLinkController | `resources/js/actions/Laravel/Fortify/Http/Controllers/PasswordResetLinkController.ts` |
| Controllers | RecoveryCodeController | `resources/js/actions/Laravel/Fortify/Http/Controllers/RecoveryCodeController.ts` |
| Controllers | RegisteredUserController | `resources/js/actions/Laravel/Fortify/Http/Controllers/RegisteredUserController.ts` |
| Controllers | TwoFactorAuthenticatedSessionController | `resources/js/actions/Laravel/Fortify/Http/Controllers/TwoFactorAuthenticatedSessionController.ts` |
| Controllers | TwoFactorAuthenticationController | `resources/js/actions/Laravel/Fortify/Http/Controllers/TwoFactorAuthenticationController.ts` |
| Controllers | TwoFactorQrCodeController | `resources/js/actions/Laravel/Fortify/Http/Controllers/TwoFactorQrCodeController.ts` |
| Controllers | TwoFactorSecretKeyController | `resources/js/actions/Laravel/Fortify/Http/Controllers/TwoFactorSecretKeyController.ts` |
| Controllers | index | `resources/js/actions/Laravel/Fortify/Http/Controllers/index.ts` |
| Controllers | PasskeyConfirmationController | `resources/js/actions/Laravel/Passkeys/Http/Controllers/PasskeyConfirmationController.ts` |
| Controllers | PasskeyLoginController | `resources/js/actions/Laravel/Passkeys/Http/Controllers/PasskeyLoginController.ts` |
| Controllers | PasskeyRegistrationController | `resources/js/actions/Laravel/Passkeys/Http/Controllers/PasskeyRegistrationController.ts` |
| Controllers | index | `resources/js/actions/Laravel/Passkeys/Http/Controllers/index.ts` |
| Models | Membership | `app/Models/Membership.php` |
| Models | Team | `app/Models/Team.php` |
| Models | TeamInvitation | `app/Models/TeamInvitation.php` |
| Models | User | `app/Models/User.php` |
| Policies | TeamPolicy | `app/Policies/TeamPolicy.php` |
| Rotas e APIs | console | `routes/console.php` |
| Rotas e APIs | settings | `routes/settings.php` |
| Rotas e APIs | web | `routes/web.php` |
| Views | app | `resources/views/app.blade.php` |
| Páginas | layout | `resources/js/layouts/settings/layout.tsx` |
| Páginas | confirm-password | `resources/js/pages/auth/confirm-password.tsx` |
| Páginas | forgot-password | `resources/js/pages/auth/forgot-password.tsx` |
| Páginas | login | `resources/js/pages/auth/login.tsx` |
| Páginas | register | `resources/js/pages/auth/register.tsx` |
| Páginas | reset-password | `resources/js/pages/auth/reset-password.tsx` |
| Páginas | two-factor-challenge | `resources/js/pages/auth/two-factor-challenge.tsx` |
| Páginas | dashboard | `resources/js/pages/dashboard.tsx` |
| Páginas | index | `resources/js/pages/directory/teams/index.tsx` |
| Páginas | show | `resources/js/pages/directory/teams/show.tsx` |
| Páginas | index | `resources/js/pages/directory/users/index.tsx` |
| Páginas | show | `resources/js/pages/directory/users/show.tsx` |
| Páginas | appearance | `resources/js/pages/settings/appearance.tsx` |
| Páginas | profile | `resources/js/pages/settings/profile.tsx` |
| Páginas | security | `resources/js/pages/settings/security.tsx` |
| Páginas | edit | `resources/js/pages/teams/edit.tsx` |
| Páginas | index | `resources/js/pages/teams/index.tsx` |
| Páginas | welcome | `resources/js/pages/welcome.tsx` |
| Componentes | alert-error | `resources/js/components/alert-error.tsx` |
| Componentes | app-content | `resources/js/components/app-content.tsx` |
| Componentes | app-header | `resources/js/components/app-header.tsx` |
| Componentes | app-logo-icon | `resources/js/components/app-logo-icon.tsx` |
| Componentes | app-logo | `resources/js/components/app-logo.tsx` |
| Componentes | app-shell | `resources/js/components/app-shell.tsx` |
| Componentes | app-sidebar-header | `resources/js/components/app-sidebar-header.tsx` |
| Componentes | app-sidebar | `resources/js/components/app-sidebar.tsx` |
| Componentes | appearance-tabs | `resources/js/components/appearance-tabs.tsx` |
| Componentes | breadcrumbs | `resources/js/components/breadcrumbs.tsx` |
| Componentes | cancel-invitation-modal | `resources/js/components/cancel-invitation-modal.tsx` |
| Componentes | create-team-modal | `resources/js/components/create-team-modal.tsx` |
| Componentes | delete-team-modal | `resources/js/components/delete-team-modal.tsx` |
| Componentes | delete-user | `resources/js/components/delete-user.tsx` |
| Componentes | heading | `resources/js/components/heading.tsx` |
| Componentes | input-error | `resources/js/components/input-error.tsx` |
| Componentes | invite-member-modal | `resources/js/components/invite-member-modal.tsx` |
| Componentes | leave-team-modal | `resources/js/components/leave-team-modal.tsx` |
| Componentes | manage-passkeys | `resources/js/components/manage-passkeys.tsx` |
| Componentes | manage-two-factor | `resources/js/components/manage-two-factor.tsx` |
| Componentes | nav-footer | `resources/js/components/nav-footer.tsx` |
| Componentes | nav-main | `resources/js/components/nav-main.tsx` |
| Componentes | nav-user | `resources/js/components/nav-user.tsx` |
| Componentes | passkey-item | `resources/js/components/passkey-item.tsx` |
| Componentes | passkey-register | `resources/js/components/passkey-register.tsx` |
| Componentes | passkey-verify | `resources/js/components/passkey-verify.tsx` |
| Componentes | password-input | `resources/js/components/password-input.tsx` |
| Componentes | pending-invitations-modal | `resources/js/components/pending-invitations-modal.tsx` |
| Componentes | remove-member-modal | `resources/js/components/remove-member-modal.tsx` |
| Componentes | team-invitation-alert | `resources/js/components/team-invitation-alert.tsx` |
| Componentes | team-switcher | `resources/js/components/team-switcher.tsx` |
| Componentes | text-link | `resources/js/components/text-link.tsx` |
| Componentes | two-factor-recovery-codes | `resources/js/components/two-factor-recovery-codes.tsx` |
| Componentes | two-factor-setup-modal | `resources/js/components/two-factor-setup-modal.tsx` |
| Componentes | alert | `resources/js/components/ui/alert.tsx` |
| Componentes | avatar | `resources/js/components/ui/avatar.tsx` |
| Componentes | badge | `resources/js/components/ui/badge.tsx` |
| Componentes | breadcrumb | `resources/js/components/ui/breadcrumb.tsx` |
| Componentes | button | `resources/js/components/ui/button.tsx` |
| Componentes | card | `resources/js/components/ui/card.tsx` |
| Componentes | checkbox | `resources/js/components/ui/checkbox.tsx` |
| Componentes | collapsible | `resources/js/components/ui/collapsible.tsx` |
| Componentes | dialog | `resources/js/components/ui/dialog.tsx` |
| Componentes | dropdown-menu | `resources/js/components/ui/dropdown-menu.tsx` |
| Componentes | icon | `resources/js/components/ui/icon.tsx` |
| Componentes | input-otp | `resources/js/components/ui/input-otp.tsx` |
| Componentes | input | `resources/js/components/ui/input.tsx` |
| Componentes | label | `resources/js/components/ui/label.tsx` |
| Componentes | navigation-menu | `resources/js/components/ui/navigation-menu.tsx` |
| Componentes | placeholder-pattern | `resources/js/components/ui/placeholder-pattern.tsx` |
| Componentes | select | `resources/js/components/ui/select.tsx` |
| Componentes | separator | `resources/js/components/ui/separator.tsx` |
| Componentes | sheet | `resources/js/components/ui/sheet.tsx` |
| Componentes | sidebar | `resources/js/components/ui/sidebar.tsx` |
| Componentes | skeleton | `resources/js/components/ui/skeleton.tsx` |
| Componentes | sonner | `resources/js/components/ui/sonner.tsx` |
| Componentes | spinner | `resources/js/components/ui/spinner.tsx` |
| Componentes | toggle-group | `resources/js/components/ui/toggle-group.tsx` |
| Componentes | toggle | `resources/js/components/ui/toggle.tsx` |
| Componentes | tooltip | `resources/js/components/ui/tooltip.tsx` |
| Componentes | user-info | `resources/js/components/user-info.tsx` |
| Componentes | user-menu-content | `resources/js/components/user-menu-content.tsx` |
| Testes | AuthenticationTest | `tests/Feature/Auth/AuthenticationTest.php` |
| Testes | PasswordConfirmationTest | `tests/Feature/Auth/PasswordConfirmationTest.php` |
| Testes | PasswordResetTest | `tests/Feature/Auth/PasswordResetTest.php` |
| Testes | RegistrationTest | `tests/Feature/Auth/RegistrationTest.php` |
| Testes | TwoFactorChallengeTest | `tests/Feature/Auth/TwoFactorChallengeTest.php` |
| Testes | DashboardTest | `tests/Feature/DashboardTest.php` |
| Testes | TeamDetailTest | `tests/Feature/Directory/TeamDetailTest.php` |
| Testes | TeamDirectoryTest | `tests/Feature/Directory/TeamDirectoryTest.php` |
| Testes | UserDirectoryTest | `tests/Feature/Directory/UserDirectoryTest.php` |
| Testes | UserProfileTest | `tests/Feature/Directory/UserProfileTest.php` |
| Testes | UserSearchTest | `tests/Feature/Directory/UserSearchTest.php` |
| Testes | ExampleTest | `tests/Feature/ExampleTest.php` |
| Testes | ProfileUpdateTest | `tests/Feature/Settings/ProfileUpdateTest.php` |
| Testes | SecurityTest | `tests/Feature/Settings/SecurityTest.php` |
| Testes | PruneExpiredTeamInvitationsTest | `tests/Feature/Teams/PruneExpiredTeamInvitationsTest.php` |
| Testes | TeamInvitationTest | `tests/Feature/Teams/TeamInvitationTest.php` |
| Testes | TeamMemberTest | `tests/Feature/Teams/TeamMemberTest.php` |
| Testes | TeamTest | `tests/Feature/Teams/TeamTest.php` |
| Testes | Pest | `tests/Pest.php` |
| Testes | TestCase | `tests/TestCase.php` |
| Testes | ExampleTest | `tests/Unit/ExampleTest.php` |
| Testes | directory_team_detail | `tests/features/directory_team_detail.feature` |
| Testes | directory_teams | `tests/features/directory_teams.feature` |
| Testes | directory_user_profile | `tests/features/directory_user_profile.feature` |
| Testes | directory_user_search | `tests/features/directory_user_search.feature` |
| Testes | directory_users | `tests/features/directory_users.feature` |
| Testes | documentation | `tests/features/documentation.feature` |
| Testes | directory_steps | `tests/features/steps/directory_steps.py` |
| Testes | documentation_steps | `tests/features/steps/documentation_steps.py` |
| Testes | test_documentation | `tests/test_documentation.py` |
| Outras fontes | CreateNewUser | `app/Actions/Fortify/CreateNewUser.php` |
| Outras fontes | ResetUserPassword | `app/Actions/Fortify/ResetUserPassword.php` |
| Outras fontes | CreateTeam | `app/Actions/Teams/CreateTeam.php` |
| Outras fontes | GeneratesUniqueTeamSlugs | `app/Concerns/GeneratesUniqueTeamSlugs.php` |
| Outras fontes | HasTeams | `app/Concerns/HasTeams.php` |
| Outras fontes | PasswordValidationRules | `app/Concerns/PasswordValidationRules.php` |
| Outras fontes | ProfileValidationRules | `app/Concerns/ProfileValidationRules.php` |
| Outras fontes | TeamPermissions | `app/Data/TeamPermissions.php` |
| Outras fontes | UserTeam | `app/Data/UserTeam.php` |
| Outras fontes | TeamPermission | `app/Enums/TeamPermission.php` |
| Outras fontes | TeamRole | `app/Enums/TeamRole.php` |
| Outras fontes | EnsureTeamMembership | `app/Http/Middleware/EnsureTeamMembership.php` |
| Outras fontes | HandleAppearance | `app/Http/Middleware/HandleAppearance.php` |
| Outras fontes | HandleInertiaRequests | `app/Http/Middleware/HandleInertiaRequests.php` |
| Outras fontes | SetTeamUrlDefaults | `app/Http/Middleware/SetTeamUrlDefaults.php` |
| Outras fontes | PasswordUpdateRequest | `app/Http/Requests/Settings/PasswordUpdateRequest.php` |
| Outras fontes | ProfileDeleteRequest | `app/Http/Requests/Settings/ProfileDeleteRequest.php` |
| Outras fontes | ProfileUpdateRequest | `app/Http/Requests/Settings/ProfileUpdateRequest.php` |
| Outras fontes | TwoFactorAuthenticationRequest | `app/Http/Requests/Settings/TwoFactorAuthenticationRequest.php` |
| Outras fontes | CreateTeamInvitationRequest | `app/Http/Requests/Teams/CreateTeamInvitationRequest.php` |
| Outras fontes | DeleteTeamRequest | `app/Http/Requests/Teams/DeleteTeamRequest.php` |
| Outras fontes | RespondToTeamInvitationRequest | `app/Http/Requests/Teams/RespondToTeamInvitationRequest.php` |
| Outras fontes | SaveTeamRequest | `app/Http/Requests/Teams/SaveTeamRequest.php` |
| Outras fontes | UpdateTeamMemberRequest | `app/Http/Requests/Teams/UpdateTeamMemberRequest.php` |
| Outras fontes | RedirectsToCurrentTeam | `app/Http/Responses/Concerns/RedirectsToCurrentTeam.php` |
| Outras fontes | LoginResponse | `app/Http/Responses/LoginResponse.php` |
| Outras fontes | PasskeyLoginResponse | `app/Http/Responses/PasskeyLoginResponse.php` |
| Outras fontes | RegisterResponse | `app/Http/Responses/RegisterResponse.php` |
| Outras fontes | TwoFactorLoginResponse | `app/Http/Responses/TwoFactorLoginResponse.php` |
| Outras fontes | TeamInvitation | `app/Notifications/Teams/TeamInvitation.php` |
| Outras fontes | AppServiceProvider | `app/Providers/AppServiceProvider.php` |
| Outras fontes | FortifyServiceProvider | `app/Providers/FortifyServiceProvider.php` |
| Outras fontes | TeamName | `app/Rules/TeamName.php` |
| Outras fontes | UniqueTeamInvitation | `app/Rules/UniqueTeamInvitation.php` |
| Outras fontes | ValidTeamInvitation | `app/Rules/ValidTeamInvitation.php` |
| Outras fontes | app | `bootstrap/app.php` |
| Outras fontes | providers | `bootstrap/providers.php` |
| Outras fontes | app | `config/app.php` |
| Outras fontes | auth | `config/auth.php` |
| Outras fontes | cache | `config/cache.php` |
| Outras fontes | database | `config/database.php` |
| Outras fontes | filesystems | `config/filesystems.php` |
| Outras fontes | fortify | `config/fortify.php` |
| Outras fontes | inertia | `config/inertia.php` |
| Outras fontes | logging | `config/logging.php` |
| Outras fontes | mail | `config/mail.php` |
| Outras fontes | queue | `config/queue.php` |
| Outras fontes | services | `config/services.php` |
| Outras fontes | session | `config/session.php` |
| Outras fontes | TeamFactory | `database/factories/TeamFactory.php` |
| Outras fontes | TeamInvitationFactory | `database/factories/TeamInvitationFactory.php` |
| Outras fontes | UserFactory | `database/factories/UserFactory.php` |
| Outras fontes | 0001_01_01_000000_create_users_table | `database/migrations/0001_01_01_000000_create_users_table.php` |
| Outras fontes | 0001_01_01_000001_create_cache_table | `database/migrations/0001_01_01_000001_create_cache_table.php` |
| Outras fontes | 0001_01_01_000002_create_jobs_table | `database/migrations/0001_01_01_000002_create_jobs_table.php` |
| Outras fontes | 2024_01_01_000000_create_passkeys_table | `database/migrations/2024_01_01_000000_create_passkeys_table.php` |
| Outras fontes | 2025_08_14_170933_add_two_factor_columns_to_users_table | `database/migrations/2025_08_14_170933_add_two_factor_columns_to_users_table.php` |
| Outras fontes | 2026_01_27_000001_create_teams_table | `database/migrations/2026_01_27_000001_create_teams_table.php` |
| Outras fontes | 2026_01_27_000002_add_current_team_id_to_users_table | `database/migrations/2026_01_27_000002_add_current_team_id_to_users_table.php` |
| Outras fontes | DatabaseSeeder | `database/seeders/DatabaseSeeder.php` |
| Outras fontes | eslint.config | `eslint.config.js` |
| Outras fontes | index | `public/index.php` |
| Outras fontes | index | `resources/js/actions/App/Http/index.ts` |
| Outras fontes | index | `resources/js/actions/App/index.ts` |
| Outras fontes | RedirectController | `resources/js/actions/Illuminate/Routing/RedirectController.ts` |
| Outras fontes | index | `resources/js/actions/Illuminate/Routing/index.ts` |
| Outras fontes | index | `resources/js/actions/Illuminate/index.ts` |
| Outras fontes | Controller | `resources/js/actions/Inertia/Controller.ts` |
| Outras fontes | index | `resources/js/actions/Inertia/index.ts` |
| Outras fontes | index | `resources/js/actions/Laravel/Fortify/Http/index.ts` |
| Outras fontes | index | `resources/js/actions/Laravel/Fortify/index.ts` |
| Outras fontes | index | `resources/js/actions/Laravel/Passkeys/Http/index.ts` |
| Outras fontes | index | `resources/js/actions/Laravel/Passkeys/index.ts` |
| Outras fontes | index | `resources/js/actions/Laravel/index.ts` |
| Outras fontes | app | `resources/js/app.tsx` |
| Outras fontes | use-appearance | `resources/js/hooks/use-appearance.tsx` |
| Outras fontes | use-clipboard | `resources/js/hooks/use-clipboard.ts` |
| Outras fontes | use-current-url | `resources/js/hooks/use-current-url.ts` |
| Outras fontes | use-flash-toast | `resources/js/hooks/use-flash-toast.ts` |
| Outras fontes | use-initials | `resources/js/hooks/use-initials.tsx` |
| Outras fontes | use-mobile-navigation | `resources/js/hooks/use-mobile-navigation.ts` |
| Outras fontes | use-mobile | `resources/js/hooks/use-mobile.tsx` |
| Outras fontes | use-two-factor-auth | `resources/js/hooks/use-two-factor-auth.ts` |
| Outras fontes | app-header-layout | `resources/js/layouts/app/app-header-layout.tsx` |
| Outras fontes | app-sidebar-layout | `resources/js/layouts/app/app-sidebar-layout.tsx` |
| Outras fontes | app-layout | `resources/js/layouts/app-layout.tsx` |
| Outras fontes | auth-card-layout | `resources/js/layouts/auth/auth-card-layout.tsx` |
| Outras fontes | auth-simple-layout | `resources/js/layouts/auth/auth-simple-layout.tsx` |
| Outras fontes | auth-split-layout | `resources/js/layouts/auth/auth-split-layout.tsx` |
| Outras fontes | auth-layout | `resources/js/layouts/auth-layout.tsx` |
| Outras fontes | utils | `resources/js/lib/utils.ts` |
| Outras fontes | index | `resources/js/routes/appearance/index.ts` |
| Outras fontes | index | `resources/js/routes/boost/index.ts` |
| Outras fontes | index | `resources/js/routes/directory/index.ts` |
| Outras fontes | index | `resources/js/routes/directory/teams/index.ts` |
| Outras fontes | index | `resources/js/routes/directory/users/index.ts` |
| Outras fontes | index | `resources/js/routes/index.ts` |
| Outras fontes | index | `resources/js/routes/invitations/index.ts` |
| Outras fontes | index | `resources/js/routes/login/index.ts` |
| Outras fontes | index | `resources/js/routes/passkey/index.ts` |
| Outras fontes | index | `resources/js/routes/password/confirm/index.ts` |
| Outras fontes | index | `resources/js/routes/password/index.ts` |
| Outras fontes | index | `resources/js/routes/profile/index.ts` |
| Outras fontes | index | `resources/js/routes/register/index.ts` |
| Outras fontes | index | `resources/js/routes/security/index.ts` |
| Outras fontes | index | `resources/js/routes/teams/index.ts` |
| Outras fontes | index | `resources/js/routes/teams/invitations/index.ts` |
| Outras fontes | index | `resources/js/routes/teams/members/index.ts` |
| Outras fontes | index | `resources/js/routes/two-factor/index.ts` |
| Outras fontes | index | `resources/js/routes/two-factor/login/index.ts` |
| Outras fontes | index | `resources/js/routes/user-password/index.ts` |
| Outras fontes | index | `resources/js/routes/well-known/index.ts` |
| Outras fontes | auth | `resources/js/types/auth.ts` |
| Outras fontes | directory | `resources/js/types/directory.ts` |
| Outras fontes | global.d | `resources/js/types/global.d.ts` |
| Outras fontes | index | `resources/js/types/index.ts` |
| Outras fontes | navigation | `resources/js/types/navigation.ts` |
| Outras fontes | teams | `resources/js/types/teams.ts` |
| Outras fontes | ui | `resources/js/types/ui.ts` |
| Outras fontes | vite-env.d | `resources/js/types/vite-env.d.ts` |
| Outras fontes | index | `resources/js/wayfinder/index.ts` |
| Outras fontes | vite.config | `vite.config.ts` |

## Mapa de responsabilidades

| Área | Leitura recomendada |
| --- | --- |
| Controllers e APIs | Entradas HTTP, validação e orquestração |
| Models e entidades | Estado persistente, relações e invariantes |
| Serviços e jobs | Casos de uso, integrações e processamento assíncrono |
| Views, páginas e componentes | Apresentação e interação |
<!-- specsfy:documentator:end -->
