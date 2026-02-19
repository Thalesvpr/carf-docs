import * as React from "react";
import { View, Text, ScrollView } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import {
  Alert,
  Button,
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  Input,
} from "@/components/ui";
import { useToast } from "@/hooks/useToast";

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

export function FeedbackComponentsScreen() {
  const insets = useSafeAreaInsets();
  const toast = useToast();
  const [dialogOpen, setDialogOpen] = React.useState(false);
  const [confirmDialogOpen, setConfirmDialogOpen] = React.useState(false);

  return (
    <ScrollView
      className="flex-1 bg-background"
      contentContainerStyle={{
        paddingTop: 16,
        paddingBottom: insets.bottom + 16,
        paddingHorizontal: 16,
      }}
    >
      {/* Alert Section */}
      <Section title="Alert">
        <Subsection title="Variants">
          <View className="gap-3">
            <Alert
              variant="default"
              title="Informacao"
              description="Esta e uma mensagem informativa para o usuario."
            />
            <Alert
              variant="destructive"
              title="Erro"
              description="Ocorreu um erro ao processar sua solicitacao."
            />
            <Alert
              variant="warning"
              title="Atencao"
              description="Esta acao pode ter consequencias irreversiveis."
            />
            <Alert
              variant="success"
              title="Sucesso"
              description="Operacao realizada com sucesso!"
            />
          </View>
        </Subsection>

        <Subsection title="Closable">
          <Alert
            variant="default"
            title="Notificacao"
            description="Este alerta pode ser fechado clicando no X."
            closable
            onClose={() => toast.show({ message: "Alerta fechado!" })}
          />
        </Subsection>
      </Section>

      {/* Toast Section */}
      <Section title="Toast">
        <Subsection title="Disparar Toasts">
          <View className="flex-row flex-wrap gap-2">
            <Button
              variant="default"
              size="sm"
              onPress={() =>
                toast.show({
                  message: "Mensagem padrao",
                  variant: "default",
                })
              }
            >
              Default
            </Button>
            <Button
              variant="destructive"
              size="sm"
              onPress={() =>
                toast.show({
                  message: "Erro ao salvar!",
                  variant: "destructive",
                })
              }
            >
              Destructive
            </Button>
            <Button
              variant="outline"
              size="sm"
              onPress={() =>
                toast.show({
                  message: "Atencao: verifique os dados",
                  variant: "warning",
                })
              }
            >
              Warning
            </Button>
            <Button
              variant="secondary"
              size="sm"
              onPress={() =>
                toast.show({
                  message: "Salvo com sucesso!",
                  variant: "success",
                })
              }
            >
              Success
            </Button>
          </View>
        </Subsection>

        <Subsection title="With Action">
          <Button
            variant="outline"
            size="sm"
            onPress={() =>
              toast.show({
                message: "Item excluido",
                variant: "default",
                action: {
                  label: "Desfazer",
                  onPress: () =>
                    toast.show({
                      message: "Acao desfeita!",
                      variant: "success",
                    }),
                },
              })
            }
          >
            Toast com Acao
          </Button>
        </Subsection>
      </Section>

      {/* Dialog Section */}
      <Section title="Dialog">
        <Subsection title="Basic Dialog">
          <Button variant="outline" onPress={() => setDialogOpen(true)}>
            Abrir Dialog
          </Button>
          <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Titulo do Dialog</DialogTitle>
                <DialogDescription>
                  Esta e a descricao do dialog. Voce pode adicionar qualquer
                  conteudo aqui.
                </DialogDescription>
              </DialogHeader>
              <View className="py-4">
                <Input label="Nome" placeholder="Digite seu nome" />
              </View>
              <DialogFooter>
                <Button
                  variant="outline"
                  size="sm"
                  onPress={() => setDialogOpen(false)}
                >
                  Cancelar
                </Button>
                <Button
                  size="sm"
                  onPress={() => {
                    setDialogOpen(false);
                    toast.show({
                      message: "Salvo com sucesso!",
                      variant: "success",
                    });
                  }}
                >
                  Salvar
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </Subsection>

        <Subsection title="Confirmation Dialog">
          <Button variant="destructive" onPress={() => setConfirmDialogOpen(true)}>
            Excluir Item
          </Button>
          <Dialog open={confirmDialogOpen} onOpenChange={setConfirmDialogOpen}>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Confirmar exclusao</DialogTitle>
                <DialogDescription>
                  Tem certeza que deseja excluir este item? Esta acao nao pode
                  ser desfeita.
                </DialogDescription>
              </DialogHeader>
              <DialogFooter>
                <Button
                  variant="outline"
                  size="sm"
                  onPress={() => setConfirmDialogOpen(false)}
                >
                  Cancelar
                </Button>
                <Button
                  variant="destructive"
                  size="sm"
                  onPress={() => {
                    setConfirmDialogOpen(false);
                    toast.show({
                      message: "Item excluido",
                      variant: "destructive",
                    });
                  }}
                >
                  Excluir
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </Subsection>
      </Section>
    </ScrollView>
  );
}
