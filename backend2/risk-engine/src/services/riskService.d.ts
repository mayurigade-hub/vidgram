import { InfluencerInput, CampaignContext, RiskClassification, RiskMetrics } from '../types';
/**
 * Classifies the risk of an influencer based on their authenticity score.
 * > 70 = Shortlist
 * 55-70 = Monitor
 * 40-55 = Pause
 * < 40 = Reject
 */
export declare function classifyRisk(authenticityScore: number): RiskClassification;
/**
 * Analyzes an influencer's campaign risk and calculates metrics.
 */
export declare function analyzeInfluencerRisk(influencer: InfluencerInput, context: CampaignContext): RiskMetrics;
//# sourceMappingURL=riskService.d.ts.map