import * as React from "react";
import { View, Text, ScrollView } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { Button, IconButton, Input, Checkbox, Switch } from "@/components/ui";
import {
  Plus,
  Trash2,
  Edit3,
  Heart,
  Share2,
  Settings,
  Search,
  Menu,
} from "lucide-react-native";

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

export function FormComponentsScreen() {
  const insets = useSafeAreaInsets();
  const [inputValue, setInputValue] = React.useState("");
  const [checked, setChecked] = React.useState(false);
  const [indeterminate, setIndeterminate] = React.useState(true);
  const [switchOn, setSwitchOn] = React.useState(false);

  return (
    <ScrollView
      className="flex-1 bg-background"
      contentContainerStyle={{
        paddingTop: 16,
        paddingBottom: insets.bottom + 16,
        paddingHorizontal: 16,
      }}
    >
      {/* Button Section */}
      <Section title="Button">
        <Subsection title="Variants">
          <View className="flex-row flex-wrap gap-2">
            <Button variant="default">Default</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="outline">Outline</Button>
            <Button variant="ghost">Ghost</Button>
            <Button variant="destructive">Destructive</Button>
          </View>
        </Subsection>

        <Subsection title="Sizes">
          <View className="flex-row items-center gap-2">
            <Button size="sm">Small</Button>
            <Button size="default">Default</Button>
            <Button size="lg">Large</Button>
          </View>
        </Subsection>

        <Subsection title="States">
          <View className="flex-row gap-2">
            <Button disabled>Disabled</Button>
            <Button loading>Loading</Button>
          </View>
        </Subsection>
      </Section>

      {/* IconButton Section */}
      <Section title="IconButton">
        <Subsection title="Variants">
          <View className="flex-row flex-wrap gap-2">
            <IconButton variant="default" icon={Plus} />
            <IconButton variant="secondary" icon={Edit3} />
            <IconButton variant="outline" icon={Settings} />
            <IconButton variant="ghost" icon={Search} />
            <IconButton variant="destructive" icon={Trash2} />
          </View>
        </Subsection>

        <Subsection title="Sizes">
          <View className="flex-row items-center gap-2">
            <IconButton size="sm" icon={Heart} />
            <IconButton size="default" icon={Heart} />
            <IconButton size="lg" icon={Heart} />
            <IconButton size="xl" icon={Heart} />
          </View>
        </Subsection>

        <Subsection title="States">
          <View className="flex-row gap-2">
            <IconButton icon={Share2} disabled />
            <IconButton icon={Menu} loading />
          </View>
        </Subsection>
      </Section>

      {/* Input Section */}
      <Section title="Input">
        <Subsection title="Default">
          <Input
            placeholder="Digite algo..."
            value={inputValue}
            onChangeText={setInputValue}
          />
        </Subsection>

        <Subsection title="With Label">
          <Input
            label="Email"
            placeholder="email@exemplo.com"
            keyboardType="email-address"
          />
        </Subsection>

        <Subsection title="With Error">
          <Input
            label="Senha"
            placeholder="Digite sua senha"
            secureTextEntry
            error="Senha deve ter pelo menos 8 caracteres"
          />
        </Subsection>

        <Subsection title="Disabled">
          <Input
            label="Campo desabilitado"
            placeholder="Nao editavel"
            editable={false}
            value="Valor fixo"
          />
        </Subsection>
      </Section>

      {/* Checkbox Section */}
      <Section title="Checkbox">
        <Subsection title="States">
          <View className="gap-3">
            <Checkbox
              checked={checked}
              onCheckedChange={setChecked}
              label="Checkbox interativo"
            />
            <Checkbox checked={true} label="Checked" />
            <Checkbox checked={false} label="Unchecked" />
            <Checkbox
              indeterminate={indeterminate}
              onCheckedChange={() => setIndeterminate(false)}
              label="Indeterminate"
            />
            <Checkbox disabled label="Disabled" />
            <Checkbox disabled checked label="Disabled checked" />
          </View>
        </Subsection>
      </Section>

      {/* Switch Section */}
      <Section title="Switch">
        <Subsection title="States">
          <View className="gap-4">
            <Switch
              checked={switchOn}
              onCheckedChange={setSwitchOn}
              label="Switch interativo"
            />
            <Switch checked={true} label="On" />
            <Switch checked={false} label="Off" />
            <Switch disabled label="Disabled off" />
            <Switch disabled checked label="Disabled on" />
          </View>
        </Subsection>
      </Section>
    </ScrollView>
  );
}
