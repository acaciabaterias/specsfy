# Testes

<!-- specsfy:documentator:start -->
## Runner e comandos

- Runner observado: **Pest**

| Comando | Origem |
| --- | --- |
| `php artisan test` | manifest ou padrão do framework |

## Resumo dos testes

| Classe | Quantidade |
| --- | --- |
| Feature/integração | 26 |
| Outros | 3 |
| Unidade | 1 |

## Inventário

| Teste | Caminho |
| --- | --- |
| AuthenticationTest | `tests/Feature/Auth/AuthenticationTest.php` |
| PasswordConfirmationTest | `tests/Feature/Auth/PasswordConfirmationTest.php` |
| PasswordResetTest | `tests/Feature/Auth/PasswordResetTest.php` |
| RegistrationTest | `tests/Feature/Auth/RegistrationTest.php` |
| TwoFactorChallengeTest | `tests/Feature/Auth/TwoFactorChallengeTest.php` |
| DashboardTest | `tests/Feature/DashboardTest.php` |
| TeamDetailTest | `tests/Feature/Directory/TeamDetailTest.php` |
| TeamDirectoryTest | `tests/Feature/Directory/TeamDirectoryTest.php` |
| UserDirectoryTest | `tests/Feature/Directory/UserDirectoryTest.php` |
| UserProfileTest | `tests/Feature/Directory/UserProfileTest.php` |
| UserSearchTest | `tests/Feature/Directory/UserSearchTest.php` |
| ExampleTest | `tests/Feature/ExampleTest.php` |
| ProfileUpdateTest | `tests/Feature/Settings/ProfileUpdateTest.php` |
| SecurityTest | `tests/Feature/Settings/SecurityTest.php` |
| PruneExpiredTeamInvitationsTest | `tests/Feature/Teams/PruneExpiredTeamInvitationsTest.php` |
| TeamInvitationTest | `tests/Feature/Teams/TeamInvitationTest.php` |
| TeamMemberTest | `tests/Feature/Teams/TeamMemberTest.php` |
| TeamTest | `tests/Feature/Teams/TeamTest.php` |
| Pest | `tests/Pest.php` |
| TestCase | `tests/TestCase.php` |
| ExampleTest | `tests/Unit/ExampleTest.php` |
| directory_team_detail | `tests/features/directory_team_detail.feature` |
| directory_teams | `tests/features/directory_teams.feature` |
| directory_user_profile | `tests/features/directory_user_profile.feature` |
| directory_user_search | `tests/features/directory_user_search.feature` |
| directory_users | `tests/features/directory_users.feature` |
| documentation | `tests/features/documentation.feature` |
| directory_steps | `tests/features/steps/directory_steps.py` |
| documentation_steps | `tests/features/steps/documentation_steps.py` |
| test_documentation | `tests/test_documentation.py` |

## Guia

1. Executar primeiro o teste focal da mudança.
2. Executar a suíte relacionada e depois a regressão completa.
3. Registrar RED/GREEN e comandos na spec quando o projeto usar Specsfy.
4. Não considerar erro de ambiente ou fixture como RED válido.
<!-- specsfy:documentator:end -->
