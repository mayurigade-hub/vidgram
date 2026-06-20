import express from 'express';
import cors from 'cors';
import axios from 'axios';
import { analyzeInfluencerRisk } from './services/riskService';
import { InfluencerInput, CampaignContext } from './types';

const app = express();
const PORT = 3000;
const BACKEND1_URL = 'http://localhost:8000';

app.use(cors());
app.use(express.json());

app.get('/api/risk/:username', async (req, res) => {
    const { username } = req.params;
    const budgetParam = req.query.budget;
    const budget = budgetParam ? parseFloat(budgetParam as string) : 250000;

    try {
        // 1. Fetch data from Backend 1
        const response = await axios.get(`${BACKEND1_URL}/api/analyze/${username}`);
        const data = response.data;

        // 2. Prepare inputs for Risk Engine
        const influencer: InfluencerInput = {
            name: data.username,
            followers: data.followers,
            engagementRate: data.engagement_rate,
            authenticityScore: data.authenticity_score
        };

        const context: CampaignContext = {
            campaignBudget: budget
        };

        // 3. Calculate Risk Metrics
        const riskMetrics = analyzeInfluencerRisk(influencer, context);
        
        // Form response matching the prompt spec
        res.json({
            genuineReach: riskMetrics.genuineReach,
            fakeReach: riskMetrics.fakeReach,
            budgetLoss: riskMetrics.budgetLoss,
            costPerGenuineFollower: riskMetrics.costPerGenuineFollower,
            recommendation: riskMetrics.classification.label
        });
    } catch (error: any) {
        if (error.response && error.response.status === 404) {
            res.status(404).json({ error: "Influencer not found in Backend 1" });
        } else {
            console.error(error);
            res.status(500).json({ error: "Failed to communicate with Backend 1 or process request" });
        }
    }
});

app.listen(PORT, () => {
    console.log(`Backend 2 (Financial Engine) running on http://localhost:${PORT}`);
});
