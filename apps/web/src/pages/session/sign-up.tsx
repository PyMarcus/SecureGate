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
import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { Link, useNavigate } from 'react-router-dom'
import * as zod from 'zod'

export const SignUp = () => {
  const navigate = useNavigate()

  const formSchema = zod
    .object({
      name: zod.string().min(3, {
        message: 'Name must be at least 3 characters long',
      }),
      email: zod.string().email({
        message: 'Invalid email address',
      }),
      password: zod.string().min(8, {
        message: 'Password must be at least 8 characters long',
      }),
      confirmPassword: zod.string().min(8, {
        message: 'Password must be at least 8 characters long',
      }),
    })
    .refine((data) => data.password === data.confirmPassword, {
      message: 'Passwords do not match',
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

  const handleFormSubmit = (data: FormType) => {
    console.log(data)
    navigate('/')
  }

  return (
    <section className="w-full max-w-sm">
      <div>
        <Button
          variant="ghost"
          className="fixed top-6 right-6 md:top-8 md:right-8"
          asChild
        >
          <Link to="/session/sign-in">Sign In</Link>
        </Button>
      </div>
      <header className="mb-4">
        <h1 className="text-2xl font-semibold tracking-tight">
          Sign up to Your Account
        </h1>
        <p className="text-sm text-muted-foreground">
          Fill in your details to create an account
        </p>
      </header>

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
                <FormLabel>Name</FormLabel>
                <FormControl>
                  <Input placeholder="Name" {...field} />
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
                <FormLabel>Password</FormLabel>
                <FormControl>
                  <Input placeholder="Password" type="password" {...field} />
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
                <FormLabel>Confirm Password</FormLabel>
                <FormControl>
                  <Input
                    placeholder="Confirm Password"
                    type="password"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button className="w-full" type="submit">
            Sign Up
          </Button>
        </form>
      </Form>
    </section>
  )
}