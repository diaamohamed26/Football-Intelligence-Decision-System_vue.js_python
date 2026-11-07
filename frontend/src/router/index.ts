import { createRouter, createWebHistory } from 'vue-router'

import PublicLayout from '@/layouts/PublicLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'

// =============================================================
// PUBLIC VIEWS
// =============================================================

import Home from '@/views/Home.vue'
import Live from '@/views/Live.vue'
import Matches from '@/views/Matches.vue'
import MatchDetails from '@/views/MatchDetails.vue'
import Competitions from '@/views/Competitions.vue'
import Teams from '@/views/Teams.vue'
import TeamDetails from '@/views/TeamDetails.vue'
import Players from '@/views/Players.vue'
import PlayerDetails from '@/views/PlayerDetails.vue'
import Intelligence from '@/views/Intelligence.vue'
import Scouting from '@/views/Scouting.vue'
import News from '@/views/News.vue'
import FidsAI from '@/views/FidsAI.vue'
import Search from '@/views/Search.vue'

// =============================================================
// AUTH VIEWS
// =============================================================

import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'
import ForgotPassword from '@/views/auth/ForgotPassword.vue'
import ResetPassword from '@/views/auth/ResetPassword.vue'
import VerifyEmail from '@/views/auth/VerifyEmail.vue'

// =============================================================
// ACCOUNT VIEWS
// =============================================================

import Profile from '@/views/account/Profile.vue'
import Favorites from '@/views/account/Favorites.vue'
import Alerts from '@/views/account/Alerts.vue'
import Settings from '@/views/account/Settings.vue'

// =============================================================
// ADMIN VIEWS
// =============================================================

import AdminDashboard from '@/views/admin/Dashboard.vue'
import AdminUsers from '@/views/admin/Users.vue'
import AdminUserDetails from '@/views/admin/UserDetails.vue'
import AdminUserProfile from '@/views/admin/UserProfile.vue'
import AdminMatches from '@/views/admin/Matches.vue'
import AdminTeams from '@/views/admin/Teams.vue'
import AdminPlayers from '@/views/admin/Players.vue'
import AdminCompetitions from '@/views/admin/Competitions.vue'
import AdminNews from '@/views/admin/News.vue'
import AdminScouting from '@/views/admin/Scouting.vue'
import AdminIntelligence from '@/views/admin/Intelligence.vue'
import AdminSettings from '@/views/admin/Settings.vue'

// =============================================================
// 404
// =============================================================

import NotFound from '@/views/NotFound.vue'

// =============================================================
// AUTH TYPES & HELPERS
// =============================================================

interface StoredUser {
  id?: number | string
  username?: string
  name?: string
  email?: string
  role?: string
  is_admin?: boolean
  isAdmin?: boolean
  is_staff?: boolean
  is_superuser?: boolean
  is_active?: boolean
}

interface StoredAuth {
  token: string | null
  user: StoredUser | null
}

function getStoredAuth(): StoredAuth {
  // Check both storage locations because the login form may
  // use localStorage or sessionStorage depending on "Remember me".
  const storages: Storage[] = [localStorage, sessionStorage]

  const tokenKeys = [
    'fids_access_token',
    'access',
    'access_token',
    'accessToken',
    'token',
  ]

  for (const storage of storages) {
    const tokenKey = tokenKeys.find((key) => storage.getItem(key))
    if (!tokenKey) continue

    const token = storage.getItem(tokenKey)
    const userRaw =
      storage.getItem('fids_user') || storage.getItem('user')

    try {
      const user: StoredUser | null = userRaw
        ? JSON.parse(userRaw)
        : null

      return { token, user }
    } catch {
      return { token, user: null }
    }
  }

  return { token: null, user: null }
}

function isAdminUser(user: StoredUser | null): boolean {
  if (!user) return false

  return (
    user.role?.toLowerCase() === 'admin' ||
    user.is_admin === true ||
    user.isAdmin === true ||
    user.is_staff === true ||
    user.is_superuser === true
  )
}

function getUserHome(user: StoredUser | null): string {
  return isAdminUser(user)
    ? '/admin/dashboard'
    : '/account/profile'
}

