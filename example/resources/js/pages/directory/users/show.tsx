import { Head, Link } from '@inertiajs/react';
import { UsersRound } from 'lucide-react';
import Heading from '@/components/heading';
import { Badge } from '@/components/ui/badge';
import { show as teamShow } from '@/routes/directory/teams';
import {
    index as usersIndex,
    show as userShow,
} from '@/routes/directory/users';
import type { DirectoryUserProfile } from '@/types';

type Props = {
    user: DirectoryUserProfile;
};

function formatDate(date: string | null): string {
    return date
        ? new Intl.DateTimeFormat(undefined, { dateStyle: 'long' }).format(
              new Date(`${date}T00:00:00`),
          )
        : 'Unknown';
}

export default function UserDirectoryShow({ user }: Props) {
    return (
        <>
            <Head title={user.name} />
            <h1 className="sr-only">{user.name}</h1>

            <div className="flex flex-col gap-8">
                <section className="rounded-lg border bg-card p-6">
                    <Heading
                        title={user.name}
                        description="Public directory profile"
                    />
                    <dl className="grid gap-4 sm:grid-cols-3">
                        <div>
                            <dt className="text-sm text-muted-foreground">
                                Status
                            </dt>
                            <dd className="mt-1">
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
                            </dd>
                        </div>
                        <div>
                            <dt className="text-sm text-muted-foreground">
                                Joined
                            </dt>
                            <dd className="mt-1 font-medium">
                                {formatDate(user.joinedAt)}
                            </dd>
                        </div>
                        <div>
                            <dt className="text-sm text-muted-foreground">
                                Teams
                            </dt>
                            <dd className="mt-1 font-medium">
                                {user.teams.length}
                            </dd>
                        </div>
                    </dl>
                </section>

                <section className="flex flex-col gap-4">
                    <Heading
                        variant="small"
                        title="Team memberships"
                        description="Roles are specific to each team."
                    />

                    {user.teams.length === 0 ? (
                        <div className="flex flex-col items-center gap-2 rounded-lg border px-4 py-12 text-center">
                            <UsersRound className="size-8 text-muted-foreground" />
                            <p className="font-medium">No teams linked</p>
                        </div>
                    ) : (
                        <div className="grid gap-3 md:grid-cols-2">
                            {user.teams.map((team) => (
                                <Link
                                    key={team.id}
                                    href={teamShow(team.slug)}
                                    className="flex items-center justify-between gap-4 rounded-lg border bg-card p-4 transition-colors hover:bg-accent focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none"
                                    prefetch
                                >
                                    <div>
                                        <p className="font-medium">
                                            {team.name}
                                        </p>
                                        <p className="text-sm text-muted-foreground">
                                            {team.isPersonal
                                                ? 'Personal team'
                                                : 'Shared team'}
                                        </p>
                                    </div>
                                    <Badge variant="secondary">
                                        {team.roleLabel}
                                    </Badge>
                                </Link>
                            ))}
                        </div>
                    )}
                </section>
            </div>
        </>
    );
}

UserDirectoryShow.layout = (props: Props) => ({
    breadcrumbs: [
        {
            title: 'Users',
            href: usersIndex(),
        },
        {
            title: props.user.name,
            href: userShow(props.user.id),
        },
    ],
});
