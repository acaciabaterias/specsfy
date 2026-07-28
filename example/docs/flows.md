# Fluxos

<!-- specsfy:documentator:start -->
## Entradas observadas

| Método/Tipo | Caminho | Destino observado |
| --- | --- | --- |
| REDIRECT | settings | '/settings/profile' |
| GET | settings/profile | [ProfileController::class, 'edit'])->name('profile.edit' |
| PATCH | settings/profile | [ProfileController::class, 'update'])->name('profile.update' |
| DELETE | settings/profile | [ProfileController::class, 'destroy'])->name('profile.destroy' |
| INERTIA | settings/appearance | 'settings/appearance')->name('appearance.edit' |
| GET | settings/teams | [TeamController::class, 'index'])->name('teams.index' |
| POST | settings/teams | [TeamController::class, 'store'])->name('teams.store' |
| GET | settings/teams/{team} | [TeamController::class, 'edit'])->name('teams.edit' |
| PATCH | settings/teams/{team} | [TeamController::class, 'update'])->name('teams.update' |
| DELETE | settings/teams/{team} | [TeamController::class, 'destroy'])->name('teams.destroy' |
| POST | settings/teams/{team}/switch | [TeamController::class, 'switch'])->name('teams.switch' |
| DELETE | settings/teams/{team}/leave | [TeamController::class, 'leave'])->name('teams.leave' |
| PATCH | settings/teams/{team}/members/{user} | [TeamMemberController::class, 'update'])->name('teams.members.update' |
| DELETE | settings/teams/{team}/members/{user} | [TeamMemberController::class, 'destroy'])->name('teams.members.destroy' |
| POST | settings/teams/{team}/invitations | [TeamInvitationController::class, 'store'])->name('teams.invitations.store' |
| DELETE | settings/teams/{team}/invitations/{invitation} | [TeamInvitationController::class, 'destroy'])->name('teams.invitations.destroy' |
| INERTIA | / | 'welcome')->name('home' |
| GET | dashboard | DashboardController::class)->name('dashboard' |
| GET | users | [UserDirectoryController::class, 'index'])->name('users.index' |
| GET | users/{user} | [UserDirectoryController::class, 'show'])->name('users.show' |
| GET | teams | [TeamDirectoryController::class, 'index'])->name('teams.index' |
| GET | teams/{team} | [TeamDirectoryController::class, 'show'])->name('teams.show' |
| GET | invitations/{invitation}/accept | [TeamInvitationController::class, 'accept'])->name('invitations.accept' |
| DELETE | invitations/{invitation} | [TeamInvitationController::class, 'decline'])->name('invitations.decline' |

## Fluxo de navegação e requisição

```mermaid
flowchart LR
  Client[Cliente] --> Entry[Rota / Página]
  Entry --> R1["REDIRECT settings"]
  R1 --> T1["'/settings/profile'"]
  Entry --> R2["GET settings/profile"]
  R2 --> T2["[ProfileController::class, 'edit'])->name('profile.edit'"]
  Entry --> R3["PATCH settings/profile"]
  R3 --> T3["[ProfileController::class, 'update'])->name('profile.update'"]
  Entry --> R4["DELETE settings/profile"]
  R4 --> T4["[ProfileController::class, 'destroy'])->name('profile.destroy'"]
  Entry --> R5["INERTIA settings/appearance"]
  R5 --> T5["'settings/appearance')->name('appearance.edit'"]
  Entry --> R6["GET settings/teams"]
  R6 --> T6["[TeamController::class, 'index'])->name('teams.index'"]
  Entry --> R7["POST settings/teams"]
  R7 --> T7["[TeamController::class, 'store'])->name('teams.store'"]
  Entry --> R8["GET settings/teams/{team}"]
  R8 --> T8["[TeamController::class, 'edit'])->name('teams.edit'"]
  Entry --> R9["PATCH settings/teams/{team}"]
  R9 --> T9["[TeamController::class, 'update'])->name('teams.update'"]
  Entry --> R10["DELETE settings/teams/{team}"]
  R10 --> T10["[TeamController::class, 'destroy'])->name('teams.destroy'"]
  Entry --> R11["POST settings/teams/{team}/switch"]
  R11 --> T11["[TeamController::class, 'switch'])->name('teams.switch'"]
  Entry --> R12["DELETE settings/teams/{team}/leave"]
  R12 --> T12["[TeamController::class, 'leave'])->name('teams.leave'"]
  Entry --> R13["PATCH settings/teams/{team}/members/{user}"]
  R13 --> T13["[TeamMemberController::class, 'update'])->name('teams.members.update'"]
  Entry --> R14["DELETE settings/teams/{team}/members/{user}"]
  R14 --> T14["[TeamMemberController::class, 'destroy'])->name('teams.members.destroy'"]
  Entry --> R15["POST settings/teams/{team}/invitations"]
  R15 --> T15["[TeamInvitationController::class, 'store'])->name('teams.invitations.store'"]
  Entry --> R16["DELETE settings/teams/{team}/invitations/{invitation}"]
  R16 --> T16["[TeamInvitationController::class, 'destroy'])->name('teams.invitations.destroy'"]
  Entry --> R17["INERTIA /"]
  R17 --> T17["'welcome')->name('home'"]
  Entry --> R18["GET dashboard"]
  R18 --> T18["DashboardController::class)->name('dashboard'"]
  Entry --> R19["GET users"]
  R19 --> T19["[UserDirectoryController::class, 'index'])->name('users.index'"]
  Entry --> R20["GET users/{user}"]
  R20 --> T20["[UserDirectoryController::class, 'show'])->name('users.show'"]
  Entry --> R21["GET teams"]
  R21 --> T21["[TeamDirectoryController::class, 'index'])->name('teams.index'"]
  Entry --> R22["GET teams/{team}"]
  R22 --> T22["[TeamDirectoryController::class, 'show'])->name('teams.show'"]
  Entry --> R23["GET invitations/{invitation}/accept"]
  R23 --> T23["[TeamInvitationController::class, 'accept'])->name('invitations.accept'"]
  Entry --> R24["DELETE invitations/{invitation}"]
  R24 --> T24["[TeamInvitationController::class, 'decline'])->name('invitations.decline'"]
```

## Sequência representativa

```mermaid
sequenceDiagram
  actor User as Pessoa usuária
  participant UI as Interface/API
  participant App as '/settings/profile'
  participant DB as Persistência
  User->>UI: inicia ação
  UI->>App: envia entrada
  App->>DB: consulta ou persiste
  DB-->>App: retorna estado
  App-->>UI: produz resposta
  UI-->>User: apresenta resultado
```
<!-- specsfy:documentator:end -->
