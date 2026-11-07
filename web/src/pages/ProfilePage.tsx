import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { api } from "../lib/api";

const profileSchema = z.object({
  name: z.string().min(1, "Company name is required").max(255),
  inn: z.string().min(1, "INN is required").max(12),
  description: z.string().max(1000).optional(),
});

type ProfileForm = z.infer<typeof profileSchema>;
type Company = ProfileForm & { id: string; verification_status: string };

export function ProfilePage() {
  const [error, setError] = useState("");
  const [saved, setSaved] = useState(false);
  const { register, reset, handleSubmit, formState: { errors, isSubmitting } } = useForm<ProfileForm>({
    defaultValues: { name: "", inn: "", description: "" },
  });

  useEffect(() => {
    async function loadCompany(): Promise<void> {
      try {
        const response = await api.get<Company>("/companies/me");
        reset({ name: response.data.name, inn: response.data.inn, description: response.data.description ?? "" });
      } catch {
        setError("Unable to load company profile.");
      }
    }
    void loadCompany();
  }, [reset]);

  async function submit(values: ProfileForm): Promise<void> {
    setError("");
    setSaved(false);
    const parsed = profileSchema.safeParse(values);
    if (!parsed.success) {
      setError(parsed.error.issues[0]?.message ?? "Enter valid company details.");
      return;
    }
    try {
      await api.patch("/companies/me", parsed.data);
      setSaved(true);
    } catch {
      setError("Unable to save company profile.");
    }
  }

  return (
    <section className="max-w-[720px]">
      <div className="mb-5">
        <h1 className="text-xl font-semibold">Profile</h1>
        <p className="mt-1 text-sm text-secondary">Company details used for tenders and bids.</p>
      </div>
      <form onSubmit={handleSubmit(submit)} className="rounded-control border border-border bg-white p-5">
        <label className="mb-1 block text-sm font-medium" htmlFor="name">Company name</label>
        <input id="name" {...register("name")} className="mb-1 h-10 w-full rounded-control border border-border px-3 outline-none focus:border-secondary" />
        {errors.name && <p className="mb-3 text-sm text-red-700">{errors.name.message}</p>}
        {!errors.name && <div className="mb-4" />}

        <label className="mb-1 block text-sm font-medium" htmlFor="inn">INN</label>
        <input id="inn" {...register("inn")} className="mb-1 h-10 w-full rounded-control border border-border px-3 outline-none focus:border-secondary" />
        {errors.inn && <p className="mb-3 text-sm text-red-700">{errors.inn.message}</p>}
        {!errors.inn && <div className="mb-4" />}

        <label className="mb-1 block text-sm font-medium" htmlFor="description">Description</label>
        <textarea id="description" rows={5} {...register("description")} className="mb-4 w-full resize-y rounded-control border border-border px-3 py-2 outline-none focus:border-secondary" />
        {error && <p className="mb-4 text-sm text-red-700">{error}</p>}
        {saved && <p className="mb-4 text-sm text-green-700">Profile saved.</p>}
        <button type="submit" disabled={isSubmitting} className="h-10 rounded-control bg-signal px-4 text-sm font-medium text-white disabled:opacity-60">
          {isSubmitting ? "Saving..." : "Save changes"}
        </button>
      </form>
    </section>
  );
}
