import { FullLayout } from '@/components/layouts/full-layout'
import { Home } from '@/pages/app/home'
import { NotFound } from '@/pages/common/not-found'
import { PrivateRoutes } from '@/routes/private-routes'
import { BrowserRouter, Route, Routes } from 'react-router-dom'

export const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<FullLayout />}>
          <Route element={<PrivateRoutes />}></Route>

          <Route path="/" element={<Home />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
