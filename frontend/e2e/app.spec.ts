import { test, expect } from '@playwright/test';

test('has title and loads config', async ({ page }) => {
  await page.goto('http://localhost:5173/');

  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/NIST Chatbot/i);

  // Expect Sidebar to render the agents (config loaded)
  await expect(page.locator('text=Specialist Agents')).toBeVisible();
});
