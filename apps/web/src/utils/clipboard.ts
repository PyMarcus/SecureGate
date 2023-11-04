export const unsafeCopyToClipboard = (text: string) => {
  const textArea = document.createElement('textarea')
  textArea.value = text

  document.body.appendChild(textArea)
  textArea.focus()
  textArea.select()
  try {
    document.execCommand('copy')
  } catch (err) {
    console.error('Unable to copy', err)
  } finally {
    textArea.remove()
  }
}
