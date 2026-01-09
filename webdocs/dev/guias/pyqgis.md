# PyQGIS API

Guia de desenvolvimento do plugin QGIS GEOGIS usando PyQGIS.

## Visão Geral

O plugin GEOGIS utiliza a API PyQGIS para integração com QGIS Desktop, permitindo:
- Importação/exportação de dados do CARF
- Visualização de camadas geoespaciais
- Edição de geometrias de unidades habitacionais
- Análises espaciais de comunidades REURB

## Estrutura do Plugin

```
carf-geogis/
├── __init__.py           # Entry point do plugin
├── geogis.py             # Classe principal do plugin
├── metadata.txt          # Metadados do plugin
├── resources.qrc         # Recursos (ícones, UI)
├── ui/
│   ├── main_dialog.ui    # Interface principal
│   └── settings_dialog.ui
├── core/
│   ├── api_client.py     # Cliente HTTP para CARF API
│   ├── layer_manager.py  # Gerenciamento de camadas
│   └── sync_manager.py   # Sincronização de dados
└── utils/
    ├── geometry.py       # Utilitários de geometria
    └── validators.py     # Validações
```

## Inicialização do Plugin

### `__init__.py`

```python
def classFactory(iface):
    """Load GeoGisPlugin class from file geogis."""
    from .geogis import GeoGisPlugin
    return GeoGisPlugin(iface)
```

### `geogis.py`

```python
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsProject

class GeoGisPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []

    def initGui(self):
        """Criar UI do plugin"""
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        action = QAction(QIcon(icon_path), 'CARF GeoGIS', self.iface.mainWindow())
        action.triggered.connect(self.run)
        self.iface.addToolBarIcon(action)
        self.actions.append(action)

    def unload(self):
        """Remover plugin"""
        for action in self.actions:
            self.iface.removeToolBarIcon(action)

    def run(self):
        """Executar plugin"""
        from .ui.main_dialog import MainDialog
        dlg = MainDialog()
        dlg.show()
```

## Gerenciamento de Camadas

### Criar Camada de Unidades

```python
from qgis.core import (
    QgsVectorLayer,
    QgsProject,
    QgsField,
    QgsFeature,
    QgsGeometry,
    QgsPointXY
)
from qgis.PyQt.QtCore import QVariant

def create_units_layer():
    # Criar camada de polígonos
    layer = QgsVectorLayer("Polygon?crs=EPSG:4326", "Unidades REURB", "memory")
    provider = layer.dataProvider()

    # Adicionar campos
    provider.addAttributes([
        QgsField("id", QVariant.String),
        QgsField("code", QVariant.String),
        QgsField("address", QVariant.String),
        QgsField("area", QVariant.Double),
        QgsField("holder_name", QVariant.String),
        QgsField("status", QVariant.String)
    ])
    layer.updateFields()

    # Adicionar ao projeto
    QgsProject.instance().addMapLayer(layer)

    return layer
```

### Adicionar Features

```python
from qgis.core import QgsFeature, QgsGeometry

def add_unit_feature(layer, unit_data):
    feature = QgsFeature()

    # Criar geometria do GeoJSON
    geometry = QgsGeometry.fromWkt(unit_data['geometry_wkt'])
    feature.setGeometry(geometry)

    # Definir atributos
    feature.setAttributes([
        unit_data['id'],
        unit_data['code'],
        unit_data['address'],
        unit_data['area'],
        unit_data['holder_name'],
        unit_data['status']
    ])

    # Adicionar feature à camada
    layer.dataProvider().addFeatures([feature])
    layer.updateExtents()
```

### Estilizar Camada

