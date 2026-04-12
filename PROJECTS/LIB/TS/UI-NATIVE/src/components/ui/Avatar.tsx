import * as React from "react";
import { View, Text, Image, type ImageSourcePropType } from "react-native";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const avatarVariants = cva(
  "rounded-full items-center justify-center overflow-hidden bg-muted",
  {
    variants: {
      size: {
        sm: "h-8 w-8",
        default: "h-10 w-10",
        lg: "h-16 w-16",
      },
    },
    defaultVariants: {
      size: "default",
    },
  }
);

const avatarTextVariants = cva("font-semibold text-muted-foreground", {
  variants: {
    size: {
      sm: "text-xs",
      default: "text-sm",
      lg: "text-xl",
    },
  },
  defaultVariants: {
    size: "default",
  },
});

const statusIndicatorVariants = cva(
  "absolute rounded-full border-2 border-background",
  {
    variants: {
      size: {
        sm: "h-2 w-2 -bottom-0 -right-0",
        default: "h-3 w-3 -bottom-0.5 -right-0.5",
        lg: "h-4 w-4 -bottom-0.5 -right-0.5",
      },
      status: {
        online: "bg-success",
        offline: "bg-muted-foreground",
        busy: "bg-destructive",
        away: "bg-warning",
      },
    },
    defaultVariants: {
      size: "default",
    },
  }
);

export interface AvatarProps extends VariantProps<typeof avatarVariants> {
  src?: ImageSourcePropType | string;
  alt?: string;
  fallback?: string;
  status?: "online" | "offline" | "busy" | "away";
  className?: string;
}

function getInitials(name: string): string {
  const words = name.trim().split(/\s+/);
  if (words.length === 1) {
    return words[0].substring(0, 2).toUpperCase();
  }
  return (words[0][0] + words[words.length - 1][0]).toUpperCase();
}

function getColorFromName(name: string): string {
  const colors = [
    "bg-red-500",
    "bg-orange-500",
    "bg-amber-500",
    "bg-yellow-500",
    "bg-lime-500",
    "bg-green-500",
    "bg-emerald-500",
    "bg-teal-500",
    "bg-cyan-500",
    "bg-sky-500",
    "bg-blue-500",
    "bg-indigo-500",
    "bg-violet-500",
    "bg-purple-500",
    "bg-fuchsia-500",
    "bg-pink-500",
    "bg-rose-500",
  ];

  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  return colors[Math.abs(hash) % colors.length];
}

const Avatar = React.forwardRef<View, AvatarProps>(
  ({ size, src, alt, fallback, status, className }, ref) => {
    const [imageError, setImageError] = React.useState(false);

    const imageSource =
      typeof src === "string" ? { uri: src } : src;

    const showFallback = !src || imageError;
    const initials = fallback ? getInitials(fallback) : "?";
    const bgColor = fallback ? getColorFromName(fallback) : "bg-muted";

    return (
      <View ref={ref} className="relative">
        <View
          className={cn(
            avatarVariants({ size }),
            showFallback && bgColor,
            className
          )}
        >
          {!showFallback && imageSource ? (
            <Image
              source={imageSource}
              className="h-full w-full"
              accessibilityLabel={alt}
              onError={() => setImageError(true)}
            />
          ) : (
            <Text className={cn(avatarTextVariants({ size }), "text-white")}>
              {initials}
            </Text>
          )}
        </View>
        {status && (
          <View className={cn(statusIndicatorVariants({ size, status }))} />
        )}
      </View>
    );
  }
);

Avatar.displayName = "Avatar";

export { Avatar, avatarVariants };
