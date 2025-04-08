const path = require('path');
const fs = require('fs');

// Get the --apps flag value
const apps_flag_index = process.argv.indexOf('--apps');
const apps = apps_flag_index > -1 ? process.argv[apps_flag_index + 1].split(',') : [];

// Get the production flag
const production = process.argv.includes('--production');

function get_public_path(app) {
    return path.resolve(`./${app}/public`);
}

function get_build_json_path(app) {
    return path.resolve(`./${app}/public/build.json`);
}

function get_build_map(app) {
    const build_json_path = get_build_json_path(app);
    if (!fs.existsSync(build_json_path)) {
        return null;
    }
    return require(build_json_path);
}

async function build() {
    const esbuild = require('esbuild');
    
    for (const app of apps) {
        const build_map = get_build_map(app);
        if (!build_map || !build_map[app]) continue;

        const public_path = get_public_path(app);
        const app_build_map = build_map[app];

        for (const [bundle, files] of Object.entries(app_build_map)) {
            const outfile = path.resolve(public_path, 'dist', bundle);
            const entryPoints = files.map(file => path.resolve(public_path, file));

            try {
                await esbuild.build({
                    entryPoints,
                    bundle: true,
                    minify: production,
                    sourcemap: !production,
                    target: ['es2017'],
                    outfile,
                    format: 'iife',
                    loader: {
                        '.js': 'jsx',
                        '.css': 'css',
                        '.vue': 'js'
                    },
                    logLevel: 'info'
                });
            } catch (e) {
                console.error(`Failed to build ${bundle}:`, e.message);
                process.exit(1);
            }
        }
    }
}

build(); 