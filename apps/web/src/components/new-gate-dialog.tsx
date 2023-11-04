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
import { toast } from '@/components/ui/use-toast'
import { useCreateDevice } from '@/services/api/requests/devices'
import { zodResolver } from '@hookform/resolvers/zod'
import { Password, PlusCircle, WifiHigh } from '@phosphor-icons/react'
import { useId, useState } from 'react'
import { FormProvider, useForm } from 'react-hook-form'
import * as zod from 'zod'
import { CopyButton } from './copy-button'
import { LoadingIndicator } from './loading-indicator'
import { NewGateForm } from './new-gate-form'
import { ScrollArea, ScrollBar } from './ui/scroll-area'

interface Step {
  content: React.ReactNode
  leftButtonText: string
  rightButtonText: string
  onLeftButton?: (params?: unknown) => void
  onRightButton?: (params?: unknown) => void
}

export const NewGateDialog = () => {
  const { VITE_BOARD_AP_SSID, VITE_BOARD_AP_PASSWORD } = import.meta.env

  const [formStep, setFormStep] = useState(0)
  const [isOpen, setIsOpen] = useState(false)

  const { isLoading, mutateAsync } = useCreateDevice()

  const handleOpenChange = (open: boolean) => setIsOpen(open)
  const handleNextStep = () => setFormStep((prev) => prev + 1)
  const handlePreviousStep = () => setFormStep((prev) => prev - 1)
  const handleResetStep = () => setFormStep(0)

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
  const formState = form.formState

  const handleResetAndClose = () => {
    form.reset()
    closeDialog()
    handleResetStep()
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

  const formSteps: Record<number, Step> = {
    0: {
      content: (
        <div className="flex-1 grid place-content-center">
          <div className="text-center space-y-8 max-w-sm">
            <div className="space-y-4">
              <strong>Conecte-se a rede Wifi</strong>
              <p className="text-sm text-muted-foreground">
                Para realizar a configuração, você deve se conectar a rede Wifi
                do dispositivo. Após conectar, clique em próximo e siga os
                passos
              </p>
            </div>

            <div className="space-y-4">
              <div className="flex flex-1 p-4 border rounded-lg gap-4">
                <WifiHigh className="mt-1" />
                <div className="flex-1 text-start">
                  <strong className="text-start leading-none">Rede wifi</strong>
                  <p className="text-muted-foreground text-sm">
                    {VITE_BOARD_AP_SSID}
                  </p>
                </div>
                <CopyButton value={VITE_BOARD_AP_SSID} />
              </div>
              <div className="flex flex-1 p-4 border rounded-lg gap-4">
                <Password className="mt-1" />
                <div className="flex-1 text-start">
                  <strong className="text-start text-sm leading-none">
                    Senha
                  </strong>
                  <p className="text-muted-foreground text-sm">
                    {VITE_BOARD_AP_PASSWORD}
                  </p>
                </div>
                <CopyButton value={VITE_BOARD_AP_PASSWORD} />
              </div>
            </div>
          </div>
        </div>
      ),
      leftButtonText: 'Cancelar',
      rightButtonText: 'Próximo',
      onLeftButton: handleResetAndClose,
      onRightButton: handleNextStep,
    },
    1: {
      content: (
        <form
          id={formId}
          className="space-y-2 flex-1 flex flex-col justify-center"
        >
          <FormProvider {...form}>
            <NewGateForm />
          </FormProvider>
        </form>
      ),
      leftButtonText: 'Voltar',
      rightButtonText: 'Próximo',
      onLeftButton: handlePreviousStep,
      onRightButton: handleNextStep,
    },
    2: {
      content: (
        <div className="flex-1 grid place-content-center">
          <div className="text-center space-y-8 max-w-sm">
            <div className="space-y-4">
              <strong>Conecte-se novamente a sua rede Wifi</strong>
              <p className="text-sm text-muted-foreground">
                Para finalizar a configuração, você deve se conectar a sua rede
                Wifi novamente. Após conectar, clique em adicionar para
                adicionar o novo portão.
              </p>
            </div>
          </div>
        </div>
      ),
      leftButtonText: 'Voltar',
      rightButtonText: 'Adicionar',
      onLeftButton: handlePreviousStep,
      onRightButton: form.handleSubmit(handleFormSubmit),
    },
  }

  const currentStep = formSteps[formStep]
  const isFistStep = formStep === 0
  const isOnFormStep = formStep === 1

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
          <DialogTitle>Novo portão</DialogTitle>
          <DialogDescription>
            Siga os passos abaixo para adicionar um novo portão
          </DialogDescription>
        </DialogHeader>

        <ScrollArea>
          <div
            className="flex flex-col gap-2 m-px h-[calc(100vh-20rem)] 
          md:h-[calc(100vh-26rem)]"
          >
            {currentStep.content}
            <ScrollBar />
          </div>
        </ScrollArea>

        <DialogFooter className="flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
          {isFistStep ? (
            <DialogClose onClick={currentStep.onLeftButton} asChild>
              <Button variant="outline">{currentStep.leftButtonText}</Button>
            </DialogClose>
          ) : (
            <Button variant="outline" onClick={currentStep.onLeftButton}>
              {currentStep.leftButtonText}
            </Button>
          )}

          <Button
            form={formId}
            onClick={currentStep.onRightButton}
            disabled={isLoading || (isOnFormStep && !formState.isValid)}
          >
            {isLoading && <LoadingIndicator className="mr-2" />}
            {currentStep.rightButtonText}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
