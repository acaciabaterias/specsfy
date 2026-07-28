import { Head, Link, router } from '@inertiajs/react';
import { Search, UserRound } from 'lucide-react';
import { useState } from 'react';
import type { FormEvent } from 'react';
import Heading from '@/components/heading';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
    index as usersIndex,
    show as userShow,
} from '@/routes/directory/users';
import type { DirectoryPagination, DirectoryUser } from '@/types';

type Props = {
    users: DirectoryPagination<DirectoryUser>;
    filters: {
        q: string;
    };
};

function formatDate(date: string | null): string {
    return date
        ? new Intl.DateTimeFormat(undefined, { dateStyle: 'medium' }).format(
              new Date(`${date}T00:00:00`),
          )
        : 'Unknown';
}

export default function UserDirectoryIndex({ users, filters }: Props) {
    const [query, setQuery] = useState(filters.q);

    const search = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        router.get(usersIndex().url, query.trim() === '' ? {} : { q: query }, {
            preserveState: true,
            replace: true,
        });
    };

    const clearSearch = () => {
        setQuery('');
        router.get(
            usersIndex().url,
            {},
            { preserveState: true, replace: true },
        );
    };

    return (
        <>
            <Head title="User directory" />
            <h1 className="sr-only">User directory</h1>

            <div className="flex flex-col gap-6">
                <Heading
                    title="User directory"
                    description="Browse people across the application without exposing private contact or security data."
                />

                <form
                    className="flex flex-col gap-3 rounded-lg border bg-card p-4 sm:flex-row sm:items-end"
                    onSubmit={search}
                >
                    <div className="grid flex-1 gap-2">
                        <Label htmlFor="user-search">Search by name</Label>
                        <Input
                            id="user-search"
                            value={query}
                            maxLength={100}
                            onChange={(event) => setQuery(event.target.value)}
                            placeholder="e.g. Ana"
                        />
                    </div>
                    <div className="flex gap-2">
                        <Button type="submit">
                            <Search />
                            Search
                        </Button>
                        {filters.q ? (
                            <Button
                                type="button"
                                variant="outline"
                                onClick={clearSearch}
                            >
                                Clear
                            </Button>
                        ) : null}
                    </div>
                </form>

                <section className="overflow-hidden rounded-lg border bg-card">
                    <div className="flex items-center justify-between gap-4 border-b px-4 py-3">
                        <p className="text-sm text-muted-foreground">
                            {users.meta.total}{' '}
                            {users.meta.total === 1 ? 'person' : 'people'}
                        </p>
                        <p className="text-sm text-muted-foreground">
                            Page {users.meta.currentPage} of{' '}
                            {users.meta.lastPage}
                        </p>
                    </div>

                    {users.data.length === 0 ? (
                        <div className="flex flex-col items-center gap-2 px-4 py-12 text-center">
                            <UserRound className="size-8 text-muted-foreground" />
                            <p className="font-medium">No users found</p>
                            <p className="text-sm text-muted-foreground">
                                {filters.q
                                    ? 'Try a different name.'
                                    : 'There are no accounts to display.'}
                            </p>
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-muted/50 text-muted-foreground">
                                    <tr>
                                        <th
                                            scope="col"
                                            className="px-4 py-3 font-medium"
                                        >
                                            Name
                                        </th>
                                        <th
                                            scope="col"
                                            className="px-4 py-3 font-medium"
                                        >
                                            Status
                                        </th>
                                        <th
                                            scope="col"
                                            className="px-4 py-3 font-medium"
                                        >
                                            Teams
                                        </th>
                                        <th
                                            scope="col"
                                            className="px-4 py-3 font-medium"
                                        >
                                            Joined
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y">
                                    {users.data.map((user) => (
                                        <tr key={user.id}>
                                            <td className="px-4 py-3 font-medium">
                                                <Link
                                                    href={userShow(user.id)}
                                                    className="underline-offset-4 hover:underline focus-visible:underline"
                                                    prefetch
                                                >
                                                    {user.name}
                                                </Link>
                                            </td>
                                            <td className="px-4 py-3">
                                                <Badge
                                                    variant={
                                                        user.isVerified
                                                            ? 'secondary'
                                                            : 'outline'
                                                    }
                                                >
                                                    {user.isVerified
                                                        ? 'Verified'
                                                        : 'Unverified'}
                                                </Badge>
                                            </td>
                                            <td className="px-4 py-3">
                                                {user.teamsCount}
                                            </td>
                                            <td className="px-4 py-3 text-muted-foreground">
                                                {formatDate(user.joinedAt)}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </section>

                <nav
                    aria-label="User directory pagination"
                    className="flex items-center justify-between"
                >
                    {users.links.previous ? (
                        <Button variant="outline" asChild>
                            <Link href={users.links.previous} preserveScroll>
                                Previous
                            </Link>
                        </Button>
                    ) : (
                        <Button variant="outline" disabled>
                            Previous
                        </Button>
                    )}
                    {users.links.next ? (
                        <Button variant="outline" asChild>
                            <Link href={users.links.next} preserveScroll>
                                Next
                            </Link>
                        </Button>
                    ) : (
                        <Button variant="outline" disabled>
                            Next
                        </Button>
                    )}
                </nav>
            </div>
        </>
    );
}

UserDirectoryIndex.layout = {
    breadcrumbs: [
        {
            title: 'Users',
            href: usersIndex(),
        },
    ],
};
