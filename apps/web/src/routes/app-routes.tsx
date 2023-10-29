import { AppLayout } from '@/components/layouts/app-layout'
import { FullLayout } from '@/components/layouts/full-layout'
import { SessionLayout } from '@/components/layouts/session-layout'
import { Dashboard } from '@/pages/app/dashboard'
import { Analytics } from '@/pages/app/dashboard/tabs/analytics'
import { Members } from '@/pages/app/dashboard/tabs/members'
import { Overview } from '@/pages/app/dashboard/tabs/overview'
import { Users } from '@/pages/app/dashboard/tabs/users'
import { Preferences } from '@/pages/app/preferences'
import { Profile } from '@/pages/app/profile'
import { NotFound } from '@/pages/common/not-found'
import { SignIn } from '@/pages/session/sign-in'
import { SignUp } from '@/pages/session/sign-up'
import { PrivateRoutes } from '@/routes/private-routes'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'

export const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<FullLayout />}>
          <Route path="/session" element={<SessionLayout />}>
            <Route path="sign-in" element={<SignIn />} />
            <Route path="sign-up" element={<SignUp />} />
          </Route>

          <Route element={<PrivateRoutes />}>
            <Route element={<AppLayout />}>
              <Route path="/" element={<Navigate to="/dashboard/overview" />} />
              <Route
                path="/dashboard"
                element={<Navigate to="/dashboard/overview" />}
              />

              <Route path="/dashboard" element={<Dashboard />}>
                <Route
                  index
                  path="/dashboard/overview"
                  element={<Overview />}
                />
                <Route path="/dashboard/analytics" element={<Analytics />} />
                <Route path="/dashboard/members" element={<Members />} />

                <Route element={<PrivateRoutes enabledRole="ROOT" />}>
                  <Route path="/dashboard/users" element={<Users />} />
                </Route>
              </Route>

              <Route path="/preferences" element={<Preferences />} />

              <Route path="/profile" element={<Profile />} />
            </Route>
          </Route>

          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
