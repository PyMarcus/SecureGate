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

export const NewMemberDialog = () => {
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
          <span className="sr-only md:not-sr-only">New member</span>
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Add a new member</DialogTitle>
          <DialogDescription>
            Fill in the form below to add a new member.
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
                  <FormLabel>Gate Name</FormLabel>
                  <FormControl>
                    <Input placeholder="Gate Name" {...field} />
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
                  <FormLabel>Wifi SSID</FormLabel>
                  <FormControl>
                    <Input placeholder="Wifi SSID" {...field} />
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
                  <FormLabel>Wifi Password</FormLabel>
                  <FormControl>
                    <Input
                      placeholder="Wifi password"
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
                  <FormLabel>Confirm Wifi Password</FormLabel>
                  <FormControl>
                    <Input placeholder="Confirm Wifi password" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </form>
        </Form>
        <DialogFooter className="flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
          <DialogClose onClick={handleResetAndClose} asChild>
            <Button variant="outline">Cancel</Button>
          </DialogClose>
          <Button form={formId} type="submit">
            Add Gate
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
