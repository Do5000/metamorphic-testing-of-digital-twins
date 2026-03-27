grammar DtTestingDsl

entry Model:
    (elements+=AbstractElement)*;

AbstractElement:
    Thing | MetamorphicRelation;

// Repräsentiert ein Objekt in Eclipse Ditto
Thing:
    'Thing' name=ID '{'
        (properties+=Property)*
    '}';

Property:
    name=ID ':' type=('Number' | 'String' | 'Boolean');

// Die Metamorphic Relation (MR)
MetamorphicRelation:
    'Relation' name=ID
    'on' target=[Thing]
    '{'
        'transformation:' trans=Transformation
        'expect:' oracle=Oracle
    '}';

Transformation:
    // Beispiel: Erhöhe einen Wert (Source Input -> Follow-up Input)
    type=('Increase' | 'Decrease' | 'Scale') 'property' property=ID 'by' value=NUMBER;

Oracle:
    // Die Beziehung zwischen den Outputs (Source Output -> Follow-up Output)
    operator=('STRICTLY_GREATER' | 'STRICTLY_LESS' | 'EQUIVALENT' | 'INVARIANT');

terminal NUMBER returns number: /[0-9]+(\.[0-9]+)?/;
terminal ID: /[_a-zA-Z][\w_]*/;
hidden terminal WS: /\s+/;