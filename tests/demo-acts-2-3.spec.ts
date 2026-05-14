import { test, expect } from '@playwright/test';
import {
  settingsGear,
  settingsPanel,
  generalTab,
  darkModeToggle,
  navItem,
  helpButton,
  assertDarkShell,
} from './helpers/shell';

// ─────────────────────────────────────────────────────────────────────────────
// DEMO SCRIPT — Acts 2 & 3
//
// Act 2 — "Discovery": Maya turns on dark mode in Settings
// Act 3 — "It Follows Her": Dark mode persists and covers every shell surface
// ─────────────────────────────────────────────────────────────────────────────

const BASE_URL =
  'https://daily.powerbi.com/home?darkModeInUserSettings=1&experience=fabric-developer';

test.describe('Fabric Dark Mode Demo – Acts 2 & 3', () => {

  // ── Act 2: Enable dark mode via Settings ────────────────────────────────────
  test('Act 2 — Maya enables dark mode from Settings › General', async ({ page }) => {

    // ── Step 1: Land on Fabric home ──────────────────────────────────────────
    await test.step('Navigate to Fabric home (light mode)', async () => {
      await page.goto(BASE_URL);
      await page.waitForLoadState('networkidle');
      await page.screenshot({ path: 'test-results/screenshots/act2-01-light-home.png', fullPage: false });
      console.log('\n🎬  Act 2 — Maya opens Fabric at the end of a long day...');
      console.log('     The bright white shell is jarring in her dim office.\n');
    });

    // ── Step 2: Open Settings gear ───────────────────────────────────────────
    await test.step('Click the Settings gear icon in the header', async () => {
      const gear = settingsGear(page);
      await gear.waitFor({ state: 'visible', timeout: 20_000 });
      await gear.highlight();
      await page.screenshot({ path: 'test-results/screenshots/act2-02-gear-highlight.png' });
      await gear.click();
      console.log('⚙️   Settings gear clicked');
    });

    // ── Step 3: Go to General tab ────────────────────────────────────────────
    await test.step('Click the "General" tab in Settings panel', async () => {
      const panel = settingsPanel(page);
      await panel.waitFor({ state: 'visible', timeout: 15_000 });
      await page.screenshot({ path: 'test-results/screenshots/act2-03-settings-open.png' });

      const general = generalTab(page);
      await general.waitFor({ state: 'visible' });
      await general.click();
      console.log('📋  Settings › General tab opened');
      await page.screenshot({ path: 'test-results/screenshots/act2-04-general-tab.png' });
    });

    // ── Step 4: Toggle dark mode ON ──────────────────────────────────────────
    await test.step('Toggle "Enable dark mode" to ON', async () => {
      const toggle = darkModeToggle(page);
      await toggle.waitFor({ state: 'visible', timeout: 10_000 });

      // Capture before state
      const isBefore = await toggle.isChecked().catch(() => false);
      console.log(`🌑  Dark mode toggle — before: ${isBefore ? 'ON' : 'OFF'}`);

      if (!isBefore) {
        await toggle.click();
      }

      await page.screenshot({ path: 'test-results/screenshots/act2-05-toggle-on.png' });
      console.log('✅  Toggled dark mode ON');
    });

    // ── Step 5: Close settings and verify shell goes dark immediately ────────
    await test.step('Close Settings — shell switches to dark immediately', async () => {
      await page.keyboard.press('Escape');
      // Give the theme transition animation time to complete
      await page.waitForTimeout(1000);
      await page.screenshot({ path: 'test-results/screenshots/act2-06-dark-applied.png', fullPage: false });
      await assertDarkShell(page, 'Home (post-toggle)');
      console.log('🌙  Shell is now DARK — zero-friction, instant, no reload required\n');
    });
  });


  // ── Act 3: Dark mode persists + covers every shell entry point ───────────────
  test('Act 3 — Dark mode persists and spans every shell surface', async ({ page }) => {

    // Assume dark mode is already saved from Act 2; if running isolated, re-enable
    await test.step('Navigate to Fabric home (expect dark mode already active)', async () => {
      await page.goto(BASE_URL);
      await page.waitForLoadState('networkidle');
      console.log('\n🎬  Act 3 — Maya closes & reopens her browser the next morning...');
    });

    // ── Refresh: preference survived ────────────────────────────────────────
    await test.step('Refresh — dark mode persists after reload', async () => {
      await page.reload({ waitUntil: 'networkidle' });
      await page.waitForTimeout(800);
      await assertDarkShell(page, 'Home (after refresh)');
      await page.screenshot({ path: 'test-results/screenshots/act3-01-persist-after-refresh.png' });
      console.log('♻️   Refreshed — still dark. Preference is stored server-side.\n');
    });

    // ── Entry point tour ─────────────────────────────────────────────────────
    const entryPoints: Array<{ label: string; navLabel?: string; url?: string }> = [
      { label: 'Home',            url: '/home?darkModeInUserSettings=1&experience=fabric-developer' },
      { label: 'Browse',          navLabel: 'Browse' },
      { label: 'Workspace list',  navLabel: 'Workspaces' },
      { label: 'Monitoring Hub',  navLabel: 'Monitor' },
    ];

    for (const [i, entry] of entryPoints.entries()) {
      await test.step(`Visit entry point: ${entry.label}`, async () => {
        if (entry.url) {
          await page.goto(entry.url);
          await page.waitForLoadState('networkidle');
        } else if (entry.navLabel) {
          const link = navItem(page, entry.navLabel);
          await link.waitFor({ state: 'visible', timeout: 15_000 });
          await link.click();
          await page.waitForLoadState('networkidle');
        }

        await page.waitForTimeout(600);
        const slug = entry.label.toLowerCase().replace(/\s+/g, '-');
        await page.screenshot({
          path: `test-results/screenshots/act3-0${i + 2}-${slug}.png`,
          fullPage: false,
        });
        await assertDarkShell(page, entry.label);
        console.log(`✅  ${entry.label.padEnd(18)} → header is dark`);
      });
    }

    // ── Help pane ────────────────────────────────────────────────────────────
    await test.step('Open Help pane — also dark', async () => {
      const help = helpButton(page);
      await help.waitFor({ state: 'visible', timeout: 10_000 });
      await help.click();
      await page.waitForTimeout(600);
      await page.screenshot({ path: 'test-results/screenshots/act3-06-help-pane.png' });
      await assertDarkShell(page, 'Help pane open');
      console.log('✅  Help pane          → dark');
      await page.keyboard.press('Escape');
    });

    console.log('\n🎯  All shell entry points confirmed DARK.');
    console.log('    Maya\'s preference follows her everywhere — across sessions and surfaces.\n');
  });

});
