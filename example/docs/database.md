# Banco de dados

<!-- specsfy:documentator:start -->
## Mapa de persistência

| Entidade/Tabela | Campos | Relações | Fonte |
| --- | --- | --- | --- |
| cache | key:string, value:mediumText, expiration:bigInteger | não inferidas | `database/migrations/0001_01_01_000001_create_cache_table.php` |
| cache_locks | key:string, owner:string, expiration:bigInteger | não inferidas | `database/migrations/0001_01_01_000001_create_cache_table.php` |
| failed_jobs | id:id, uuid:string, connection:string, queue:string, payload:longText, exception:longText, failed_at:timestamp | não inferidas | `database/migrations/0001_01_01_000002_create_jobs_table.php` |
| job_batches | id:string, name:string, total_jobs:integer, pending_jobs:integer, failed_jobs:integer, failed_job_ids:longText, options:mediumText, cancelled_at:integer, created_at:integer, finished_at:integer | não inferidas | `database/migrations/0001_01_01_000002_create_jobs_table.php` |
| jobs | id:id, queue:string, payload:longText, attempts:unsignedSmallInteger, reserved_at:unsignedInteger, available_at:unsignedInteger, created_at:unsignedInteger | não inferidas | `database/migrations/0001_01_01_000002_create_jobs_table.php` |
| passkeys | id:id, created_at:timestamp, updated_at:timestamp, user_id:foreignId, name:string, credential_id:string, credential:json, last_used_at:timestamp | users | `database/migrations/2024_01_01_000000_create_passkeys_table.php` |
| password_reset_tokens | email:string, token:string, created_at:timestamp | não inferidas | `database/migrations/0001_01_01_000000_create_users_table.php` |
| sessions | id:string, user_id:foreignId, ip_address:string, user_agent:text, payload:longText, last_activity:integer | não inferidas | `database/migrations/0001_01_01_000000_create_users_table.php` |
| team_invitations | id:id, created_at:timestamp, updated_at:timestamp, code:string, team_id:foreignId, email:string, role:string, invited_by:foreignId, expires_at:timestamp, accepted_at:timestamp | teams, users | `database/migrations/2026_01_27_000001_create_teams_table.php` |
| team_members | id:id, created_at:timestamp, updated_at:timestamp, team_id:foreignId, user_id:foreignId, role:string | teams, users | `database/migrations/2026_01_27_000001_create_teams_table.php` |
| teams | id:id, deleted_at:timestamp, created_at:timestamp, updated_at:timestamp, name:string, slug:string, is_personal:boolean | não inferidas | `database/migrations/2026_01_27_000001_create_teams_table.php` |
| users | id:id, remember_token:rememberToken, created_at:timestamp, updated_at:timestamp, name:string, email:string, email_verified_at:timestamp, password:string, two_factor_secret:text, two_factor_recovery_codes:text, two_factor_confirmed_at:timestamp, current_team_id:foreignId | teams | `database/migrations/0001_01_01_000000_create_users_table.php; database/migrations/2025_08_14_170933_add_two_factor_columns_to_users_table.php; database/migrations/2026_01_27_000002_add_current_team_id_to_users_table.php` |

```mermaid
erDiagram
  CACHE {
    string key
    mediumText value
    bigInteger expiration
  }
  CACHE_LOCKS {
    string key
    string owner
    bigInteger expiration
  }
  FAILED_JOBS {
    id id
    string uuid
    string connection
    string queue
    longText payload
    longText exception
    timestamp failed_at
  }
  JOB_BATCHES {
    string id
    string name
    integer total_jobs
    integer pending_jobs
    integer failed_jobs
    longText failed_job_ids
    mediumText options
    integer cancelled_at
    integer created_at
    integer finished_at
  }
  JOBS {
    id id
    string queue
    longText payload
    unsignedSmallInteger attempts
    unsignedInteger reserved_at
    unsignedInteger available_at
    unsignedInteger created_at
  }
  PASSKEYS {
    id id
    timestamp created_at
    timestamp updated_at
    foreignId user_id
    string name
    string credential_id
    json credential
    timestamp last_used_at
  }
  USERS ||--o{ PASSKEYS : relaciona
  PASSWORD_RESET_TOKENS {
    string email
    string token
    timestamp created_at
  }
  SESSIONS {
    string id
    foreignId user_id
    string ip_address
    text user_agent
    longText payload
    integer last_activity
  }
  TEAM_INVITATIONS {
    id id
    timestamp created_at
    timestamp updated_at
    string code
    foreignId team_id
    string email
    string role
    foreignId invited_by
    timestamp expires_at
    timestamp accepted_at
  }
  TEAMS ||--o{ TEAM_INVITATIONS : relaciona
  USERS ||--o{ TEAM_INVITATIONS : relaciona
  TEAM_MEMBERS {
    id id
    timestamp created_at
    timestamp updated_at
    foreignId team_id
    foreignId user_id
    string role
  }
  TEAMS ||--o{ TEAM_MEMBERS : relaciona
  USERS ||--o{ TEAM_MEMBERS : relaciona
  TEAMS {
    id id
    timestamp deleted_at
    timestamp created_at
    timestamp updated_at
    string name
    string slug
    boolean is_personal
  }
  USERS {
    id id
    rememberToken remember_token
    timestamp created_at
    timestamp updated_at
    string name
    string email
    timestamp email_verified_at
    string password
    text two_factor_secret
    text two_factor_recovery_codes
    timestamp two_factor_confirmed_at
    foreignId current_team_id
  }
  TEAMS ||--o{ USERS : relaciona
```

## Fonte complementar

Consulte [`.specsfy/DATABASE.md`](../.specsfy/DATABASE.md) para decisões,
ownership, retenção e detalhes humanos não inferíveis.
<!-- specsfy:documentator:end -->
