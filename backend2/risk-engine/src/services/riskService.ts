import { 
  InfluencerInput, 
  CampaignContext, 
  RiskClassification, 
  RiskMetrics 
} from '../types';
import { 
  calculateGenuineReach, 
  calculateFakeReach, 
  calculateBudgetLoss, 
  calculateCostPerGenuine 
} from '../utils/formulas';

/**
 * Classifies the risk of an influencer based on their authenticity score.
 * > 70 = Shortlist
 * 55-70 = Monitor
 * 40-55 = Pause
 * < 40 = Reject
 */
export function classifyRisk(authenticityScore: number): RiskClassification {
  if (authenticityScore > 70) {
    return { label: 'Shortlist', severity: 1 };
  } else if (authenticityScore >= 55) {
    return { label: 'Monitor', severity: 2 };
  } else if (authenticityScore >= 40) {
    return { label: 'Pause', severity: 3 };
  } else {
    return { label: 'Reject', severity: 4 };
  }
}

/**
 * Analyzes an influencer's campaign risk and calculates metrics.
 */
export function analyzeInfluencerRisk(influencer: InfluencerInput, context: CampaignContext): RiskMetrics {
  const genuineReach = calculateGenuineReach(influencer.followers, influencer.authenticityScore);
  const fakeReach = calculateFakeReach(influencer.followers, genuineReach);
  const budgetLoss = calculateBudgetLoss(fakeReach, influencer.followers, context.campaignBudget);
  const costPerGenuineFollower = calculateCostPerGenuine(context.campaignBudget, genuineReach);
  const classification = classifyRisk(influencer.authenticityScore);

  return {
    genuineReach,
    fakeReach,
    budgetLoss,
    costPerGenuineFollower,
    classification
  };
}
