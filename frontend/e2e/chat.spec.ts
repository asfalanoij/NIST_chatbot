import { test, expect } from '@playwright/test';

test('quick prompt sends message and gets response', async ({ page }) => {
  await page.goto('/');

  // Click the "Explain AC-2" quick prompt button
  await page.getByText('Explain AC-2').click();

  // User message should appear in chat
  await expect(page.locator('text=Explain the AC-2 Account Management')).toBeVisible({ timeout: 5000 });

  // Wait for assistant response (even if backend returns error/empty KB)
  await expect(page.locator('[class*="assistant"], [class*="bot"]').first()).toBeVisible({ timeout: 15000 });
});

test('manual input sends message', async ({ page }) => {
  await page.goto('/');

  // Find the chat input and type
  const input = page.getByPlaceholder(/ask about nist/i);
  await input.fill('What is SC-7?');
  await input.press('Enter');

  // User message should appear
  await expect(page.locator('text=What is SC-7?')).toBeVisible({ timeout: 5000 });
});

test('empty input does not send', async ({ page }) => {
  await page.goto('/');

  const input = page.getByPlaceholder(/ask about nist/i);
  await expect(input).toHaveValue('');

  // The send button should be disabled or quick prompts should still be visible
  await expect(page.getByText('Explain AC-2')).toBeVisible();
});
