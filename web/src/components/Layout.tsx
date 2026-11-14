import { Bot, FileText, LayoutDashboard, LogOut, User } from "lucide-react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { clearToken, getEmail } from "../lib/auth";

const linkClass = ({ isActive }: { isActive: boolean }) =>
  `flex h-10 items-center gap-2 rounded-md px-3 text-sm font-medium ${isActive ? "border border-[#DEE2E6] bg-[#F8F9FA]" : "hover:bg-gray-50"}`;

export function Layout() {
  const navigate = useNavigate();
  const email = getEmail();
  function logout(): void { clearToken(); navigate("/login"); }

  return <div className="flex min-h-screen bg-[#F8F9FA]">
    <aside className="fixed inset-y-0 left-0 w-[240px] border-r border-[#DEE2E6] bg-white">
      <div className="flex h-[64px] items-center border-b border-[#DEE2E6] px-5"><span className="text-[17px] font-semibold">TenderTruck</span></div>
      <nav className="space-y-1 p-3">
        <NavLink to="/dashboard" className={linkClass}><LayoutDashboard size={16} /> Дашборд</NavLink>
        <NavLink to="/tenders" className={linkClass}><FileText size={16} /> Тендеры</NavLink>
        <NavLink to="/auto-bids" className={linkClass}><Bot size={16} /> Авто-брокер</NavLink>
        <NavLink to="/profile" className={linkClass}><User size={16} /> Профиль</NavLink>
      </nav>
    </aside>
    <div className="ml-[240px] flex-1">
      <header className="flex h-16 items-center justify-between border-b border-[#DEE2E6] bg-white px-6"><div className="text-sm font-medium text-gray-700">Операции</div><div className="flex items-center gap-4"><span className="text-sm text-gray-500">{email}</span><button onClick={logout} className="flex items-center gap-1 text-sm text-gray-600 hover:text-black"><LogOut size={16} /> Выйти</button></div></header>
      <main className="p-6"><Outlet /></main>
    </div>
  </div>;
}
