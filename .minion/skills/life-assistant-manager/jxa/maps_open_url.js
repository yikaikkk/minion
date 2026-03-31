// Run: osascript -l JavaScript jxa/maps_open_url.js "maps://?q=coffee"
// Original maps.ts used Application("Maps") + openLocation / search.

function run(argv) {
  const Maps = Application("Maps");
  Maps.activate();
  if (argv.length > 0) {
    const app = Application.currentApplication();
    app.includeStandardAdditions = true;

    const  safeUrl=encodeURI(argv[0])

    app.openLocation(safeUrl);
  }
}