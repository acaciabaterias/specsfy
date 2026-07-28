<?php

use App\Models\User;
use Inertia\Testing\AssertableInertia as Assert;

// SPECSFY: FR-001 FR-002 FR-003 NFR-001 NFR-002 AC-001
test('authenticated people can browse a private paginated user directory', function () {
    $viewer = User::factory()->create(['name' => 'Viewer']);

    foreach (range(1, 15) as $number) {
        User::factory()->create([
            'name' => sprintf('User %02d', $number),
            'email' => sprintf('user-%02d@example.test', $number),
        ]);
    }

    $this
        ->actingAs($viewer)
        ->get(route('directory.users.index'))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->component('directory/users/index')
            ->has('users.data', 15)
            ->where('users.data.0.name', 'User 01')
            ->where('users.data.0.isVerified', true)
            ->where('users.data.0.teamsCount', 1)
            ->where('users.data.0.joinedAt', fn ($date) => is_string($date))
            ->missing('users.data.0.email')
            ->where('users.meta.total', 16)
            ->where('users.meta.perPage', 15)
            ->where('users.meta.currentPage', 1)
            ->where('users.links.previous', null)
            ->where('filters.q', ''),
        );

    $this
        ->actingAs($viewer)
        ->get(route('directory.users.index', ['page' => 2]))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->has('users.data', 1)
            ->where('users.data.0.name', 'Viewer')
            ->missing('users.data.0.email'),
        );
});

test('guests cannot browse the user directory', function () {
    $this
        ->get(route('directory.users.index'))
        ->assertRedirect(route('login'));
});
