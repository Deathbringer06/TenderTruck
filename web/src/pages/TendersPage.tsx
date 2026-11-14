import { useMutation, useQuery } from "@tanstack/react-query";
import { FileDown } from "lucide-react";
import { api } from "../lib/api";

type Tender = { id: string; title: string; current_price: number; deadline: string; status: string };

export function TendersPage() {
  const { data: tenders, isLoading, isError } = useQuery({ queryKey: ["tenders"], queryFn: async () => (await api.get<Tender[]>("/tenders")).data });
  const contractMutation = useMutation({
    mutationFn: async (id: string) => api.get(`/documents/tenders/${id}/contract.pdf`, { responseType: "blob" }),
    onSuccess: (response, id) => {
      const url = URL.createObjectURL(new Blob([response.data], { type: "application/pdf" }));
      const link = document.createElement("a");
      link.href = url;
      link.download = `tender-${id}-contract.pdf`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
    },
  });
  return <section><div className="mb-5 flex items-center justify-between"><h1 className="text-xl font-semibold">Тендеры</h1></div><div className="overflow-hidden rounded-md border border-[#DEE2E6] bg-white">{isLoading && <div className="p-5 text-sm text-gray-500">Загрузка тендеров...</div>}{isError && <div className="p-5 text-sm text-red-500">Не удалось загрузить тендеры.</div>}{!isLoading && !isError && <table className="w-full border-collapse text-left text-sm"><thead className="border-b border-[#DEE2E6] bg-[#F8F9FA] text-gray-500"><tr><th className="px-4 py-3 font-medium">ID</th><th className="px-4 py-3 font-medium">Название</th><th className="px-4 py-3 font-medium">Цена</th><th className="px-4 py-3 font-medium">Срок</th><th className="px-4 py-3 font-medium">Статус</th><th className="px-4 py-3 font-medium">Действия</th></tr></thead><tbody>{tenders?.map((tender) => <tr key={tender.id} className="border-b border-[#DEE2E6] last:border-b-0 hover:bg-[#FAFAFA]"><td className="px-4 py-3 font-mono text-xs text-gray-500">{tender.id.slice(0, 8)}</td><td className="px-4 py-3 font-medium">{tender.title}</td><td className="px-4 py-3 font-mono tabular-nums">{(tender.current_price / 100).toFixed(2)}</td><td className="px-4 py-3 font-mono text-xs">{new Date(tender.deadline).toLocaleString()}</td><td className="px-4 py-3"><span className="rounded-md border border-[#DEE2E6] px-2 py-1 text-xs">{tender.status}</span></td><td className="px-4 py-3">{tender.status === "CLOSED" && <button type="button" onClick={() => contractMutation.mutate(tender.id)} disabled={contractMutation.isPending} className="inline-flex items-center gap-1 text-[#D9480F] hover:underline disabled:opacity-50"><FileDown size={16} /> Договор</button>}{contractMutation.isError && <span className="ml-2 text-xs text-red-500">Ошибка</span>}</td></tr>)}{tenders?.length === 0 && <tr><td colSpan={6} className="px-4 py-8 text-center text-gray-500">Тендеров нет</td></tr>}</tbody></table>}</div></section>;
}
