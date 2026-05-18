# Fabric Team Onboarding to Dark Mode

## Purpose
This document helps Fabric teams onboard to dark mode support across common extension stacks.

## Scope
The guidance below covers three common scenarios:
1. Repos based on the PBIClient stack (for example, Power BI teams)
2. React extensions using Fluent UI v8/v9 and 1JS ribbon
3. Angular extensions or other iframe-based apps

## 1) PBIClient-Based Repos (for example, Power BI)
### Current state
Dark mode is already enabled in the platform for these repos.

### What teams should do
- Run a full validation pass in dark mode across core user journeys.
- Focus on visual regressions, contrast issues, token mismatches, and unreadable states.
- Prioritize high-traffic surfaces and critical workflows first.

### Legacy token migration
- For legacy tokens, leverage AI tooling to accelerate detection and fixes.
- The AI tool can help identify outdated token usage patterns and suggest replacements.
- Keep a manual review step for edge cases and accessibility-sensitive UI.

### Estimated effort
- Effort depends on how many issues are found during testing.
- If issues are limited, this can be a short stabilization pass.
- If many legacy token issues surface, plan for additional fix-and-verify cycles.

## 2) React + Fluent UI v8/v9 + 1JS Ribbon Extensions
### Recommended approach
To support dark mode:
- Upgrade the relevant React/Fluent UI and extension dependencies.
- Wrap the extension with `ExtensionThemeProvider` from `@trident/extension-client-theme`.

### Estimated effort
- Typical estimate: about one day.
- This assumes no major custom theming conflicts and normal validation scope.

### Implementation checklist
- Upgrade package versions.
- Apply `ExtensionThemeProvider` at the app root.
- Verify both initial theme render and runtime theme switching.
- Validate key UI surfaces for accessibility and contrast.

## 3) Angular or Other iframe-Based Extensions
### Theme integration
For Angular or other iframe apps, use:
- `ExtensionClientAPI`
- `themeAPI`

### Required capabilities
- Detect the current theme on load.
- Listen for theme changes at runtime.
- Re-apply theme styles/tokens immediately after a theme change event.

### Practical notes
- Keep theme handling centralized in one service/module.
- Avoid hard-coded colors in component styles.
- Confirm iframe content updates without requiring a full reload.

## Validation Exit Criteria (All Scenarios)
- No blocking contrast or readability issues.
- Theme switching works reliably at runtime.
- No major visual regressions in core user journeys.
- Accessibility checks pass for key surfaces.

## Summary
- PBIClient-based repos: dark mode is enabled; main work is comprehensive test + targeted fixes, especially legacy token cleanup with AI assistance.
- React + Fluent + 1JS ribbon: package upgrades + `ExtensionThemeProvider`; usually about one day.
- Angular/iframe apps: use `ExtensionClientAPI themeAPI` to detect and react to current theme and theme changes.
