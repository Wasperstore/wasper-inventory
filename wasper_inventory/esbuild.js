const esbuild = require('esbuild');
const path = require('path');
const fs = require('fs');

// Get the --apps flag value
const apps = process.argv.includes('--apps') 
    ? process.argv[process.argv.indexOf('--apps') + 1].split(',')
    : [];

// Get the --production flag
const isProduction = process.argv.includes('--production');

// Function to get the public path for an app
function get_public_path(app) {
    return path.resolve(__dirname, app, 'public');
}

// Function to get the build.json path for an app
function get_build_json_path(app) {
    return path.resolve(get_public_path(app), 'build.json');
}

// Function to read the build map from build.json
function read_build_map(app) {
    const build_json_path = get_build_json_path(app);
    if (!fs.existsSync(build_json_path)) {
        console.error(`build.json not found for app ${app} at ${build_json_path}`);
        return null;
    }
    const build_map = JSON.parse(fs.readFileSync(build_json_path, 'utf8'));
    return build_map[app] || null;
}

// Function to get all files to build for an app
function get_all_files_to_build(app) {
    const build_map = read_build_map(app);
    if (!build_map) return [];
    
    const files = [];
    for (const [bundle, sources] of Object.entries(build_map)) {
        files.push(...sources.map(source => ({
            source: path.resolve(get_public_path(app), source),
            bundle: path.resolve(get_public_path(app), bundle)
        })));
    }
    return files;
}

// Build function
async function build() {
    for (const app of apps) {
        console.log(`Building assets for ${app}...`);
        const files = get_all_files_to_build(app);
        
        if (files.length === 0) {
            console.error(`No files to build for ${app}`);
            continue;
        }

        for (const { source, bundle } of files) {
            try {
                if (!fs.existsSync(source)) {
                    console.error(`Source file not found: ${source}`);
                    continue;
                }

                await esbuild.build({
                    entryPoints: [source],
                    bundle: true,
                    outfile: bundle,
                    minify: isProduction,
                    sourcemap: !isProduction,
                    target: ['es2017'],
                    format: 'iife',
                    platform: 'browser',
                    define: {
                        'process.env.NODE_ENV': isProduction ? '"production"' : '"development"'
                    }
                });
                console.log(`Built ${bundle}`);
            } catch (error) {
                console.error(`Error building ${bundle}:`, error);
            }
        }
    }
}

// Run the build
build().catch(error => {
    console.error('Build failed:', error);
    process.exit(1);
});