import React from 'react';
import { useParams } from 'react-router-dom';

const ImportDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-4">Import Details</h1>
      {/* Add your import detail content here */}
    </div>
  );
};

export default ImportDetail;
