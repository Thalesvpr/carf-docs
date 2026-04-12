import * as React from "react";
import {
  View,
  Text,
  TouchableOpacity,
  Animated,
  Dimensions,
} from "react-native";
import { X, CheckCircle2, AlertCircle, Info } from "lucide-react-native";
import { cn } from "@/lib/utils";

const { width: SCREEN_WIDTH } = Dimensions.get("window");

export type ToastVariant = "default" | "destructive" | "warning" | "success";
export type ToastPosition = "top" | "bottom";

export interface ToastProps {
  id: string;
  message: string;
  variant?: ToastVariant;
  duration?: number;
  position?: ToastPosition;
  action?: {
    label: string;
    onPress: () => void;
  };
  onDismiss?: (id: string) => void;
}

const variantStyles = {
  default: "bg-foreground",
  destructive: "bg-destructive",
  warning: "bg-warning",
  success: "bg-success",
};

const variantIcons = {
  default: Info,
  destructive: AlertCircle,
  warning: AlertCircle,
  success: CheckCircle2,
};

export function Toast({
  id,
  message,
  variant = "default",
  duration = 3000,
  action,
  onDismiss,
}: ToastProps) {
  const translateY = React.useRef(new Animated.Value(-100)).current;
  const opacity = React.useRef(new Animated.Value(0)).current;

  React.useEffect(() => {
    // Animate in
    Animated.parallel([
      Animated.spring(translateY, {
        toValue: 0,
        useNativeDriver: true,
        tension: 50,
        friction: 8,
      }),
      Animated.timing(opacity, {
        toValue: 1,
        duration: 200,
        useNativeDriver: true,
      }),
    ]).start();

    // Auto dismiss
    const timer = setTimeout(() => {
      handleDismiss();
    }, duration);

    return () => clearTimeout(timer);
  }, [duration]);

  const handleDismiss = () => {
    Animated.parallel([
      Animated.timing(translateY, {
        toValue: -100,
        duration: 200,
        useNativeDriver: true,
      }),
      Animated.timing(opacity, {
        toValue: 0,
        duration: 200,
        useNativeDriver: true,
      }),
    ]).start(() => {
      onDismiss?.(id);
    });
  };

  const IconComponent = variantIcons[variant];

  return (
    <Animated.View
      style={{
        transform: [{ translateY }],
        opacity,
        width: SCREEN_WIDTH - 32,
      }}
      className={cn(
        "rounded-lg p-4 flex-row items-center mx-4 shadow-lg",
        variantStyles[variant]
      )}
    >
      <IconComponent size={20} color="#fff" />
      <Text className="flex-1 text-white text-sm font-medium ml-3">
        {message}
      </Text>
      {action && (
        <TouchableOpacity
          onPress={() => {
            action.onPress();
            handleDismiss();
          }}
          className="ml-2 px-2 py-1"
        >
          <Text className="text-white text-sm font-semibold underline">
            {action.label}
          </Text>
        </TouchableOpacity>
      )}
      <TouchableOpacity
        onPress={handleDismiss}
        className="ml-2 p-1"
        hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
      >
        <X size={18} color="#fff" />
      </TouchableOpacity>
    </Animated.View>
  );
}

export { Toast as default };
