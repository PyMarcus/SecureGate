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
import { useDeviceStore } from '@/stores/device-store'
import { CaretUpDown, Check } from '@phosphor-icons/react'

import { Device } from '@/@types/schemas/device'
import {
  useDeviceUsers,
  useGetAllDevices,
} from '@/services/api/requests/devices'
import { useUserStore } from '@/stores/user-store'
import { useEffect, useState } from 'react'
import { LoadingIndicator } from './loading-indicator'

export function GatesSelector() {
  const [open, setOpen] = useState(false)
  const [filter, setFilter] = useState('')

  const { devices, currentDevice, setCurrentDevice, setIsLoadingDevices } =
    useDeviceStore()

  const { setIsLoadingUsers } = useUserStore()

  const { isLoading: devicesLoading } = useGetAllDevices()
  const { isLoading: deviceUsersLoading } = useDeviceUsers({
    deviceId: currentDevice?.id || '-',
  })

  useEffect(() => {
    setIsLoadingUsers(deviceUsersLoading)
  }, [deviceUsersLoading, setIsLoadingUsers])

  useEffect(() => {
    setIsLoadingDevices(devicesLoading)
  }, [devicesLoading, setIsLoadingDevices])

  const handleSelectDevice = (device: Device) => setCurrentDevice(device)

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-full md:w-64 justify-between"
        >
          {currentDevice ? currentDevice.name : 'Selecione um portão'}
          <CaretUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-full md:w-64 p-0">
        <Command>
          <CommandInput placeholder="Buscar portão" className="h-9" />
          <CommandEmpty>
            {devicesLoading ? 'Buscando portões!' : 'Nenhum portão encontrado!'}
          </CommandEmpty>
          <CommandGroup>
            {devicesLoading ? (
              <div className="grid place-items-center mb-4">
                <LoadingIndicator />
              </div>
            ) : (
              devices.map((gate) => (
                <CommandItem
                  key={gate.id}
                  value={gate.name}
                  onSelect={(currentValue) => {
                    handleSelectDevice(gate)
                    setFilter(currentValue === filter ? '' : currentValue)
                    setOpen(false)
                  }}
                >
                  {gate.name}
                  <Check
                    className={cn(
                      'ml-auto h-4 w-4',
                      currentDevice?.name === gate.name
                        ? 'opacity-100'
                        : 'opacity-0',
                    )}
                  />
                </CommandItem>
              ))
            )}
          </CommandGroup>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
