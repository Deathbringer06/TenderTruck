/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_USE_MOCKS: string | undefined
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
