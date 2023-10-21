import { FullLayout } from '@/components/layouts/full-layout'
import { SessionLayout } from '@/components/layouts/session-layout'
import { Home } from '@/pages/app/home'
import { NotFound } from '@/pages/common/not-found'
import { SignIn } from '@/pages/session/sign-in'
import { SignUp } from '@/pages/session/sign-up'
import { PrivateRoutes } from '@/routes/private-routes'
import { BrowserRouter, Route, Routes } from 'react-router-dom'

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
            <Route path="/" element={<Home />} />
          </Route>

          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
