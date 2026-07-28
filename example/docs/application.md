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
| Routes and APIs | console | `routes/console.php` |
| Routes and APIs | settings | `routes/settings.php` |
| Routes and APIs | web | `routes/web.php` |
| Views | app | `resources/views/app.blade.php` |
| Pages | layout | `resources/js/layouts/settings/layout.tsx` |
| Pages | confirm-password | `resources/js/pages/auth/confirm-password.tsx` |
| Pages | forgot-password | `resources/js/pages/auth/forgot-password.tsx` |
| Pages | login | `resources/js/pages/auth/login.tsx` |
| Pages | register | `resources/js/pages/auth/register.tsx` |
| Pages | reset-password | `resources/js/pages/auth/reset-password.tsx` |
| Pages | two-factor-challenge | `resources/js/pages/auth/two-factor-challenge.tsx` |
| Pages | dashboard | `resources/js/pages/dashboard.tsx` |
| Pages | index | `resources/js/pages/directory/teams/index.tsx` |
| Pages | show | `resources/js/pages/directory/teams/show.tsx` |
| Pages | index | `resources/js/pages/directory/users/index.tsx` |
| Pages | show | `resources/js/pages/directory/users/show.tsx` |
| Pages | appearance | `resources/js/pages/settings/appearance.tsx` |
| Pages | profile | `resources/js/pages/settings/profile.tsx` |
| Pages | security | `resources/js/pages/settings/security.tsx` |
| Pages | edit | `resources/js/pages/teams/edit.tsx` |
| Pages | index | `resources/js/pages/teams/index.tsx` |
| Pages | welcome | `resources/js/pages/welcome.tsx` |
| Components | alert-error | `resources/js/components/alert-error.tsx` |
| Components | app-content | `resources/js/components/app-content.tsx` |
| Components | app-header | `resources/js/components/app-header.tsx` |
| Components | app-logo-icon | `resources/js/components/app-logo-icon.tsx` |
| Components | app-logo | `resources/js/components/app-logo.tsx` |
| Components | app-shell | `resources/js/components/app-shell.tsx` |
| Components | app-sidebar-header | `resources/js/components/app-sidebar-header.tsx` |
| Components | app-sidebar | `resources/js/components/app-sidebar.tsx` |
| Components | appearance-tabs | `resources/js/components/appearance-tabs.tsx` |
| Components | breadcrumbs | `resources/js/components/breadcrumbs.tsx` |
| Components | cancel-invitation-modal | `resources/js/components/cancel-invitation-modal.tsx` |
| Components | create-team-modal | `resources/js/components/create-team-modal.tsx` |
| Components | delete-team-modal | `resources/js/components/delete-team-modal.tsx` |
| Components | delete-user | `resources/js/components/delete-user.tsx` |
| Components | heading | `resources/js/components/heading.tsx` |
| Components | input-error | `resources/js/components/input-error.tsx` |
| Components | invite-member-modal | `resources/js/components/invite-member-modal.tsx` |
| Components | leave-team-modal | `resources/js/components/leave-team-modal.tsx` |
| Components | manage-passkeys | `resources/js/components/manage-passkeys.tsx` |
| Components | manage-two-factor | `resources/js/components/manage-two-factor.tsx` |
| Components | nav-footer | `resources/js/components/nav-footer.tsx` |
| Components | nav-main | `resources/js/components/nav-main.tsx` |
| Components | nav-user | `resources/js/components/nav-user.tsx` |
| Components | passkey-item | `resources/js/components/passkey-item.tsx` |
| Components | passkey-register | `resources/js/components/passkey-register.tsx` |
| Components | passkey-verify | `resources/js/components/passkey-verify.tsx` |
| Components | password-input | `resources/js/components/password-input.tsx` |
| Components | pending-invitations-modal | `resources/js/components/pending-invitations-modal.tsx` |
| Components | remove-member-modal | `resources/js/components/remove-member-modal.tsx` |
| Components | team-invitation-alert | `resources/js/components/team-invitation-alert.tsx` |
| Components | team-switcher | `resources/js/components/team-switcher.tsx` |
| Components | text-link | `resources/js/components/text-link.tsx` |
| Components | two-factor-recovery-codes | `resources/js/components/two-factor-recovery-codes.tsx` |
| Components | two-factor-setup-modal | `resources/js/components/two-factor-setup-modal.tsx` |
| Components | alert | `resources/js/components/ui/alert.tsx` |
| Components | avatar | `resources/js/components/ui/avatar.tsx` |
| Components | badge | `resources/js/components/ui/badge.tsx` |
| Components | breadcrumb | `resources/js/components/ui/breadcrumb.tsx` |
| Components | button | `resources/js/components/ui/button.tsx` |
| Components | card | `resources/js/components/ui/card.tsx` |
| Components | checkbox | `resources/js/components/ui/checkbox.tsx` |
| Components | collapsible | `resources/js/components/ui/collapsible.tsx` |
| Components | dialog | `resources/js/components/ui/dialog.tsx` |
| Components | dropdown-menu | `resources/js/components/ui/dropdown-menu.tsx` |
| Components | icon | `resources/js/components/ui/icon.tsx` |
| Components | input-otp | `resources/js/components/ui/input-otp.tsx` |
| Components | input | `resources/js/components/ui/input.tsx` |
| Components | label | `resources/js/components/ui/label.tsx` |
| Components | navigation-menu | `resources/js/components/ui/navigation-menu.tsx` |
| Components | placeholder-pattern | `resources/js/components/ui/placeholder-pattern.tsx` |
| Components | select | `resources/js/components/ui/select.tsx` |
| Components | separator | `resources/js/components/ui/separator.tsx` |
| Components | sheet | `resources/js/components/ui/sheet.tsx` |
| Components | sidebar | `resources/js/components/ui/sidebar.tsx` |
| Components | skeleton | `resources/js/components/ui/skeleton.tsx` |
| Components | sonner | `resources/js/components/ui/sonner.tsx` |
| Components | spinner | `resources/js/components/ui/spinner.tsx` |
| Components | toggle-group | `resources/js/components/ui/toggle-group.tsx` |
| Components | toggle | `resources/js/components/ui/toggle.tsx` |
| Components | tooltip | `resources/js/components/ui/tooltip.tsx` |
| Components | user-info | `resources/js/components/user-info.tsx` |
| Components | user-menu-content | `resources/js/components/user-menu-content.tsx` |
| Tests | AuthenticationTest | `tests/Feature/Auth/AuthenticationTest.php` |
| Tests | PasswordConfirmationTest | `tests/Feature/Auth/PasswordConfirmationTest.php` |
| Tests | PasswordResetTest | `tests/Feature/Auth/PasswordResetTest.php` |
| Tests | RegistrationTest | `tests/Feature/Auth/RegistrationTest.php` |
| Tests | TwoFactorChallengeTest | `tests/Feature/Auth/TwoFactorChallengeTest.php` |
| Tests | DashboardTest | `tests/Feature/DashboardTest.php` |
| Tests | TeamDetailTest | `tests/Feature/Directory/TeamDetailTest.php` |
| Tests | TeamDirectoryTest | `tests/Feature/Directory/TeamDirectoryTest.php` |
| Tests | UserDirectoryTest | `tests/Feature/Directory/UserDirectoryTest.php` |
| Tests | UserProfileTest | `tests/Feature/Directory/UserProfileTest.php` |
| Tests | UserSearchTest | `tests/Feature/Directory/UserSearchTest.php` |
| Tests | ExampleTest | `tests/Feature/ExampleTest.php` |
| Tests | ProfileUpdateTest | `tests/Feature/Settings/ProfileUpdateTest.php` |
| Tests | SecurityTest | `tests/Feature/Settings/SecurityTest.php` |
| Tests | PruneExpiredTeamInvitationsTest | `tests/Feature/Teams/PruneExpiredTeamInvitationsTest.php` |
| Tests | TeamInvitationTest | `tests/Feature/Teams/TeamInvitationTest.php` |
| Tests | TeamMemberTest | `tests/Feature/Teams/TeamMemberTest.php` |
| Tests | TeamTest | `tests/Feature/Teams/TeamTest.php` |
| Tests | Pest | `tests/Pest.php` |
| Tests | TestCase | `tests/TestCase.php` |
| Tests | ExampleTest | `tests/Unit/ExampleTest.php` |
| Tests | directory_team_detail | `tests/features/directory_team_detail.feature` |
| Tests | directory_teams | `tests/features/directory_teams.feature` |
| Tests | directory_user_profile | `tests/features/directory_user_profile.feature` |
| Tests | directory_user_search | `tests/features/directory_user_search.feature` |
| Tests | directory_users | `tests/features/directory_users.feature` |
| Tests | documentation | `tests/features/documentation.feature` |
| Tests | directory_steps | `tests/features/steps/directory_steps.py` |
| Tests | documentation_steps | `tests/features/steps/documentation_steps.py` |
| Tests | test_documentation | `tests/test_documentation.py` |
| Other source | CreateNewUser | `app/Actions/Fortify/CreateNewUser.php` |
| Other source | ResetUserPassword | `app/Actions/Fortify/ResetUserPassword.php` |
| Other source | CreateTeam | `app/Actions/Teams/CreateTeam.php` |
| Other source | GeneratesUniqueTeamSlugs | `app/Concerns/GeneratesUniqueTeamSlugs.php` |
| Other source | HasTeams | `app/Concerns/HasTeams.php` |
| Other source | PasswordValidationRules | `app/Concerns/PasswordValidationRules.php` |
| Other source | ProfileValidationRules | `app/Concerns/ProfileValidationRules.php` |
| Other source | TeamPermissions | `app/Data/TeamPermissions.php` |
| Other source | UserTeam | `app/Data/UserTeam.php` |
| Other source | TeamPermission | `app/Enums/TeamPermission.php` |
| Other source | TeamRole | `app/Enums/TeamRole.php` |
| Other source | EnsureTeamMembership | `app/Http/Middleware/EnsureTeamMembership.php` |
| Other source | HandleAppearance | `app/Http/Middleware/HandleAppearance.php` |
| Other source | HandleInertiaRequests | `app/Http/Middleware/HandleInertiaRequests.php` |
| Other source | SetTeamUrlDefaults | `app/Http/Middleware/SetTeamUrlDefaults.php` |
| Other source | PasswordUpdateRequest | `app/Http/Requests/Settings/PasswordUpdateRequest.php` |
| Other source | ProfileDeleteRequest | `app/Http/Requests/Settings/ProfileDeleteRequest.php` |
| Other source | ProfileUpdateRequest | `app/Http/Requests/Settings/ProfileUpdateRequest.php` |
| Other source | TwoFactorAuthenticationRequest | `app/Http/Requests/Settings/TwoFactorAuthenticationRequest.php` |
| Other source | CreateTeamInvitationRequest | `app/Http/Requests/Teams/CreateTeamInvitationRequest.php` |
| Other source | DeleteTeamRequest | `app/Http/Requests/Teams/DeleteTeamRequest.php` |
| Other source | RespondToTeamInvitationRequest | `app/Http/Requests/Teams/RespondToTeamInvitationRequest.php` |
| Other source | SaveTeamRequest | `app/Http/Requests/Teams/SaveTeamRequest.php` |
| Other source | UpdateTeamMemberRequest | `app/Http/Requests/Teams/UpdateTeamMemberRequest.php` |
| Other source | RedirectsToCurrentTeam | `app/Http/Responses/Concerns/RedirectsToCurrentTeam.php` |
| Other source | LoginResponse | `app/Http/Responses/LoginResponse.php` |
| Other source | PasskeyLoginResponse | `app/Http/Responses/PasskeyLoginResponse.php` |
| Other source | RegisterResponse | `app/Http/Responses/RegisterResponse.php` |
| Other source | TwoFactorLoginResponse | `app/Http/Responses/TwoFactorLoginResponse.php` |
| Other source | TeamInvitation | `app/Notifications/Teams/TeamInvitation.php` |
| Other source | AppServiceProvider | `app/Providers/AppServiceProvider.php` |
| Other source | FortifyServiceProvider | `app/Providers/FortifyServiceProvider.php` |
| Other source | TeamName | `app/Rules/TeamName.php` |
| Other source | UniqueTeamInvitation | `app/Rules/UniqueTeamInvitation.php` |
| Other source | ValidTeamInvitation | `app/Rules/ValidTeamInvitation.php` |
| Other source | app | `bootstrap/app.php` |
| Other source | providers | `bootstrap/providers.php` |
| Other source | app | `config/app.php` |
| Other source | auth | `config/auth.php` |
| Other source | cache | `config/cache.php` |
| Other source | database | `config/database.php` |
| Other source | filesystems | `config/filesystems.php` |
| Other source | fortify | `config/fortify.php` |
| Other source | inertia | `config/inertia.php` |
| Other source | logging | `config/logging.php` |
| Other source | mail | `config/mail.php` |
| Other source | queue | `config/queue.php` |
| Other source | services | `config/services.php` |
| Other source | session | `config/session.php` |
| Other source | TeamFactory | `database/factories/TeamFactory.php` |
| Other source | TeamInvitationFactory | `database/factories/TeamInvitationFactory.php` |
| Other source | UserFactory | `database/factories/UserFactory.php` |
| Other source | 0001_01_01_000000_create_users_table | `database/migrations/0001_01_01_000000_create_users_table.php` |
| Other source | 0001_01_01_000001_create_cache_table | `database/migrations/0001_01_01_000001_create_cache_table.php` |
| Other source | 0001_01_01_000002_create_jobs_table | `database/migrations/0001_01_01_000002_create_jobs_table.php` |
| Other source | 2024_01_01_000000_create_passkeys_table | `database/migrations/2024_01_01_000000_create_passkeys_table.php` |
| Other source | 2025_08_14_170933_add_two_factor_columns_to_users_table | `database/migrations/2025_08_14_170933_add_two_factor_columns_to_users_table.php` |
| Other source | 2026_01_27_000001_create_teams_table | `database/migrations/2026_01_27_000001_create_teams_table.php` |
| Other source | 2026_01_27_000002_add_current_team_id_to_users_table | `database/migrations/2026_01_27_000002_add_current_team_id_to_users_table.php` |
| Other source | DatabaseSeeder | `database/seeders/DatabaseSeeder.php` |
| Other source | eslint.config | `eslint.config.js` |
| Other source | index | `public/index.php` |
| Other source | index | `resources/js/actions/App/Http/index.ts` |
| Other source | index | `resources/js/actions/App/index.ts` |
| Other source | RedirectController | `resources/js/actions/Illuminate/Routing/RedirectController.ts` |
| Other source | index | `resources/js/actions/Illuminate/Routing/index.ts` |
| Other source | index | `resources/js/actions/Illuminate/index.ts` |
| Other source | Controller | `resources/js/actions/Inertia/Controller.ts` |
| Other source | index | `resources/js/actions/Inertia/index.ts` |
| Other source | index | `resources/js/actions/Laravel/Fortify/Http/index.ts` |
| Other source | index | `resources/js/actions/Laravel/Fortify/index.ts` |
| Other source | index | `resources/js/actions/Laravel/Passkeys/Http/index.ts` |
| Other source | index | `resources/js/actions/Laravel/Passkeys/index.ts` |
| Other source | index | `resources/js/actions/Laravel/index.ts` |
| Other source | app | `resources/js/app.tsx` |
| Other source | use-appearance | `resources/js/hooks/use-appearance.tsx` |
| Other source | use-clipboard | `resources/js/hooks/use-clipboard.ts` |
| Other source | use-current-url | `resources/js/hooks/use-current-url.ts` |
| Other source | use-flash-toast | `resources/js/hooks/use-flash-toast.ts` |
| Other source | use-initials | `resources/js/hooks/use-initials.tsx` |
| Other source | use-mobile-navigation | `resources/js/hooks/use-mobile-navigation.ts` |
| Other source | use-mobile | `resources/js/hooks/use-mobile.tsx` |
| Other source | use-two-factor-auth | `resources/js/hooks/use-two-factor-auth.ts` |
| Other source | app-header-layout | `resources/js/layouts/app/app-header-layout.tsx` |
| Other source | app-sidebar-layout | `resources/js/layouts/app/app-sidebar-layout.tsx` |
| Other source | app-layout | `resources/js/layouts/app-layout.tsx` |
| Other source | auth-card-layout | `resources/js/layouts/auth/auth-card-layout.tsx` |
| Other source | auth-simple-layout | `resources/js/layouts/auth/auth-simple-layout.tsx` |
| Other source | auth-split-layout | `resources/js/layouts/auth/auth-split-layout.tsx` |
| Other source | auth-layout | `resources/js/layouts/auth-layout.tsx` |
| Other source | utils | `resources/js/lib/utils.ts` |
| Other source | index | `resources/js/routes/appearance/index.ts` |
| Other source | index | `resources/js/routes/boost/index.ts` |
| Other source | index | `resources/js/routes/directory/index.ts` |
| Other source | index | `resources/js/routes/directory/teams/index.ts` |
| Other source | index | `resources/js/routes/directory/users/index.ts` |
| Other source | index | `resources/js/routes/index.ts` |
| Other source | index | `resources/js/routes/invitations/index.ts` |
| Other source | index | `resources/js/routes/login/index.ts` |
| Other source | index | `resources/js/routes/passkey/index.ts` |
| Other source | index | `resources/js/routes/password/confirm/index.ts` |
| Other source | index | `resources/js/routes/password/index.ts` |
| Other source | index | `resources/js/routes/profile/index.ts` |
| Other source | index | `resources/js/routes/register/index.ts` |
| Other source | index | `resources/js/routes/security/index.ts` |
| Other source | index | `resources/js/routes/teams/index.ts` |
| Other source | index | `resources/js/routes/teams/invitations/index.ts` |
| Other source | index | `resources/js/routes/teams/members/index.ts` |
| Other source | index | `resources/js/routes/two-factor/index.ts` |
| Other source | index | `resources/js/routes/two-factor/login/index.ts` |
| Other source | index | `resources/js/routes/user-password/index.ts` |
| Other source | index | `resources/js/routes/well-known/index.ts` |
| Other source | auth | `resources/js/types/auth.ts` |
| Other source | directory | `resources/js/types/directory.ts` |
| Other source | global.d | `resources/js/types/global.d.ts` |
| Other source | index | `resources/js/types/index.ts` |
| Other source | navigation | `resources/js/types/navigation.ts` |
| Other source | teams | `resources/js/types/teams.ts` |
| Other source | ui | `resources/js/types/ui.ts` |
| Other source | vite-env.d | `resources/js/types/vite-env.d.ts` |
| Other source | index | `resources/js/wayfinder/index.ts` |
| Other source | vite.config | `vite.config.ts` |

## Mapa de responsabilidades

| Área | Leitura recomendada |
| --- | --- |
| Controllers e APIs | Entradas HTTP, validação e orquestração |
| Models e entidades | Estado persistente, relações e invariantes |
| Services e jobs | Casos de uso, integrações e processamento assíncrono |
| Views, páginas e componentes | Apresentação e interação |
<!-- specsfy:documentator:end -->
