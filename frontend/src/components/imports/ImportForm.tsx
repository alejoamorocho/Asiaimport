import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Card } from '../ui/card';
import { useToast } from '../ui/use-toast';
import { api } from '@/lib/api';

const importSchema = z.object({
  file: z.instanceof(File).refine(
    (file) => {
      const validTypes = [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel',
        'text/csv'
      ];
      return validTypes.includes(file.type);
    },
    {
      message: 'El archivo debe ser Excel (.xlsx, .xls) o CSV (.csv)',
    }
  ).refine(
    (file) => file.size <= 10 * 1024 * 1024,
    {
      message: 'El archivo no puede ser mayor a 10MB',
    }
  ),
});

type ImportFormData = z.infer<typeof importSchema>;

export function ImportForm() {
  const { toast } = useToast();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<ImportFormData>({
    resolver: zodResolver(importSchema),
  });

  const onSubmit = async (data: ImportFormData) => {
    try {
      const formData = new FormData();
      formData.append('file', data.file);

      await api.post('/imports/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      toast({
        title: 'Archivo subido correctamente',
        description: 'El archivo se está procesando. Te notificaremos cuando termine.',
      });

      reset();
    } catch (error) {
      toast({
        title: 'Error al subir el archivo',
        description: 'Hubo un error al subir el archivo. Por favor, intenta de nuevo.',
        variant: 'destructive',
      });
    }
  };

  const downloadTemplate = async () => {
    try {
      const response = await api.get('/imports/download_template/', {
        responseType: 'blob',
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'plantilla_importacion.xlsx');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      toast({
        title: 'Error al descargar la plantilla',
        description: 'No se pudo descargar la plantilla. Por favor, intenta de nuevo.',
        variant: 'destructive',
      });
    }
  };

  return (
    <Card className="p-6">
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold">Importar Productos</h2>
          <p className="text-sm text-gray-500">
            Sube un archivo Excel o CSV con los productos a importar.
            Asegúrate de usar la plantilla correcta.
          </p>
        </div>

        <div className="flex items-center gap-4">
          <Button
            type="button"
            variant="outline"
            onClick={downloadTemplate}
          >
            Descargar Plantilla
          </Button>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <Input
              type="file"
              accept=".xlsx,.xls,.csv"
              {...register('file')}
            />
            {errors.file && (
              <p className="mt-1 text-sm text-red-500">
                {errors.file.message}
              </p>
            )}
          </div>

          <Button
            type="submit"
            disabled={isSubmitting}
            className="w-full"
          >
            {isSubmitting ? 'Subiendo...' : 'Importar Productos'}
          </Button>
        </form>
      </div>
    </Card>
  );
}
