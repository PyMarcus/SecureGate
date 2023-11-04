import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import { unsafeCopyToClipboard } from '@/utils/clipboard'
import { Check, Clipboard } from '@phosphor-icons/react'
import { useEffect, useState } from 'react'
import { useToast } from './ui/use-toast'

interface CopyButtonProps extends React.HTMLAttributes<HTMLButtonElement> {
  value: string
}

export const CopyButton = ({ value, className, ...props }: CopyButtonProps) => {
  const [hasCopied, setHasCopied] = useState(false)

  const { toast } = useToast()

  useEffect(() => {
    setTimeout(() => {
      setHasCopied(false)
    }, 2000)
  }, [hasCopied])

  const copyIsSupported = window.isSecureContext && navigator.clipboard

  const handleCopyToClipboard = async () => {
    try {
      copyIsSupported
        ? await navigator.clipboard.writeText(value)
        : unsafeCopyToClipboard(value)

      toast({
        title: 'Copiado!',
        description: 'O texto foi copiado para a área de transferência.',
      })

      setHasCopied(true)
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <Button
      size="icon"
      variant="ghost"
      className={cn(
        'relative z-10 h-7 w-7 text-zinc-50 hover:bg-zinc-700 hover:text-zinc-50',
        className,
      )}
      onClick={handleCopyToClipboard}
      {...props}
    >
      <span className="sr-only">Copy</span>
      {hasCopied ? <Check /> : <Clipboard />}
    </Button>
  )
}
