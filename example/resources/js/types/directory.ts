export type DirectoryPagination<T> = {
    data: T[];
    links: {
        previous: string | null;
        next: string | null;
    };
    meta: {
        currentPage: number;
        lastPage: number;
        perPage: number;
        total: number;
    };
};

export type DirectoryUser = {
    id: number;
    name: string;
    isVerified: boolean;
    joinedAt: string | null;
    teamsCount: number;
};

export type DirectoryTeam = {
    id: number;
    name: string;
    slug: string;
    isPersonal: boolean;
    createdAt: string | null;
    membersCount: number;
};

export type DirectoryMembership = {
    id: number;
    name: string;
    slug: string;
    isPersonal: boolean;
    role: 'owner' | 'admin' | 'member';
    roleLabel: string;
};

export type DirectoryUserProfile = Omit<DirectoryUser, 'teamsCount'> & {
    teams: DirectoryMembership[];
};

export type DirectoryMember = {
    id: number;
    name: string;
    role: 'owner' | 'admin' | 'member';
    roleLabel: string;
};

export type DirectoryTeamProfile = DirectoryTeam & {
    members: DirectoryMember[];
};
