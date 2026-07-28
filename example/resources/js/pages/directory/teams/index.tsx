import { Head, Link } from '@inertiajs/react';
import { Building2 } from 'lucide-react';
import Heading from '@/components/heading';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
    index as teamsIndex,
    show as teamShow,
} from '@/routes/directory/teams';
import type { DirectoryPagination, DirectoryTeam } from '@/types';

type Props = {
    teams: DirectoryPagination<DirectoryTeam>;
};

function formatDate(date: string | null): string {
    return date
        ? new Intl.DateTimeFormat(undefined, { dateStyle: 'medium' }).format(
              new Date(`${date}T00:00:00`),
          )
        : 'Unknown';
}

export default function TeamDirectoryIndex({ teams }: Props) {
    return (
        <>
            <Head title="Team directory" />
            <h1 className="sr-only">Team directory</h1>

            <div className="flex flex-col gap-6">
                <Heading
                    title="Team directory"
                    description="Browse active personal and shared teams across the application."
                />

                <section className="overflow-hidden rounded-lg border bg-card">
                    <div className="flex items-center justify-between gap-4 border-b px-4 py-3">
                        <p className="text-sm text-muted-foreground">
                            {teams.meta.total}{' '}
                            {teams.meta.total === 1 ? 'team' : 'teams'}
                        </p>
                        <p className="text-sm text-muted-foreground">
                            Page {teams.meta.currentPage} of{' '}
                            {teams.meta.lastPage}
                        </p>
                    </div>

                    {teams.data.length === 0 ? (
                        <div className="flex flex-col items-center gap-2 px-4 py-12 text-center">
                            <Building2 className="size-8 text-muted-foreground" />
                            <p className="font-medium">No teams found</p>
                            <p className="text-sm text-muted-foreground">
                                There are no active teams to display.
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
                                            Team
                                        </th>
                                        <th
                                            scope="col"
                                            className="px-4 py-3 font-medium"
                                        >
                                            Type
                                        </th>
                                        <th
                                            scope="col"
                                            className="px-4 py-3 font-medium"
                                        >
                                            Members
                                        </th>
                                        <th
                                            scope="col"
                                            className="px-4 py-3 font-medium"
                                        >
                                            Created
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y">
                                    {teams.data.map((team) => (
                                        <tr key={team.id}>
                                            <td className="px-4 py-3 font-medium">
                                                <Link
                                                    href={teamShow(team.slug)}
                                                    className="underline-offset-4 hover:underline focus-visible:underline"
                                                    prefetch
                                                >
                                                    {team.name}
                                                </Link>
                                            </td>
                                            <td className="px-4 py-3">
                                                <Badge
                                                    variant={
                                                        team.isPersonal
                                                            ? 'outline'
                                                            : 'secondary'
                                                    }
                                                >
                                                    {team.isPersonal
                                                        ? 'Personal'
                                                        : 'Shared'}
                                                </Badge>
                                            </td>
                                            <td className="px-4 py-3">
                                                {team.membersCount}
                                            </td>
                                            <td className="px-4 py-3 text-muted-foreground">
                                                {formatDate(team.createdAt)}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </section>

                <nav
                    aria-label="Team directory pagination"
                    className="flex items-center justify-between"
                >
                    {teams.links.previous ? (
                        <Button variant="outline" asChild>
                            <Link href={teams.links.previous} preserveScroll>
                                Previous
                            </Link>
                        </Button>
                    ) : (
                        <Button variant="outline" disabled>
                            Previous
                        </Button>
                    )}
                    {teams.links.next ? (
                        <Button variant="outline" asChild>
                            <Link href={teams.links.next} preserveScroll>
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

TeamDirectoryIndex.layout = {
    breadcrumbs: [
        {
            title: 'Teams',
            href: teamsIndex(),
        },
    ],
};
