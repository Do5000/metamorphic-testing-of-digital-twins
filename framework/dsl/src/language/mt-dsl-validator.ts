import { AstUtils, type ValidationAcceptor, type ValidationChecks } from 'langium';
import { 
    type MtDslAstType, 
    type TestDefinition,
    type DeviceFeature,
    type SetFeature,
    type RequirePrecondition,
    type MeasureLatency
} from './generated/ast.js';
import type { MtDslServices } from './mt-dsl-module.js';
import * as fs from 'fs';
import * as path from 'path';

interface DeviceCatalogEntry {
    full_id?: string;
    features?: string[];
    attributes?: Record<string, any>;
}

type DeviceCatalog = Record<string, DeviceCatalogEntry>;

function findCatalogPath(startDir?: string): string | null {
    let curr = startDir;
    while (curr && curr !== path.dirname(curr)) {
        const c1 = path.join(curr, 'device_catalog.json');
        if (fs.existsSync(c1)) return c1;
        const c2 = path.join(curr, 'framework', 'device_catalog.json');
        if (fs.existsSync(c2)) return c2;
        curr = path.dirname(curr);
    }
    const fallbackPaths = [
        path.resolve(process.cwd(), 'framework', 'device_catalog.json'),
        path.resolve(process.cwd(), 'device_catalog.json'),
        path.resolve(__dirname, '..', '..', '..', 'device_catalog.json'),
        path.resolve(__dirname, '..', '..', 'device_catalog.json')
    ];
    for (const p of fallbackPaths) {
        if (fs.existsSync(p)) return p;
    }
    return null;
}

let cachedCatalog: DeviceCatalog | null = null;
let cachedCatalogMtime: number = 0;

function getDeviceCatalog(node?: any): DeviceCatalog | null {
    try {
        let startDir: string | undefined;
        if (node) {
            try {
                const doc = AstUtils.getDocument(node);
                if (doc && doc.uri) {
                    startDir = path.dirname(doc.uri.fsPath);
                }
            } catch {}
        }
        const catalogPath = findCatalogPath(startDir);
        if (!catalogPath) return null;

        const stat = fs.statSync(catalogPath);
        if (cachedCatalog && cachedCatalogMtime === stat.mtimeMs) {
            return cachedCatalog;
        }

        const raw = fs.readFileSync(catalogPath, 'utf-8');
        cachedCatalog = JSON.parse(raw);
        cachedCatalogMtime = stat.mtimeMs;
        return cachedCatalog;
    } catch {
        return null;
    }
}

function levenshtein(a: string, b: string): number {
    const matrix: number[][] = [];
    for (let i = 0; i <= b.length; i++) matrix[i] = [i];
    for (let j = 0; j <= a.length; j++) matrix[0][j] = j;
    for (let i = 1; i <= b.length; i++) {
        for (let j = 1; j <= a.length; j++) {
            if (b.charAt(i - 1) === a.charAt(j - 1)) {
                matrix[i][j] = matrix[i - 1][j - 1];
            } else {
                matrix[i][j] = Math.min(
                    matrix[i - 1][j - 1] + 1,
                    matrix[i][j - 1] + 1,
                    matrix[i - 1][j] + 1
                );
            }
        }
    }
    return matrix[b.length][a.length];
}

function findBestSuggestion(target: string, candidates: string[], maxDistance: number = 6): string | null {
    let best: string | null = null;
    let minD = Infinity;
    const lowerTarget = target.toLowerCase();

    for (const cand of candidates) {
        const d = levenshtein(lowerTarget, cand.toLowerCase());
        if (d < minD && d <= maxDistance) {
            minD = d;
            best = cand;
        }
    }
    return best;
}

function validateDeviceAndFeature(
    node: any,
    deviceId: string | undefined,
    feature: string | undefined,
    devicePropName: string,
    featurePropName: string,
    accept: ValidationAcceptor
): void {
    if (!deviceId) return;

    const catalog = getDeviceCatalog(node);
    if (!catalog) return;

    const catalogKeys = Object.keys(catalog);
    if (!catalog[deviceId]) {
        const suggestion = findBestSuggestion(deviceId, catalogKeys, 6);
        const suggestionText = suggestion ? ` Did you mean "${suggestion}"?` : '';
        accept('warning', `Device "${deviceId}" not found in device catalog.${suggestionText}`, {
            node,
            property: devicePropName
        });
        return;
    }

    if (!feature) return;
    const availableFeatures = catalog[deviceId].features || [];
    if (availableFeatures.length > 0 && !availableFeatures.includes(feature)) {
        const suggestion = findBestSuggestion(feature, availableFeatures, 4);
        const suggestionText = suggestion ? ` Did you mean "${suggestion}"?` : '';
        accept('warning', `Feature "${feature}" is not defined on device "${deviceId}".${suggestionText} (Available: ${availableFeatures.join(', ')})`, {
            node,
            property: featurePropName
        });
    }
}

/**
 * Register custom validation checks.
 */
export function registerValidationChecks(services: MtDslServices): void {
    const registry = services.validation.ValidationRegistry;
    const validator = services.validation.MtDslValidator;
    const checks: ValidationChecks<MtDslAstType> = {
        TestDefinition: validator.checkTestDefinitionActionsMatchActuators,
        DeviceFeature: validator.checkDeviceFeature,
        SetFeature: validator.checkSetFeature,
        RequirePrecondition: validator.checkRequirePrecondition,
        MeasureLatency: validator.checkMeasureLatency
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
            accept('error', `The number of values in sourceAction (${testDef.sourceActions.length}) must match the number of defined actuators (${actuatorCount}).`, {
                node: testDef,
                property: 'sourceActions'
            });
        }

        // Validation for followupActions
        if (testDef.followupActions.length > 0 && testDef.followupActions.length !== actuatorCount) {
            accept('error', `The number of values in followUpAction (${testDef.followupActions.length}) must match the number of defined actuators (${actuatorCount}).`, {
                node: testDef,
                property: 'followupActions'
            });
        }
    }

    checkDeviceFeature(df: DeviceFeature, accept: ValidationAcceptor): void {
        validateDeviceAndFeature(df, df.deviceId, df.feature, 'deviceId', 'feature', accept);
    }

    checkSetFeature(sf: SetFeature, accept: ValidationAcceptor): void {
        validateDeviceAndFeature(sf, sf.actuator, sf.feature, 'actuator', 'feature', accept);
    }

    checkRequirePrecondition(rp: RequirePrecondition, accept: ValidationAcceptor): void {
        validateDeviceAndFeature(rp, rp.sensor, rp.feature, 'sensor', 'feature', accept);
    }

    checkMeasureLatency(ml: MeasureLatency, accept: ValidationAcceptor): void {
        validateDeviceAndFeature(ml, ml.actuator, ml.actuatorFeature, 'actuator', 'actuatorFeature', accept);
        validateDeviceAndFeature(ml, ml.sensor, ml.sensorFeature, 'sensor', 'sensorFeature', accept);
    }

}

