---
type: leaf
status: review
updated: 2026-02-08
---

# Integracao de Mapas - REURBCAD

Integracao de mapas no aplicativo REURBCAD usando react-native-maps, tile caching offline, renderizacao de poligonos GeoJSON, rastreamento GPS e visualizacao de ortofotos.

## Visao Geral

O mapa e o componente central do REURBCAD, usado para visualizar comunidades, quadras, unidades habitacionais e ortofotos. Funciona offline com tiles pre-baixados e GPS nativo para coleta em campo.

| Capacidade | Biblioteca | Modo Offline |
|-----------|-----------|-------------|
| Renderizacao de mapa | react-native-maps (Google Maps) | Tiles pre-cacheados |
| Ortofotos | TMS/WMS via @carf/geoapi-client | Download previo de pacotes |
| GPS tracking | expo-location | Foreground + Background |
| Poligonos GeoJSON | react-native-maps Polygon/Polyline | Dados locais WatermelonDB |
| Clustering | react-native-map-clustering (supercluster) | Processamento local |
| Geometria | @turf/turf | Calculo local |

## Setup react-native-maps

### Configuracao do Provider

```typescript
// components/Map/MapContainer.tsx
import MapView, { PROVIDER_GOOGLE, Region } from 'react-native-maps';
import { Platform } from 'react-native';

interface MapContainerProps {
  initialRegion: Region;
  children?: React.ReactNode;
  onRegionChange?: (region: Region) => void;
}

export function MapContainer({
  initialRegion,
  children,
  onRegionChange,
}: MapContainerProps) {
  return (
    <MapView
      provider={Platform.OS === 'android' ? PROVIDER_GOOGLE : undefined}
      style={{ flex: 1 }}
      initialRegion={initialRegion}
      onRegionChangeComplete={onRegionChange}
      showsUserLocation
      showsMyLocationButton
      showsCompass
      rotateEnabled={false} // Simplificar UX em campo
      mapType="satellite" // Default para identificar construcoes
      maxZoomLevel={21}
      minZoomLevel={10}
    >
      {children}
    </MapView>
  );
}
```

### Regiao Inicial por Comunidade

```typescript
// hooks/useMapRegion.ts
import { useMemo } from 'react';
import { Region } from 'react-native-maps';
import * as turf from '@turf/turf';
import { Community } from '@/database/models/Community';

export function useMapRegion(community: Community | null): Region {
  return useMemo(() => {
    if (!community?.boundaryGeoJSON) {
      // Fallback: centro do Brasil
      return {
        latitude: -15.7801,
        longitude: -47.9292,
        latitudeDelta: 0.01,
        longitudeDelta: 0.01,
      };
    }

    const geojson = JSON.parse(community.boundaryGeoJSON);
    const bbox = turf.bbox(geojson);
    // bbox = [minLng, minLat, maxLng, maxLat]

    return {
      latitude: (bbox[1] + bbox[3]) / 2,
      longitude: (bbox[0] + bbox[2]) / 2,
      latitudeDelta: (bbox[3] - bbox[1]) * 1.2, // 20% padding
      longitudeDelta: (bbox[2] - bbox[0]) * 1.2,
    };
  }, [community]);
}
```

## Cache de Tiles Offline

### Estrategia de Download

Tiles de mapa base e ortofotos sao baixados como pacotes via @carf/geoapi-client antes da saida a campo. O download e organizado por comunidade e nivel de zoom.

```typescript
// services/tile-cache.ts
import * as FileSystem from 'expo-file-system';
import { geoapiClient } from '@carf/geoapi-client';

interface TilePackage {
  communityId: string;
  zoomLevels: number[]; // ex: [15, 16, 17, 18, 19, 20]
  bbox: [number, number, number, number]; // [minLng, minLat, maxLng, maxLat]
  tileCount: number;
  sizeBytes: number;
}

export async function downloadTilePackage(
  communityId: string,
  bbox: [number, number, number, number],
  onProgress: (percent: number) => void
): Promise<void> {
  const zoomLevels = [15, 16, 17, 18, 19, 20];

  // Solicitar pacote ao backend
  const packageInfo = await geoapiClient.orthofotos.requestTilePackage({
    communityId,
    bbox,
    zoomLevels,
    format: 'mbtiles', // SQLite com tiles compactados
  });

  // Download do arquivo .mbtiles
  const localPath = `${FileSystem.documentDirectory}tiles/${communityId}.mbtiles`;

  const downloadResumable = FileSystem.createDownloadResumable(
    packageInfo.downloadUrl,
    localPath,
    {},
    (downloadProgress) => {
      const percent =
        downloadProgress.totalBytesWritten /
        downloadProgress.totalBytesExpectedToWrite;
      onProgress(percent * 100);
    }
  );

  await downloadResumable.downloadAsync();
}
```

