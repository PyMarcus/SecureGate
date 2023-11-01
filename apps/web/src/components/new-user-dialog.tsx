import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
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
import { Input } from '@/components/ui/input'
import { toast } from '@/components/ui/use-toast'
import { useCreateUser } from '@/services/api/requests/users'
import { useSessionStore } from '@/stores/session-store'
import { zodResolver } from '@hookform/resolvers/zod'
import { PlusCircle } from '@phosphor-icons/react'
import { useId, useState } from 'react'
import { useForm } from 'react-hook-form'
import * as zod from 'zod'

export const NewUserDialog = () => {
  const [isOpen, setIsOpen] = useState(false)

  const { session } = useSessionStore()
  const { mutateAsync } = useCreateUser()

  const handleOpenChange = (open: boolean) => setIsOpen(open)
  const closeDialog = () => setIsOpen(false)

  const formSchema = zod.object({
    name: zod.string().min(3, {
      message: 'O nome deve ter no mínimo 3 caracteres',
    }),
    email: zod.string().email({
      message: 'Formato de email inválido',
    }),
    rfid: zod.string().length(8, {
      message: 'O rfid deve ter 8 caracteres',
    }),
    authorized: zod.boolean().default(true),
  })

  type FormType = zod.infer<typeof formSchema>

  const form = useForm<FormType>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      email: '',
      rfid: '',
      authorized: true,
    },
  })
  const formId = useId()

  const handleResetAndClose = () => {
    form.reset()
    closeDialog()
  }

  const handleFormSubmit = async (values: FormType) => {
    const response = await mutateAsync({
      ...values,
      added_by: session!.user.id,
    })

    console.log(response)
    if (response && response.success) {
      toast({
        title: 'Novo usuário',
        description: 'O usuário foi adicionado com sucesso!',
      })
      handleResetAndClose()
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={handleOpenChange}>
      <DialogTrigger asChild>
        <Button className="space-x-2 min-w-max">
          <PlusCircle />
          <span className="sr-only md:not-sr-only">Novo usuário</span>
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Adicionar novo usuário</DialogTitle>
          <DialogDescription>
            Preencha os campos abaixo para adicionar um novo usuário.
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
                    <Input placeholder="Gate Name" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input placeholder="Email" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="rfid"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Rfid</FormLabel>
                  <FormControl>
                    <Input placeholder="Rfid" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="authorized"
              render={({ field }) => (
                <FormItem>
                  <div className="inline-flex items-center gap-1">
                    <FormControl>
                      <Checkbox
                        checked={field.value}
                        onCheckedChange={field.onChange}
                      />
                    </FormControl>
                    <FormLabel>Autorizado</FormLabel>
                  </div>
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
