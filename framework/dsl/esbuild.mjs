import * as esbuild from 'esbuild';
import path from 'path';

const watch = process.argv.includes('--watch');

const ctxExtension = await esbuild.context({
    entryPoints: ['src/extension/main.ts'],
    outfile: 'out/extension/main.cjs',
    bundle: true,
    format: 'cjs',
    external: ['vscode'],
    platform: 'node',
    sourcemap: true,
    minify: false
});

const ctxServer = await esbuild.context({
    entryPoints: ['src/language/main.ts'],
    outfile: 'out/language/main.cjs',
    bundle: true,
    format: 'cjs',
    external: ['vscode'],
    platform: 'node',
    sourcemap: true,
    minify: false
});

if (watch) {
    await Promise.all([ctxExtension.watch(), ctxServer.watch()]);
} else {
    await Promise.all([ctxExtension.rebuild(), ctxServer.rebuild()]);
    await Promise.all([ctxExtension.dispose(), ctxServer.dispose()]);
}