### Estimativa de Tamanho por Zoom

| Zoom | Resolucao | Tiles/km2 | Tamanho/tile | Tamanho/km2 |
|------|----------|----------|-------------|-------------|
| 15 | ~4.8m | ~4 | ~30KB | ~120KB |
| 16 | ~2.4m | ~16 | ~30KB | ~480KB |
| 17 | ~1.2m | ~64 | ~30KB | ~1.9MB |
| 18 | ~0.6m | ~256 | ~30KB | ~7.7MB |
| 19 | ~0.3m | ~1024 | ~25KB | ~25MB |
| 20 | ~0.15m | ~4096 | ~20KB | ~82MB |

Para uma comunidade tipica de 1 km2, o pacote completo (zooms 15-20) ocupa aproximadamente 117 MB. Recomendacao: baixar zooms 15-19 (~35 MB) como padrao, zoom 20 apenas quando necessario.

## Carregamento de Ortofotos (TMS/WMS)

### Online: Tile URL Template

```typescript
// components/Map/OrthophotoOverlay.tsx
import { UrlTile } from 'react-native-maps';

interface OrthophotoOverlayProps {
  tenantId: string;
  communityId: string;
  visible: boolean;
}

export function OrthophotoOverlay({
  tenantId,
  communityId,
  visible,
}: OrthophotoOverlayProps) {
  if (!visible) return null;

  const tileUrl =
    `${GEOAPI_URL}/api/tiles/${tenantId}/${communityId}` +
    `/{z}/{x}/{y}.png?token={accessToken}`;

  return (
    <UrlTile
      urlTemplate={tileUrl}
      maximumZ={20}
      minimumZ={15}
      flipY={false} // TMS padrao
      tileSize={256}
      opacity={0.85}
      zIndex={1}
    />
  );
}
```

### Offline: Tiles Locais

```typescript
// components/Map/OfflineTileOverlay.tsx
import { LocalTile } from 'react-native-maps';
import * as FileSystem from 'expo-file-system';

interface OfflineTileOverlayProps {
  communityId: string;
  visible: boolean;
}

export function OfflineTileOverlay({
  communityId,
  visible,
}: OfflineTileOverlayProps) {
  if (!visible) return null;

  const tilePath = `${FileSystem.documentDirectory}tiles/${communityId}`;

  return (
    <LocalTile
      pathTemplate={`${tilePath}/{z}/{x}/{y}.png`}
      tileSize={256}
      zIndex={1}
    />
  );
}
```

## Renderizacao GeoJSON

### Poligonos de Comunidades e Unidades

```typescript
// components/Map/GeoJSONLayer.tsx
import { Polygon, Polyline, Marker } from 'react-native-maps';

// Cores por tipo de entidade
const LAYER_COLORS = {
  community: { fill: 'rgba(33, 150, 243, 0.15)', stroke: '#2196F3' },
  block: { fill: 'rgba(76, 175, 80, 0.15)', stroke: '#4CAF50' },
  unit: { fill: 'rgba(255, 152, 0, 0.2)', stroke: '#FF9800' },
  unitApproved: { fill: 'rgba(76, 175, 80, 0.3)', stroke: '#4CAF50' },
  unitRejected: { fill: 'rgba(244, 67, 54, 0.3)', stroke: '#F44336' },
};

interface GeoJSONPolygonProps {
  coordinates: number[][];
  type: keyof typeof LAYER_COLORS;
  onPress?: () => void;
}

export function GeoJSONPolygon({
  coordinates,
  type,
  onPress,
}: GeoJSONPolygonProps) {
  const colors = LAYER_COLORS[type];
  const latLngs = coordinates.map(([lng, lat]) => ({
    latitude: lat,
    longitude: lng,
  }));

  return (
    <Polygon
      coordinates={latLngs}
      fillColor={colors.fill}
      strokeColor={colors.stroke}
      strokeWidth={2}
      tappable={!!onPress}
      onPress={onPress}
    />
  );
}
```

### Renderizacao de Multiplas Unidades

```typescript
// components/Map/UnitsLayer.tsx
import { useDatabase } from '@nozbe/watermelondb/hooks';
import { Q } from '@nozbe/watermelondb';
import { Unit } from '@/database/models/Unit';

interface UnitsLayerProps {
  communityId: string;
  visible: boolean;
  onUnitPress: (unitId: string) => void;
}

export function UnitsLayer({ communityId, visible, onUnitPress }: UnitsLayerProps) {
  const database = useDatabase();
  const units = useObservable(
    database.get<Unit>('units')
      .query(Q.where('community_id', communityId))
      .observe()
  );

  if (!visible || !units) return null;

  return (
    <>
      {units.map((unit) => {
        if (!unit.polygonGeoJSON) return null;
        const coords = JSON.parse(unit.polygonGeoJSON).coordinates[0];
        const type = unit.status === 'APPROVED'
          ? 'unitApproved'
          : unit.status === 'REJECTED'
            ? 'unitRejected'
            : 'unit';

        return (
          <GeoJSONPolygon
            key={unit.id}
            coordinates={coords}
            type={type}
            onPress={() => onUnitPress(unit.id)}
          />
        );
      })}
    </>
  );
}
```

