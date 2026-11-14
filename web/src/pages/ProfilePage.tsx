import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { api } from "../lib/api";

const profileSchema = z.object({
  name: z.string().min(1, "Введите название компании").max(255),
  inn: z.string().min(1, "Введите ИНН").max(12),
  description: z.string().max(1000).optional(),
});

type ProfileForm = z.infer<typeof profileSchema>;
type Company = ProfileForm & { id: string; verification_status: string };

export function ProfilePage() {
  const [error, setError] = useState("");
  const [saved, setSaved] = useState(false);
  const { register, reset, handleSubmit, formState: { errors, isSubmitting } } = useForm<ProfileForm>({
    resolver: zodResolver(profileSchema),
    defaultValues: { name: "", inn: "", description: "" },
  });

  useEffect(() => {
    async function load() {
      try {
        const res = await api.get<Company>("/companies/me");
        reset({ name: res.data.name, inn: res.data.inn, description: res.data.description ?? "" });
      } catch (err: any) {
        if (err.response?.status !== 404) {
          setError("Не удалось загрузить профиль.");
        }
      }
    }
    load();
  }, [reset]);

  async function onSubmit(data: ProfileForm) {
    setError("");
    setSaved(false);
    try {
      await api.patch("/companies/me", data);
      setSaved(true);
    } catch (err: any) {
      if (err.response?.status === 404) {
        try {
          await api.post("/companies", data);
          setSaved(true);
        } catch {
          setError("Не удалось создать профиль компании.");
        }
      } else {
        setError("Не удалось сохранить профиль компании.");
      }
    }
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-1">Профиль</h1>
      <p className="text-sm text-gray-500 mb-6">Информация о компании, используемая для проведения тендеров и подачи заявок.</p>
      <div className="bg-white border border-[#DEE2E6] rounded-md p-6 max-w-2xl">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Название компании</label>
            <input {...register("name")} className="w-full border border-[#DEE2E6] rounded-md px-3 py-2 text-sm focus:outline-none focus:border-[#D9480F]" />
            {errors.name && <p className="text-red-500 text-xs mt-1">{errors.name.message}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">ИНН</label>
            <input {...register("inn")} className="w-full border border-[#DEE2E6] rounded-md px-3 py-2 text-sm focus:outline-none focus:border-[#D9480F]" />
            {errors.inn && <p className="text-red-500 text-xs mt-1">{errors.inn.message}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Описание</label>
            <textarea {...register("description")} rows={4} className="w-full border border-[#DEE2E6] rounded-md px-3 py-2 text-sm focus:outline-none focus:border-[#D9480F]" />
            {errors.description && <p className="text-red-500 text-xs mt-1">{errors.description.message}</p>}
          </div>
          {error && <p className="text-red-500 text-sm">{error}</p>}
          {saved && <p className="text-green-600 text-sm">Профиль сохранен.</p>}
          <button type="submit" disabled={isSubmitting} className="bg-[#D9480F] text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-[#c13e0d] disabled:opacity-50">
            {isSubmitting ? "Сохранение..." : "Сохраните изменения"}
          </button>
        </form>
      </div>
    </div>
  );
}