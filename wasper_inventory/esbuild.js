const path = require('path');
const fs = require('fs');

// Get the --apps flag value
const apps_flag_index = process.argv.indexOf('--apps');
const apps = apps_flag_index > -1 ? process.argv[apps_flag_index + 1].split(',') : [];

// Get the production flag
const production = process.argv.includes('--production');

function get_public_path(app) {
    // First try the app directory itself
    const direct_path = path.resolve(__dirname, 'public');
    if (fs.existsSync(direct_path)) {
        return direct_path;
    }
    // Fallback to looking in parent directory
    return path.resolve(__dirname, '..', 'public');
}

function get_build_json_path(app) {
    const public_path = get_public_path(app);
    const build_json_path = path.resolve(public_path, 'build.json');
    if (!fs.existsSync(build_json_path)) {
        console.error(`Build JSON not found at: ${build_json_path}`);
        return null;
    }
    return build_json_path;
}

function get_build_map(app) {
    const build_json_path = get_build_json_path(app);
    if (!build_json_path) return null;
    
    try {
        return require(build_json_path);
    } catch (e) {
        console.error(`Error reading build.json for app ${app}:`, e.message);
        return null;
    }
}

async function build() {
    const esbuild = require('esbuild');
    
    for (const app of apps) {
        console.log(`Building assets for app: ${app}`);
        const build_map = get_build_map(app);
        
        if (!build_map || !build_map[app]) {
            console.error(`Invalid build map for app: ${app}`);
            continue;
        }

        const public_path = get_public_path(app);
        const app_build_map = build_map[app];

        for (const [bundle, files] of Object.entries(app_build_map)) {
            console.log(`Building bundle: ${bundle}`);
            
            // Ensure the dist directory exists
            const dist_dir = path.resolve(public_path, 'dist');
            if (!fs.existsSync(dist_dir)) {
                fs.mkdirSync(dist_dir, { recursive: true });
            }

            const outfile = path.resolve(dist_dir, bundle);
            const entryPoints = files.map(file => {
                // Remove 'public/' prefix if it exists
                const clean_file = file.replace(/^public\//, '');
                const entry_path = path.resolve(public_path, clean_file);
                
                if (!fs.existsSync(entry_path)) {
                    console.error(`Entry point not found: ${entry_path}`);
                    return null;
                }
                return entry_path;
            }).filter(Boolean);

            if (entryPoints.length === 0) {
                console.error(`No valid entry points found for bundle: ${bundle}`);
                continue;
            }

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
                console.log(`Successfully built: ${bundle}`);
            } catch (e) {
                console.error(`Failed to build ${bundle}:`, e.message);
                process.exit(1);
            }
        }
    }
}

build();