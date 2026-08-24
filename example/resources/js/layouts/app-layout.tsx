/**
 * Compõe o shell autenticado e injeta a equipe ativa na trilha de navegação.
 * O componente Breadcrumbs continua pertencendo ao layout filho existente.
 */
import { usePage } from '@inertiajs/react';
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout';
import { dashboard } from '@/routes';
import type { BreadcrumbItem } from '@/types';
import type { Team } from '@/types/teams';

export default function AppLayout({
    breadcrumbs = [],
    children,
}: {
    breadcrumbs?: BreadcrumbItem[];
    children: React.ReactNode;
}) {
    const { currentTeam } = usePage<{ currentTeam: Team | null }>().props;
    const teamBreadcrumb: BreadcrumbItem | null = currentTeam
        ? {
              title: currentTeam.name,
              href: dashboard(currentTeam.slug),
          }
        : null;
    const breadcrumbsWithTeam: BreadcrumbItem[] =
        teamBreadcrumb &&
        !breadcrumbs.some((item) => item.title === teamBreadcrumb.title)
            ? [teamBreadcrumb, ...breadcrumbs]
            : breadcrumbs;

    return (
        <AppLayoutTemplate breadcrumbs={breadcrumbsWithTeam}>
            {children}
        </AppLayoutTemplate>
    );
}
