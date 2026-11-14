import { useQuery } from "@tanstack/react-query";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "../lib/api";

type Carrier = { name?: string; carrier_name?: string; value?: number; count?: number; total?: number; wins?: number };
type DashboardStats = { savings?: number; savings_amount?: number; total_saved?: number; active_tenders?: number; average_bids?: number; average_bid_count?: number; avg_bids_per_tender?: number; top_carrier?: string; top_carriers?: Carrier[] };

export function DashboardPage() {
  const { data, isLoading, isError } = useQuery({ queryKey: ["dashboard"], queryFn: async () => (await api.get<DashboardStats>("/dashboard/stats")).data });
  if (isLoading) return <p className="text-sm text-gray-500">Загрузка дашборда...</p>;
  if (isError) return <p className="text-sm text-red-500">Не удалось загрузить дашборд.</p>;
  const carriers = (data?.top_carriers ?? []).map((carrier) => ({ name: carrier.name ?? carrier.carrier_name ?? "Неизвестно", value: carrier.value ?? carrier.count ?? carrier.total ?? carrier.wins ?? 0 }));
  const cards: [string, string | number][] = [["Экономия", `${(data?.savings ?? data?.savings_amount ?? data?.total_saved ?? 0).toLocaleString("ru-RU")} ₽`], ["Активные тендеры", data?.active_tenders ?? 0], ["Среднее ставок", data?.average_bids ?? data?.average_bid_count ?? data?.avg_bids_per_tender ?? 0], ["Топ перевозчик", data?.top_carrier ?? carriers[0]?.name ?? "—"]];
  return <section className="space-y-6"><div><h1 className="text-2xl font-semibold">Дашборд</h1><p className="mt-1 text-sm text-gray-500">Ключевые показатели тендерной активности.</p></div><div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">{cards.map(([label, value]) => <div key={label} className="rounded-md border border-[#DEE2E6] bg-white p-5"><p className="text-sm text-gray-500">{label}</p><p className="mt-2 text-xl font-semibold">{value}</p></div>)}</div><div className="rounded-md border border-[#DEE2E6] bg-white p-5"><h2 className="mb-4 text-lg font-semibold">Топ перевозчиков</h2><div className="h-[400px]"><ResponsiveContainer width="100%" height="100%"><BarChart data={carriers}><CartesianGrid strokeDasharray="3 3" stroke="#DEE2E6" /><XAxis dataKey="name" /><YAxis allowDecimals={false} /><Tooltip /><Bar dataKey="value" fill="#D9480F" isAnimationActive={false} /></BarChart></ResponsiveContainer></div></div></section>;
}
