import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { zodResolver } from '@hookform/resolvers/zod'
import { PlusCircle } from '@phosphor-icons/react'
import { useId, useState } from 'react'
import { useForm } from 'react-hook-form'
import * as zod from 'zod'
import { Input } from './ui/input'

export const NewGateDialog = () => {
  const [isOpen, setIsOpen] = useState(false)

  const handleOpenChange = (open: boolean) => setIsOpen(open)
  const closeDialog = () => setIsOpen(false)

  const formSchema = zod
    .object({
      name: zod.string().min(3, {
        message: 'Name must be at least 3 characters',
      }),
      wifiSSID: zod.string().min(3, {
        message: 'SSID must be at least 3 characters',
      }),
      wifiPassword: zod.string().min(8, {
        message: 'Password must be at least 8 characters',
      }),
      confirmWifiPassword: zod.string().min(8, {
        message: 'Password must be at least 8 characters',
      }),
    })
    .refine((data) => data.wifiPassword === data.confirmWifiPassword, {
      message: 'Passwords do not match',
      path: ['confirmPassword'],
    })

  type FormType = zod.infer<typeof formSchema>

  const form = useForm<FormType>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      wifiSSID: '',
      wifiPassword: '',
      confirmWifiPassword: '',
    },
  })
  const formId = useId()

  const handleResetAndClose = () => {
    form.reset()
    closeDialog()
  }

  const handleFormSubmit = async (values: FormType) => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { confirmWifiPassword, ...rest } = values
    console.log(rest)
    handleResetAndClose()
  }

  return (
    <Dialog open={isOpen} onOpenChange={handleOpenChange}>
      <DialogTrigger asChild>
        <Button className="space-x-2 min-w-max">
          <PlusCircle />
          <span className="sr-only md:not-sr-only">Novo portão</span>
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Adicionar novo portão</DialogTitle>
          <DialogDescription>
            Preencha os campos abaixo para adicionar um novo portão
          </DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form
            id={formId}
            className="space-y-2"
            onSubmit={form.handleSubmit(handleFormSubmit)}
          >
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
                    <Input placeholder="Confirme a senha" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </form>
        </Form>
        <DialogFooter className="flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
          <DialogClose onClick={handleResetAndClose} asChild>
            <Button variant="outline">Cancelar</Button>
          </DialogClose>
          <Button form={formId} type="submit">
            Adicionar
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
