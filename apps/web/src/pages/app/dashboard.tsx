import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

export const Dashboard = () => {
  return (
    <section className="flex-1 flex flex-col gap-6 md:gap-8 bg-background">
      <header className="flex items-center justify-between flex-wrap">
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
      </header>

      <Tabs defaultValue="overview" className="flex flex-1 flex-col">
        <TabsList className="w-full sm:w-auto justify-start flex-wrap h-auto self-start">
          <TabsTrigger value="overview" className="flex-1">
            Overview
          </TabsTrigger>
          <TabsTrigger value="users" className="flex-1" disabled>
            Users
          </TabsTrigger>
          <TabsTrigger value="analytics" className="flex-1" disabled>
            Analytics
          </TabsTrigger>
        </TabsList>

        <TabsContent
          value="overview"
          className="flex-1 flex flex-col gap-4 justify-between"
        >
          {/* <ul className=""></ul>

          <div className="grid gap-4 grid-rows-2 md:grid-rows-1 md:grid-cols-7 ">
            <Card className="col-span-3">
              <CardHeader>
                <CardTitle>Recent activity</CardTitle>
                <CardDescription>
                  Last update: <span className="font-bold">2 min ago</span>
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-center text-4xl font-bold">265</p>
              </CardContent>
            </Card>
            <Card className="col-span-4">
              <CardHeader>
                <CardTitle>Overview</CardTitle>
              </CardHeader>
              <CardContent className="pl-2">
                <ScrollArea>
                  <Overview />
                </ScrollArea>
              </CardContent>
            </Card>
          </div> */}
        </TabsContent>
      </Tabs>
    </section>
  )
}
