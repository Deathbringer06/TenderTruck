import { useState } from 'react'
import { NavLink, Outlet } from 'react-router-dom'

export function CabinetLayout() {
  const [menuOpen, setMenuOpen] = useState(false)
  const token = localStorage.getItem('access_token')
  const role = token?.endsWith('perevozchik') ? 'Перевозчик' : 'Заказчик'

  return (
    <div className="cabinet-shell">
      <header className="topbar">
        <div className="brand-lockup">
          <span className="brand-mark" aria-hidden="true">Т</span>
          <span>ТендерТрак</span>
        </div>
        <button aria-expanded={menuOpen} aria-label={menuOpen ? 'Закрыть меню' : 'Открыть меню'} className="menu-toggle" onClick={() => setMenuOpen((open) => !open)} type="button">
          <span />
          <span />
          <span />
        </button>
        <div className="topbar-user">
          <span className="avatar" aria-hidden="true">Т</span>
          <span>{role}</span>
        </div>
      </header>

      <div className="cabinet-body">
        <aside className={`sidebar${menuOpen ? ' sidebar-open' : ''}`}>
          <span className="sidebar-caption">ЛИЧНЫЙ КАБИНЕТ</span>
          <nav aria-label="Главное меню" className="sidebar-nav">
            <NavLink className={({ isActive }) => `nav-link${isActive ? ' nav-link-active' : ''}`} onClick={() => setMenuOpen(false)} to="/cabinet/profile">
              <span aria-hidden="true" className="nav-icon">◉</span>
              Мой профиль
            </NavLink>
          </nav>
          <div className="sidebar-help">
            <span className="help-icon" aria-hidden="true">?</span>
            <div>
              <strong>Нужна помощь?</strong>
              <p>Мы всегда готовы помочь</p>
            </div>
          </div>
        </aside>
        {menuOpen && <button aria-label="Закрыть меню" className="mobile-backdrop" onClick={() => setMenuOpen(false)} type="button" />}
        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
