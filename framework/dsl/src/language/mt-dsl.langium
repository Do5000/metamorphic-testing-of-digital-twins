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
    'precondition' sensor=STRING 'feature' feature=STRING 'equals' value=Value ('skipMessage' skipMessage=STRING)?;

MeasureLatency:
    'calibrateLatency' '{'
        'actuator' actuator=STRING 'feature' actuatorFeature=STRING
        'sensor' sensor=STRING 'feature' sensorFeature=STRING
        'valOff' valOff=Value
        'valOn' valOn=Value
        ('minChangePercent' minChangePercent=NUMBER)?
        ('toleranceFactor' toleranceFactor=NUMBER)?
        ('addSeconds' addSeconds=NUMBER)?
        ('timeout' timeout=NUMBER)?
        ('runs' runs=NUMBER)?
    '}';

TestDefinition:
    'test' name=STRING '{'
        'relation' ':' (not?='not')? relation=ID ('tolerance' ':' tolerance=NUMBER)? ('duration' ':' duration=NUMBER)? ('profile' ':' profile=STRING)? ('historicalSamples' ':' historicalSamples=NUMBER)? ('historicalFile' ':' historicalFile=STRING)? ('waitTime' ':' waitTime=NUMBER)?
        
        ('actuators' '[' (actuators+=DeviceFeature (',' actuators+=DeviceFeature)*)? ']')?
        ('sensors' '[' (sensors+=DeviceFeature (',' sensors+=DeviceFeature)*)? ']')?
        
        ('sourceAction' '[' (sourceActions+=Value (',' sourceActions+=Value)*)? ']')?
        ('intermediateAction' '[' (intermediateActions+=Value (',' intermediateActions+=Value)*)? ']')?
        ('followUpAction' '[' (followupActions+=Value (',' followupActions+=Value)*)? ']')?
        ('brightnessLevels' ('=')? '[' (brightnessLevels+=Value (',' brightnessLevels+=Value)*)? ']')?
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
