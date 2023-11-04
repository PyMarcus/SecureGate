import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { useFormContext } from 'react-hook-form'

export const NewGateForm = () => {
  const form = useFormContext()

  return (
    <Form {...form}>
      <FormField
        control={form.control}
        name="name"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Nome</FormLabel>
            <FormControl>
              <Input placeholder="Nome" {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      <FormField
        control={form.control}
        name="version"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Versão</FormLabel>
            <FormControl>
              <Input placeholder="Versão" {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      <FormField
        control={form.control}
        name="wifiSSID"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Nome da rede Wifi</FormLabel>
            <FormControl>
              <Input placeholder="Nome da rede Wifi" {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      <FormField
        control={form.control}
        name="wifiPassword"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Senha da rede Wifi</FormLabel>
            <FormControl>
              <Input
                placeholder="Senha da rede Wifi"
                type="password"
                {...field}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      <FormField
        control={form.control}
        name="confirmWifiPassword"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Confirme a senha</FormLabel>
            <FormControl>
              <Input
                placeholder="Confirme a senha"
                type="password"
                {...field}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
    </Form>
  )
}
