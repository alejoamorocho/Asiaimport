import React, { forwardRef } from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helperText, className = '', ...props }, ref) => {
    return (
      <div className="w-full">
        {label && (
          <label
            htmlFor={props.id}
            className="block text-sm font-medium text-secondary-700 mb-1"
          >
            {label}
          </label>
        )}
        <div className="relative">
          <input
            ref={ref}
            className={`
              block w-full rounded-md border-secondary-300 shadow-sm
              focus:border-primary-500 focus:ring-primary-500 sm:text-sm
              ${error ? 'border-red-300' : 'border-secondary-300'}
              ${
                error
                  ? 'focus:border-red-500 focus:ring-red-500'
                  : 'focus:border-primary-500 focus:ring-primary-500'
              }
              ${props.disabled ? 'bg-secondary-100 cursor-not-allowed' : ''}
              ${className}
            `}
            {...props}
          />
        </div>
        {(error || helperText) && (
          <p
            className={`mt-1 text-sm ${
              error ? 'text-red-600' : 'text-secondary-500'
            }`}
          >
            {error || helperText}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;
