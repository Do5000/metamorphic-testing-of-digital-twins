https://eclipse.dev/ditto/basic-overview.html

1. thingId (Pflicht)

Das ist der weltweit eindeutige Name des Zwillings. Er besteht immer aus einem Namespace (z. B. org.example) und dem eigentlichen Namen (smart-lamp-0815), getrennt durch einen Doppelpunkt.

2. policyId (Pflicht)

In Ditto existiert kein Ding ohne Rechteverwaltung. Die policyId verweist auf ein anderes Dokument, in dem steht: "Darf der Benutzer 'Techniker' die Helligkeit ändern, aber der Benutzer 'Gast' sie nur sehen?" Das ist ein riesiger Unterschied zu Home Assistant, wo meist jeder, der Zugriff aufs Dashboard hat, alles darf.

3. attributes (Optional)

Hier landen statische Daten. Dinge, die sich fast nie ändern.

Beispiel: Seriennummer, Installationsdatum, Standort, Hardware-Version.

Wichtig: Attribute lösen normalerweise keine Aktionen aus, sie dienen der Suche und Metadaten-Verwaltung.

4. features (Das Herzstück)

Hier landen die dynamischen Daten (Zustände). Ein Feature gruppiert zusammengehörige Eigenschaften (properties).

Im obigen Beispiel gibt es das Feature dimmer. Alle Daten zur Helligkeit liegen darin.

Warum Features? Damit man Dinge modular aufbauen kann. Ein "Roboter" könnte ein Feature arm, ein Feature kamera und ein Feature akku haben.


Example:

{
  "thingId": "the.namespace:theName",
  "policyId": "the.namespace:thePolicyName",
  "definition": "org.eclipse.ditto:HeatingDevice:2.1.0",
  "attributes": {
      "someAttr": 32,
      "manufacturer": "ACME corp"
  },
  "features": {
      "heating-no1": {
          "properties": {
              "connected": true,
              "complexProperty": {
                  "street": "my street",
                  "house no": 42
              }
          },
          "desiredProperties": {
              "connected": false
          }
      },
      "switchable": {
          "definition": [ "org.eclipse.ditto:Switcher:1.0.0" ],
          "properties": {
              "on": true,
              "lastToggled": "2017-11-15T18:21Z"
          }
      }
  }
}
