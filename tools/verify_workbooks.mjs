import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const files = [
  "spreadsheets/CRAMPACS_Governance_Master.xlsx",
  "spreadsheets/domains/crampacs-med_CRAMPACS-MED_Workbook.xlsx",
  "spreadsheets/domains/crampacs-fin_CRAMPACS-FIN_Workbook.xlsx",
  "spreadsheets/domains/crampacs-phy_CRAMPACS-PHY_Workbook.xlsx",
];

for (const file of files) {
  const blob = await FileBlob.load(file);
  const workbook = await SpreadsheetFile.importXlsx(blob);
  const inspect = await workbook.inspect({
    kind: "table",
    range: "A1:H12",
    include: "values",
    tableMaxRows: 12,
    tableMaxCols: 8,
  });
  console.log(`VERIFIED ${file}`);
  console.log(inspect.ndjson.split("\n").slice(0, 3).join("\n"));
}
