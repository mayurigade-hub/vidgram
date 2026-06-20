/**
 * Estimates how many followers are likely genuine.
 * @param followers Total number of followers
 * @param authenticityScore Score from 0 to 100
 * @returns Genuine Reach count
 */
export function calculateGenuineReach(followers: number, authenticityScore: number): number {
  // Ensure we don't have negative numbers or >100 score issues
  const validScore = Math.max(0, Math.min(100, authenticityScore));
  return Math.max(0, followers * (validScore / 100));
}

/**
 * Estimates suspicious audience.
 * @param followers Total number of followers
 * @param genuineReach The calculated genuine reach
 * @returns Fake Reach count
 */
export function calculateFakeReach(followers: number, genuineReach: number): number {
  return Math.max(0, followers - genuineReach);
}

/**
 * Estimates potential campaign budget waste.
 * @param fakeReach Suspicious audience count
 * @param followers Total number of followers
 * @param campaignBudget Total campaign budget
 * @returns Budget loss amount
 */
export function calculateBudgetLoss(fakeReach: number, followers: number, campaignBudget: number): number {
  if (followers <= 0) return 0;
  return (fakeReach / followers) * campaignBudget;
}

/**
 * Determines the actual cost of reaching a real audience.
 * @param campaignBudget Total campaign budget
 * @param genuineReach Genuine reach count
 * @returns Cost per genuine follower
 */
export function calculateCostPerGenuine(campaignBudget: number, genuineReach: number): number {
  if (genuineReach <= 0) return Infinity; // Prevent division by zero
  return campaignBudget / genuineReach;
}
