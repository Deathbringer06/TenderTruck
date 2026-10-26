import type { PropsWithChildren, ReactNode } from 'react'

type FieldProps = PropsWithChildren<{
  htmlFor: string
  label: string
  hint?: ReactNode | undefined
  error?: string | undefined
}>

export function Field({ children, error, htmlFor, hint, label }: FieldProps) {
  return (
    <div className="field">
      <label className="field-label" htmlFor={htmlFor}>{label}</label>
      {children}
      {error ? (
        <span className="field-error" role="alert">{error}</span>
      ) : hint ? (
        <span className="field-hint">{hint}</span>
      ) : null}
    </div>
  )
}
