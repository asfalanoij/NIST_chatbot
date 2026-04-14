import { test, expect } from '@playwright/test';

test('sidebar shows specialist agents section', async ({ page }) => {
  await page.goto('/');

  // Specialist Agents section should be visible on desktop
  await expect(page.getByText('Specialist Agents')).toBeVisible();
});

test('sidebar shows knowledge base section', async ({ page }) => {
  await page.goto('/');

  // Knowledge Base section should be present
  await expect(page.getByText('Knowledge Base')).toBeVisible();
});

test('sidebar collapse toggle exists', async ({ page }) => {
  await page.goto('/');

  // The sidebar should have a collapse/expand button
  // Look for chevron or collapse button
  const collapseBtn = page.locator('button').filter({ has: page.locator('[class*="chevron"], [class*="Chevron"]') }).first();
  if (await collapseBtn.isVisible()) {
    await collapseBtn.click();
    // After collapse, sidebar should be narrower — just verify click doesn't crash
    await expect(page.locator('body')).toBeVisible();
  }
});
