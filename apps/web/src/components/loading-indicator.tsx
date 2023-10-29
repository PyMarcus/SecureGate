import { cn } from '@/lib/utils'
import { IconProps, SpinnerGap } from '@phosphor-icons/react'

type LoadingIndicatorProps = IconProps

export const LoadingIndicator = ({
  className,
  ...props
}: LoadingIndicatorProps) => {
  return <SpinnerGap className={cn('animate-spin', className)} {...props} />
}
