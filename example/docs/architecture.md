# Arquitetura

<!-- specsfy:documentator:start -->
## Contexto arquitetural

- Frameworks e superfícies observadas: Laravel, Pest, React, Tailwind CSS.
- A topologia abaixo é inferida de manifests e caminhos; confirme limites não
  expressos no código.

```mermaid
flowchart LR
  Human[Pessoa usuária] --> UI[Interface / API]
  Agent[Agente de código] --> Docs[docs/]
  UI --> App[Aplicação]
  App --> Database[Persistência]
  App --> Integrations[Integrações externas]
  Docs --> App
```

## UML de componentes implementados

```mermaid
classDiagram
  class Controller
  class DashboardController
  class TeamDirectoryController
  class UserDirectoryController
  class ProfileController
  class SecurityController
  class TeamController
  class TeamInvitationController
  class TeamMemberController
  class index
  class Membership
  class Team
  class TeamInvitation
  class User
  class alert_error
  class app_content
  class app_header
  class app_logo_icon
  class app_logo
  class app_shell
  class app_sidebar_header
  class app_sidebar
  class appearance_tabs
  class breadcrumbs
  class cancel_invitation_modal
  class create_team_modal
  class delete_team_modal
  class delete_user
  class heading
  class input_error
  class invite_member_modal
  class leave_team_modal
  class manage_passkeys
  class manage_two_factor
```

## Evidência por camada

| Camada | Quantidade | Exemplos |
| --- | --- | --- |
| Controllers | 38 | `app/Http/Controllers/Controller.php`, `app/Http/Controllers/DashboardController.php`, `app/Http/Controllers/Directory/TeamDirectoryController.php`, `app/Http/Controllers/Directory/UserDirectoryController.php`, `app/Http/Controllers/Settings/ProfileController.php` |
| Models | 4 | `app/Models/Membership.php`, `app/Models/Team.php`, `app/Models/TeamInvitation.php`, `app/Models/User.php` |
| Services | 0 | — |
| Jobs | 0 | — |
| Policies | 1 | `app/Policies/TeamPolicy.php` |
| Routes and APIs | 3 | `routes/console.php`, `routes/settings.php`, `routes/web.php` |
| Views | 1 | `resources/views/app.blade.php` |
| Pages | 18 | `resources/js/layouts/settings/layout.tsx`, `resources/js/pages/auth/confirm-password.tsx`, `resources/js/pages/auth/forgot-password.tsx`, `resources/js/pages/auth/login.tsx`, `resources/js/pages/auth/register.tsx` |
| Components | 62 | `resources/js/components/alert-error.tsx`, `resources/js/components/app-content.tsx`, `resources/js/components/app-header.tsx`, `resources/js/components/app-logo-icon.tsx`, `resources/js/components/app-logo.tsx` |
| Tests | 30 | `tests/Feature/Auth/AuthenticationTest.php`, `tests/Feature/Auth/PasswordConfirmationTest.php`, `tests/Feature/Auth/PasswordResetTest.php`, `tests/Feature/Auth/RegistrationTest.php`, `tests/Feature/Auth/TwoFactorChallengeTest.php` |
| Other source | 122 | `app/Actions/Fortify/CreateNewUser.php`, `app/Actions/Fortify/ResetUserPassword.php`, `app/Actions/Teams/CreateTeam.php`, `app/Concerns/GeneratesUniqueTeamSlugs.php`, `app/Concerns/HasTeams.php` |
<!-- specsfy:documentator:end -->
