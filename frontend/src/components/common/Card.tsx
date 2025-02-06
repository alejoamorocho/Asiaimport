import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  subtitle?: string;
  action?: React.ReactNode;
}

const Card: React.FC<CardProps> = ({
  children,
  className = '',
  title,
  subtitle,
  action,
}) => {
  return (
    <div
      className={`bg-white shadow-sm rounded-lg border border-secondary-200 ${className}`}
    >
      {(title || action) && (
        <div className="px-4 py-5 sm:px-6 border-b border-secondary-200">
          <div className="flex items-center justify-between">
            <div>
              {title && (
                <h3 className="text-lg font-medium leading-6 text-secondary-900">
                  {title}
                </h3>
              )}
              {subtitle && (
                <p className="mt-1 text-sm text-secondary-500">{subtitle}</p>
              )}
            </div>
            {action && <div>{action}</div>}
          </div>
        </div>
      )}
      <div className="px-4 py-5 sm:p-6">{children}</div>
    </div>
  );
};

export default Card;
