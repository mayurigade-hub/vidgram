/**
 * Estimates how many followers are likely genuine.
 * @param followers Total number of followers
 * @param authenticityScore Score from 0 to 100
 * @returns Genuine Reach count
 */
export declare function calculateGenuineReach(followers: number, authenticityScore: number): number;
/**
 * Estimates suspicious audience.
 * @param followers Total number of followers
 * @param genuineReach The calculated genuine reach
 * @returns Fake Reach count
 */
export declare function calculateFakeReach(followers: number, genuineReach: number): number;
/**
 * Estimates potential campaign budget waste.
 * @param fakeReach Suspicious audience count
 * @param followers Total number of followers
 * @param campaignBudget Total campaign budget
 * @returns Budget loss amount
 */
export declare function calculateBudgetLoss(fakeReach: number, followers: number, campaignBudget: number): number;
/**
 * Determines the actual cost of reaching a real audience.
 * @param campaignBudget Total campaign budget
 * @param genuineReach Genuine reach count
 * @returns Cost per genuine follower
 */
export declare function calculateCostPerGenuine(campaignBudget: number, genuineReach: number): number;
//# sourceMappingURL=formulas.d.ts.map