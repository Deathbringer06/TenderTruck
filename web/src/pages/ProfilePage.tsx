import { useEffect, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { api } from "../lib/api";

const profileSchema = z.object({ name: z.string().min(1, "Введите название компании").max(255), inn: z.string().min(1, "Введите ИНН").max(12), description: z.string().max(1000).optional() });
type ProfileForm = z.infer<typeof profileSchema>;
type Company = ProfileForm & { id: string; verification_status: string };
type ScoringResult = { risk: "LOW" | "MEDIUM" | "HIGH"; reason: string };

export function ProfilePage() {
  const [error, setError] = useState("");
  const [saved, setSaved] = useState(false);
  const [inn, setInn] = useState("");
  const { register, reset, handleSubmit, formState: { errors, isSubmitting } } = useForm<ProfileForm>({ resolver: zodResolver(profileSchema), defaultValues: { name: "", inn: "", description: "" } });
  const scoringMutation = useMutation({ mutationFn: async (value: string) => (await api.get<ScoringResult>(`/scoring/check?inn=${encodeURIComponent(value)}`)).data });

  useEffect(() => { void (async () => { try { const res = await api.get<Company>("/companies/me"); reset({ name: res.data.name, inn: res.data.inn, description: res.data.description ?? "" }); setInn(res.data.inn); } catch (err: any) { if (err.response?.status !== 404) setError("Не удалось загрузить профиль."); } })(); }, [reset]);
  async function onSubmit(data: ProfileForm) { setError(""); setSaved(false); try { await api.patch("/companies/me", data); setSaved(true); } catch (err: any) { if (err.response?.status === 404) { try { await api.post("/companies", data); setSaved(true); } catch { setError("Не удалось создать профиль компании."); } } else setError("Не удалось сохранить профиль компании."); } }
  const riskClass = scoringMutation.data?.risk === "LOW" ? "border-green-200 bg-green-50 text-green-700" : scoringMutation.data?.risk === "MEDIUM" ? "border-yellow-200 bg-yellow-50 text-yellow-700" : "border-red-200 bg-red-50 text-red-700";
  return <div><h1 className="mb-1 text-2xl font-semibold">Профиль</h1><p className="mb-6 text-sm text-gray-500">Информация о компании.</p><div className="max-w-2xl space-y-6"><div className="rounded-md border border-[#DEE2E6] bg-white p-6"><form onSubmit={handleSubmit(onSubmit)} className="space-y-4"><div><label className="mb-1 block text-sm font-medium">Название компании</label><input {...register("name")} className="w-full rounded-md border border-[#DEE2E6] px-3 py-2 text-sm focus:border-[#D9480F] focus:outline-none" />{errors.name && <p className="mt-1 text-xs text-red-500">{errors.name.message}</p>}</div><div><label className="mb-1 block text-sm font-medium">ИНН</label><input {...register("inn")} className="w-full rounded-md border border-[#DEE2E6] px-3 py-2 text-sm focus:border-[#D9480F] focus:outline-none" />{errors.inn && <p className="mt-1 text-xs text-red-500">{errors.inn.message}</p>}</div><div><label className="mb-1 block text-sm font-medium">Описание</label><textarea {...register("description")} rows={4} className="w-full rounded-md border border-[#DEE2E6] px-3 py-2 text-sm focus:border-[#D9480F] focus:outline-none" />{errors.description && <p className="mt-1 text-xs text-red-500">{errors.description.message}</p>}</div>{error && <p className="text-sm text-red-500">{error}</p>}{saved && <p className="text-sm text-green-600">Профиль сохранён.</p>}<button type="submit" disabled={isSubmitting} className="rounded-md bg-[#D9480F] px-4 py-2 text-sm font-medium text-white hover:bg-[#C13E0D] disabled:opacity-50">{isSubmitting ? "Сохранение..." : "Сохранить изменения"}</button></form></div><div className="rounded-md border border-[#DEE2E6] bg-white p-6"><h2 className="mb-4 text-lg font-semibold">Проверка ИНН</h2><div className="flex gap-3"><input value={inn} onChange={(event) => setInn(event.target.value)} placeholder="Введите ИНН" className="min-w-0 flex-1 rounded-md border border-[#DEE2E6] px-3 py-2 text-sm focus:border-[#D9480F] focus:outline-none" /><button type="button" onClick={() => scoringMutation.mutate(inn)} disabled={!inn || scoringMutation.isPending} className="rounded-md bg-[#D9480F] px-4 py-2 text-sm font-medium text-white disabled:opacity-50">{scoringMutation.isPending ? "Проверка..." : "Проверить"}</button></div>{scoringMutation.isError && <p className="mt-3 text-sm text-red-500">Не удалось проверить ИНН.</p>}{scoringMutation.data && <div className="mt-4"><span className={`inline-flex rounded-md border px-2 py-1 text-xs font-medium ${riskClass}`}>{scoringMutation.data.risk}</span><p className="mt-2 text-sm text-gray-600">{scoringMutation.data.reason}</p></div>}</div></div></div>;
}
