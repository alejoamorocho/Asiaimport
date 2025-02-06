import { Loader2 } from 'lucide-react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const sizes = {
  sm: 'h-4 w-4',
  md: 'h-8 w-8',
  lg: 'h-12 w-12',
};

const LoadingSpinner = ({ size = 'md', className = '' }: LoadingSpinnerProps) => {
  return (
    <div className="flex items-center justify-center p-4">
      <Loader2
        className={`animate-spin text-primary-600 ${sizes[size]} ${className}`}
      />
    </div>
  );
};

export default LoadingSpinner;
