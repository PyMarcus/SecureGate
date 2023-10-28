import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis } from 'recharts'

const week_data = [
  {
    name: 'Mon',
    value: Math.floor(Math.random() * 5000) + 1000,
  },
  {
    name: 'Tue',
    value: Math.floor(Math.random() * 5000) + 1000,
  },
  {
    name: 'Wed',
    value: Math.floor(Math.random() * 5000) + 1000,
  },
  {
    name: 'Thu',
    value: Math.floor(Math.random() * 5000) + 1000,
  },
  {
    name: 'Fri',
    value: Math.floor(Math.random() * 5000) + 1000,
  },
  {
    name: 'Sat',
    value: Math.floor(Math.random() * 5000) + 1000,
  },
  {
    name: 'Sun',
    value: Math.floor(Math.random() * 5000) + 1000,
  },
]

export const Overview = () => {
  return (
    <ResponsiveContainer width="100%" height={350}>
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
  )
}
