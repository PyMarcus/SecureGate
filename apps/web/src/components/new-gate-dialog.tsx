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
import { useCreateDevice } from '@/services/api/requests/devices'
import { zodResolver } from '@hookform/resolvers/zod'
import { PlusCircle } from '@phosphor-icons/react'
import { useId, useState } from 'react'
import { useForm } from 'react-hook-form'
import * as zod from 'zod'
import { LoadingIndicator } from './loading-indicator'
import { Input } from './ui/input'
import { toast } from './ui/use-toast'

export const NewGateDialog = () => {
  const [isOpen, setIsOpen] = useState(false)

  const { isLoading, mutateAsync } = useCreateDevice()

  const handleOpenChange = (open: boolean) => setIsOpen(open)
  const closeDialog = () => setIsOpen(false)

  const formSchema = zod
    .object({
      name: zod.string().min(3, {
        message: 'O nome deve ter no mínimo 3 caracteres',
      }),
      version: zod.string().min(3, {
        message: 'A versão deve ter no mínimo 3 caracteres',
      }),
      wifiSSID: zod.string().min(3, {
        message: 'O nome deve ter no mínimo 3 caracteres',
      }),
      wifiPassword: zod.string().min(8, {
        message: 'A senha deve ter no mínimo 8 caracteres',
      }),
      confirmWifiPassword: zod.string().min(8, {
        message: 'A senha deve ter no mínimo 8 caracteres',
      }),
    })
    .refine((data) => data.wifiPassword === data.confirmWifiPassword, {
      message: 'As senhas devem ser iguais',
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

    const response = await mutateAsync({
      ...rest,
      wifi_password: values.wifiPassword,
      wifi_ssid: values.wifiSSID,
    })

    if (response && response.success) {
      toast({
        title: 'Novo portão',
        description: `O portão ${values.name} foi adicionado com sucesso!`,
      })
      handleResetAndClose()
    }
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
          </form>
        </Form>
        <DialogFooter className="flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
          <DialogClose onClick={handleResetAndClose} asChild>
            <Button variant="outline">Cancelar</Button>
          </DialogClose>
          <Button form={formId} type="submit">
            {isLoading && <LoadingIndicator className="mr-2" />}
            Adicionar
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
