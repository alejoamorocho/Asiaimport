import Card from '../components/common/Card';
import { Package, FileImport, Boxes, AlertTriangle } from 'lucide-react';

const Dashboard = () => {
  // Estos datos deberían venir de la API
  const stats = [
    {
      name: 'Total Productos',
      value: '24',
      icon: Package,
      change: '+4.75%',
      changeType: 'increase',
    },
    {
      name: 'Importaciones Activas',
      value: '3',
      icon: FileImport,
      change: '+54.02%',
      changeType: 'increase',
    },
    {
      name: 'Unidades Disponibles',
      value: '156',
      icon: Boxes,
      change: '-1.39%',
      changeType: 'decrease',
    },
    {
      name: 'Alertas',
      value: '2',
      icon: AlertTriangle,
      change: '-10.34%',
      changeType: 'decrease',
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-secondary-900">Dashboard</h2>
        <p className="mt-1 text-sm text-secondary-500">
          Resumen general del sistema
        </p>
      </div>

      {/* Estadísticas */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.name} className="px-4 py-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <stat.icon
                  className="h-6 w-6 text-primary-600"
                  aria-hidden="true"
                />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-secondary-500 truncate">
                    {stat.name}
                  </dt>
                  <dd>
                    <div className="text-lg font-medium text-secondary-900">
                      {stat.value}
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-4">
              <span
                className={`text-sm font-medium ${
                  stat.changeType === 'increase'
                    ? 'text-green-600'
                    : 'text-red-600'
                }`}
              >
                {stat.change}
              </span>
              <span className="text-sm text-secondary-500"> vs mes anterior</span>
            </div>
          </Card>
        ))}
      </div>

      {/* Actividad Reciente */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <Card
          title="Importaciones Recientes"
          subtitle="Últimas 5 importaciones registradas"
        >
          <div className="space-y-4">
            {/* Aquí irá la lista de importaciones recientes */}
            <p className="text-sm text-secondary-500">
              No hay importaciones recientes
            </p>
          </div>
        </Card>

        <Card
          title="Alertas del Sistema"
          subtitle="Notificaciones y alertas importantes"
        >
          <div className="space-y-4">
            {/* Aquí irá la lista de alertas */}
            <p className="text-sm text-secondary-500">No hay alertas activas</p>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
