import React, { useState } from 'react';
import { ImportForm } from '@/components/imports/ImportForm';
import { ImportList } from '@/components/imports/ImportList';
import { ImportDetails } from '@/components/imports/ImportDetails';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';

function ImportsPage() {
  const [selectedImportId, setSelectedImportId] = useState<number | null>(null);

  return (
    <div className="container mx-auto py-8 space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Formulario de importación */}
        <div className="md:col-span-1">
          <ImportForm />
        </div>

        {/* Lista de importaciones */}
        <div className="md:col-span-2">
          <ImportList onViewDetails={setSelectedImportId} />
        </div>
      </div>

      {/* Modal de detalles */}
      <Dialog
        open={selectedImportId !== null}
        onOpenChange={() => setSelectedImportId(null)}
      >
        <DialogContent className="max-w-4xl">
          <DialogHeader>
            <DialogTitle>Detalles de la Importación #{selectedImportId}</DialogTitle>
          </DialogHeader>
          {selectedImportId && <ImportDetails importId={selectedImportId} />}
        </DialogContent>
      </Dialog>
    </div>
  );
}

export default ImportsPage;
