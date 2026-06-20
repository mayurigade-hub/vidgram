import { analyzeInfluencerRisk } from '../services/riskService';
import { compareInfluencers } from '../services/comparisonService';

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
const metricsA = analyzeInfluencerRisk(influencerA, { campaignBudget });
console.log(JSON.stringify(metricsA, null, 2));

console.log('\n--- Comparing Influencer A and B ---');
const comparison = compareInfluencers({
  influencerA,
  influencerB,
  campaignBudget
});
console.log(JSON.stringify(comparison, null, 2));
