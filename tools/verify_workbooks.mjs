import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";
import fs from "node:fs/promises";
import path from "node:path";

const domainDir = "spreadsheets/domains";
const domainFiles = (await fs.readdir(domainDir))
  .filter((file) => file.endsWith(".xlsx"))
  .sort()
  .map((file) => path.join(domainDir, file));

const files = [
  "spreadsheets/CRAMPACS_Governance_Master.xlsx",
  ...domainFiles,
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
