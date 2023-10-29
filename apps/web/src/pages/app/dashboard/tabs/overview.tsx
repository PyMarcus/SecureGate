import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area'
import { LockKeyOpen, Users } from '@phosphor-icons/react'

export const Overview = () => {
  return (
    <section className="flex-1">
      <ScrollArea className="w-full">
        <div className="w-[calc(100vw-3rem)] flex items-center gap-4">
          <Card className="w-full">
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
          <Card className="w-full">
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
                Today&apos;s total accesses
              </p>
            </CardContent>
          </Card>
        </div>
        <ScrollBar orientation="horizontal" />
      </ScrollArea>
    </section>
  )
}
