import type { TextareaHTMLAttributes } from 'react'

type TextareaProps = TextareaHTMLAttributes<HTMLTextAreaElement>

export function Textarea({ className = '', ...props }: TextareaProps) {
  return <textarea className={`text-input text-area ${className}`.trim()} {...props} />
}
