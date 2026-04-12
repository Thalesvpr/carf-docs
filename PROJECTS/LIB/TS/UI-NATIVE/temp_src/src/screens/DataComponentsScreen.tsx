import * as React from "react";
import { View, Text, ScrollView } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { Avatar, Badge } from "@/components/ui";

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <View className="mb-8">
      <Text className="text-lg font-semibold text-foreground mb-4">
        {title}
      </Text>
      {children}
    </View>
  );
}

function Subsection({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <View className="mb-4">
      <Text className="text-sm font-medium text-muted-foreground mb-2">
        {title}
      </Text>
      {children}
    </View>
  );
}

export function DataComponentsScreen() {
  const insets = useSafeAreaInsets();

  return (
    <ScrollView
      className="flex-1 bg-background"
      contentContainerStyle={{
        paddingTop: 16,
        paddingBottom: insets.bottom + 16,
        paddingHorizontal: 16,
      }}
    >
      {/* Avatar Section */}
      <Section title="Avatar">
        <Subsection title="Sizes">
          <View className="flex-row items-end gap-4">
            <View className="items-center">
              <Avatar size="sm" fallback="Ana Silva" />
              <Text className="text-xs text-muted-foreground mt-2">sm</Text>
            </View>
            <View className="items-center">
              <Avatar size="default" fallback="Bruno Costa" />
              <Text className="text-xs text-muted-foreground mt-2">default</Text>
            </View>
            <View className="items-center">
              <Avatar size="lg" fallback="Carlos Dias" />
              <Text className="text-xs text-muted-foreground mt-2">lg</Text>
            </View>
          </View>
        </Subsection>

        <Subsection title="With Status Indicator">
          <View className="flex-row items-center gap-4">
            <View className="items-center">
              <Avatar fallback="Maria" status="online" />
              <Text className="text-xs text-muted-foreground mt-2">Online</Text>
            </View>
            <View className="items-center">
              <Avatar fallback="Jose" status="offline" />
              <Text className="text-xs text-muted-foreground mt-2">Offline</Text>
            </View>
            <View className="items-center">
              <Avatar fallback="Pedro" status="busy" />
              <Text className="text-xs text-muted-foreground mt-2">Busy</Text>
            </View>
            <View className="items-center">
              <Avatar fallback="Laura" status="away" />
              <Text className="text-xs text-muted-foreground mt-2">Away</Text>
            </View>
          </View>
        </Subsection>

        <Subsection title="Fallback Colors (by name)">
          <View className="flex-row flex-wrap gap-2">
            <Avatar fallback="Alice" />
            <Avatar fallback="Bob" />
            <Avatar fallback="Charlie" />
            <Avatar fallback="Diana" />
            <Avatar fallback="Eduardo" />
            <Avatar fallback="Fernanda" />
            <Avatar fallback="Gabriel" />
            <Avatar fallback="Helena" />
          </View>
        </Subsection>
      </Section>

      {/* Badge Section */}
      <Section title="Badge">
        <Subsection title="Variants">
          <View className="flex-row flex-wrap gap-2">
            <Badge variant="default">Default</Badge>
            <Badge variant="secondary">Secondary</Badge>
            <Badge variant="outline">Outline</Badge>
            <Badge variant="destructive">Destructive</Badge>
            <Badge variant="warning">Warning</Badge>
            <Badge variant="success">Success</Badge>
          </View>
        </Subsection>

        <Subsection title="Sizes">
          <View className="flex-row items-center gap-2">
            <Badge size="sm">Small</Badge>
            <Badge size="default">Default</Badge>
          </View>
        </Subsection>

        <Subsection title="As Counter">
          <View className="flex-row items-center gap-4">
            <View className="items-center">
              <Badge count={5} />
              <Text className="text-xs text-muted-foreground mt-2">5</Text>
            </View>
            <View className="items-center">
              <Badge count={42} />
              <Text className="text-xs text-muted-foreground mt-2">42</Text>
            </View>
            <View className="items-center">
              <Badge count={150} max={99} />
              <Text className="text-xs text-muted-foreground mt-2">99+</Text>
            </View>
            <View className="items-center">
              <Badge count={0} showZero />
              <Text className="text-xs text-muted-foreground mt-2">0</Text>
            </View>
          </View>
        </Subsection>

        <Subsection title="Counter Variants">
          <View className="flex-row flex-wrap gap-2">
            <Badge count={3} variant="default" />
            <Badge count={7} variant="secondary" />
            <Badge count={12} variant="destructive" />
            <Badge count={5} variant="warning" />
            <Badge count={8} variant="success" />
          </View>
        </Subsection>
      </Section>
    </ScrollView>
  );
}
