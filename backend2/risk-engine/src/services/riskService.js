"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.classifyRisk = classifyRisk;
exports.analyzeInfluencerRisk = analyzeInfluencerRisk;
const types_1 = require("../types");
const formulas_1 = require("../utils/formulas");
/**
 * Classifies the risk of an influencer based on their authenticity score.
 * > 70 = Shortlist
 * 55-70 = Monitor
 * 40-55 = Pause
 * < 40 = Reject
 */
function classifyRisk(authenticityScore) {
    if (authenticityScore > 70) {
        return { label: 'Shortlist', severity: 1 };
    }
    else if (authenticityScore >= 55) {
        return { label: 'Monitor', severity: 2 };
    }
    else if (authenticityScore >= 40) {
        return { label: 'Pause', severity: 3 };
    }
    else {
        return { label: 'Reject', severity: 4 };
    }
}
/**
 * Analyzes an influencer's campaign risk and calculates metrics.
 */
function analyzeInfluencerRisk(influencer, context) {
    const genuineReach = (0, formulas_1.calculateGenuineReach)(influencer.followers, influencer.authenticityScore);
    const fakeReach = (0, formulas_1.calculateFakeReach)(influencer.followers, genuineReach);
    const budgetLoss = (0, formulas_1.calculateBudgetLoss)(fakeReach, influencer.followers, context.campaignBudget);
    const costPerGenuineFollower = (0, formulas_1.calculateCostPerGenuine)(context.campaignBudget, genuineReach);
    const classification = classifyRisk(influencer.authenticityScore);
    return {
        genuineReach,
        fakeReach,
        budgetLoss,
        costPerGenuineFollower,
        classification
    };
}
//# sourceMappingURL=riskService.js.map