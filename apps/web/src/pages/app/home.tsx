import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'

export const Home = () => {
  return (
    <section className="flex-1 flex flex-col gap-6 md:gap-8">
      <div className="flex flex-col gap-6 md:gap-8 bg-background">
        <header className="flex items-center justify-between flex-wrap">
          <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        </header>

        <Tabs defaultValue="logs" className="">
          <TabsList className="w-full sm:w-auto justify-start flex-wrap h-auto">
            <TabsTrigger value="logs" className="flex-1">
              Logs
            </TabsTrigger>
            <TabsTrigger value="users" className="flex-1" disabled>
              Users
            </TabsTrigger>
            <TabsTrigger value="analytics" className="flex-1" disabled>
              Analytics
            </TabsTrigger>
          </TabsList>
        </Tabs>
      </div>
      <div className="flex-1"></div>
    </section>
  )
}
