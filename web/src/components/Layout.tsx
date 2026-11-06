import { LogOut, PackageSearch } from "lucide-react";
import { Outlet, useNavigate } from "react-router-dom";
import { clearToken, getEmail } from "../lib/auth";

export function Layout() {
  const navigate = useNavigate();

  function logout(): void {
    clearToken();
    navigate("/login");
  }

  return (
    <div className="min-h-screen bg-[#f5f6f7]">
      <aside className="fixed inset-y-0 left-0 w-[240px] border-r border-border bg-white">
        <div className="flex h-[64px] items-center border-b border-border px-5">
          <PackageSearch size={20} className="mr-2 text-signal" />
          <span className="text-[17px] font-semibold">TenderTruck</span>
        </div>
        <nav className="p-3">
          <a
            href="/tenders"
            className="flex h-10 items-center rounded-control border border-[#e1e3e5] bg-[#f7f8f9] px-3 text-sm font-medium"
          >
            Tenders
          </a>
        </nav>
      </aside>
      <div className="ml-[240px]">
        <header className="flex h-[64px] items-center justify-between border-b border-border bg-white px-6">
          <span className="text-sm font-medium text-secondary">Operations</span>
          <div className="flex items-center gap-3">
            <span className="text-sm text-secondary">{getEmail() ?? "Signed in"}</span>
            <button
            type="button"
            onClick={logout}
            className="flex h-8 items-center gap-2 rounded-control border border-border bg-white px-3 text-sm hover:bg-[#f7f8f9]"
          >
            <LogOut size={16} />
            Log out
          </button>
          </div>
        </header>
        <main className="p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
