import * as React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import {
  HomeScreen,
  FormComponentsScreen,
  DataComponentsScreen,
  FeedbackComponentsScreen,
} from "@/screens";

export type RootStackParamList = {
  Home: undefined;
  FormComponents: undefined;
  DataComponents: undefined;
  FeedbackComponents: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerStyle: {
            backgroundColor: "hsl(0 0% 100%)",
          },
          headerTintColor: "hsl(222.2 84% 4.9%)",
          headerTitleStyle: {
            fontWeight: "600",
          },
          contentStyle: {
            backgroundColor: "hsl(0 0% 100%)",
          },
        }}
      >
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{
            title: "@carf/ui-native",
          }}
        />
        <Stack.Screen
          name="FormComponents"
          component={FormComponentsScreen}
          options={{
            title: "Form Components",
          }}
        />
        <Stack.Screen
          name="DataComponents"
          component={DataComponentsScreen}
          options={{
            title: "Data Components",
          }}
        />
        <Stack.Screen
          name="FeedbackComponents"
          component={FeedbackComponentsScreen}
          options={{
            title: "Feedback Components",
          }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
