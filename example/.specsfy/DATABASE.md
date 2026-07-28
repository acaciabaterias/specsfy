# Banco de dados

Mapa de persistência do sistema. Modelo inicial sugerido para **Laravel**.

Para Laravel, descreva módulos de domínio, fronteiras HTTP/console e use `database/migrations` como primeira evidência do mapa de dados.

## Fontes de dados

<!-- specsfy:database:start -->
| Fonte | Tecnologia/forma | Evidência |
| --- | --- | --- |
| Principal | SQLite | `.env.example` (`DB_CONNECTION`) |
| Estrutura | Schema/migration | `database/migrations/0001_01_01_000000_create_users_table.php` |
| Estrutura | Schema/migration | `database/migrations/0001_01_01_000001_create_cache_table.php` |
| Estrutura | Schema/migration | `database/migrations/0001_01_01_000002_create_jobs_table.php` |
| Estrutura | Schema/migration | `database/migrations/2024_01_01_000000_create_passkeys_table.php` |
| Estrutura | Schema/migration | `database/migrations/2025_08_14_170933_add_two_factor_columns_to_users_table.php` |
| Estrutura | Schema/migration | `database/migrations/2026_01_27_000001_create_teams_table.php` |
| Estrutura | Schema/migration | `database/migrations/2026_01_27_000002_add_current_team_id_to_users_table.php` |

## Estruturas detectadas

| Estrutura | Tipo | Campos | Relações | Fonte |
| --- | --- | --- | --- | --- |
| users | Tabela | id, name, email, email_verified_at, password, current_team_id, two_factor_secret, two_factor_recovery_codes, two_factor_confirmed_at, remember_token, created_at, updated_at | current_team_id → teams.id (SET NULL) | `database/migrations/0001_01_01_000000_create_users_table.php`; `database/migrations/2025_08_14_170933_add_two_factor_columns_to_users_table.php`; `database/migrations/2026_01_27_000002_add_current_team_id_to_users_table.php` |
| password_reset_tokens | Tabela | email, token, created_at | Não detectadas | `database/migrations/0001_01_01_000000_create_users_table.php` |
| sessions | Tabela | id, user_id, ip_address, user_agent, payload, last_activity | `user_id` indexado; sem foreign key declarada | `database/migrations/0001_01_01_000000_create_users_table.php` |
| cache | Tabela | key, value, expiration | Não detectadas | `database/migrations/0001_01_01_000001_create_cache_table.php` |
| cache_locks | Tabela | key, owner, expiration | Não detectadas | `database/migrations/0001_01_01_000001_create_cache_table.php` |
| jobs | Tabela | id, queue, payload, attempts, reserved_at, available_at, created_at | Não detectadas | `database/migrations/0001_01_01_000002_create_jobs_table.php` |
| job_batches | Tabela | id, name, total_jobs, pending_jobs, failed_jobs, failed_job_ids, options, cancelled_at, created_at, finished_at | Não detectadas | `database/migrations/0001_01_01_000002_create_jobs_table.php` |
| failed_jobs | Tabela | id, uuid, connection, queue, payload, exception, failed_at | Não detectadas | `database/migrations/0001_01_01_000002_create_jobs_table.php` |
| passkeys | Tabela | id, user_id, name, credential_id, credential, last_used_at, created_at, updated_at | user_id → users.id (CASCADE) | `database/migrations/2024_01_01_000000_create_passkeys_table.php` |
| teams | Tabela | id, name, slug, is_personal, created_at, updated_at, deleted_at | Não detectadas | `database/migrations/2026_01_27_000001_create_teams_table.php` |
| team_members | Tabela | id, team_id, user_id, role, created_at, updated_at | team_id → teams.id (CASCADE); user_id → users.id (CASCADE) | `database/migrations/2026_01_27_000001_create_teams_table.php` |
| team_invitations | Tabela | id, code, team_id, email, role, invited_by, expires_at, accepted_at, created_at, updated_at | team_id → teams.id (CASCADE); invited_by → users.id (CASCADE) | `database/migrations/2026_01_27_000001_create_teams_table.php` |
<!-- specsfy:database:end -->

## Decisões, ownership e retenção

Registre finalidade, ownership, classificação, retenção, constraints e decisões
que não estejam explícitas nos schemas.
