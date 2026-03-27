import type { Model } from '../../language/src/generated/ast.js';
import { expandToNode, toString } from 'langium/generate';
import * as fs from 'node:fs';
import * as path from 'node:path';

export function generateJavaScript(model: Model, filePath: string, destination: string | undefined): string {
    // Wir berechnen den Namen und Pfad einfach direkt hier
    const name = path.basename(filePath, path.extname(filePath));
    const dest = destination ?? path.join(path.dirname(filePath), 'generated');
    const generatedFilePath = path.join(dest, `${name}.js`);

    const fileNode = expandToNode`
        "use strict";
        // Metamorphic Testing Framework für Digital Twins
        // Modell: ${name}
        console.log("Anzahl der Test-Elemente: ${model.elements.length}");
    `.appendNewLine();

    if (!fs.existsSync(dest)) {
        fs.mkdirSync(dest, { recursive: true });
    }
    fs.writeFileSync(generatedFilePath, toString(fileNode));
    return generatedFilePath;
}