// =============================================================
// ROUTER
// =============================================================

const router = createRouter({
  history: createWebHistory(),

  routes: [
    // =========================================================
    // PUBLIC WEBSITE
    // =========================================================

    {
      path: '/',
      component: PublicLayout,

      children: [
        {
          path: '',
          name: 'home',
          component: Home,
          meta: {
            title: 'FIDS — Football Intelligence Decision System',
          },
        },
        {
          path: 'live',
          name: 'live',
          component: Live,
          meta: {
            title: 'Live Matches — FIDS',
          },
        },
        {
          path: 'matches',
          name: 'matches',
          component: Matches,
          meta: {
            title: 'Matches — FIDS',
          },
        },
        {
          path: 'matches/:id',
          name: 'match-details',
          component: MatchDetails,
          meta: {
            title: 'Match Details — FIDS',
          },
        },
        {
          path: 'competitions',
          name: 'competitions',
          component: Competitions,
          meta: {
            title: 'Competitions — FIDS',
          },
        },
        {
          path: 'teams',
          name: 'teams',
          component: Teams,
          meta: {
            title: 'Teams — FIDS',
          },
        },
        {
          path: 'teams/:id',
          name: 'team-details',
          component: TeamDetails,
          meta: {
            title: 'Team Details — FIDS',
          },
        },
        {
          path: 'players',
          name: 'players',
          component: Players,
          meta: {
            title: 'Players — FIDS',
          },
        },
        {
          path: 'players/:id',
          name: 'player-details',
          component: PlayerDetails,
          meta: {
            title: 'Player Details — FIDS',
          },
        },
        {
          path: 'intelligence',
          name: 'intelligence',
          component: Intelligence,
          meta: {
            title: 'Football Intelligence — FIDS',
          },
        },
        {
          path: 'scouting',
          name: 'scouting',
          component: Scouting,
          meta: {
            title: 'AI Scouting — FIDS',
          },
        },
        {
          path: 'news',
          name: 'news',
          component: News,
          meta: {
            title: 'Football News — FIDS',
          },
        },
        {
          path: 'search',
          name: 'search',
          component: Search,
          meta: {
            title: 'Search — FIDS',
          },
        },
        {
          path: 'ai',
          name: 'fids-ai',
          component: FidsAI,
          meta: {
            title: 'FIDS AI — Football Intelligence',
          },
        },

        // -----------------------------------------------------
        // ACCOUNT — AUTHENTICATED USERS
        // -----------------------------------------------------

        {
          path: 'account/profile',
          name: 'profile',
          component: Profile,
          meta: {
            title: 'My Profile — FIDS',
            requiresAuth: true,
          },
        },
        {
          path: 'account/favorites',
          name: 'favorites',
          component: Favorites,
          meta: {
            title: 'My Favorites — FIDS',
            requiresAuth: true,
          },
        },
        {
          path: 'account/alerts',
          name: 'alerts',
          component: Alerts,
          meta: {
            title: 'My Alerts — FIDS',
            requiresAuth: true,
          },
        },
        {
          path: 'account/settings',
          name: 'settings',
          component: Settings,
          meta: {
            title: 'Settings — FIDS',
            requiresAuth: true,
          },
        },
      ],
    },

    // =========================================================
    // AUTHENTICATION — SEPARATE AUTH LAYOUT
    // =========================================================

    {
      path: '/auth',
      component: AuthLayout,

      children: [
        {
          path: 'login',
          name: 'login',
          component: Login,
          meta: {
            title: 'Login — FIDS',
            guestOnly: true,
          },
        },
        {
          path: 'register',
          name: 'register',
          component: Register,
          meta: {
            title: 'Create Account — FIDS',
            guestOnly: true,
          },
        },
        {
          path: 'forgot-password',
          name: 'forgot-password',
          component: ForgotPassword,
          meta: {
            title: 'Forgot Password — FIDS',
            guestOnly: true,
          },
        },
        {
          path: 'reset-password',
          name: 'reset-password',
          component: ResetPassword,
          meta: {
            title: 'Reset Password — FIDS',
            guestOnly: true,
          },
        },
        {
          path: 'verify-email',
          name: 'verify-email',
          component: VerifyEmail,
          meta: {
            title: 'Verify Email — FIDS',
          },
        },
      ],
    },

    // =========================================================
    // ADMIN PANEL — ADMIN ONLY
    // =========================================================

    {
      path: '/admin',
      component: AdminLayout,

      meta: {
        requiresAuth: true,
        requiresAdmin: true,
      },

      children: [
        {
          path: '',
          redirect: { name: 'admin-dashboard' },
        },

        // DASHBOARD
        {
          path: 'dashboard',
          name: 'admin-dashboard',
          component: AdminDashboard,
          meta: {
            title: 'Admin Dashboard — FIDS',
          },
        },

        // USERS
        {
          path: 'users',
          name: 'admin-users',
          component: AdminUsers,
          meta: {
            title: 'Users Management — FIDS',
          },
        },
        {
          path: 'users/:id',
          name: 'admin-user-details',
          component: AdminUserDetails,
          meta: {
            title: 'User Details — FIDS',
          },
        },
        {
          path: 'users/:id/profile',
          name: 'admin-user-profile',
          component: AdminUserProfile,
          meta: {
            title: 'User Profile — FIDS',
          },
        },

        // FOOTBALL MANAGEMENT
        {
          path: 'matches',
          name: 'admin-matches',
          component: AdminMatches,
          meta: {
            title: 'Manage Matches — FIDS',
          },
        },
        {
          path: 'teams',
          name: 'admin-teams',
          component: AdminTeams,
          meta: {
            title: 'Manage Teams — FIDS',
          },
        },
        {
          path: 'players',
          name: 'admin-players',
          component: AdminPlayers,
          meta: {
            title: 'Manage Players — FIDS',
          },
        },
        {
          path: 'competitions',
          name: 'admin-competitions',
          component: AdminCompetitions,
          meta: {
            title: 'Manage Competitions — FIDS',
          },
        },
        {
          path: 'news',
          name: 'admin-news',
          component: AdminNews,
          meta: {
            title: 'Manage News — FIDS',
          },
        },

        // INTELLIGENCE
        {
          path: 'scouting',
          name: 'admin-scouting',
          component: AdminScouting,
          meta: {
            title: 'Scouting Management — FIDS',
          },
        },
        {
          path: 'intelligence',
          name: 'admin-intelligence',
          component: AdminIntelligence,
          meta: {
            title: 'Intelligence Management — FIDS',
          },
        },

        // SETTINGS
        {
          path: 'settings',
          name: 'admin-settings',
          component: AdminSettings,
          meta: {
            title: 'Admin Settings — FIDS',
          },
        },
      ],
    },

    // =========================================================
    // 404
    // =========================================================

    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: NotFound,
      meta: {
        title: 'Page Not Found — FIDS',
      },
    },
  ],

  // ===========================================================
  // SCROLL BEHAVIOR
  // ===========================================================

  scrollBehavior(to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }

    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      }
    }

    return {
      top: 0,
      behavior: 'smooth',
    }
  },
})

// =============================================================
// PAGE TITLE
// =============================================================

router.afterEach((to) => {
  const title = to.meta.title

  if (typeof title === 'string') {
    document.title = title
  }
})

// =============================================================
// NAVIGATION GUARD
// =============================================================

router.beforeEach((to) => {
  const { token, user } = getStoredAuth()
  const isAuthenticated = Boolean(token)
  const isAdmin = isAdminUser(user)

  // Redirect guests to login when accessing protected pages.
  if (to.meta.requiresAuth && !isAuthenticated) {
    return {
      name: 'login',
      query: {
        redirect: to.fullPath,
      },
    }
  }

  // Admin routes require both a token and an admin role.
  if (to.meta.requiresAdmin) {
    if (!isAuthenticated) {
      return {
        name: 'login',
        query: {
          redirect: to.fullPath,
        },
      }
    }

    if (!isAdmin) {
      return { name: 'profile' }
    }
  }

  // Logged-in users should not revisit guest-only pages.
  if (to.meta.guestOnly && isAuthenticated) {
    return getUserHome(user)
  }

  return true
})

// =============================================================
// EXPORT
// =============================================================

export default router
