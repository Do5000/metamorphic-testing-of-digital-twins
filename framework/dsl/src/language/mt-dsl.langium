grammar MtDsl

entry Model:
    (elements+=Element)*;

Element:
    TestDefinition | LifecycleHook;

LifecycleHook:
    type=('beforeAll' | 'afterAll' | 'beforeEach' | 'afterEach') '{'
        statements+=Statement*
    '}';

Statement:
    SetFeature | RequirePrecondition | MeasureLatency;

SetFeature:
    'set' actuator=STRING 'feature' feature=STRING 'to' value=Value;

RequirePrecondition:
    'precondition' sensor=STRING 'feature' feature=STRING 'equals' value=Value ('skip_message' skipMessage=STRING)?;

MeasureLatency:
    'calibrate_latency' '{'
        'actuator' actuator=STRING 'feature' actuatorFeature=STRING
        'sensor' sensor=STRING 'feature' sensorFeature=STRING
        'val_off' valOff=Value
        'val_on' valOn=Value
        ('min_change_percent' minChangePercent=NUMBER)?
        ('tolerance_factor' toleranceFactor=NUMBER)?
        ('add_seconds' addSeconds=NUMBER)?
        ('timeout' timeout=NUMBER)?
        ('runs' runs=NUMBER)?
    '}';

TestDefinition:
    'test' name=STRING '{'
        'relation' ':' relation=ID ('tolerance' ':' tolerance=NUMBER)? ('duration' ':' duration=NUMBER)? ('profile' ':' profile=STRING)? ('historical_samples' ':' historicalSamples=NUMBER)? ('historical_file' ':' historicalFile=STRING)? ('wait_time' ':' waitTime=NUMBER)?
        
        ('actuators' '[' (actuators+=DeviceFeature (',' actuators+=DeviceFeature)*)? ']')?
        ('sensors' '[' (sensors+=DeviceFeature (',' sensors+=DeviceFeature)*)? ']')?
        
        ('source_action' '[' (sourceActions+=Value (',' sourceActions+=Value)*)? ']')?
        ('intermediate_action' '[' (intermediateActions+=Value (',' intermediateActions+=Value)*)? ']')?
        ('followup_action' '[' (followupActions+=Value (',' followupActions+=Value)*)? ']')?
        ('brightness_levels' ('=')? '[' (brightnessLevels+=Value (',' brightnessLevels+=Value)*)? ']')?
    '}';

DeviceFeature:
    deviceId=STRING 'feature' feature=STRING;

Value:
    stringValue=STRING | numValue=NUMBER | boolValue=BOOLEAN;

terminal ID: /[_a-zA-Z][\w_]*/;
terminal STRING: /"(\\.|[^"\\])*"|'(\\.|[^'\\])*'/;
terminal NUMBER returns number: /[0-9]+(\.[0-9]+)?/;
terminal INT returns number: /[0-9]+/;
terminal BOOLEAN returns boolean: /(true|false)/;

hidden terminal WS: /\s+/;
hidden terminal ML_COMMENT: /\/\*[\s\S]*?\*\//;
hidden terminal SL_COMMENT: /\/\/[^\n\r]*/;
