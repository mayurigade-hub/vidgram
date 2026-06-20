import { InfluencerComparisonInput, ComparisonResult } from '../types';
import { analyzeInfluencerRisk } from './riskService';

/**
 * Compares two influencers and evaluates which one is a safer investment.
 */
export function compareInfluencers(input: InfluencerComparisonInput): ComparisonResult {
  const { influencerA, influencerB, campaignBudget } = input;
  const context = { campaignBudget };

  const metricsA = analyzeInfluencerRisk(influencerA, context);
  const metricsB = analyzeInfluencerRisk(influencerB, context);

  // Determine safer choice (lower severity is better, tiebreaker: higher genuine reach)
  let saferChoice = '';
  if (metricsA.classification.severity < metricsB.classification.severity) {
    saferChoice = influencerA.name;
  } else if (metricsB.classification.severity < metricsA.classification.severity) {
    saferChoice = influencerB.name;
  } else {
    saferChoice = metricsA.genuineReach >= metricsB.genuineReach ? influencerA.name : influencerB.name;
  }

  // Determine more genuine reach
  const moreGenuineReach = metricsA.genuineReach >= metricsB.genuineReach ? influencerA.name : influencerB.name;

  // Determine less budget waste
  const lessBudgetWaste = metricsA.budgetLoss <= metricsB.budgetLoss ? influencerA.name : influencerB.name;

  // Potential savings (Difference in budget waste)
  const potentialSavings = Math.abs(metricsA.budgetLoss - metricsB.budgetLoss);

  return {
    influencerA: { ...metricsA, name: influencerA.name },
    influencerB: { ...metricsB, name: influencerB.name },
    saferChoice,
    moreGenuineReach,
    lessBudgetWaste,
    potentialSavings
  };
}
