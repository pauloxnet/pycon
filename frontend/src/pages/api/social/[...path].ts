import { NowRequest, NowResponse } from "@now/node";
import chrome from "chrome-aws-lambda";
import puppeteer from "puppeteer-core";

import { CardType, getSize } from "~/helpers/social-card";

export default async (req: NowRequest, res: NowResponse) => {
  const type = "png";
  const userAgent = req.headers["user-agent"];
  const path = (req.query.path as string[]).join("/");
  const sizeName = getSizeNameForScraper(userAgent);
  const secure = !req.headers.host.includes("localhost");
  const url = `http${secure ? "s" : ""}://${
    req.headers.host
  }/${path}/social?card-type=${sizeName}`;

  console.log("Taking screenshot of", url);
  const options = process.env.AWS_REGION
    ? {
        args: chrome.args,
        executablePath: await chrome.executablePath,
        headless: chrome.headless,
      }
    : {
        args: [],
        executablePath:
          process.platform === "win32"
            ? "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            : process.platform === "linux"
            ? "/usr/bin/google-chrome"
            : "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
      };

  try {
    const size = getSize(sizeName);

    const browser = await puppeteer.launch(options);

    const page = await browser.newPage();
    await page.setViewport({ ...size, deviceScaleFactor: 2 });
    await page.goto(url);
    await page.waitForSelector("#social-card");

    const file = await page.screenshot();

    res.statusCode = 200;
    res.setHeader("Content-Type", `image/${type}`);
    res.end(file);
  } catch (e) {
    res.statusCode = 500;
    res.setHeader("Content-Type", "text/html");
    res.end("<h1>Server Error</h1><p>Sorry, there was a problem</p>");
    console.error(e.message);
  }
};

export type Scraper = "twitter" | "generic";

const getSizeNameForScraper = (userAgent: string): CardType => {
  const scraper = getScraperName(userAgent);

  switch (scraper) {
    case "twitter":
      return "social-twitter";
    default:
      return "social";
  }
};

const getScraperName = (userAgent: string): Scraper => {
  if (userAgent.indexOf("Twitterbot/") !== -1) {
    return "twitter";
  }

  return "generic";
};
