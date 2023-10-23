import { Button } from '@/components/ui/button'
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
import { SpinnerGap } from '@phosphor-icons/react'
import { useForm } from 'react-hook-form'
import { Link, useNavigate } from 'react-router-dom'
import * as zod from 'zod'

export const SignIn = () => {
  const { setSession } = useSessionStore()

  const { toast } = useToast()
  const navigate = useNavigate()

  const { isSuccess, data: response, isLoading, mutate } = useSignIn()

  const formSchema = zod.object({
    email: zod.string().email({
      message: 'Invalid email address',
    }),
    password: zod.string().min(8, {
      message: 'Password must be at least 8 characters long',
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

  const handleFormSubmit = (data: FormType) => {
    mutate(data)

    if (isSuccess && response) {
      setSession({
        user: {
          id: response.user_id,
          email: response.email,
          name: response.user_request,
        },
        token: response.token,
      })
      toast({
        title: `Hi, ${response.user_request}!`,
        description: 'You have successfully logged in to your account.',
      })
      navigate('/')
    }
  }

  return (
    <section className="w-full max-w-sm">
      <div>
        <Button
          variant="ghost"
          className="fixed top-6 right-6 md:top-8 md:right-8"
          asChild
        >
          <Link to="/session/sign-up">Sign Up</Link>
        </Button>
      </div>
      <header className="mb-4 text-center">
        <h1 className="text-2xl font-semibold tracking-tight">
          Sign in to your account
        </h1>
        <p className="text-sm text-muted-foreground">
          Fill in your details to login to your account
        </p>
      </header>

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
                <FormLabel>Password</FormLabel>
                <FormControl>
                  <Input placeholder="Password" type="password" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button className="w-full" type="submit">
            {isLoading && <SpinnerGap className="mr-2 animate-spin" />}
            <span>Sign In</span>
          </Button>
        </form>
      </Form>
    </section>
  )
}
