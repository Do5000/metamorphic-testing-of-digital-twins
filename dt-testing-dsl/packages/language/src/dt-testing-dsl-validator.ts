import type { ValidationChecks } from 'langium';
import type { DtTestingDslAstType } from './generated/ast.js';
import type { DtTestingDslServices } from './dt-testing-dsl-module.js';

export function registerValidationChecks(services: DtTestingDslServices) {
    const registry = services.validation.ValidationRegistry;
    const validator = services.validation.DtTestingDslValidator;
    const checks: ValidationChecks<DtTestingDslAstType> = {
        // Die alten "Person"-Checks sind weg!
    };
    registry.register(checks, validator);
}

export class DtTestingDslValidator {
    // Hier bauen wir später die Logik für dein Living Lab ein
}