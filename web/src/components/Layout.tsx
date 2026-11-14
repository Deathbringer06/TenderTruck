import { LogOut, FileText, User } from "lucide-react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { clearToken, getEmail } from "../lib/auth";

export function Layout() {
  const navigate = useNavigate();
  const email = getEmail();

  function logout(): void {
    clearToken();
    navigate("/login");
  }

  return (
    <div className="min-h-screen bg-[#F8F9FA] flex">
      <aside className="fixed inset-y-0 left-0 w-[240px] border-r border-[#DEE2E6] bg-white">
        <div className="flex h-[64px] items-center border-b border-[#DEE2E6] px-5">
          <span className="text-[17px] font-semibold">TenderTruck</span>
        </div>
        <nav className="p-3 space-y-1">
          <NavLink to="/tenders" className={({isActive}) => `flex h-10 items-center gap-2 rounded-md px-3 text-sm font-medium ${isActive ? "bg-[#F8F9FA] border border-[#DEE2E6]" : "hover:bg-gray-50"}`}>
            <FileText size={16} /> Тендеры
          </NavLink>
          <NavLink to="/profile" className={({isActive}) => `flex h-10 items-center gap-2 rounded-md px-3 text-sm font-medium ${isActive ? "bg-[#F8F9FA] border border-[#DEE2E6]" : "hover:bg-gray-50"}`}>
            <User size={16} /> Профиль
          </NavLink>
        </nav>
      </aside>
      <div className="flex-1 ml-[240px]">
        <header className="h-16 border-b border-[#DEE2E6] bg-white flex items-center justify-between px-6">
          <div className="text-sm font-medium text-gray-700">Операции</div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-500">{email}</span>
            <button onClick={logout} className="flex items-center gap-1 text-sm text-gray-600 hover:text-black">
              <LogOut size={16} /> Выйти
            </button>
          </div>
        </header>
        <main className="p-6"><Outlet /></main>
      </div>
    </div>
  );
}