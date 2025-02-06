import React from 'react';
import { Link } from 'react-router-dom';

const NotFound: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4">
      <h1 className="text-4xl font-bold mb-4">404 - Page Not Found</h1>
      <p className="text-gray-600 mb-8">The page you are looking for doesn't exist.</p>
      <Link to="/" className="text-blue-500 hover:text-blue-700">
        Go back to home
      </Link>
    </div>
  );
};

export default NotFound;
