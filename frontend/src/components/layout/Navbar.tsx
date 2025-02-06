import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../../store';
import { logout } from '../../store/slices/authSlice';
import { Bell, ChevronDown } from 'lucide-react';

const Navbar = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);
  const [isProfileOpen, setIsProfileOpen] = useState(false);

  const handleLogout = () => {
    dispatch(logout());
  };

  const toggleDropdown = () => {
    setIsProfileOpen(!isProfileOpen);
  };

  return (
    <nav className="bg-white border-b border-secondary-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo y Título */}
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <img
                className="h-8 w-auto"
                src="/logo.svg"
                alt="Cosmedical Import"
              />
              <span className="ml-2 text-xl font-semibold text-secondary-900">
                Cosmedical Import
              </span>
            </div>
          </div>

          {/* Menú derecho */}
          <div className="flex items-center">
            {/* Notificaciones */}
            <button 
              className="p-2 rounded-full text-secondary-400 hover:text-secondary-500"
              aria-label="Notificaciones"
              title="Notificaciones"
            >
              <Bell className="h-6 w-6" />
            </button>

            {/* Perfil */}
            <div className="ml-4 relative">
              <button
                id="user-menu-button"
                onClick={toggleDropdown}
                className="flex items-center text-sm text-secondary-700 hover:text-secondary-900"
                role="button"
                aria-controls="user-menu"
                aria-label="Menú de usuario"
                title="Menú de usuario"
              >
                <img
                  className="h-8 w-8 rounded-full"
                  src={user?.avatar || '/default-avatar.png'}
                  alt=""
                />
                <span className="ml-2 text-secondary-700">{user?.username}</span>
                <ChevronDown className="ml-1 h-4 w-4 text-secondary-400" />
              </button>

              {/* Menú desplegable */}
              {isProfileOpen && (
                <div
                  id="user-menu"
                  className="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5"
                  role="menu"
                  aria-orientation="vertical"
                  aria-labelledby="user-menu-button"
                >
                  <div className="py-1" role="none">
                    <Link
                      to="/profile"
                      className="block px-4 py-2 text-sm text-secondary-700 hover:bg-secondary-100"
                      role="menuitem"
                      tabIndex={-1}
                    >
                      Mi Perfil
                    </Link>
                    <Link
                      to="/settings"
                      className="block px-4 py-2 text-sm text-secondary-700 hover:bg-secondary-100"
                      role="menuitem"
                      tabIndex={-1}
                    >
                      Configuración
                    </Link>
                    <Link
                      to="/imports"
                      className="block px-4 py-2 text-sm text-secondary-700 hover:bg-secondary-100"
                      role="menuitem"
                      tabIndex={-1}
                    >
                      Importaciones
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="w-full text-left px-4 py-2 text-sm text-secondary-700 hover:bg-secondary-100"
                      role="menuitem"
                      tabIndex={-1}
                    >
                      Cerrar Sesión
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
