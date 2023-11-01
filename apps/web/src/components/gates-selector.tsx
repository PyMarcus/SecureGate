import { Button } from '@/components/ui/button'
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from '@/components/ui/command'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { cn } from '@/lib/utils'
import { CaretUpDown, Check } from '@phosphor-icons/react'

import * as React from 'react'

const gatesList = [
  { label: 'Gate 1', value: 'gate1' },
  { label: 'Gate 2', value: 'gate2' },
  { label: 'Gate 3', value: 'gate3' },
] as const

export function GatesSelector() {
  const [open, setOpen] = React.useState(false)
  const [value, setValue] = React.useState('')

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-full md:w-64 justify-between"
        >
          {value
            ? gatesList.find((gate) => gate.value === value)?.label
            : 'Select gate...'}
          <CaretUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-full md:w-64 p-0">
        <Command>
          <CommandInput placeholder="Buscar portão" className="h-9" />
          <CommandEmpty>Nenhum portão encontrado!</CommandEmpty>
          <CommandGroup>
            {gatesList.map((gate) => (
              <CommandItem
                key={gate.value}
                value={gate.value}
                onSelect={(currentValue) => {
                  setValue(currentValue === value ? '' : currentValue)
                  setOpen(false)
                }}
              >
                {gate.label}
                <Check
                  className={cn(
                    'ml-auto h-4 w-4',
                    value === gate.value ? 'opacity-100' : 'opacity-0',
                  )}
                />
              </CommandItem>
            ))}
          </CommandGroup>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
