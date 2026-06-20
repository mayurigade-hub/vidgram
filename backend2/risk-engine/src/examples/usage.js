"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const riskService_1 = require("../services/riskService");
const comparisonService_1 = require("../services/comparisonService");
const influencerA = {
    name: 'Influencer A',
    followers: 100000,
    engagementRate: 3.5,
    authenticityScore: 80
};
const influencerB = {
    name: 'Influencer B',
    followers: 150000,
    engagementRate: 2.1,
    authenticityScore: 50
};
const campaignBudget = 250000;
console.log('--- Analyzing Influencer A ---');
const metricsA = (0, riskService_1.analyzeInfluencerRisk)(influencerA, { campaignBudget });
console.log(JSON.stringify(metricsA, null, 2));
console.log('\n--- Comparing Influencer A and B ---');
const comparison = (0, comparisonService_1.compareInfluencers)({
    influencerA,
    influencerB,
    campaignBudget
});
console.log(JSON.stringify(comparison, null, 2));
//# sourceMappingURL=usage.js.map