<?php

namespace App\Http\Controllers\Directory;

use App\Http\Controllers\Controller;
use App\Models\Team;
use App\Models\User;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Http\Request;
use Illuminate\Pagination\LengthAwarePaginator;
use Inertia\Inertia;
use Inertia\Response;

class UserDirectoryController extends Controller
{
    /**
     * Display the global user directory.
     */
    public function index(Request $request): Response
    {
        $search = $request->string('q')->trim()->limit(100, '')->toString();

        $users = User::query()
            ->select(['id', 'name', 'email_verified_at', 'created_at'])
            ->withCount('teams')
            ->when(
                $search !== '',
                fn ($query) => $query->where('name', 'like', "%{$search}%"),
            )
            ->orderByRaw('LOWER(name)')
            ->orderBy('id')
            ->paginate(15)
            ->withQueryString();

        return Inertia::render('directory/users/index', [
            'users' => $this->paginate($users, fn (User $user) => [
                'id' => $user->id,
                'name' => $user->name,
                'isVerified' => $user->email_verified_at !== null,
                'joinedAt' => $user->created_at?->toDateString(),
                'teamsCount' => $user->teams_count,
            ]),
            'filters' => [
                'q' => $search,
            ],
        ]);
    }

    /**
     * Display a public directory profile.
     */
    public function show(User $user): Response
    {
        $user->load([
            'teams' => fn (BelongsToMany $query) => $query
                ->select(['teams.id', 'teams.name', 'teams.slug', 'teams.is_personal'])
                ->orderByRaw('LOWER(teams.name)')
                ->orderBy('teams.id'),
        ]);

        return Inertia::render('directory/users/show', [
            'user' => [
                'id' => $user->id,
                'name' => $user->name,
                'isVerified' => $user->email_verified_at !== null,
                'joinedAt' => $user->created_at?->toDateString(),
                'teams' => $user->teams->map(fn (Team $team) => [
                    'id' => $team->id,
                    'name' => $team->name,
                    'slug' => $team->slug,
                    'isPersonal' => $team->is_personal,
                    'role' => $team->pivot->role->value,
                    'roleLabel' => $team->pivot->role->label(),
                ])->values(),
            ],
        ]);
    }

    /**
     * Transform a paginator into the stable directory contract.
     *
     * @template TModel
     * @template TItem
     *
     * @param  LengthAwarePaginator<int, TModel>  $paginator
     * @param  callable(TModel): TItem  $transform
     * @return array{
     *     data: list<TItem>,
     *     links: array{previous: string|null, next: string|null},
     *     meta: array{currentPage: int, lastPage: int, perPage: int, total: int}
     * }
     */
    private function paginate(LengthAwarePaginator $paginator, callable $transform): array
    {
        return [
            'data' => array_values(collect($paginator->items())->map($transform)->all()),
            'links' => [
                'previous' => $paginator->previousPageUrl(),
                'next' => $paginator->nextPageUrl(),
            ],
            'meta' => [
                'currentPage' => $paginator->currentPage(),
                'lastPage' => $paginator->lastPage(),
                'perPage' => $paginator->perPage(),
                'total' => $paginator->total(),
            ],
        ];
    }
}