```python
from qgis.core import (
    QgsSymbol,
    QgsSingleSymbolRenderer,
    QgsCategorizedSymbolRenderer,
    QgsRendererCategory
)
from qgis.PyQt.QtGui import QColor

def style_units_layer(layer):
    # Estilo categorizado por status
    categories = []

    # Unidades regularizadas - verde
    symbol_regularized = QgsSymbol.defaultSymbol(layer.geometryType())
    symbol_regularized.setColor(QColor(46, 204, 113))
    symbol_regularized.setOpacity(0.7)
    categories.append(QgsRendererCategory('regularized', symbol_regularized, 'Regularizada'))

    # Unidades em análise - amarelo
    symbol_pending = QgsSymbol.defaultSymbol(layer.geometryType())
    symbol_pending.setColor(QColor(241, 196, 15))
    symbol_pending.setOpacity(0.7)
    categories.append(QgsRendererCategory('pending', symbol_pending, 'Em Análise'))

    # Unidades com pendências - vermelho
    symbol_issue = QgsSymbol.defaultSymbol(layer.geometryType())
    symbol_issue.setColor(QColor(231, 76, 60))
    symbol_issue.setOpacity(0.7)
    categories.append(QgsRendererCategory('issue', symbol_issue, 'Com Pendências'))

    # Aplicar renderer
    renderer = QgsCategorizedSymbolRenderer('status', categories)
    layer.setRenderer(renderer)
    layer.triggerRepaint()
```

## Integração com API CARF

### Cliente HTTP

```python
import requests
from typing import List, Dict

class CarfApiClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token
        self.headers = {'Authorization': f'Bearer {token}'}

    def get_units(self, community_id: str = None) -> List[Dict]:
        """Obter unidades da API"""
        params = {}
        if community_id:
            params['communityId'] = community_id

        response = requests.get(
            f'{self.base_url}/api/units',
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()['data']

    def create_unit(self, unit_data: Dict) -> Dict:
        """Criar nova unidade"""
        response = requests.post(
            f'{self.base_url}/api/units',
            headers=self.headers,
            json=unit_data
        )
        response.raise_for_status()
        return response.json()

    def update_unit(self, unit_id: str, unit_data: Dict) -> Dict:
        """Atualizar unidade existente"""
        response = requests.put(
            f'{self.base_url}/api/units/{unit_id}',
            headers=self.headers,
            json=unit_data
        )
        response.raise_for_status()
        return response.json()
```

### Sincronização QGIS ↔ API

```python
from qgis.core import QgsProject, QgsFeature

class SyncManager:
    def __init__(self, api_client: CarfApiClient):
        self.api = api_client

    def sync_units_from_api(self, layer_name: str = "Unidades REURB"):
        """Sincronizar unidades da API para QGIS"""
        # Obter dados da API
        units = self.api.get_units()

        # Obter ou criar camada
        layer = QgsProject.instance().mapLayersByName(layer_name)
        if not layer:
            layer = create_units_layer()
        else:
            layer = layer[0]

        # Limpar features existentes
        layer.dataProvider().truncate()

        # Adicionar features da API
        for unit in units:
            add_unit_feature(layer, {
                'id': unit['id'],
                'code': unit['code'],
                'address': unit['address'],
                'area': unit['area'],
                'holder_name': unit.get('holderName', ''),
                'status': unit['status'],
                'geometry_wkt': self._geojson_to_wkt(unit['geometry'])
            })

        layer.updateExtents()
        self.iface.messageBar().pushSuccess("Sincronização", f"{len(units)} unidades sincronizadas")

    def sync_units_to_api(self, layer_name: str = "Unidades REURB"):
        """Sincronizar unidades do QGIS para API"""
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]

        for feature in layer.getFeatures():
            unit_data = {
                'code': feature['code'],
                'address': feature['address'],
                'area': feature['area'],
                'geometry': self._wkt_to_geojson(feature.geometry().asWkt())
            }

            unit_id = feature['id']
            if unit_id:
                # Atualizar existente
                self.api.update_unit(unit_id, unit_data)
            else:
                # Criar novo
                result = self.api.create_unit(unit_data)
                # Atualizar ID no QGIS
                layer.dataProvider().changeAttributeValues({
                    feature.id(): {0: result['id']}
                })

    def _geojson_to_wkt(self, geojson: Dict) -> str:
        """Converter GeoJSON para WKT"""
        from shapely.geometry import shape
        return shape(geojson).wkt

    def _wkt_to_geojson(self, wkt: str) -> Dict:
        """Converter WKT para GeoJSON"""
        from shapely.wkt import loads
        from shapely.geometry import mapping
        return mapping(loads(wkt))
```

## Análises Espaciais

