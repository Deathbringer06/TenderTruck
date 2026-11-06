import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import { z } from "zod";
import { api } from "../lib/api";

const registerSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  role: z.enum(["customer", "carrier"]),
});

type RegisterForm = z.infer<typeof registerSchema>;

export function RegisterPage() {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const { register, handleSubmit } = useForm<RegisterForm>({
    defaultValues: { role: "customer" },
  });

  async function submit(values: RegisterForm): Promise<void> {
    setError("");
    const parsed = registerSchema.safeParse(values);
    if (!parsed.success) {
      setError("Enter a valid email, password, and role.");
      return;
    }
    try {
      await api.post("/auth/register", parsed.data);
      navigate("/login");
    } catch {
      setError("Registration failed.");
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#f5f6f7]">
      <form onSubmit={handleSubmit(submit)} className="w-full max-w-[380px] rounded-control border border-border bg-white p-6">
        <h1 className="mb-6 text-xl font-semibold">Create account</h1>
        <label className="mb-1 block text-sm font-medium">Email</label>
        <input type="email" required {...register("email")}
          className="mb-4 h-10 w-full rounded-control border border-border px-3 outline-none" />
        <label className="mb-1 block text-sm font-medium">Password</label>
        <input type="password" required minLength={8} {...register("password")}
          className="mb-4 h-10 w-full rounded-control border border-border px-3 outline-none" />
        <label className="mb-1 block text-sm font-medium">Role</label>
        <select {...register("role")}
          className="mb-4 h-10 w-full rounded-control border border-border bg-white px-3">
          <option value="customer">Customer</option>
          <option value="carrier">Carrier</option>
        </select>
        {error && <p className="mb-4 text-sm text-red-700">{error}</p>}
        <button className="h-10 w-full rounded-control bg-signal px-4 text-sm font-medium text-white">
          Register
        </button>
        <p className="mt-4 text-sm text-secondary">
          Already registered? <Link to="/login" className="font-medium text-signal">Sign in</Link>
        </p>
      </form>
    </div>
  );
}
