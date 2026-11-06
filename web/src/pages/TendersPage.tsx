import { useQuery } from "@tanstack/react-query";
import { api } from "../lib/api";

type Tender = {
  id: string;
  title: string;
  current_price: number;
  deadline: string;
  status: string;
};

export function TendersPage() {
  const { data: tenders, isLoading, isError } = useQuery({
    queryKey: ["tenders"],
    queryFn: async () => (await api.get<Tender[]>("/tenders")).data,
  });

  return (
    <section>
      <div className="mb-5 flex items-center justify-between">
        <h1 className="text-xl font-semibold">Tenders</h1>
      </div>
      <div className="overflow-hidden rounded-control border border-border bg-white">
        {isLoading && <div className="p-5 text-sm text-secondary">Loading tenders...</div>}
        {isError && <div className="p-5 text-sm text-red-700">Unable to load tenders.</div>}
        {!isLoading && !isError && (
          <table className="w-full border-collapse text-left text-sm">
            <thead className="border-b border-border bg-[#f7f8f9] text-secondary">
              <tr>
                <th className="px-4 py-3 font-medium">ID</th>
                <th className="px-4 py-3 font-medium">Title</th>
                <th className="px-4 py-3 font-medium">Price</th>
                <th className="px-4 py-3 font-medium">Deadline</th>
                <th className="px-4 py-3 font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              {tenders?.map((tender) => (
                <tr key={tender.id} className="border-b border-border last:border-b-0 hover:bg-[#fafafa]">
                  <td className="px-4 py-3 font-mono text-xs text-secondary">
                    {tender.id.slice(0, 8)}
                  </td>
                  <td className="px-4 py-3 font-medium">{tender.title}</td>
                  <td className="px-4 py-3 font-mono tabular-nums">
                    {(tender.current_price / 100).toFixed(2)}
                  </td>
                  <td className="px-4 py-3 font-mono text-xs">
                    {new Date(tender.deadline).toLocaleString()}
                  </td>
                  <td className="px-4 py-3">
                    <span className="rounded-control border border-border px-2 py-1 text-xs">{tender.status}</span>
                  </td>
                </tr>
              ))}
              {tenders?.length === 0 && (
                <tr><td colSpan={5} className="px-4 py-8 text-center text-secondary">No tenders</td></tr>
              )}
            </tbody>
          </table>
        )}
      </div>
    </section>
  );
}
