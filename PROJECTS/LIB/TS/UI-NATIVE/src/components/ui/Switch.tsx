import * as React from "react";
import {
  TouchableOpacity,
  View,
  Text,
  Animated,
  Easing,
} from "react-native";
import { cn } from "@/lib/utils";

export interface SwitchProps {
  checked?: boolean;
  onCheckedChange?: (checked: boolean) => void;
  disabled?: boolean;
  label?: string;
  className?: string;
}

const Switch = React.forwardRef<View, SwitchProps>(
  (
    { checked = false, onCheckedChange, disabled = false, label, className },
    ref
  ) => {
    const translateX = React.useRef(new Animated.Value(checked ? 20 : 2)).current;

    React.useEffect(() => {
      Animated.timing(translateX, {
        toValue: checked ? 20 : 2,
        duration: 200,
        easing: Easing.bezier(0.4, 0, 0.2, 1),
        useNativeDriver: true,
      }).start();
    }, [checked, translateX]);

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
        activeOpacity={0.8}
        className={cn(
          "flex-row items-center",
          disabled && "opacity-50",
          className
        )}
        accessibilityRole="switch"
        accessibilityState={{ checked, disabled }}
      >
        <View
          className={cn(
            "h-7 w-12 rounded-full p-0.5",
            checked ? "bg-primary" : "bg-muted"
          )}
        >
          <Animated.View
            style={{ transform: [{ translateX }] }}
            className="h-6 w-6 rounded-full bg-white shadow-sm"
          />
        </View>
        {label && (
          <Text className="text-base text-foreground ml-3">{label}</Text>
        )}
      </TouchableOpacity>
    );
  }
);

Switch.displayName = "Switch";

export { Switch };
