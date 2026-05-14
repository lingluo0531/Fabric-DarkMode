import { Page, Locator, expect } from '@playwright/test';

/**
 * Selectors for Fabric Shell UI elements.
 * These are intentionally kept as CSS attribute / role selectors
 * rather than hard-coded class names so they survive minor shell updates.
 */

// ── Header ────────────────────────────────────────────────────────────────────
export const header = (page: Page): Locator =>
  page.locator('[data-testid="shell-header"], header[role="banner"], .fui-header').first();

// ── Settings gear in header ───────────────────────────────────────────────────
export const settingsGear = (page: Page): Locator =>
  page.locator('[data-testid="settings-gear"], [aria-label*="Settings"], button[title*="Settings"]').first();

// ── Settings panel ────────────────────────────────────────────────────────────
export const settingsPanel = (page: Page): Locator =>
  page.locator('[data-testid="settings-panel"], [role="dialog"][aria-label*="Settings"]').first();

// ── General tab inside settings ───────────────────────────────────────────────
export const generalTab = (page: Page): Locator =>
  page.locator('[role="tab"][name*="General"], button:has-text("General")').first();

// ── Dark mode toggle ──────────────────────────────────────────────────────────
export const darkModeToggle = (page: Page): Locator =>
  page.locator(
    '[data-testid="dark-mode-toggle"], ' +
    '[aria-label*="dark mode"], ' +
    'input[type="checkbox"][name*="dark"], ' +
    'div:has-text("Enable dark mode") [role="switch"]'
  ).first();

// ── Left nav rail ─────────────────────────────────────────────────────────────
export const navRail = (page: Page): Locator =>
  page.locator('[data-testid="nav-rail"], nav[aria-label*="navigation"], .ms-Nav').first();

// ── Help pane trigger ─────────────────────────────────────────────────────────
export const helpButton = (page: Page): Locator =>
  page.locator('[aria-label*="Help"], button[title*="Help"]').first();

// ── Nav items by label ────────────────────────────────────────────────────────
export const navItem = (page: Page, label: string): Locator =>
  page.locator(`[data-testid="nav-item-${label.toLowerCase()}"], a:has-text("${label}"), [role="menuitem"]:has-text("${label}")`).first();

// ── Theme detection ───────────────────────────────────────────────────────────
/**
 * Returns true when the shell root has a dark-mode class / attribute applied.
 */
export async function isDarkMode(page: Page): Promise<boolean> {
  return page.evaluate(() => {
    const root = document.documentElement;
    return (
      root.classList.contains('dark') ||
      root.getAttribute('data-theme') === 'dark' ||
      root.getAttribute('data-color-scheme') === 'dark' ||
      document.body.classList.contains('dark') ||
      document.body.getAttribute('data-theme') === 'dark' ||
      // Fluent v9 theme token check – background should be very dark
      window.getComputedStyle(document.body).backgroundColor.includes('rgb(1') === false &&
      (() => {
        const bg = window.getComputedStyle(document.body).backgroundColor;
        const match = bg.match(/\d+/g);
        if (!match) return false;
        const [r, g, b] = match.map(Number);
        return r < 60 && g < 60 && b < 60;
      })()
    );
  });
}

/**
 * Assert the shell is in dark mode by checking background luminance of the header.
 */
export async function assertDarkShell(page: Page, entryPoint: string) {
  const bgColor = await page.evaluate(() => {
    const header =
      document.querySelector('[data-testid="shell-header"]') ||
      document.querySelector('header') ||
      document.body;
    return window.getComputedStyle(header).backgroundColor;
  });

  // Extract RGB and compute rough luminance
  const rgb = bgColor.match(/\d+/g)?.map(Number) ?? [255, 255, 255];
  const luminance = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2];

  console.log(`  [${entryPoint}] header bg="${bgColor}" luminance=${luminance.toFixed(0)}`);

  // Dark theme: luminance below 80 (vs. white = 255)
  expect(luminance, `Shell should be dark at "${entryPoint}" (bg: ${bgColor})`).toBeLessThan(80);
}