## Clustering para Grandes Datasets

Para comunidades com centenas de unidades, clustering agrupa markers proximos em um unico indicador numerico ate o usuario dar zoom.

```typescript
// components/Map/ClusteredMap.tsx
import MapView from 'react-native-maps';
import { ClusterMap } from 'react-native-map-clustering';

export function ClusteredMap({ children, ...props }: MapViewProps) {
  return (
    <ClusterMap
      {...props}
      clusterColor="#FF9800"
      clusterTextColor="#FFF"
      clusterFontFamily="Inter-Bold"
      radius={60} // Raio de agrupamento em pixels
      minZoom={10}
      maxZoom={18} // Desclusterizar a partir do zoom 18
      extent={512}
      nodeSize={64}
      animationEnabled
    >
      {children}
    </ClusterMap>
  );
}
```

## GPS Tracking

### Foreground Location

```typescript
// hooks/useGPSTracking.ts
import * as Location from 'expo-location';
import { useState, useEffect, useCallback } from 'react';

interface GPSPosition {
  latitude: number;
  longitude: number;
  accuracy: number;
  altitude: number | null;
  timestamp: number;
}

export function useGPSTracking(options?: { continuous?: boolean }) {
  const [position, setPosition] = useState<GPSPosition | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isTracking, setIsTracking] = useState(false);

  const requestPermission = useCallback(async () => {
    const { status } = await Location.requestForegroundPermissionsAsync();
    if (status !== 'granted') {
      setError('Permissao de localizacao negada');
      return false;
    }
    return true;
  }, []);

  const capturePosition = useCallback(async (): Promise<GPSPosition | null> => {
    const granted = await requestPermission();
    if (!granted) return null;

    try {
      const loc = await Location.getCurrentPositionAsync({
        accuracy: Location.Accuracy.High,
        timeInterval: 5000,
        distanceInterval: 1,
      });

      const pos: GPSPosition = {
        latitude: loc.coords.latitude,
        longitude: loc.coords.longitude,
        accuracy: loc.coords.accuracy ?? 0,
        altitude: loc.coords.altitude,
        timestamp: loc.timestamp,
      };

      setPosition(pos);
      return pos;
    } catch (err) {
      setError('Erro ao capturar GPS');
      return null;
    }
  }, [requestPermission]);

  // Tracking continuo (opcional)
  useEffect(() => {
    if (!options?.continuous) return;

    let subscription: Location.LocationSubscription;

    (async () => {
      const granted = await requestPermission();
      if (!granted) return;

      setIsTracking(true);
      subscription = await Location.watchPositionAsync(
        {
          accuracy: Location.Accuracy.High,
          timeInterval: 3000,
          distanceInterval: 2,
        },
        (loc) => {
          setPosition({
            latitude: loc.coords.latitude,
            longitude: loc.coords.longitude,
            accuracy: loc.coords.accuracy ?? 0,
            altitude: loc.coords.altitude,
            timestamp: loc.timestamp,
          });
        }
      );
    })();

    return () => {
      subscription?.remove();
      setIsTracking(false);
    };
  }, [options?.continuous, requestPermission]);

  return { position, error, isTracking, capturePosition };
}
```

### Background Location (Sync de Trajeto)

```typescript
// services/background-location.ts
import * as Location from 'expo-location';
import * as TaskManager from 'expo-task-manager';

const BACKGROUND_LOCATION_TASK = 'reurbcad-background-location';

TaskManager.defineTask(BACKGROUND_LOCATION_TASK, ({ data, error }) => {
  if (error) {
    console.error('Background location error:', error);
    return;
  }

  const { locations } = data as { locations: Location.LocationObject[] };
  // Salvar posicoes no WatermelonDB para audit trail
  locations.forEach((loc) => {
    saveTrackPoint({
      latitude: loc.coords.latitude,
      longitude: loc.coords.longitude,
      accuracy: loc.coords.accuracy ?? 0,
      timestamp: loc.timestamp,
    });
  });
});

export async function startBackgroundTracking() {
  const { status } = await Location.requestBackgroundPermissionsAsync();
  if (status !== 'granted') return;

  await Location.startLocationUpdatesAsync(BACKGROUND_LOCATION_TASK, {
    accuracy: Location.Accuracy.Balanced,
    timeInterval: 30000, // A cada 30 segundos
    distanceInterval: 10, // Ou a cada 10 metros
    foregroundService: {
      notificationTitle: 'REURBCAD',
      notificationBody: 'Rastreamento de campo ativo',
    },
  });
}
```

