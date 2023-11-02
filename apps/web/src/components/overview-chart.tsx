import { AccessHistory } from '@/@types/schemas/access-history'
import { ScrollArea } from '@/components/ui/scroll-area'
import { useEffect, useState } from 'react'
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis } from 'recharts'

interface ChartData {
  name: string
  value: number
}

interface BaseChartData {
  [key: string]: number
}

const BaseData: BaseChartData = {
  '06:00': 0,
  '07:00': 0,
  '08:00': 0,
  '09:00': 0,
  '10:00': 0,
  '11:00': 0,
  '12:00': 0,
  '13:00': 0,
  '14:00': 0,
  '15:00': 0,
  '16:00': 0,
  '17:00': 0,
  '18:00': 0,
  '19:00': 0,
  '20:00': 0,
  '21:00': 0,
  '22:00': 0,
  '23:00': 0,
}

interface OverviewChartProps {
  history: AccessHistory[]
}

export const OverviewChart = ({ history }: OverviewChartProps) => {
  const [chartData, setChartData] = useState<ChartData[]>([])
  useEffect(() => {
    if (history) {
      const data = history.reduce((acc, access) => {
        const date = new Date(access.when)
        const hour = `${date.getHours()}:00`

        acc[hour] && acc[hour]++

        return acc
      }, BaseData)

      setChartData(
        Object.entries(data).map(([name, value]) => ({ name, value })),
      )
    }
  }, [history])

  return (
    <ScrollArea className="w-full">
      <ResponsiveContainer height={310} width="100%">
        <BarChart data={chartData}>
          <XAxis
            dataKey="name"
            stroke="#888888"
            fontSize={12}
            tickLine={false}
            axisLine={false}
          />
          <YAxis
            stroke="#888888"
            fontSize={12}
            tickLine={false}
            axisLine={false}
          />
          <Bar dataKey="value" fill="#2563eb" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ScrollArea>
  )
}
