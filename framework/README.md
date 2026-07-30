# Unreal Twin
# 0. Introduction
This is the Readme of Unreal Digital Twin as a Service.
The system consists of 3 parts:
DT Backend (see 1.)
Translation Unit (see 2.)
UE5 Application (see 3.)

Furthermore, the IFC file is created in Autodesk Revit which is covered in 4.
How everything can be started in the Living Lab is described in 5.

Author: Simon Senoner

# 1. DT Backend:
The backend of the system uses Eclipse Hono for IoT connection.
and Eclipse Ditto for handling DTs.
It is deployed using the helm package `cloud2edge` (https://eclipse.dev/packages/packages/cloud2edge/tour/).
## 1.1. Getting Started
##### Prerequisites:
* Docker (see https://docs.docker.com/engine/install/)
* minikube (see https://minikube.sigs.k8s.io/docs/start/)
  ```shell
  # to enable enough memory and CPU cores start initially using:
  minikube start --memory=10240 --cpus=8
  ```
* Helm (see https://helm.sh/docs/intro/install/)
* MongoDB
  ```shell
  # The mongo db is used by cloud2edge and set up in 
  # `./values-cloud2edge.yaml` to be accessible at port 27017
  # Currently does not use any security
  docker run -d `
    --name mongodb `
    --restart unless-stopped `
    -p 27017:27017 `
    mongo
  ```
##### Installation of cloud2edge:
Setup of cloud2edge is defined in file `./middleware/values-cloud2edge.yaml`.
Run the following commands:
``` shell
cd ./middleware
helm repo update
kubectl create namespace cloud2edge
helm repo add eclipse-iot https://eclipse.org/packages/charts

# used to uninstall possible existing versions:
helm uninstall c2e -n cloud2edge
kubectl delete pod --force -n cloud2edge --all

helm install -n cloud2edge c2e eclipse-iot/cloud2edge  -f ./values-cloud2edge.yaml

# was once needed due to deprecation of kafka dependency (https://hub.docker.com/r/bitnami/kafka):
kubectl set image statefulset/c2e-kafka-controller auto-discovery=docker.io/bitnamilegacy/kubectl:1.29.2-debian-12-r2 -n cloud2edge
kubectl set image statefulset/c2e-kafka-controller kafka-init=bitnamilegacy/kafka:3.6.1-debian-12-r12 -n cloud2edge
kubectl set image statefulset/c2e-kafka-controller kafka=bitnamilegacy/kafka:3.6.1-debian-12-r12 -n cloud2edge
```
##### Activation:
Once installed, it can be started using:
```shell
docker desktop start | minikube start | minikube tunnel --bind-address=0.0.0.0
```

## 1.2. Communication Interface
This part is already implemented in the system and can be skipped for setting it up. It is there for documentation and further extensions.
The DT Backend is connected to the Translation Unit using MQTT.
The UE5 Application is connected to the DT Backend using a Websocket and a HTTP Connection.
The following table explains the placeholders used in this chapter:
| **Placeholder**        | **Description**                                                                | **Example**                                   |
|------------------------|--------------------------------------------------------------------------------|-----------------------------------------------|
| `TENANT`               | Hono and Ditto Tenant used to group all devices of this application            | `at.uibk.ut.tenants`                          |
| `DEVICE`               | Name of a specific Device represented by a Ditto Thing, like lamps, switches…  | `light-1`                                     |
| `PARAM`                | Name of a parameter of a DEVICE, like brightness of a specific lamp            | `brightness`; `state`; ...                    |
| `VALUE`                | Value assigned to a DT PARAM, can be any JSON value                            | `0`; `"text"`; `{"json":1}`                   |
| `MW_HTTP_ADDRESS`      | Address of the HTTP endpoint of the middleware in the Living Lab               | `127.0.0.1:8081`                              |
| `MW_MQTT_ADDRESS`      | Address of the MQTT broker of the middleware in the Living Lab                 | `127.0.0.1:1884`                              |
| `HONO_HTTP_ADDRESS`    | Address of the HTTP endpoint of Hono                                           | `127.0.0.1:8443`                              |
| `HONO_MQTT_ADDRESS`    | Address of the MQTT broker of Hono                                             | `127.0.0.1:8883`                              |
| `DITTO_HTTP_ADDRESS`   | Address of the HTTP endpoint of Ditto                                          | `127.0.0.1:8080`                              |
| `DITTO_WS_ADDRESS`     | Address of the WebSocket of Ditto                                              | `127.0.0.1:8080`                              |
| `ATTRIBUTES`           | Features of a Ditto Thing, a collection of PARAM with a VALUE that are static  | `{"version":"2.0.1a"}`                        |
| `FEATURES`             | Features of a Ditto Thing, a collection of PARAM with a VALUE that change dynamically | `{"state":{"properties":{"value":1}}}` |
| `CONNECTION_ID`        | ID of the Ditto Connection between Ditto and Hono                              | `pre-authenticated: hono-connection-<TENANT>` |
| `POLICY_ID`            | ID of the Ditto Policy used to set access level of all Things                  | `<TENANT>:demo-device`                        |
| `PASSWORD`             | Password of a device set for Hono that the device must know to publish updates | `Secret1234#`                                 |
| `GATEWAY_DEVICE`       | Name of the device used as a Hono Gateway                                      | `homeassistantgateway`                        |


### 1.2.1. Living Lab
The Living Lab in the university of Innsbruck has its own middleware to simplify device communication and exposes MQTT updates and uses HTTP for commands.
```shell
# MQTT endpoint to request all device updates: (user/password required)
middleware/#

# Updates received with topic
middleware/<DEVICE>/<PARAM>
# and payload with the
<VALUE>
```

```shell
# HTTP Request to send a command
POST http://<MW_HTTP_ADDRESS>/middleware/command
{
    "uuid": <DEVICE>,
    "parameters": [{"name": <PARAM>, "value": <VALUE>}]
}
```

### 1.2.2. Eclipse Hono
Eclipse Hono which is used for IoT Connection sends commands to devices over MQTT and receives messages if they updated over MQTT.
The devices can be created and deleted and secured with passwords.
To handle multiple devices at once with one MQTT connection, devices can be grouped using a Gateway device.

```shell
# MQTT endpoint to request all device updates: (devicename/password required)
command/<TENANT>/+/req/#

# Updates received have the form
{
    "topic": "<TENANT>/<DEVICE>/things/live/messages/<PARAM>",
    "headers": {
        "version": 2,
        "x-real-ip": "10.244.0.1",
        "x-forwarded-user": "ditto",
        "x-ditto-pre-authenticated": "nginx:ditto",
        "accept": "*/*",
        "channel": "live",
        "timeout": "0",
        "response-required": false,
        "ditto-originator": "nginx:ditto",
        "requested-acks": [],
        "ditto-message-direction": "TO",
        "ditto-message-subject": "<PARAM>",
        "ditto-message-thing-id": "<TENANT>:<DEVICE>",
        "content-type": "application/json",
        "timestamp": "2025-10-01T16:17:03.258412560+02:00",
        "correlation-id": "e2450364-cf6e-43e9-9539-e467c0673365"
    },
    "path": "/inbox/messages/<PARAM>",
    "value": <VALUE>
}
```
```shell
# Updates can be sent using MQTT topic
telemetry/<TENANT>/<TENANT>:<DEVICE>
# and payload
{
    "topic": "<TENANT>/<DEVICE>/things/twin/commands/modify",
    "path": "/features/<PARAM>/properties/value",
    "value": <VALUE>
}
```

```shell
# Devices can be created using
POST https://<HONO_HTTP_ADDRESS>/v1/devices/<TENANT>/<TENANT>:<DEVICE>
# Deleted Using
DELETE https://<HONO_HTTP_ADDRESS>/v1/devices/<TENANT>/<TENANT>:<DEVICE>
# A password can be set using
PUT https://<HONO_HTTP_ADDRESS>/v1/credentials/<TENANT>/<TENANT>:<DEVICE>
[{
  "type": "hashed-password",
  "auth-id": <DEVICE>,
  "secrets": [{
    "pwd-plain": <PASSWORD>,
    "hash-function": "sha-256"
  }]
}]
# A gateway device can be added using
PUT https://<HONO_HTTP_ADDRESS>/v1/devices/<TENANT>/<TENANT>:<DEVICE>
{
  "via": [<GATEWAY_DEVICE>]
}
```

### 1.2.2. Eclipse Ditto
Eclipse Ditto handles the DT data. It exposes a websocket connection to the UE5 application for real time data and a HTTP interface for fetching previous values and managing devices.
```shell
# The websocket connection is at
ws://<DITTO_WS_ADDRESS>/ws/2
# feature updates are received of form
{
    "topic": "<TENANT>/<DEVICE>/things/twin/events/modified",
    "headers": {
        "correlation-id": "c8d33ced-bb6e-4dc2-a1b6-a2f44e95cb3a",
        "requested-acks": [],
        "ditto-originator": "pre-authenticated:hono-connection-<TENANT>",
        "response-required": false,
        "version": 2,
        "content-type": "application/json"
    },
    "path": "/features/<PARAM>/properties/value",
    "value": <VALUE>,
    "revision": 12513,
    "timestamp": "2025-10-01T12:20:05Z"
}
# commands can be sent to the websocket using
{
    "topic":"<TENANT>/<DEVICE>/things/live/messages/<PARAM>",
    "headers":{
        "content-type": "application/json",
        "response-required": false
    },
    "path":"/inbox/messages/<PARAM>",
    "value":<VALUE>
}
```
```shell
# To request existing devices over HTTP a GET request can be sent like
GET http://<DITTO_HTTP_ADDRESS>/api/2/search/things?option=size(200),cursor(<CURSOR>)
# which leads to the response
{
  "items": [
    {
      "thingId": "<TENANT>:<DEVICE>",
      "policyId": "<POLICY_ID>",
      "attributes": <ATTRIBUTES>,
      "features": <FEATURES>
    },
    ...
  ],
  "cursor": "<CURSOR>"
}

# Devices can be created and updated using
PUT http://<DITTO_HTTP_ADDRESS>/api/2/things/<TENANT>:<DEVICE>
{
  "policyId": <POLICY_ID>,
  "attributes": <ATTRIBUTES>,
  "features": <FEATURES>
}
# and deleted using
DELETE http://<DITTO_HTTP_ADDRESS>/api/2/things/<TENANT>:<DEVICE>
```




## 1.3. Useful commands for Debugging
```shell
kubectl get svc -n cloud2edge
# or
kubectl get pods -n cloud2edge
# or from a specific pod using
kubectl logs <INSERT_POD_ID> -n cloud2edge
kubectl describe pod <INSERT_POD_ID> -n cloud2edge

# get performance using
minikube addons enable metrics-server
kubectl top pods -n cloud2edge
```

# 2. Translation Unit
The translation unit is a python script that acts as a bridge between the Physical Layer and the DT Backend.

##### Prerequisites:
* Python3
* manual installation of packages (no `requirements.txt` yet)

## 2.1. Quickstart
There are standalone python scripts to start the translation unit:
##### Eclipse Hono/Ditto, Living Lab:
```shell
python ./middleware/translationunit_honodittobackend_middleware.py
```
##### Eclipse Hono/Ditto, No Physical Layer:
```shell
python ./middleware/translationunit_honodittobackend_nomiddleware.py
```
##### Custom DT Backend, Living Lab:
```shell
python ./middleware/translationunit_mockbackend_middleware.py
```
##### Custom DT Backend, No Physical Layer:
```shell
python ./middleware/translationunit_mockbackend_nomiddleware.py
```

## 2.2. File Structure
**The files are given relative to `./middleware/`.**
Values are set up in `./ut_params.py`.
Endpoints for communication are defined in `./ut_mqtt_endpoints.py`
and the mocked version of the Hono/Ditto connection is defined in `./ut_ditto_mock.py`.
Helper methods to use the APIs are defined iin `./ut_helpers.py`

## 2.2. Jupyter Notebook
The notebook contains the code for each setup in addition to code to calculate
the ODTE using a dedicated TCP socket connection to get events quickly from the UE5 application
a connection to InfluxDB to visualize Grafana Data (see ./middleware/ut_grafana)
and the code for the evaluation.

# 3. UE5 Application
## 3.1. Getting Started
##### Prerequisites:
* Unreal Engine 5.5 (https://www.unrealengine.com/en-US/download)
* Possibly IDE (tested with Jetbrains Rider)
##### Installation:
(Possibly not working: Open UnrealTwin.uproject using Unreal Engine 5.5 => could complain about missing compilation)
Tested alternative: Open Project in IDE (either Visual Studio OR Jetbrains Rider) and compile it.

Default Scene (Content Drawer => All/Content/MyScene) should be loaded by default and ready to be started.

## 3.2. UE5 Application Features
* Camera Controls
    * Scroll: Move In/Out
    * Right click drag: Rotate Camera
    * Middle click drag: Drag Camera
    * Space/Ctrl: Move Camera Up/Down
    * W/A/S/D: Move Camera Forward/Left/Backward/Right
* Device Mouse Interaction:
    * Hover Mouse over Device: Mark it
    * Click Device: Select/Deselect it
* Side Panel:
    * Drag Handle: Resize it
    * Upload Button: Upload new IFC model (also works using drag and drop)
    * Select Tab
* Twin Tab:
    * Group Commands:
        * send the current command to all devices
        * works only for devices and features currently filtered for
        * if the device is selected it is only sent to selected devices
    * Heatmap:
        * show heatmap based on number values
    * Filter Devices/Values:
        * Regex Filter for device name/feature name
    * Table:
        * list with all devices and their features with textboxes to send commands to change them
* Connection Tab:
    * Set up connection parameters for connection to DT Backend and reconnect
* Visualization:
    * select floor
    * select culling height (objects above are invisible to look into the current floor)
    * select sun pitch and yaw

## 3.3. UE5 Application Code
The full class diagram is visible at:
<img src="/middleware/documentation_assets/class_diagram.svg" width="100%">

A simplified version is visble at:
![Class Diagram simplified](/middleware/documentation_assets/class_diagram_simple.svg)

##### <span style="color:red">DittoController</span>:
Handles connection to DT Backend.

##### <span style="color:green">UnrealTwinController</span>:
Handles the Digital Twin. Has callbacks like `SendCommandCallback`, `OnDeviceValueChangedCallback` and `OnDeviceFilterChangedCallback` extensions can subscribe to and exposes both `DeviceComponents` and a filtered version of them.

##### <span style="color:blue">DeviceComponent</span>:
Represents one device in the IFC scene and is directly attached to the device in the scene hierarchy. `Id` of device, `Attributes` and `Features` are represented by the `DeviceRepresentation`. Also exposes a filtered version where some `Attributes` and `Features` may be missing.
Has a selection status (`Unselected` | `Hovered` | `Selected`) and exposes function `OnSelectionStateChangedCallback`.
Can be extended by device type specific versions (e.g. as it is done for light) that override the `InitWithMetaData` and `OnValueChanged` methods in order to change the scene.
Is created by the `DeviceComponentFactory` when the IFC structure is loaded.

##### <span style="color:purple">Extensions</span>:
Additional Code can be added to the scene either by adding new UE5 Actors that find an `UnrealTwinController` and listen for DT events or by extending
`DeviceComponent`, adding new rules to the `DeviceComponentFactory` and adding new behaviour.

##### <span style="color:orange">User Interface</span>:
The code for the user interface is mostly implemented in `CustomHUD` with a substantial additional amount being used to visualize the device hierarchy in the side panel. The classes responsible for that are `DeviceTable` for the device names. Each entry of the `DeviceTable` is a `DeviceEditorTable` that visualizes tha attributes and features of each device, fires commands and listens for value updates and filter changes. This is implemented recursively using an UE5 `TreeTable`.
Each UI element has an UE5 Widget Blueprint where the visualization is defined.
The folder for all ui elements is called `ui` and the Widget Blueprints are in the editor in `All/Content/UnrealTwinUI`.



# 4. IFC Creation using Revit
* Device Id should be represented by an `Instance` parameter of type `General` called `UUID` as shown in
  <img src="/middleware/documentation_assets/MasterThesis-RevitTutorial_deviceparam.svg" width="100%">
* Photometric parameters are used from Revit and should use Revits Light system
* Attributes and Features can be specified using `Instance General UT\_attributes` and `Instance General UT_features`
    * When a JSON structure is provided directly, the specified values are used as-is for attributes or features.
      e.g. `{"feat1":1,"feat2":"text"}` $\Rightarrow$ `{"feat1":1,"feat2":"text"}`
    * When comma-separated names are used, empty string values are created for each attribute or feature name.
      e.g. `{feat1,feat2}` $\Rightarrow$ `{"feat1":"","feat2":""}`
    * Values can also be directly assigned using \texttt{'='}. Brackets can be used to define more complex structures.
      e.g. `feat1,feat2=test,feat3=1,feat4={"a":1,"b":"1=2"}` $\Rightarrow$
      `{"feat1":"","feat2":"test","feat3":1.0,"feat4":{"a":1,"b":"1=2"}}`
* Global Project Information parameters can be defined in Revit to set up connection
  (e.g. `UT_DittoAddressHttp` will be used as the value for `DittoAddressHttp` in `DittoConnection`, see class diagram in **3.3.** - works for all values of `DittoConnection`)
  <img src="/middleware/documentation_assets/MasterThesis-RevitTutorial_global.svg" width="100%">

To export the Revit file as a IFC that can be used by the UE5 application, the export option `Export Revit property sets` must be selected as e.g. is in `IFC2x3 Coordination View Setup` or in a custom configuration.

# 5. Living Lab Demo
* Start DT Backend
    * Either Hono/Ditto using
      ```shell
      docker desktop start | minikube start | minikube tunnel --bind-address=0.0.0.0
      ```
      Start `./middleware/translationunit_honodittobackend_middleware.py` OR `./middleware/translationunit_honodittobackend_nomiddleware.py`
    * Or mocked DT Backend:
      Start `./middleware/translationunit_mockbackend_middleware.py` OR `./middleware/translationunit_mockbackend_nomiddleware.py`
* Enter uibk firewall (`https://fwauth-tech.uibk.ac.at/` inside UIBK network)
* Start UE5 Demo using IDE
    * Open Project in Rider => Wait for initalization => Run => Run UE5 Scene
    * Upload IFC file
        * Connection either set up in IFC file (see 4.)
        * or in Connection Tab
