import type { HTMLAttributes } from 'react'

type AlertProps = HTMLAttributes<HTMLDivElement> & {
  variant?: 'success' | 'error' | 'info'
}

export function Alert({ children, className = '', variant = 'info', ...props }: AlertProps) {
  return (
    <div aria-live={variant === 'error' ? 'assertive' : 'polite'} className={`alert alert-${variant} ${className}`.trim()} role={variant === 'error' ? 'alert' : 'status'} {...props}>
      {children}
    </div>
  )
}
