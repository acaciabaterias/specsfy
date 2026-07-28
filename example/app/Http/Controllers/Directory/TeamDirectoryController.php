<?php

namespace App\Http\Controllers\Directory;

use App\Http\Controllers\Controller;
use App\Models\Team;
use App\Models\User;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Pagination\LengthAwarePaginator;
use Inertia\Inertia;
use Inertia\Response;

class TeamDirectoryController extends Controller
{
    /**
     * Display the global team directory.
     */
    public function index(): Response
    {
        $teams = Team::query()
            ->select(['id', 'name', 'slug', 'is_personal', 'created_at'])
            ->withCount('members')
            ->orderByRaw('LOWER(name)')
            ->orderBy('id')
            ->paginate(15);

        return Inertia::render('directory/teams/index', [
            'teams' => $this->paginate($teams, fn (Team $team) => [
                'id' => $team->id,
                'name' => $team->name,
                'slug' => $team->slug,
                'isPersonal' => $team->is_personal,
                'createdAt' => $team->created_at?->toDateString(),
                'membersCount' => $team->members_count,
            ]),
        ]);
    }

    /**
     * Display a team and its public roster.
     */
    public function show(Team $team): Response
    {
        $team->load([
            'members' => fn (BelongsToMany $query) => $query
                ->select(['users.id', 'users.name'])
                ->orderByRaw('LOWER(users.name)')
                ->orderBy('users.id'),
        ]);

        return Inertia::render('directory/teams/show', [
            'team' => [
                'id' => $team->id,
                'name' => $team->name,
                'slug' => $team->slug,
                'isPersonal' => $team->is_personal,
                'createdAt' => $team->created_at?->toDateString(),
                'membersCount' => $team->members->count(),
                'members' => $team->members->map(fn (User $member) => [
                    'id' => $member->id,
                    'name' => $member->name,
                    'role' => $member->pivot->role->value,
                    'roleLabel' => $member->pivot->role->label(),
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
