# Dark Mode Onboarding — Reference Guide

> This file consolidates the three onboarding scenarios, the recommended tools for each, and estimated effort. Use it as the authoritative source when writing or updating the team onboarding guide.
>
> Wiki source: https://dev.azure.com/powerbi/Trident/_wiki/wikis/Trident.wiki/173475/Shell-UX-dark-theme-support-guide

---

## Quick-Reference Table

| # | Scenario | Key Tool / API | Estimated Effort |
|---|----------|---------------|-----------------|
| 1 | React + Fluent UI v8/v9 + 1JS ribbon extension | `ExtensionThemeProvider` from `@trident/extension-client-theme` | ~1 day |
| 2 | Angular / other iframe-based extension | `ExtensionClientAPI` → `themeAPI` | Varies (see below) |
| 3 | PBIClient-based repo | AI tool provided by Shell team | Varies (depends on issue count) |

---

## Scenario 1 — React + Fluent UI v8/v9 + 1JS Ribbon

### What to do
1. Upgrade the relevant packages (React, Fluent UI v8/v9, 1JS ribbon).
2. Wrap the extension root with `ExtensionThemeProvider` from `@trident/extension-client-theme`.

```tsx
import { ExtensionThemeProvider } from '@trident/extension-client-theme';

function App() {
  return (
    <ExtensionThemeProvider>
      {/* your extension content */}
    </ExtensionThemeProvider>
  );
}
```

### Estimated effort
About **one day**, assuming no major custom theming conflicts and a normal validation scope.

### Validation checklist
- [ ] Package versions upgraded successfully.
- [ ] `ExtensionThemeProvider` applied at the app root.
- [ ] Initial theme renders correctly (both light and dark).
- [ ] Runtime theme switching works without a page reload.
- [ ] Key UI surfaces pass accessibility / contrast checks.

---

## Scenario 2 — Angular / Other iframe-Based Extensions

### What to do
Use the Shell-provided APIs to detect the current theme and react to theme changes at runtime:

| API | Purpose |
|-----|---------|
| `ExtensionClientAPI` | Entry point for all Shell extension APIs |
| `themeAPI` | Exposes current theme and theme-change events |

#### Pattern

```typescript
import { ExtensionClientAPI } from '@trident/extension-client';

const theme = ExtensionClientAPI.themeAPI.getCurrentTheme();
applyTheme(theme);

ExtensionClientAPI.themeAPI.onThemeChanged((newTheme) => {
  applyTheme(newTheme);
});
```

### Key requirements
- Detect the current theme **on load** (don't assume light mode).
- Listen for `themeChanged` events and re-apply styles immediately.
- Avoid hard-coded colors in component styles; use design tokens instead.
- Confirm that iframe content updates **without** requiring a full reload.

### Estimated effort
Varies. Centralizing theme handling in a single service/module and avoiding hard-coded colors are the biggest risk factors.

### Validation checklist
- [ ] `ExtensionClientAPI.themeAPI` integrated in a single theme service.
- [ ] Theme applied correctly on initial load.
- [ ] `onThemeChanged` handler fires and updates UI without reload.
- [ ] No hard-coded hex/rgb colors in component styles.

---

## Scenario 3 — PBIClient-Based Repos

### Current state
Dark mode is **already enabled** in the platform for PBIClient-based repos (e.g., Power BI). The main work is validation and legacy token cleanup.

### What to do
1. Run a full validation pass in dark mode across core user journeys.
2. Focus on: visual regressions, contrast issues, token mismatches, unreadable states.
3. **Leverage the AI tool provided by the Shell team** to accelerate detection and fixes:
   - The AI tool identifies outdated / legacy token usage patterns.
   - It suggests modern token replacements.
   - Keep a manual review step for edge cases and accessibility-sensitive UI.

### Estimated effort
Depends on the number of issues found during testing:
- **Few issues** → short stabilization pass.
- **Many legacy token issues** → plan for additional fix-and-verify cycles.

### Validation checklist
- [ ] Full dark mode validation pass completed across core journeys.
- [ ] AI tool run; legacy token suggestions reviewed and applied.
- [ ] Manual review done for edge cases and a11y-sensitive surfaces.
- [ ] No blocking contrast or readability regressions.

---

## Shared Validation Exit Criteria (All Scenarios)

- No blocking contrast or readability issues.
- Theme switching works reliably at runtime.
- No major visual regressions in core user journeys.
- Accessibility checks pass for key surfaces.

---

## References

- Shell UX dark theme support guide (internal wiki): https://dev.azure.com/powerbi/Trident/_wiki/wikis/Trident.wiki/173475/Shell-UX-dark-theme-support-guide
- `@trident/extension-client-theme` — provides `ExtensionThemeProvider` for React extensions.
- `@trident/extension-client` — provides `ExtensionClientAPI` and `themeAPI` for iframe-based extensions.
