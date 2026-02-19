import * as React from "react";
import { View, Text, TouchableOpacity } from "react-native";
import {
  Info,
  AlertTriangle,
  AlertCircle,
  CheckCircle2,
  X,
} from "lucide-react-native";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const alertVariants = cva(
  "w-full rounded-lg border p-4 flex-row",
  {
    variants: {
      variant: {
        default: "border-border bg-background",
        destructive: "border-destructive/50 bg-destructive/10",
        warning: "border-warning/50 bg-warning/10",
        success: "border-success/50 bg-success/10",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

const alertIconColors = {
  default: "#6B7280",
  destructive: "#EF4444",
  warning: "#F59E0B",
  success: "#22C55E",
};

const alertIcons = {
  default: Info,
  destructive: AlertCircle,
  warning: AlertTriangle,
  success: CheckCircle2,
};

export interface AlertProps extends VariantProps<typeof alertVariants> {
  title?: string;
  description?: string;
  icon?: React.ReactNode;
  closable?: boolean;
  onClose?: () => void;
  className?: string;
  children?: React.ReactNode;
}

const Alert = React.forwardRef<View, AlertProps>(
  (
    {
      variant = "default",
      title,
      description,
      icon,
      closable = false,
      onClose,
      className,
      children,
    },
    ref
  ) => {
    const IconComponent = alertIcons[variant || "default"];
    const iconColor = alertIconColors[variant || "default"];

    return (
      <View ref={ref} className={cn(alertVariants({ variant }), className)}>
        <View className="mr-3 mt-0.5">
          {icon || <IconComponent size={20} color={iconColor} />}
        </View>
        <View className="flex-1">
          {title && (
            <Text className="text-base font-semibold text-foreground mb-1">
              {title}
            </Text>
          )}
          {description && (
            <Text className="text-sm text-muted-foreground">{description}</Text>
          )}
          {children}
        </View>
        {closable && (
          <TouchableOpacity
            onPress={onClose}
            className="ml-2 -mt-1 -mr-1 p-1"
            hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
          >
            <X size={18} color="#9CA3AF" />
          </TouchableOpacity>
        )}
      </View>
    );
  }
);

Alert.displayName = "Alert";

export { Alert, alertVariants };
