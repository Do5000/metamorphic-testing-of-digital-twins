## DSL Parameter

- Test-Name / Identifier (z.B. "TC_01_Monotony_DeskLight")
- Relation (monotony, invarianz .....)
- Aktuatoren + Feature (Als Liste/Array, da z.B. `conservation` 2 Aktuatoren benötigt)
- Sensoren + Feature (Als Liste/Array, da z.B. `proportionality` 2 Sensoren benötigt)
- BeforeEach, BeforeAll, AfterEach, AfterAll
- Pre-Conditions (Vorbedingungen für Before-Hooks, z.B. Device + Feature + Expected Value)
- Sourcetest Value / Action Payload (z.B. nur "on" oder komplexere Werte wie Helligkeit für `substitution`)
- Follow-up Value (nicht bei jeder Relation)
- Toleranz (nicht bei jeder Relation)
- Duration / Messdauer in Sekunden (z.B. für `stability`)
- Geräte-Profile / Device Profiles (z.B. JSON-Profil für `substitution`)
- Historische Datenerzeugung: Abtastwerte(0,1,2,3...100), Outputfile Name: automatisch handhaben (z.B. basierend auf dem Testnamen und Zeitstempel), 
- Wait Time (wegen Pipline Latenz)
- Latenz Messung: min_change_percent, tolerance_factor, add_seconds, timeout, runs
