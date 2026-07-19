import { Command } from 'commander';
import chalk from 'chalk';
import * as fs from 'fs';
import { createMtDslServices } from '../language/mt-dsl-module.js';
import { Model } from '../language/generated/ast.js';
import { generateJson } from './generator.js';
import { URI } from 'langium';
import { NodeFileSystem } from 'langium/node';
import * as path from 'path';

export const generateAction = async (fileName: string | undefined, opts: { destination?: string }): Promise<void> => {
    const services = createMtDslServices(NodeFileSystem).MtDsl;
    await services.shared.workspace.WorkspaceManager.initializeWorkspace([]);
    
    const targetDir = process.env.INIT_CWD || process.cwd();
    let filesToProcess: string[] = [];
    if (fileName) {
        filesToProcess.push(path.resolve(targetDir, fileName));
    } else {
        filesToProcess = fs.readdirSync(targetDir).filter(f => f.endsWith('.mt')).map(f => path.join(targetDir, f));
        if (filesToProcess.length === 0) {
            console.error(chalk.red(`No .mt files found in the current directory.`));
            process.exit(1);
        }
    }

    for (const currentFile of filesToProcess) {
        if (!fs.existsSync(currentFile)) {
            console.error(chalk.red(`File ${currentFile} does not exist.`));
            continue;
        }

        const document = services.shared.workspace.LangiumDocumentFactory.fromString(
            fs.readFileSync(currentFile, 'utf-8'),
            URI.file(path.resolve(currentFile))
        );
        await services.shared.workspace.DocumentBuilder.build([document], { validation: true });

        const validationErrors = (document.diagnostics ?? []).filter(e => e.severity === 1);
        if (validationErrors.length > 0) {
            console.error(chalk.red(`There are validation errors in ${currentFile}:`));
            for (const validationError of validationErrors) {
                console.error(chalk.red(
                    `line ${validationError.range.start.line + 1}: ${validationError.message} [${document.textDocument.getText(validationError.range)}]`
                ));
            }
            continue;
        }

        const generatedFilePath = generateJson(document.parseResult.value as Model, currentFile, opts.destination);
        console.log(chalk.green(`JSON generated successfully: ${generatedFilePath}`));
    }
};

export default function main(): void {
    const program = new Command();
    program.version('1.0.0');

    program
        .command('generate')
        .argument('[file]', 'source file (optional, compiles all .mt files in folder if omitted)')
        .option('-d, --destination <dir>', 'destination directory of generating')
        .description('generates JSON from MT DSL')
        .action(generateAction);

    program.parse(process.argv);
}

import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
if (process.argv[1] === __filename) {
    main();
}
