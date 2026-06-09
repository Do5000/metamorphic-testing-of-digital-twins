import { Model } from '../language/generated/ast.js';
import * as fs from 'fs';
import * as path from 'path';

export function generateJson(model: Model, filePath: string, destination: string | undefined): string {
    const data = {
        elements: model.elements.map(e => extractElement(e))
    };

    const fileName = path.basename(filePath, path.extname(filePath)) + '.json';
    const outPath = destination ? path.join(destination, fileName) : path.join(path.dirname(filePath), fileName);

    fs.writeFileSync(outPath, JSON.stringify(data, null, 2), 'utf-8');
    return outPath;
}

function extractElement(e: any): any {
    if (e.$type === 'LifecycleHook') {
        return {
            type: 'LifecycleHook',
            hookType: e.type,
            statements: e.statements.map((s: any) => extractStatement(s))
        };
    } else if (e.$type === 'TestDefinition') {
        return {
            type: 'TestDefinition',
            name: e.name,
            relation: e.relation,
            not: !!e.not,
            tolerance: e.tolerance,
            duration: e.duration,
            profile: e.profile,
            historicalSamples: e.historicalSamples,
            historicalFile: e.historicalFile,
            waitTime: e.waitTime,
            actuators: e.actuators ? e.actuators.map((a: any) => ({ deviceId: a.deviceId, feature: a.feature })) : [],
            sensors: e.sensors ? e.sensors.map((s: any) => ({ deviceId: s.deviceId, feature: s.feature })) : [],
            sourceActions: e.sourceActions ? e.sourceActions.map((v: any) => extractValue(v)) : [],
            intermediateActions: e.intermediateActions ? e.intermediateActions.map((v: any) => extractValue(v)) : [],
            followupActions: e.followupActions ? e.followupActions.map((v: any) => extractValue(v)) : [],
            brightnessLevels: e.brightnessLevels ? e.brightnessLevels.map((v: any) => extractValue(v)) : []
        };
    }
    return {};
}

function extractStatement(s: any): any {
    if (s.$type === 'SetFeature') {
        return {
            type: 'SetFeature',
            actuator: s.actuator,
            feature: s.feature,
            value: extractValue(s.value)
        };
    } else if (s.$type === 'RequirePrecondition') {
        return {
            type: 'RequirePrecondition',
            sensor: s.sensor,
            feature: s.feature,
            value: extractValue(s.value),
            skipMessage: s.skipMessage
        };
    } else if (s.$type === 'MeasureLatency') {
        return {
            type: 'MeasureLatency',
            actuator: s.actuator,
            actuatorFeature: s.actuatorFeature,
            sensor: s.sensor,
            sensorFeature: s.sensorFeature,
            valOff: extractValue(s.valOff),
            valOn: extractValue(s.valOn),
            minChangePercent: s.minChangePercent,
            toleranceFactor: s.toleranceFactor,
            addSeconds: s.addSeconds,
            timeout: s.timeout,
            runs: s.runs
        };
    }
    return {};
}

function extractValue(v: any): any {
    if (v.stringValue !== undefined) return v.stringValue;
    if (v.numValue !== undefined) return v.numValue;
    if (v.boolValue !== undefined) return v.boolValue;
    return null;
}
