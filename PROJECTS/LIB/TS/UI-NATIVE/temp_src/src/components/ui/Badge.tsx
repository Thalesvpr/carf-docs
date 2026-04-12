import * as React from "react";
import { View, Text } from "react-native";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "flex-row items-center justify-center rounded-full",
  {
    variants: {
      variant: {
        default: "bg-primary",
        secondary: "bg-secondary",
        outline: "border border-border bg-transparent",
        destructive: "bg-destructive",
        warning: "bg-warning",
        success: "bg-success",
      },
      size: {
        sm: "px-2 py-0.5",
        default: "px-2.5 py-0.5",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

const badgeTextVariants = cva("font-medium", {
  variants: {
    variant: {
      default: "text-primary-foreground",
      secondary: "text-secondary-foreground",
      outline: "text-foreground",
      destructive: "text-destructive-foreground",
      warning: "text-warning-foreground",
      success: "text-success-foreground",
    },
    size: {
      sm: "text-xs",
      default: "text-sm",
    },
  },
  defaultVariants: {
    variant: "default",
    size: "default",
  },
});

export interface BadgeProps extends VariantProps<typeof badgeVariants> {
  children?: React.ReactNode;
  count?: number;
  max?: number;
  showZero?: boolean;
  className?: string;
}

const Badge = React.forwardRef<View, BadgeProps>(
  (
    {
      variant,
      size,
      children,
      count,
      max = 99,
      showZero = false,
      className,
    },
    ref
  ) => {
    // Se count for fornecido, usa como contador
    if (count !== undefined) {
      if (count === 0 && !showZero) {
        return null;
      }

      const displayCount = count > max ? `${max}+` : count.toString();

      return (
        <View ref={ref} className={cn(badgeVariants({ variant, size }), className)}>
          <Text className={cn(badgeTextVariants({ variant, size }))}>
            {displayCount}
          </Text>
        </View>
      );
    }

    // Caso contrario, renderiza children
    return (
      <View ref={ref} className={cn(badgeVariants({ variant, size }), className)}>
        {typeof children === "string" ? (
          <Text className={cn(badgeTextVariants({ variant, size }))}>
            {children}
          </Text>
        ) : (
          children
        )}
      </View>
    );
  }
);

Badge.displayName = "Badge";

export { Badge, badgeVariants };
