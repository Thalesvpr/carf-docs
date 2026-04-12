import "./global.css";
import * as React from "react";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { ToastProvider } from "@/providers/ToastProvider";
import { AppNavigator } from "@/navigation";

export default function App() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <ToastProvider>
          <AppNavigator />
        </ToastProvider>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}
