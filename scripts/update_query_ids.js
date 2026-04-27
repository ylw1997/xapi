/* eslint-disable no-console */

const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const QUERY_IDS_PATH = path.resolve(__dirname, "../query_ids.json");

const INJECTION_SCRIPT = `
(async () => {
  if (typeof webpackChunk_twitter_responsive_web !== "undefined") {
    webpackChunk_twitter_responsive_web.push([[""], {}, e => {
      window.moduleCache = [];
      for (const c in e.c) {
        window.moduleCache.push(e.c[c]);
      }
    }]);
  }

  if (window.moduleCache) {
    return window.moduleCache
      .filter(x => typeof x.exports === "object" && x.exports && "queryId" in x.exports)
      .map(x => [x.exports.operationName, x.exports.queryId]);
  }

  return [];
})()
`;

function readQueryIds() {
  return JSON.parse(fs.readFileSync(QUERY_IDS_PATH, "utf8"));
}

function writeQueryIds(queryIds) {
  fs.writeFileSync(QUERY_IDS_PATH, `${JSON.stringify(queryIds, null, 2)}\n`, "utf8");
}

async function extractQueryIds() {
  const proxyUrl =
    process.env.HTTPS_PROXY ||
    process.env.HTTP_PROXY ||
    process.env.ALL_PROXY ||
    process.env.https_proxy ||
    process.env.http_proxy ||
    process.env.all_proxy;

  const launchConfig = { headless: true };
  if (proxyUrl) {
    launchConfig.proxy = { server: proxyUrl };
    console.log(`Detected proxy: ${proxyUrl}`);
  }

  const browser = await chromium.launch(launchConfig);
  try {
    const page = await browser.newPage();
    console.log("Navigating to x.com...");
    await page.goto("https://x.com", { waitUntil: "domcontentloaded", timeout: 90000 });

    console.log("Extracting Query IDs from web modules...");
    await page.waitForTimeout(10000);

    const results = await page.evaluate(INJECTION_SCRIPT);
    if (!results || results.length === 0) {
      throw new Error("No Query IDs extracted from x.com");
    }

    console.log(`Extracted ${results.length} operation definitions.`);
    return Object.fromEntries(results.filter(([operation, queryId]) => operation && queryId));
  } finally {
    await browser.close();
  }
}

async function updateQueryIds() {
  const current = readQueryIds();
  const extracted = await extractQueryIds();
  const next = { ...current };
  let updatedCount = 0;

  for (const operation of Object.keys(current)) {
    const latestQueryId = extracted[operation];
    if (!latestQueryId) {
      console.log(`Skip ${operation}: not found on x.com`);
      continue;
    }

    if (current[operation] === latestQueryId) {
      console.log(`${operation} is up to date (${latestQueryId})`);
      continue;
    }

    console.log(`Update ${operation}: ${current[operation]} -> ${latestQueryId}`);
    next[operation] = latestQueryId;
    updatedCount += 1;
  }

  if (updatedCount > 0) {
    writeQueryIds(next);
    console.log(`Updated ${updatedCount} Query ID(s).`);
  } else {
    console.log("No Query ID changes.");
  }
}

if (require.main === module) {
  updateQueryIds().catch((error) => {
    console.error(error.message);
    process.exit(1);
  });
}

module.exports = {
  extractQueryIds,
  readQueryIds,
  updateQueryIds,
  writeQueryIds,
};
