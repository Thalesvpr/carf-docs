import * as React from "react";
import { View, Text, ScrollView, TouchableOpacity } from "react-native";
import { useNavigation } from "@react-navigation/native";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import {
  FormInput,
  LayoutGrid,
  MessageSquare,
} from "lucide-react-native";
import type { RootStackParamList } from "@/navigation";

type NavigationProp = NativeStackNavigationProp<RootStackParamList, "Home">;

interface CategoryCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  onPress: () => void;
  color: string;
}

function CategoryCard({
  title,
  description,
  icon,
  onPress,
  color,
}: CategoryCardProps) {
  return (
    <TouchableOpacity
      onPress={onPress}
      activeOpacity={0.7}
      className="bg-card rounded-2xl border border-border p-5 mb-4"
    >
      <View className="flex-row items-center">
        <View
          className="h-12 w-12 rounded-xl items-center justify-center mr-4"
          style={{ backgroundColor: color + "20" }}
        >
          {icon}
        </View>
        <View className="flex-1">
          <Text className="text-lg font-semibold text-card-foreground">
            {title}
          </Text>
          <Text className="text-sm text-muted-foreground mt-0.5">
            {description}
          </Text>
        </View>
      </View>
    </TouchableOpacity>
  );
}

export function HomeScreen() {
  const navigation = useNavigation<NavigationProp>();
  const insets = useSafeAreaInsets();

  const categories = [
    {
      title: "Form",
      description: "Button, IconButton, Input, Checkbox, Switch",
      icon: <FormInput size={24} color="#3B5BDB" />,
      route: "FormComponents" as const,
      color: "#3B5BDB",
    },
    {
      title: "Data",
      description: "Avatar, Badge",
      icon: <LayoutGrid size={24} color="#22C55E" />,
      route: "DataComponents" as const,
      color: "#22C55E",
    },
    {
      title: "Feedback",
      description: "Alert, Toast, Dialog",
      icon: <MessageSquare size={24} color="#F59E0B" />,
      route: "FeedbackComponents" as const,
      color: "#F59E0B",
    },
  ];

  return (
    <ScrollView
      className="flex-1 bg-background"
      contentContainerStyle={{
        paddingTop: insets.top + 16,
        paddingBottom: insets.bottom + 16,
        paddingHorizontal: 16,
      }}
    >
      {/* Header */}
      <View className="mb-8">
        <Text className="text-3xl font-bold text-foreground">
          @carf/ui-native
        </Text>
        <Text className="text-base text-muted-foreground mt-2">
          Biblioteca de componentes React Native baseada em React Native
          Reusables com NativeWind.
        </Text>
      </View>

      {/* Categories */}
      <Text className="text-lg font-semibold text-foreground mb-4">
        Componentes
      </Text>
      {categories.map((category) => (
        <CategoryCard
          key={category.title}
          title={category.title}
          description={category.description}
          icon={category.icon}
          onPress={() => navigation.navigate(category.route)}
          color={category.color}
        />
      ))}

      {/* Footer */}
      <View className="mt-8 pt-6 border-t border-border">
        <Text className="text-sm text-muted-foreground text-center">
          10 componentes | NativeWind v4 | Expo SDK 54
        </Text>
      </View>
    </ScrollView>
  );
}
