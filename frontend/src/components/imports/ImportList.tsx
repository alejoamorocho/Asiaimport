import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../ui/table';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';
import { useToast } from '../ui/use-toast';
import { api } from '@/lib/api';

interface Import {
  id: number;
  file: string;
  status: string;
  status_display: string;
  processed_rows: number;
  total_rows: number;
  error_log: string;
  progress: number;
  created_by: string;
  created_at: string;
}

const statusColors = {
  pending: 'bg-yellow-100 text-yellow-800',
  processing: 'bg-blue-100 text-blue-800',
  completed: 'bg-green-100 text-green-800',
  failed: 'bg-red-100 text-red-800',
};

export function ImportList() {
  const { toast } = useToast();

  const { data: imports, isLoading, refetch } = useQuery({
    queryKey: ['imports'],
    queryFn: async () => {
      const response = await api.get<{ results: Import[] }>('/imports/');
      return response.data.results;
    },
  });

  const retryImport = async (importId: number) => {
    try {
      await api.post(`/imports/${importId}/retry/`);
      toast({
        title: 'Importación reiniciada',
        description: 'La importación se está procesando nuevamente.',
      });
      refetch();
    } catch (error) {
      toast({
        title: 'Error al reiniciar la importación',
        description: 'No se pudo reiniciar la importación. Por favor, intenta de nuevo.',
        variant: 'destructive',
      });
    }
  };

  const viewDetails = async (importId: number) => {
    try {
      const response = await api.get(`/imports/${importId}/items/`);
      // Aquí podrías abrir un modal o navegar a una página de detalles
      console.log(response.data);
    } catch (error) {
      toast({
        title: 'Error al cargar los detalles',
        description: 'No se pudieron cargar los detalles de la importación.',
        variant: 'destructive',
      });
    }
  };

  if (isLoading) {
    return <div>Cargando importaciones...</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">Historial de Importaciones</h2>
        <p className="text-sm text-gray-500">
          Lista de todas las importaciones realizadas y su estado actual.
        </p>
      </div>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ID</TableHead>
            <TableHead>Archivo</TableHead>
            <TableHead>Estado</TableHead>
            <TableHead>Progreso</TableHead>
            <TableHead>Creado por</TableHead>
            <TableHead>Fecha</TableHead>
            <TableHead>Acciones</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {imports?.map((importItem) => (
            <TableRow key={importItem.id}>
              <TableCell>{importItem.id}</TableCell>
              <TableCell>{importItem.file.split('/').pop()}</TableCell>
              <TableCell>
                <Badge className={statusColors[importItem.status]}>
                  {importItem.status_display}
                </Badge>
              </TableCell>
              <TableCell>
                <div className="space-y-1">
                  <Progress value={importItem.progress} />
                  <p className="text-xs text-gray-500">
                    {importItem.processed_rows} de {importItem.total_rows} filas
                  </p>
                </div>
              </TableCell>
              <TableCell>{importItem.created_by}</TableCell>
              <TableCell>
                {format(new Date(importItem.created_at), 'PPp', { locale: es })}
              </TableCell>
              <TableCell>
                <div className="space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => viewDetails(importItem.id)}
                  >
                    Ver Detalles
                  </Button>
                  {importItem.status === 'failed' && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => retryImport(importItem.id)}
                    >
                      Reintentar
                    </Button>
                  )}
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
