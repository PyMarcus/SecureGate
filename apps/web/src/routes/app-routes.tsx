import { AppLayout } from '@/components/layouts/app-layout'
import { FullLayout } from '@/components/layouts/full-layout'
import { SessionLayout } from '@/components/layouts/session-layout'
import { Dashboard } from '@/pages/app/dashboard'
import { Admins } from '@/pages/app/dashboard/tabs/admins'
import { Analytics } from '@/pages/app/dashboard/tabs/analytics'
import { Overview } from '@/pages/app/dashboard/tabs/overview'
import { Users } from '@/pages/app/dashboard/tabs/users'
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
          <Route path="/sessao" element={<SessionLayout />}>
            <Route path="sign-in" element={<SignIn />} />
            <Route path="sign-up" element={<SignUp />} />
          </Route>

          <Route element={<PrivateRoutes />}>
            <Route element={<AppLayout />}>
              <Route path="/" element={<Navigate to="/painel/geral" />} />
              <Route path="/painel" element={<Navigate to="/painel/geral" />} />

              <Route path="/painel" element={<Dashboard />}>
                <Route index path="/painel/geral" element={<Overview />} />
                <Route path="/painel/graficos" element={<Analytics />} />
                <Route path="/painel/usuarios" element={<Users />} />

                <Route element={<PrivateRoutes enabledRole="ROOT" />}>
                  <Route path="/painel/admins" element={<Admins />} />
                </Route>
              </Route>

              <Route path="/perfil" element={<Profile />} />
            </Route>
          </Route>

          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
