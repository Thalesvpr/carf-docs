import * as React from "react";
import { View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { Toast, type ToastProps, type ToastVariant } from "@/components/ui/Toast";

interface ToastConfig {
  message: string;
  variant?: ToastVariant;
  duration?: number;
  action?: {
    label: string;
    onPress: () => void;
  };
}

interface ToastContextValue {
  show: (config: ToastConfig) => string;
  dismiss: (id: string) => void;
  dismissAll: () => void;
}

const ToastContext = React.createContext<ToastContextValue | null>(null);

export function useToast() {
  const context = React.useContext(ToastContext);
  if (!context) {
    throw new Error("useToast must be used within a ToastProvider");
  }
  return context;
}

interface ToastState extends ToastConfig {
  id: string;
}

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = React.useState<ToastState[]>([]);
  const insets = useSafeAreaInsets();

  const show = React.useCallback((config: ToastConfig): string => {
    const id = Math.random().toString(36).substring(2, 9);
    setToasts((prev) => [...prev, { ...config, id }]);
    return id;
  }, []);

  const dismiss = React.useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const dismissAll = React.useCallback(() => {
    setToasts([]);
  }, []);

  const value = React.useMemo(
    () => ({ show, dismiss, dismissAll }),
    [show, dismiss, dismissAll]
  );

  return (
    <ToastContext.Provider value={value}>
      {children}
      <View
        style={{ top: insets.top + 8 }}
        className="absolute left-0 right-0 z-50 items-center"
        pointerEvents="box-none"
      >
        {toasts.map((toast) => (
          <View key={toast.id} className="mb-2">
            <Toast
              id={toast.id}
              message={toast.message}
              variant={toast.variant}
              duration={toast.duration}
              action={toast.action}
              onDismiss={dismiss}
            />
          </View>
        ))}
      </View>
    </ToastContext.Provider>
  );
}
