import * as React from "react";
import {
  TouchableOpacity,
  ActivityIndicator,
  type TouchableOpacityProps,
} from "react-native";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const iconButtonVariants = cva(
  "items-center justify-center rounded-lg active:opacity-80",
  {
    variants: {
      variant: {
        default: "bg-primary",
        destructive: "bg-destructive",
        outline: "border border-input bg-transparent",
        secondary: "bg-secondary",
        ghost: "bg-transparent",
      },
      size: {
        sm: "h-8 w-8",
        default: "h-10 w-10",
        lg: "h-12 w-12",
        xl: "h-14 w-14",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

const iconColorMap = {
  default: "#FFFFFF",
  destructive: "#FFFFFF",
  outline: "#71717A",
  secondary: "#18181B",
  ghost: "#71717A",
};

const iconSizeMap = {
  sm: 16,
  default: 20,
  lg: 24,
  xl: 28,
};

interface IconButtonProps
  extends Omit<TouchableOpacityProps, "children">,
    VariantProps<typeof iconButtonVariants> {
  icon: React.ComponentType<{ size?: number; color?: string }>;
  loading?: boolean;
  iconColor?: string;
  iconSize?: number;
}

const IconButton = React.forwardRef<
  React.ElementRef<typeof TouchableOpacity>,
  IconButtonProps
>(
  (
    {
      className,
      variant = "default",
      size = "default",
      icon: Icon,
      loading = false,
      disabled,
      iconColor,
      iconSize,
      ...props
    },
    ref
  ) => {
    const defaultIconColor = iconColorMap[variant ?? "default"];
    const defaultIconSize = iconSizeMap[size ?? "default"];

    return (
      <TouchableOpacity
        ref={ref}
        className={cn(
          iconButtonVariants({ variant, size }),
          disabled && "opacity-50",
          className
        )}
        disabled={disabled || loading}
        activeOpacity={0.7}
        {...props}
      >
        {loading ? (
          <ActivityIndicator
            size="small"
            color={iconColor ?? defaultIconColor}
          />
        ) : (
          <Icon
            size={iconSize ?? defaultIconSize}
            color={iconColor ?? defaultIconColor}
          />
        )}
      </TouchableOpacity>
    );
  }
);

IconButton.displayName = "IconButton";

export { IconButton, iconButtonVariants };
