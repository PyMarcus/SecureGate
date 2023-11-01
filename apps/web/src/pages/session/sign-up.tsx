import { LoadingIndicator } from '@/components/loading-indicator'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { useToast } from '@/components/ui/use-toast'
import { useSignUp } from '@/services/api/requests/session'
import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { Link, useNavigate } from 'react-router-dom'
import * as zod from 'zod'

export const SignUp = () => {
  const { toast } = useToast()
  const navigate = useNavigate()

  const { isLoading, mutateAsync } = useSignUp()

  const formSchema = zod
    .object({
      name: zod.string().min(3, {
        message: 'O nome deve ter no mínimo 3 caracteres',
      }),
      email: zod.string().email({
        message: 'Formato de email inválido',
      }),
      password: zod.string().min(8, {
        message: 'A senha deve ter no mínimo 8 caracteres ',
      }),
      confirmPassword: zod.string().min(8, {
        message: 'A senha deve ter no mínimo 8 caracteres',
      }),
    })
    .refine((data) => data.password === data.confirmPassword, {
      message: 'As senhas devem ser iguais',
      path: ['confirmPassword'],
    })

  type FormType = zod.infer<typeof formSchema>

  const form = useForm<FormType>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      email: '',
      password: '',
      confirmPassword: '',
    },
  })

  const handleFormSubmit = async (values: FormType) => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { confirmPassword, ...rest } = values

    const response = await mutateAsync({
      ...rest,
      role: 'ROOT',
    })
    if (response && response.success) {
      toast({
        title: `Welcome, ${values.name}!`,
        description: 'Your account has been created successfully',
      })
      navigate('/sessao/sign-in')
    }
  }

  return (
    <Card className="border-transparent sm:border-border w-full max-w-sm">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl">Criar uma nova conta</CardTitle>
        <CardDescription>
          Preencha os campos abaixo para criar uma nova conta.
        </CardDescription>
      </CardHeader>

      <CardContent>
        <Form {...form}>
          <form
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
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Senha</FormLabel>
                  <FormControl>
                    <Input placeholder="Senha" type="password" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="confirmPassword"
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
            <Button className="w-full" type="submit">
              {isLoading && <LoadingIndicator className="mr-2" />}
              <span>Cadastrar</span>
            </Button>
          </form>
        </Form>
      </CardContent>
      <CardFooter className="flex items-center justify-center text-sm p-0 pb-6">
        <p className="text-muted-foreground">Já possui uma conta?</p>
        <Button variant="link" className="px-2" asChild>
          <Link to="/sessao/sign-in">Entrar</Link>
        </Button>
      </CardFooter>
    </Card>
  )
}
