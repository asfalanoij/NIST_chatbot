import { test, expect } from '@playwright/test';

test('has title and loads config', async ({ page }) => {
  await page.goto('/');

  await expect(page).toHaveTitle(/NIST Chatbot/i);
  await expect(page.locator('text=Specialist Agents')).toBeVisible();
});

test('quick prompt buttons are visible', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByText('Explain AC-2')).toBeVisible();
  await expect(page.getByText('Risk Assessment')).toBeVisible();
  await expect(page.getByText('Audit Prep')).toBeVisible();
});
