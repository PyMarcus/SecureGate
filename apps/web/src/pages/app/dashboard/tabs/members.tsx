import { Member } from '@/@types/schemas/member'
import { MembersTable } from '@/components/members-table'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area'
import { IdentificationCard, LockKeyOpen, Users } from '@phosphor-icons/react'
import { useRef, useState } from 'react'

export const Members = () => {
  const [selectedMember, setSelectedMember] = useState<Member | null>(null)

  const memberHistoryRef = useRef<HTMLHeadingElement | null>(null)

  const handleSelectMember = (member: Member) => {
    if (member.id === selectedMember?.id) {
      return setSelectedMember(null)
    }

    setSelectedMember(member)
    if (memberHistoryRef.current) {
      memberHistoryRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return (
    <section className="flex-1 flex flex-col gap-6 md:gap-8 ">
      <ScrollArea className="w-full">
        <div className="w-[calc(100vw-3rem)] flex gap-6 md:gap-8 items-stretch">
          <Card className="w-full min-w-[12rem]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Members
              </CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                <span>1,500</span>
              </div>
              <p className="text-xs text-muted-foreground">
                Total members registered
              </p>
            </CardContent>
          </Card>

          <Card className="w-full min-w-[12rem]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Authorized Members
              </CardTitle>
              <IdentificationCard className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                <span>1,234</span>
                <span className="text-sm font-medium">/1,500</span>
              </div>
              <p className="text-xs text-muted-foreground">
                Total members able to open the gate
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
            <CardTitle>Members</CardTitle>
            <CardDescription className="mt-0">
              All members registered
            </CardDescription>
          </CardHeader>
          <CardContent>
            <MembersTable
              selectedMember={selectedMember}
              onSelectMember={handleSelectMember}
            />
          </CardContent>
        </Card>
        <Card className="md:col-span-3">
          <CardHeader>
            <CardTitle ref={memberHistoryRef}>Member history</CardTitle>
            <CardDescription className="mt-0">
              Member access history
            </CardDescription>
          </CardHeader>
          <CardContent>
            {selectedMember ? (
              <p>
                {selectedMember.name} - {selectedMember.email}
              </p>
            ) : (
              <p>No member selected</p>
            )}
          </CardContent>
        </Card>
      </div>
    </section>
  )
}
