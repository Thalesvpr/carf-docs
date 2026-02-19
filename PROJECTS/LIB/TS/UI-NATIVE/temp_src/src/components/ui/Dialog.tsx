import * as React from "react";
import {
  View,
  Text,
  Modal,
  TouchableOpacity,
  TouchableWithoutFeedback,
  Animated,
  Dimensions,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import { X } from "lucide-react-native";
import { cn } from "@/lib/utils";

const { width: SCREEN_WIDTH } = Dimensions.get("window");

interface DialogContextValue {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

const DialogContext = React.createContext<DialogContextValue | null>(null);

function useDialogContext() {
  const context = React.useContext(DialogContext);
  if (!context) {
    throw new Error("Dialog components must be used within a Dialog");
  }
  return context;
}

// Root Dialog
interface DialogProps {
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  children: React.ReactNode;
}

function Dialog({ open = false, onOpenChange, children }: DialogProps) {
  const handleOpenChange = React.useCallback(
    (value: boolean) => {
      onOpenChange?.(value);
    },
    [onOpenChange]
  );

  return (
    <DialogContext.Provider value={{ open, onOpenChange: handleOpenChange }}>
      {children}
    </DialogContext.Provider>
  );
}

// Trigger
interface DialogTriggerProps {
  children: React.ReactElement;
  asChild?: boolean;
}

function DialogTrigger({ children, asChild }: DialogTriggerProps) {
  const { onOpenChange } = useDialogContext();

  if (asChild) {
    return React.cloneElement(children, {
      onPress: () => onOpenChange(true),
    } as React.Attributes & { onPress: () => void });
  }

  return (
    <TouchableOpacity onPress={() => onOpenChange(true)}>
      {children}
    </TouchableOpacity>
  );
}

// Content
interface DialogContentProps {
  children: React.ReactNode;
  className?: string;
}

function DialogContent({ children, className }: DialogContentProps) {
  const { open, onOpenChange } = useDialogContext();
  const opacity = React.useRef(new Animated.Value(0)).current;
  const scale = React.useRef(new Animated.Value(0.95)).current;

  React.useEffect(() => {
    if (open) {
      Animated.parallel([
        Animated.timing(opacity, {
          toValue: 1,
          duration: 200,
          useNativeDriver: true,
        }),
        Animated.spring(scale, {
          toValue: 1,
          tension: 50,
          friction: 8,
          useNativeDriver: true,
        }),
      ]).start();
    }
  }, [open]);

  return (
    <Modal
      visible={open}
      transparent
      animationType="none"
      onRequestClose={() => onOpenChange(false)}
    >
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        className="flex-1"
      >
        <TouchableWithoutFeedback onPress={() => onOpenChange(false)}>
          <Animated.View
            style={{ opacity }}
            className="flex-1 justify-center items-center bg-black/50 px-4"
          >
            <TouchableWithoutFeedback>
              <Animated.View
                style={{ transform: [{ scale }], width: SCREEN_WIDTH - 48 }}
                className={cn(
                  "bg-background rounded-2xl p-6 shadow-xl max-w-lg",
                  className
                )}
              >
                {children}
                <TouchableOpacity
                  onPress={() => onOpenChange(false)}
                  className="absolute top-4 right-4 p-1"
                  hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
                >
                  <X size={20} color="#9CA3AF" />
                </TouchableOpacity>
              </Animated.View>
            </TouchableWithoutFeedback>
          </Animated.View>
        </TouchableWithoutFeedback>
      </KeyboardAvoidingView>
    </Modal>
  );
}

// Header
interface DialogHeaderProps {
  children: React.ReactNode;
  className?: string;
}

function DialogHeader({ children, className }: DialogHeaderProps) {
  return <View className={cn("mb-4", className)}>{children}</View>;
}

// Title
interface DialogTitleProps {
  children: React.ReactNode;
  className?: string;
}

function DialogTitle({ children, className }: DialogTitleProps) {
  return (
    <Text className={cn("text-xl font-semibold text-foreground", className)}>
      {children}
    </Text>
  );
}

// Description
interface DialogDescriptionProps {
  children: React.ReactNode;
  className?: string;
}

function DialogDescription({ children, className }: DialogDescriptionProps) {
  return (
    <Text className={cn("text-sm text-muted-foreground mt-1", className)}>
      {children}
    </Text>
  );
}

// Footer
interface DialogFooterProps {
  children: React.ReactNode;
  className?: string;
}

function DialogFooter({ children, className }: DialogFooterProps) {
  return (
    <View className={cn("flex-row justify-end gap-2 mt-6", className)}>
      {children}
    </View>
  );
}

// Close
interface DialogCloseProps {
  children: React.ReactElement;
  asChild?: boolean;
}

function DialogClose({ children, asChild }: DialogCloseProps) {
  const { onOpenChange } = useDialogContext();

  if (asChild) {
    return React.cloneElement(children, {
      onPress: () => onOpenChange(false),
    } as React.Attributes & { onPress: () => void });
  }

  return (
    <TouchableOpacity onPress={() => onOpenChange(false)}>
      {children}
    </TouchableOpacity>
  );
}

export {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogClose,
};
