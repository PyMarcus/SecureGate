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
import { useSignIn } from '@/services/api/requests/session'
import { useSessionStore } from '@/stores/session-store'
import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { Link, useNavigate } from 'react-router-dom'
import * as zod from 'zod'

export const SignIn = () => {
  const { setSession } = useSessionStore()

  const { toast } = useToast()
  const navigate = useNavigate()

  const { isLoading, mutateAsync } = useSignIn()

  const formSchema = zod.object({
    email: zod.string().email({
      message: 'Formato de email inválido',
    }),
    password: zod.string().min(8, {
      message: 'A senha deve ter no mínimo 8 caracteres',
    }),
  })

  type FormType = zod.infer<typeof formSchema>

  const form = useForm<FormType>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  })

  const handleFormSubmit = async (values: FormType) => {
    const response = await mutateAsync(values)
    if (response && response.success) {
      const { data } = response

      setSession({
        user: {
          id: data.user_id,
          email: data.email,
          name: data.name,
          role: data.role,
        },
        token: data.token,
      })
      toast({
        title: `Olá, ${data.name}!`,
        description: 'SignIn realizado com sucesso!',
      })
      navigate('/')
    }
  }

  return (
    <Card className="border-transparent sm:border-border w-full max-w-sm">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl">Acesse sua conta</CardTitle>
        <CardDescription>
          Preencha os campos abaixo para acessar sua conta.
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
            <Button className="w-full" type="submit">
              {isLoading && <LoadingIndicator className="mr-2" />}
              <span>Entrar</span>
            </Button>
          </form>
        </Form>
      </CardContent>

      <CardFooter className="flex items-center justify-center text-sm p-0 pb-6">
        <p className="text-muted-foreground">Não tem uma conta?</p>
        <Button variant="link" className="px-2" asChild>
          <Link to="/sessao/sign-up">Cadastre-se</Link>
        </Button>
      </CardFooter>
    </Card>
  )
}
