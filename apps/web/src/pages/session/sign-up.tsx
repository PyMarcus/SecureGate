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
import { SpinnerGap } from '@phosphor-icons/react'
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

  const handleFormSubmit = async (data: FormType) => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { confirmPassword, ...rest } = data

    const response = await mutateAsync({
      ...rest,
      role: 'ROOT',
    })
    if (response) {
      toast({
        title: `Welcome, ${data.name}!`,
        description: 'Your account has been created successfully',
      })
      navigate('/session/sign-in')
    }
  }

  return (
    <Card className="border-transparent sm:border-border w-full max-w-sm">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl">Create an account</CardTitle>
        <CardDescription>
          Fill in your details to login to your account
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
              {isLoading && <SpinnerGap className="mr-2 animate-spin" />}
              <span>Sign Up</span>
            </Button>
          </form>
        </Form>
      </CardContent>
      <CardFooter className="flex items-center justify-center text-sm p-0 pb-6">
        <p className="text-muted-foreground">Already have an account?</p>
        <Button variant="link" className="px-2" asChild>
          <Link to="/session/sign-in">Sign up</Link>
        </Button>
      </CardFooter>
    </Card>
  )
}
