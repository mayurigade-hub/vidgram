export interface InfluencerInput {
    name: string;
    followers: number;
    engagementRate: number;
    authenticityScore: number;
}
export interface CampaignContext {
    campaignBudget: number;
}
export type RiskLabel = 'Shortlist' | 'Monitor' | 'Pause' | 'Reject';
export interface RiskClassification {
    label: RiskLabel;
    severity: number;
}
export interface RiskMetrics {
    genuineReach: number;
    fakeReach: number;
    budgetLoss: number;
    costPerGenuineFollower: number;
    classification: RiskClassification;
}
export interface InfluencerComparisonInput {
    influencerA: InfluencerInput;
    influencerB: InfluencerInput;
    campaignBudget: number;
}
export interface ComparisonResult {
    influencerA: RiskMetrics & {
        name: string;
    };
    influencerB: RiskMetrics & {
        name: string;
    };
    saferChoice: string;
    moreGenuineReach: string;
    lessBudgetWaste: string;
    potentialSavings: number;
}
//# sourceMappingURL=index.d.ts.map