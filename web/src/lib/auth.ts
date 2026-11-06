const TOKEN_KEY = "tendertruck_token";
const EMAIL_KEY = "tendertruck_email";

export function saveToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(EMAIL_KEY);
}

export function saveEmail(email: string): void {
  localStorage.setItem(EMAIL_KEY, email);
}

export function getEmail(): string | null {
  return localStorage.getItem(EMAIL_KEY);
}
