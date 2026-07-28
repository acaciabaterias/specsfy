import { Head, Link } from '@inertiajs/react';
import { UsersRound } from 'lucide-react';
import Heading from '@/components/heading';
import { Badge } from '@/components/ui/badge';
import {
    index as teamsIndex,
    show as teamShow,
} from '@/routes/directory/teams';
import { show as userShow } from '@/routes/directory/users';
import type { DirectoryTeamProfile } from '@/types';

type Props = {
    team: DirectoryTeamProfile;
};

function formatDate(date: string | null): string {
    return date
        ? new Intl.DateTimeFormat(undefined, { dateStyle: 'long' }).format(
              new Date(`${date}T00:00:00`),
          )
        : 'Unknown';
}

export default function TeamDirectoryShow({ team }: Props) {
    return (
        <>
            <Head title={team.name} />
            <h1 className="sr-only">{team.name}</h1>

            <div className="flex flex-col gap-8">
                <section className="rounded-lg border bg-card p-6">
                    <div className="flex flex-col justify-between gap-4 sm:flex-row">
                        <Heading
                            title={team.name}
                            description="Public team directory profile"
                        />
                        <Badge
                            variant={team.isPersonal ? 'outline' : 'secondary'}
                        >
                            {team.isPersonal ? 'Personal team' : 'Shared team'}
                        </Badge>
                    </div>
                    <dl className="grid gap-4 sm:grid-cols-2">
                        <div>
                            <dt className="text-sm text-muted-foreground">
                                Members
                            </dt>
                            <dd className="mt-1 font-medium">
                                {team.membersCount}
                            </dd>
                        </div>
                        <div>
                            <dt className="text-sm text-muted-foreground">
                                Created
                            </dt>
                            <dd className="mt-1 font-medium">
                                {formatDate(team.createdAt)}
                            </dd>
                        </div>
                    </dl>
                </section>

                <section className="flex flex-col gap-4">
                    <Heading
                        variant="small"
                        title="Team members"
                        description="Roles apply only within this team."
                    />

                    {team.members.length === 0 ? (
                        <div className="flex flex-col items-center gap-2 rounded-lg border px-4 py-12 text-center">
                            <UsersRound className="size-8 text-muted-foreground" />
                            <p className="font-medium">
                                No members in this team
                            </p>
                        </div>
                    ) : (
                        <div className="overflow-hidden rounded-lg border bg-card">
                            <div className="overflow-x-auto">
                                <table className="w-full text-left text-sm">
                                    <thead className="bg-muted/50 text-muted-foreground">
                                        <tr>
                                            <th
                                                scope="col"
                                                className="px-4 py-3 font-medium"
                                            >
                                                Member
                                            </th>
                                            <th
                                                scope="col"
                                                className="px-4 py-3 font-medium"
                                            >
                                                Role in this team
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y">
                                        {team.members.map((member) => (
                                            <tr key={member.id}>
                                                <td className="px-4 py-3 font-medium">
                                                    <Link
                                                        href={userShow(
                                                            member.id,
                                                        )}
                                                        className="underline-offset-4 hover:underline focus-visible:underline"
                                                        prefetch
                                                    >
                                                        {member.name}
                                                    </Link>
                                                </td>
                                                <td className="px-4 py-3">
                                                    <Badge variant="secondary">
                                                        {member.roleLabel}
                                                    </Badge>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    )}
                </section>
            </div>
        </>
    );
}

TeamDirectoryShow.layout = (props: Props) => ({
    breadcrumbs: [
        {
            title: 'Teams',
            href: teamsIndex(),
        },
        {
            title: props.team.name,
            href: teamShow(props.team.slug),
        },
    ],
});
