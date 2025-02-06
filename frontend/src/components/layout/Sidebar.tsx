import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Package,
  FolderOpen,
  FileImport,
  Settings,
  HelpCircle,
} from 'lucide-react';

const navigation = [
  { name: 'Dashboard', to: '/', icon: LayoutDashboard },
  { name: 'Productos', to: '/products', icon: Package },
  { name: 'Categorías', to: '/categories', icon: FolderOpen },
  { name: 'Importaciones', to: '/imports', icon: FileImport },
  { name: 'Unidades', to: '/product-units', icon: Package },
];

const secondaryNavigation = [
  { name: 'Configuración', to: '/settings', icon: Settings },
  { name: 'Ayuda', to: '/help', icon: HelpCircle },
];

const Sidebar = () => {
  return (
    <div className="hidden md:flex md:flex-shrink-0">
      <div className="flex flex-col w-64">
        <div className="flex flex-col flex-grow pt-5 pb-4 overflow-y-auto bg-white border-r border-secondary-200">
          <div className="flex-grow flex flex-col">
            <nav className="flex-1 px-2 space-y-1">
              {navigation.map((item) => (
                <NavLink
                  key={item.name}
                  to={item.to}
                  className={({ isActive }) =>
                    `group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                      isActive
                        ? 'bg-primary-50 text-primary-600'
                        : 'text-secondary-600 hover:bg-primary-50 hover:text-primary-600'
                    }`
                  }
                >
                  <item.icon
                    className="mr-3 flex-shrink-0 h-6 w-6"
                    aria-hidden="true"
                  />
                  {item.name}
                </NavLink>
              ))}
            </nav>

            {/* Navegación secundaria */}
            <div className="mt-auto">
              <div className="border-t border-secondary-200 pt-4">
                <nav className="px-2 space-y-1">
                  {secondaryNavigation.map((item) => (
                    <NavLink
                      key={item.name}
                      to={item.to}
                      className={({ isActive }) =>
                        `group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                          isActive
                            ? 'bg-primary-50 text-primary-600'
                            : 'text-secondary-600 hover:bg-primary-50 hover:text-primary-600'
                        }`
                      }
                    >
                      <item.icon
                        className="mr-3 flex-shrink-0 h-6 w-6"
                        aria-hidden="true"
                      />
                      {item.name}
                    </NavLink>
                  ))}
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