### Calcular Área de Comunidade

```python
from qgis.core import QgsGeometry, QgsDistanceArea

def calculate_community_area(features: List[QgsFeature]) -> float:
    """Calcular área total de uma comunidade (soma de unidades)"""
    calculator = QgsDistanceArea()
    calculator.setEllipsoid('WGS84')

    total_area = 0.0
    for feature in features:
        geom = feature.geometry()
        area = calculator.measureArea(geom)
        total_area += area

    return total_area  # em metros quadrados
```

### Verificar Sobreposições

```python
def check_overlaps(layer) -> List[tuple]:
    """Verificar sobreposições entre unidades"""
    overlaps = []
    features = list(layer.getFeatures())

    for i, feat1 in enumerate(features):
        for feat2 in features[i+1:]:
            if feat1.geometry().intersects(feat2.geometry()):
                intersection = feat1.geometry().intersection(feat2.geometry())
                if not intersection.isEmpty() and intersection.area() > 0:
                    overlaps.append((
                        feat1['code'],
                        feat2['code'],
                        intersection.area()
                    ))

    return overlaps
```

### Criar Buffer ao Redor de Unidade

```python
from qgis.core import QgsGeometry

def create_buffer(feature: QgsFeature, distance_meters: float) -> QgsGeometry:
    """Criar buffer ao redor de uma unidade"""
    geom = feature.geometry()

    # Converter distância para graus (aproximado para latitudes médias)
    distance_degrees = distance_meters / 111320.0

    buffer_geom = geom.buffer(distance_degrees, 5)
    return buffer_geom
```

## Interface do Usuário

### Dialog Principal

```python
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog

UI_FILE = os.path.join(os.path.dirname(__file__), 'main_dialog.ui')

class MainDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_FILE, self)

        # Conectar sinais
        self.btnSync.clicked.connect(self.on_sync_clicked)
        self.btnAnalyze.clicked.connect(self.on_analyze_clicked)

    def on_sync_clicked(self):
        """Sincronizar dados com API"""
        api_client = CarfApiClient(
            base_url=self.txtApiUrl.text(),
            token=self.txtToken.text()
        )
        sync_manager = SyncManager(api_client)
        sync_manager.sync_units_from_api()

    def on_analyze_clicked(self):
        """Executar análises espaciais"""
        layer = QgsProject.instance().mapLayersByName("Unidades REURB")[0]
        overlaps = check_overlaps(layer)

        if overlaps:
            msg = f"Encontradas {len(overlaps)} sobreposições:\n"
            for code1, code2, area in overlaps[:10]:  # Mostrar primeiras 10
                msg += f"- {code1} x {code2}: {area:.2f} m²\n"
            self.txtResults.setText(msg)
        else:
            self.txtResults.setText("Nenhuma sobreposição encontrada!")
```

## Processing Algorithms

### Criar Algorithm Customizado

```python
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterFeatureSink
)

class BufferUnitsAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    DISTANCE = 'DISTANCE'
    OUTPUT = 'OUTPUT'

    def createInstance(self):
        return BufferUnitsAlgorithm()

    def name(self):
        return 'bufferunits'

    def displayName(self):
        return 'Buffer de Unidades REURB'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                'Camada de Unidades',
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.DISTANCE,
                'Distância do Buffer (metros)',
                type=QgsProcessingParameterNumber.Double,
                defaultValue=10.0
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                'Buffer Output'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        distance = self.parameterAsDouble(parameters, self.DISTANCE, context)

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            source.fields(),
            source.wkbType(),
            source.sourceCrs()
        )

        for feature in source.getFeatures():
            buffer_geom = create_buffer(feature, distance)
            out_feature = QgsFeature()
            out_feature.setGeometry(buffer_geom)
            out_feature.setAttributes(feature.attributes())
            sink.addFeature(out_feature)

        return {self.OUTPUT: dest_id}
```

## Recursos Adicionais

- [PyQGIS Cookbook](https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/)
- [QGIS API Documentation](https://qgis.org/api/)
- [Plugin Development](https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/plugins/index.html)
- [Repositório GEOGIS](https://github.com/Thalesvpr/carf-geogis)
