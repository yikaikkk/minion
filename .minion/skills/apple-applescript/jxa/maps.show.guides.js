// Run: osascript -l JavaScript jxa/maps_show_guides.js

function run(argv) {
  void argv;
  const app = Application.currentApplication();
  app.includeStandardAdditions = true;
  const Maps = Application("Maps");
  Maps.activate();
  app.openLocation("maps://?show=guides");
}