## Toggle de Camadas

### UI de Controle de Camadas

| Camada | Default | Icone | Cor |
|--------|---------|-------|-----|
| Ortofotos | Ligado | Satellite | - |
| Comunidades (limites) | Ligado | Boundary | Azul #2196F3 |
| Quadras | Ligado | Grid | Verde #4CAF50 |
| Unidades | Ligado | House | Laranja #FF9800 |
| GPS Trail | Desligado | Route | Roxo #9C27B0 |
| Markers (pontos GPS) | Ligado | Pin | Vermelho #F44336 |

```typescript
// stores/map-layers-store.ts
import { create } from 'zustand';

interface MapLayersState {
  orthophotos: boolean;
  communities: boolean;
  blocks: boolean;
  units: boolean;
  gpsTrail: boolean;
  markers: boolean;
  toggleLayer: (layer: keyof Omit<MapLayersState, 'toggleLayer'>) => void;
}

export const useMapLayersStore = create<MapLayersState>((set) => ({
  orthophotos: true,
  communities: true,
  blocks: true,
  units: true,
  gpsTrail: false,
  markers: true,
  toggleLayer: (layer) =>
    set((state) => ({ [layer]: !state[layer] })),
}));
```

## Sistemas de Coordenadas

O REURBCAD trabalha com dois sistemas de coordenadas:

| Sistema | EPSG | Uso | Contexto |
|---------|------|-----|----------|
| WGS84 | 4326 | GPS nativo, Google Maps, armazenamento | Coordenadas do dispositivo e exibicao no mapa |
| SIRGAS2000 / UTM | 31983 (zona 23S) | Calculos de area, exportacao tecnica | Calculos geodesicos precisos e exportacao para orgaos oficiais |

### Conversao entre Sistemas

```typescript
// utils/coordinate-transform.ts
import proj4 from 'proj4';

// Definir projecoes
proj4.defs('EPSG:31983', '+proj=utm +zone=23 +south +ellps=GRS80 +units=m +no_defs');

export function wgs84ToSirgas(lng: number, lat: number): [number, number] {
  return proj4('EPSG:4326', 'EPSG:31983', [lng, lat]);
}

export function sirgasToWgs84(easting: number, northing: number): [number, number] {
  return proj4('EPSG:31983', 'EPSG:4326', [easting, northing]);
}

// Calcular area em m2 usando projecao UTM (mais preciso que haversine)
export function calculateAreaUTM(polygonWGS84: number[][]): number {
  const polygonUTM = polygonWGS84.map(([lng, lat]) =>
    wgs84ToSirgas(lng, lat)
  );
  return turf.area(turf.polygon([polygonUTM]));
}
```

## Performance

### Otimizacoes para Grandes Poligonos

| Tecnica | Quando Usar | Implementacao |
|---------|------------|---------------|
| Simplificacao Douglas-Peucker | Poligonos com > 500 vertices | `turf.simplify(polygon, { tolerance: 0.0001 })` |
| Level-of-detail | Zoom < 17 | Usar poligonos simplificados, zoom >= 17 usar originais |
| Viewport culling | Sempre | Renderizar apenas poligonos visivies no viewport atual |
| Batch rendering | > 100 unidades | Agrupar unidades em unico MultiPolygon por status |
| Tile cache limit | Sempre | Maximo 500 MB de tiles por comunidade, LRU eviction |

### Tamanho de Cache de Tiles

```typescript
// config/map-config.ts
export const MAP_CONFIG = {
  tileCacheMaxSizeMB: 500, // Por comunidade
  totalCacheMaxSizeMB: 2000, // Total no device
  defaultZoomLevels: [15, 16, 17, 18, 19],
  maxZoomLevel: 21,
  clusterRadius: 60,
  simplifyTolerance: 0.0001, // ~11m de precisao
  gpsAccuracyThreshold: 15, // metros - alertar se pior que isso
};
```

## Referencias

- [FEATURES/01-field-collection.md](../FEATURES/01-field-collection.md) - Coleta em campo
- [DATA/01-watermelondb-schema.md](../DATA/01-watermelondb-schema.md) - Schema de dados local
- [CENTRAL/DOMAIN/CONCEPTS/36-bucket-tenant.md](../../../../CENTRAL/DOMAIN/CONCEPTS/36-bucket-tenant.md) - Armazenamento de ortofotos
- [GEOAPI/DOCS/PATTERNS/02-gis-spatial-patterns.md](../../../GEOAPI/DOCS/PATTERNS/02-gis-spatial-patterns.md) - Padroes GIS no backend
