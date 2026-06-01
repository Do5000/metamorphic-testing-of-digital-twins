import { type ValidationAcceptor, type ValidationChecks } from 'langium';
import { type MtDslAstType, type TestDefinition } from './generated/ast.js';
import type { MtDslServices } from './mt-dsl-module.js';

/**
 * Register custom validation checks.
 */
export function registerValidationChecks(services: MtDslServices): void {
    const registry = services.validation.ValidationRegistry;
    const validator = services.validation.MtDslValidator;
    const checks: ValidationChecks<MtDslAstType> = {
        TestDefinition: validator.checkTestDefinitionActionsMatchActuators
    };
    registry.register(checks, validator);
}

/**
 * Implementation of custom validations.
 */
export class MtDslValidator {

    checkTestDefinitionActionsMatchActuators(testDef: TestDefinition, accept: ValidationAcceptor): void {
        const actuatorCount = testDef.actuators.length;

        // Validation for sourceActions
        if (testDef.sourceActions.length > 0 && testDef.sourceActions.length !== actuatorCount) {
            accept('error', `The number of values in source_action (${testDef.sourceActions.length}) must match the number of defined actuators (${actuatorCount}).`, {
                node: testDef,
                property: 'sourceActions'
            });
        }

        // Validation for followupActions
        if (testDef.followupActions.length > 0 && testDef.followupActions.length !== actuatorCount) {
            accept('error', `The number of values in followup_action (${testDef.followupActions.length}) must match the number of defined actuators (${actuatorCount}).`, {
                node: testDef,
                property: 'followupActions'
            });
        }
    }

}
