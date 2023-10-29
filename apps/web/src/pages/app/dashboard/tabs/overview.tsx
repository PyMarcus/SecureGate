import { MembersList } from '@/components/members-list'
import { OverviewChart } from '@/components/overview-chart'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area'
import { LockKeyOpen, Users } from '@phosphor-icons/react'
import { Link } from 'react-router-dom'

export const Overview = () => {
  return (
    <section className="flex-1 flex flex-col gap-6 md:gap-8">
      <ScrollArea className="w-full">
        <div className="w-[calc(100vw-3rem)] flex items-center gap-6 md:gap-8">
          <Card className="w-full min-w-[12rem]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Members
              </CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                <span>1,234</span>
                <span className="text-sm font-medium">/1,500</span>
              </div>
              <p className="text-xs text-muted-foreground">
                Total members registered
              </p>
            </CardContent>
          </Card>
          <Card className="w-full min-w-[12rem]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Accesses
              </CardTitle>
              <LockKeyOpen className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                <span>1,234</span>
              </div>
              <p className="text-xs text-muted-foreground">
                Today&apos;s total gate accesses
              </p>
            </CardContent>
          </Card>
        </div>
        <ScrollBar orientation="horizontal" />
      </ScrollArea>

      <div
        className="grid flex-1 grid-rows-2 md:grid-rows-1 md:grid-cols-7 
      gap-6 md:gap-8"
      >
        <Card className="md:col-span-4">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Overview</CardTitle>
              <Button variant="link" asChild>
                <Link to="/dashboard/analytics">See more</Link>
              </Button>
            </div>
            <CardDescription>Last 24 hours gate accesses</CardDescription>
          </CardHeader>
          <CardContent>
            <OverviewChart />
          </CardContent>
        </Card>
        <Card className="md:col-span-3">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Last Accesses</CardTitle>
              <Button variant="link" asChild>
                <Link to="/dashboard/members">See all</Link>
              </Button>
            </div>
            <CardDescription>Last 10 gate accesses</CardDescription>
          </CardHeader>
          <CardContent>
            <MembersList />
          </CardContent>
        </Card>
      </div>
    </section>
  )
}
