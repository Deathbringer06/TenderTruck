import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import { z } from "zod";
import { api } from "../lib/api";
import { saveEmail, saveToken } from "../lib/auth";

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
});

type LoginForm = z.infer<typeof loginSchema>;

export function LoginPage() {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const { register, handleSubmit } = useForm<LoginForm>();

  async function submit(values: LoginForm): Promise<void> {
    setError("");
    const parsed = loginSchema.safeParse(values);
    if (!parsed.success) {
      setError("Enter a valid email and password.");
      return;
    }
    try {
      const response = await api.post("/auth/login", parsed.data);
      saveToken(response.data.access_token);
      saveEmail(parsed.data.email);
      navigate("/tenders");
    } catch {
      setError("Sign in failed. Check your credentials.");
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#f5f6f7]">
      <form onSubmit={handleSubmit(submit)} className="w-full max-w-[380px] rounded-control border border-border bg-white p-6">
        <h1 className="mb-6 text-xl font-semibold">Sign in</h1>
        <label className="mb-1 block text-sm font-medium">Email</label>
        <input
          type="email"
          required
          {...register("email")}
          className="mb-4 h-10 w-full rounded-control border border-border px-3 outline-none focus:border-secondary"
        />
        <label className="mb-1 block text-sm font-medium">Password</label>
        <input
          type="password"
          required
          {...register("password")}
          className="mb-4 h-10 w-full rounded-control border border-border px-3 outline-none focus:border-secondary"
        />
        {error && <p className="mb-4 text-sm text-red-700">{error}</p>}
        <button className="h-10 w-full rounded-control bg-signal px-4 text-sm font-medium text-white">
          Sign in
        </button>
        <p className="mt-4 text-sm text-secondary">
          New account?{" "}
          <Link to="/register" className="font-medium text-signal">
            Register
          </Link>
        </p>
      </form>
    </div>
  );
}
