"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.calculateGenuineReach = calculateGenuineReach;
exports.calculateFakeReach = calculateFakeReach;
exports.calculateBudgetLoss = calculateBudgetLoss;
exports.calculateCostPerGenuine = calculateCostPerGenuine;
/**
 * Estimates how many followers are likely genuine.
 * @param followers Total number of followers
 * @param authenticityScore Score from 0 to 100
 * @returns Genuine Reach count
 */
function calculateGenuineReach(followers, authenticityScore) {
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
function calculateFakeReach(followers, genuineReach) {
    return Math.max(0, followers - genuineReach);
}
/**
 * Estimates potential campaign budget waste.
 * @param fakeReach Suspicious audience count
 * @param followers Total number of followers
 * @param campaignBudget Total campaign budget
 * @returns Budget loss amount
 */
function calculateBudgetLoss(fakeReach, followers, campaignBudget) {
    if (followers <= 0)
        return 0;
    return (fakeReach / followers) * campaignBudget;
}
/**
 * Determines the actual cost of reaching a real audience.
 * @param campaignBudget Total campaign budget
 * @param genuineReach Genuine reach count
 * @returns Cost per genuine follower
 */
function calculateCostPerGenuine(campaignBudget, genuineReach) {
    if (genuineReach <= 0)
        return Infinity; // Prevent division by zero
    return campaignBudget / genuineReach;
}
//# sourceMappingURL=formulas.js.map