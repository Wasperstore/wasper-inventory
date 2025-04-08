const esbuild = require('esbuild');
const path = require('path');

const production = process.argv.includes('--production');
const watch = process.argv.includes('--watch');

async function build() {
    try {
        const common_config = {
            entryPoints: {
                'wasper_inventory': 'public/js/wasper_inventory.js',
            },
            bundle: true,
            minify: production,
            sourcemap: !production,
            target: ['es2017'],
            outdir: path.join('public', 'dist'),
            format: 'iife',
            loader: {
                '.js': 'jsx',
                '.css': 'css',
                '.vue': 'js'
            },
            logLevel: 'info',
        };

        if (watch) {
            const context = await esbuild.context(common_config);
            await context.watch();
        } else {
            await esbuild.build(common_config);
        }
    } catch (e) {
        console.error('Build failed:', e.message);
        process.exit(1);
    }
}

build(); 