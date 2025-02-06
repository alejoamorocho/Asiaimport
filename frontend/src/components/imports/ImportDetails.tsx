import React from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../ui/table';
import { Badge } from '../ui/badge';
import { Card } from '../ui/card';
import { api } from '@/lib/api';

interface ImportItem {
  id: number;
  row_number: number;
  status: string;
  error_message: string;
  product: {
    id: number;
    name: string;
  } | null;
  raw_data: Record<string, any>;
}

interface ImportDetailsProps {
  importId: number;
}

const statusColors = {
  pending: 'bg-yellow-100 text-yellow-800',
  success: 'bg-green-100 text-green-800',
  error: 'bg-red-100 text-red-800',
};

export function ImportDetails({ importId }: ImportDetailsProps) {
  const { data: items, isLoading } = useQuery({
    queryKey: ['import-items', importId],
    queryFn: async () => {
      const response = await api.get<{ results: ImportItem[] }>(
        `/imports/${importId}/items/`
      );
      return response.data.results;
    },
  });

  if (isLoading) {
    return <div>Cargando detalles...</div>;
  }

  const hasErrors = items?.some((item) => item.status === 'error');

  return (
    <Card className="p-6">
      <div className="space-y-6">
        <div>
          <h3 className="text-xl font-bold">Detalles de la Importación</h3>
          <p className="text-sm text-gray-500">
            Resultados del procesamiento por fila
          </p>
        </div>

        {hasErrors && (
          <div className="rounded-md bg-red-50 p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg
                  className="h-5 w-5 text-red-400"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">
                  Se encontraron errores durante la importación
                </h3>
                <p className="mt-2 text-sm text-red-700">
                  Revisa los detalles de cada fila para más información.
                </p>
              </div>
            </div>
          </div>
        )}

        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Fila</TableHead>
              <TableHead>Estado</TableHead>
              <TableHead>Producto</TableHead>
              <TableHead>Datos</TableHead>
              <TableHead>Error</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {items?.map((item) => (
              <TableRow key={item.id}>
                <TableCell>{item.row_number}</TableCell>
                <TableCell>
                  <Badge className={statusColors[item.status]}>
                    {item.status === 'success' ? 'Éxito' : 
                     item.status === 'error' ? 'Error' : 'Pendiente'}
                  </Badge>
                </TableCell>
                <TableCell>
                  {item.product ? (
                    <span className="text-blue-600 hover:underline">
                      {item.product.name}
                    </span>
                  ) : (
                    <span className="text-gray-500">-</span>
                  )}
                </TableCell>
                <TableCell>
                  <pre className="text-xs whitespace-pre-wrap">
                    {JSON.stringify(item.raw_data, null, 2)}
                  </pre>
                </TableCell>
                <TableCell>
                  {item.error_message ? (
                    <span className="text-red-600 text-sm">
                      {item.error_message}
                    </span>
                  ) : (
                    <span className="text-gray-500">-</span>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </Card>
  );
}
