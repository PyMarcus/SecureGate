import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis } from 'recharts'
import { ScrollArea } from './ui/scroll-area'

const week_data = [
  {
    name: '06:00 AM',
    value: Math.floor(Math.random() * 300) + 100,
  },
  {
    name: '07:00 AM',
    value: Math.floor(Math.random() * 300) + 100,
  },
  {
    name: '08:00 AM',
    value: Math.floor(Math.random() * 300) + 100,
  },
  {
    name: '09:00 AM',
    value: Math.floor(Math.random() * 300) + 100,
  },
  {
    name: '10:00 AM',
    value: Math.floor(Math.random() * 300) + 100,
  },
  {
    name: '11:00 AM',
    value: Math.floor(Math.random() * 300) + 100,
  },
  {
    name: '12:00 AM',
    value: Math.floor(Math.random() * 300) + 100,
  },
  {
    name: '01:00 PM',
    value: Math.floor(Math.random() * 300) + 100,
  },
  {
    name: '02:00 PM',
    value: Math.floor(Math.random() * 300) + 100,
  },
  {
    name: '03:00 PM',
    value: Math.floor(Math.random() * 300) + 100,
  },
  {
    name: '04:00 PM',
    value: Math.floor(Math.random() * 300) + 100,
  },
  {
    name: '05:00 PM',
    value: Math.floor(Math.random() * 300) + 100,
  },
  {
    name: '06:00 PM',
    value: Math.floor(Math.random() * 300) + 100,
  },
  {
    name: '07:00 PM',
    value: Math.floor(Math.random() * 300) + 100,
  },
  {
    name: '08:00 PM',
    value: Math.floor(Math.random() * 300) + 100,
  },
  {
    name: '09:00 PM',
    value: Math.floor(Math.random() * 300) + 100,
  },
  {
    name: '10:00 PM',
    value: Math.floor(Math.random() * 300) + 100,
  },
  {
    name: '11:00 PM',
    value: Math.floor(Math.random() * 300) + 100,
  },
  {
    name: '12:00 PM',
    value: Math.floor(Math.random() * 300) + 100,
  },
]

export const OverviewChart = () => {
  return (
    <ScrollArea className="w-full">
      <ResponsiveContainer height={350} width="100%">
        <BarChart data={week_data}>
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
