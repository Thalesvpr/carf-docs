import * as React from "react";
import { TextInput, View, Text, type TextInputProps } from "react-native";
import { cn } from "@/lib/utils";

export interface InputProps extends TextInputProps {
  label?: string;
  error?: string;
  containerClassName?: string;
}

const Input = React.forwardRef<TextInput, InputProps>(
  ({ className, label, error, containerClassName, ...props }, ref) => {
    return (
      <View className={cn("w-full", containerClassName)}>
        {label && (
          <Text className="text-sm font-medium text-foreground mb-2">
            {label}
          </Text>
        )}
        <TextInput
          ref={ref}
          className={cn(
            "h-12 w-full rounded-md border bg-background px-3 text-base text-foreground",
            "placeholder:text-muted-foreground",
            error ? "border-destructive" : "border-input",
            "focus:border-primary",
            props.editable === false && "opacity-50 bg-muted",
            className
          )}
          placeholderTextColor="#9CA3AF"
          {...props}
        />
        {error && (
          <Text className="text-sm text-destructive mt-1">{error}</Text>
        )}
      </View>
    );
  }
);

Input.displayName = "Input";

export { Input };
