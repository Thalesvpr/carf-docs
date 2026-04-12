import * as React from "react";
import { TouchableOpacity, View, Text } from "react-native";
import { Check, Minus } from "lucide-react-native";
import { cn } from "@/lib/utils";

export interface CheckboxProps {
  checked?: boolean;
  indeterminate?: boolean;
  onCheckedChange?: (checked: boolean) => void;
  disabled?: boolean;
  label?: string;
  className?: string;
}

const Checkbox = React.forwardRef<View, CheckboxProps>(
  (
    {
      checked = false,
      indeterminate = false,
      onCheckedChange,
      disabled = false,
      label,
      className,
    },
    ref
  ) => {
    const handlePress = () => {
      if (!disabled && onCheckedChange) {
        onCheckedChange(!checked);
      }
    };

    return (
      <TouchableOpacity
        ref={ref}
        onPress={handlePress}
        disabled={disabled}
        activeOpacity={0.7}
        className={cn(
          "flex-row items-center",
          disabled && "opacity-50",
          className
        )}
        accessibilityRole="checkbox"
        accessibilityState={{ checked, disabled }}
      >
        <View
          className={cn(
            "h-5 w-5 rounded border-2 items-center justify-center",
            checked || indeterminate
              ? "bg-primary border-primary"
              : "border-input bg-background"
          )}
        >
          {indeterminate ? (
            <Minus size={14} color="#fff" strokeWidth={3} />
          ) : checked ? (
            <Check size={14} color="#fff" strokeWidth={3} />
          ) : null}
        </View>
        {label && (
          <Text className="text-base text-foreground ml-3">{label}</Text>
        )}
      </TouchableOpacity>
    );
  }
);

Checkbox.displayName = "Checkbox";

export { Checkbox };
