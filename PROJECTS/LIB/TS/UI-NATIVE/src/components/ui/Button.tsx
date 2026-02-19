import * as React from "react";
import {
  Text,
  TouchableOpacity,
  ActivityIndicator,
  type TouchableOpacityProps,
} from "react-native";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "flex-row items-center justify-center rounded-md",
  {
    variants: {
      variant: {
        default: "bg-primary active:opacity-80",
        destructive: "bg-destructive active:opacity-80",
        outline: "border border-input bg-background active:bg-accent",
        secondary: "bg-secondary active:opacity-80",
        ghost: "active:bg-accent",
        link: "underline-offset-4",
      },
      size: {
        default: "h-12 px-4 py-2",
        sm: "h-9 px-3",
        lg: "h-14 px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

const buttonTextVariants = cva("text-base font-medium text-center", {
  variants: {
    variant: {
      default: "text-primary-foreground",
      destructive: "text-destructive-foreground",
      outline: "text-foreground",
      secondary: "text-secondary-foreground",
      ghost: "text-foreground",
      link: "text-primary underline",
    },
    size: {
      default: "text-base",
      sm: "text-sm",
      lg: "text-lg",
      icon: "text-base",
    },
  },
  defaultVariants: {
    variant: "default",
    size: "default",
  },
});

export interface ButtonProps
  extends TouchableOpacityProps,
    VariantProps<typeof buttonVariants> {
  loading?: boolean;
  children?: React.ReactNode;
}

const Button = React.forwardRef<
  React.ElementRef<typeof TouchableOpacity>,
  ButtonProps
>(
  (
    {
      className,
      variant,
      size,
      disabled,
      loading = false,
      children,
      ...props
    },
    ref
  ) => {
    const isDisabled = disabled || loading;

    return (
      <TouchableOpacity
        ref={ref}
        className={cn(
          buttonVariants({ variant, size }),
          isDisabled && "opacity-50",
          className
        )}
        disabled={isDisabled}
        activeOpacity={0.7}
        {...props}
      >
        {loading ? (
          <ActivityIndicator
            size="small"
            color={
              variant === "default" || variant === "destructive"
                ? "#fff"
                : "#374151"
            }
          />
        ) : typeof children === "string" ? (
          <Text className={cn(buttonTextVariants({ variant, size }))}>
            {children}
          </Text>
        ) : (
          children
        )}
      </TouchableOpacity>
    );
  }
);

Button.displayName = "Button";

export { Button, buttonVariants, buttonTextVariants };
